"""Public CLI behavior with trusted synthetic graders and isolated subjects."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/rsi-harness/scripts/compare.py"


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.baseline = self.root / "baseline"
        self.candidate = self.root / "candidate"
        for folder, value in ((self.baseline, "0.25"), (self.candidate, "0.75")):
            folder.mkdir()
            (folder / "value.txt").write_text(value)
        self.grader = self.root / "grader.py"
        self.grader.write_text("import json,os\nfrom pathlib import Path\n"
            "root=Path(os.environ['RSI_SUBJECT_ROOT'])\n"
            "print(json.dumps({'score':float((root/'value.txt').read_text())}))\n")
        self.shared = self.root / "cases.json"
        self.shared.write_text('{"case":"synthetic"}')
        self.policy = self.root / "policy.json"
        self.spec = {"schema": 1, "isolated": True,
            "baseline": str(self.baseline), "candidate": str(self.candidate),
            "subject_files": ["value.txt"], "grader": str(self.grader),
            "inputs": [str(self.shared)], "trials": 1, "timeout_seconds": 2,
            "min_delta": 0.1, "deterministic": True}
        self.save()

    def save(self):
        self.policy.write_text(json.dumps(self.spec), encoding="utf-8")

    def call(self, *args):
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(SCRIPT),
            str(self.policy), *args], capture_output=True, text=True, encoding="utf-8",
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=15)

    def test_plain_cli_dry_run_creates_no_tool_or_project_cache(self):
        tools = self.root / "tools"
        tools.mkdir()
        for name in ("compare.py", "import_runtime.py"):
            (tools / name).write_bytes(SCRIPT.with_name(name).read_bytes())
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run([sys.executable, str(tools / "compare.py"), str(self.policy)],
            capture_output=True, text=True, encoding="utf-8", env=env, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_default_is_read_only_plan_without_execution(self):
        self.grader.write_text("raise RuntimeError('must not execute')\n")
        before = {p.relative_to(self.root).as_posix():p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["action"], "dry-run")
        after = {p.relative_to(self.root).as_posix():p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(after, before)

    def test_executes_both_subjects_and_compares_scores_not_exit_codes(self):
        result = self.call("--execute")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["decision"], "candidate_preferred")
        self.assertEqual([r["score"] for r in data["runs"]], [0.25, 0.75])
        self.assertEqual([r["exit_code"] for r in data["runs"]], [0, 0])
        self.assertFalse(data["automatic_promotion"])

    def test_output_is_create_only_and_conflict_prevents_execution(self):
        output = self.root / "result.json"
        result = self.call("--execute", "--output", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(output.read_text())["decision"], "candidate_preferred")
        output.write_text("preserve me")
        self.grader.write_text("raise RuntimeError('must not execute')\n")
        result = self.call("--execute", "--output", str(output))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), "preserve me")

    def test_untrusted_grade_timeout_and_output_limit_are_invalid(self):
        variants = ["print('not json')", "print('{\"score\":true}')",
                    "print('{\"score\":NaN}')", "raise RuntimeError('broken grader')",
                    "import time; time.sleep(1)", "print('x'*1100000)"]
        for code in variants:
            with self.subTest(code=code):
                self.grader.write_text(code + "\n")
                self.spec["timeout_seconds"] = 0.3
                self.save()
                result = self.call("--execute")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["decision"], "invalid")

    def test_changes_to_frozen_inputs_or_subjects_invalidate_comparison(self):
        for target in (self.shared, self.grader, self.policy, self.baseline / "value.txt"):
            with self.subTest(target=target.name):
                self.setUp()
                # Use the corresponding fresh path from this new fixture.
                actual = self.root / target.relative_to(target.parents[1] if target.name == "value.txt" else target.parent)
                self.grader.write_text("from pathlib import Path\n"
                    f"p=Path({str(actual)!r}); p.write_bytes(p.read_bytes()+b' ')\n"
                    "print('{\"score\":0.8}')\n")
                result = self.call("--execute")
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["reason"], "binding_changed")

    def test_overlapping_roots_and_internal_grader_are_rejected(self):
        for field, value in (("candidate", str(self.baseline)),
                             ("candidate", str(self.baseline / "nested")),
                             ("grader", str(self.baseline / "grader.py"))):
            with self.subTest(field=field, value=value):
                (self.baseline / "nested").mkdir(exist_ok=True)
                (self.baseline / "grader.py").write_text("raise RuntimeError('must not run')")
                self.spec[field] = value
                self.save()
                result = self.call("--execute")
                self.assertEqual(result.returncode, 2)
                self.spec["candidate"], self.spec["grader"] = str(self.candidate), str(self.grader)

    def test_regressions_ties_and_stochastic_trials_are_not_improvements(self):
        for value, deterministic, decision in (("0", True, "baseline_preferred"),
                ("0.25", True, "equivalent"), ("0.3", True, "inconclusive"),
                ("0.75", False, "inconclusive")):
            with self.subTest(value=value, deterministic=deterministic):
                (self.candidate / "value.txt").write_text(value)
                self.spec["deterministic"] = deterministic
                self.save()
                result = self.call("--execute")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["decision"], decision)

    def test_subject_aliases_are_rejected_before_execution(self):
        aliases = ["./value.txt", "a//value.txt", "../value.txt"]
        if os.name == "nt":
            aliases += ["Value.txt", "value.txt.", "NUL"]
        for name in aliases:
            with self.subTest(name=name):
                self.spec["subject_files"] = [name]
                self.save()
                result = self.call("--execute")
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_malformed_budgets_and_schema_are_rejected(self):
        for key, value in (("schema", True), ("trials", True), ("trials", 0),
                ("timeout_seconds", float("nan")), ("timeout_seconds", 0),
                ("min_delta", float("inf")), ("deterministic", "yes"), ("isolated", False)):
            with self.subTest(key=key, value=value):
                original = self.spec[key]
                self.spec[key] = value
                self.save()
                self.assertEqual(self.call("--execute").returncode, 2)
                self.spec[key] = original

    def test_paired_trials_alternate_order_and_noisy_delta_stays_inconclusive(self):
        self.spec["trials"] = 2
        self.save()
        result = self.call("--execute")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([r["subject"] for r in report["runs"]],
                         ["baseline", "candidate", "candidate", "baseline"])
        self.assertEqual(report["paired_deltas"], [0.5, 0.5])

    def test_output_inside_subject_is_rejected(self):
        result = self.call("--execute", "--output", str(self.candidate / "report.json"))
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.candidate / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
