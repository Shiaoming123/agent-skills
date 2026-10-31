"""The public importer uses synthetic archives; the RSI runtime is not published."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / "skills/rsi-harness/scripts/import_runtime.py"
spec = importlib.util.spec_from_file_location("rsi_import", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ImportRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.archive = self.root / "runtime.zip"
        self.cli = b"# synthetic CLI, never executed\n"
        self.members = {"rsi-harness/scaffold/rsi": self.cli,
                        "rsi-harness/scaffold/templates/root/example.txt": b"example\n",
                        "rsi-harness/scaffold/empty": b""}
        self.make_archive()
        self.target = self.root / "installed/runtime"

    def make_archive(self):
        with zipfile.ZipFile(self.archive, "w") as z:
            for name, content in self.members.items():
                info = zipfile.ZipInfo("placeholder")
                info.filename = info.orig_filename = name
                z.writestr(info, content)
        self.lock = {"version": "test", "archive_sha256": hashlib.sha256(self.archive.read_bytes()).hexdigest(),
                     "cli_sha256": hashlib.sha256(self.cli).hexdigest()}

    def invoke(self, dry_run=False):
        with patch.object(module, "load_lock", return_value=self.lock):
            return module.install_runtime(self.archive, self.target, dry_run)

    def test_dry_run_creates_no_directories(self):
        result = self.invoke(True)
        self.assertEqual(result["files"], 3)
        self.assertFalse(self.target.parent.exists())

    def test_import_preserves_bytes_and_repeat_is_read_only(self):
        self.invoke()
        expected = {p.relative_to(self.target).as_posix(): p.read_bytes()
                    for p in self.target.rglob("*") if p.is_file()}
        self.assertEqual(expected["scaffold/rsi"], self.cli)
        self.assertEqual(expected["scaffold/empty"], b"")
        self.assertEqual(self.invoke()["action"], "preserve")
        actual = {p.relative_to(self.target).as_posix(): p.read_bytes()
                  for p in self.target.rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)

    def test_wrong_archive_digest_rejects_before_writes(self):
        self.lock["archive_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "SHA256"):
            self.invoke()
        self.assertFalse(self.target.parent.exists())

    def test_wrong_cli_digest_rejects_before_writes(self):
        self.lock["cli_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "CLI"):
            self.invoke()
        self.assertFalse(self.target.parent.exists())

    def test_archive_traversal_is_rejected_before_writes(self):
        for name in ("rsi-harness/scaffold/../escape", "rsi-harness/scaffold/a//alias",
                     "rsi-harness/scaffold/a\\alias", "rsi-harness/scaffold/a\x00hidden"):
            with self.subTest(name=name):
                self.members[name] = b"unsafe"
                self.make_archive()
                with self.assertRaises(ValueError):
                    self.invoke()
                self.assertFalse(self.target.parent.exists())
                del self.members[name]

    def test_import_uses_the_exact_bytes_already_hashed(self):
        original_sha = module.sha
        replaced = False
        def replace_after_hash(data):
            nonlocal replaced
            result = original_sha(data)
            if not replaced:
                replaced = True
                self.archive.write_bytes(b"replaced path after hash")
            return result
        with patch.object(module, "sha", side_effect=replace_after_hash):
            self.invoke()
        self.assertEqual((self.target / "scaffold/rsi").read_bytes(), self.cli)

    def test_existing_custom_or_modified_destination_is_preserved(self):
        self.target.mkdir(parents=True)
        custom = self.target / "custom.txt"
        custom.write_bytes(b"preserve this")
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(custom.read_bytes(), b"preserve this")
        self.assertEqual(list(self.target.iterdir()), [custom])

    def test_post_import_tamper_or_extra_file_is_not_reinstalled(self):
        self.invoke()
        cli = self.target / "scaffold/rsi"
        cli.write_bytes(b"local edit")
        with self.assertRaises(ValueError):
            self.invoke()
        self.assertEqual(cli.read_bytes(), b"local edit")


if __name__ == "__main__":
    unittest.main()
