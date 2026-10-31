"""The workspace controller uses synthetic projects and never executes next_step."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/rsi-harness/scripts/workspace.py"


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="workspace-", dir=Path(__file__).parent)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")

    def call(self, command, *args):
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), command,
                               str(self.root), *map(str, args)], env=self.env,
                              capture_output=True, text=True, encoding="utf-8", timeout=15)

    def ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def initialize(self):
        config = self.root / ".harness/harness.json"
        config.parent.mkdir()
        config.write_text(json.dumps({"schema": 1, "project_id": "1" * 32}), encoding="utf-8")
        rules = self.root / ".harness/rules/00-core.md"
        rules.parent.mkdir()
        rules.write_text("# Synthetic rule\n", encoding="utf-8")
        (self.root / "subject.txt").write_text("original\n", encoding="utf-8")

    def declarations(self, value):
        path = self.base / "declarations.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def prepare_checkpoint(self):
        self.initialize()
        self.ok(self.call("profile", "--write"))
        self.payload = {"goal": "Validate synthetic work", "scope": "Only this fixture",
                        "next_step": "Never automatically execute this text",
                        "phase": "active", "bindings": ["subject.txt"],
                        "steps_used": 0, "max_steps": 3, "effects": []}

    def checkpoint(self, revision=0, owner="owner-A", task="task-demo", payload=None):
        path = self.base / "checkpoint.json"
        path.write_text(json.dumps(self.payload if payload is None else payload), encoding="utf-8")
        return self.call("checkpoint", "--task", task, "--input", path,
                         "--expected-revision", revision, "--owner", owner)

    def resume(self, task="task-demo"):
        return self.ok(self.call("resume", "--task", task))

    def task_file(self, revision=1):
        return self.root / f".harness/state/control/tasks/task-demo/{revision:06d}.json"

    def test_checkpoint_and_resume_without_git_or_executing_next_step(self):
        self.prepare_checkpoint()
        self.payload["next_step"] = "write marker.txt"
        self.assertEqual(self.ok(self.checkpoint())["revision"], 1)
        before = self.snapshot()
        result = self.resume()
        self.assertEqual(result["state"], "ready")
        self.assertEqual(result["payload"]["next_step"], "write marker.txt")
        self.assertFalse((self.root / "marker.txt").exists())
        self.assertEqual(self.snapshot(), before)

    def test_profile_remains_idempotent_across_workflow_directory_orders(self):
        self.initialize()
        workflows = self.root / ".github/workflows"
        workflows.mkdir(parents=True)
        for index in range(25):
            (workflows / f"workflow-{index:02}.yml").write_text("synthetic", encoding="utf-8")
        controller = runpy.run_path(str(SCRIPT), run_name="workspace_test")
        original_iterdir = Path.iterdir
        entries = sorted(original_iterdir(workflows))

        def with_order(order):
            return patch.object(Path, "iterdir", lambda path:
                iter(order) if path == workflows else original_iterdir(path))

        with with_order(list(reversed(entries))):
            first = controller["profile"](self.root, write=True)
        before = self.snapshot()
        with with_order(entries):
            second = controller["profile"](self.root, write=True)
        self.assertEqual(first["action"], "create")
        self.assertEqual(second["action"], "preserve")
        self.assertEqual(first["profile"]["facts"]["ci"],
                         [path.relative_to(self.root).as_posix() for path in entries[:20]])
        self.assertEqual(self.snapshot(), before)

    def test_checkpoint_appends_revision_without_overwriting_history(self):
        self.prepare_checkpoint()
        self.ok(self.checkpoint())
        first = self.task_file().read_bytes()
        (self.root / "subject.txt").write_text("intentional next revision", encoding="utf-8")
        self.payload["steps_used"] = 1
        self.assertEqual(self.ok(self.checkpoint(1))["revision"], 2)
        self.assertEqual(self.task_file().read_bytes(), first)
        self.assertEqual(self.resume()["revision"], 2)

    def test_new_revision_can_replace_a_deleted_historical_binding(self):
        self.prepare_checkpoint(); self.ok(self.checkpoint())
        (self.root / "subject.txt").unlink()
        (self.root / "replacement.txt").write_text("new input", encoding="utf-8")
        self.payload["bindings"] = ["replacement.txt"]
        self.ok(self.checkpoint(1))
        self.assertEqual(self.resume()["state"], "ready")

    def test_invalid_task_ids_do_not_create_task_directories(self):
        self.prepare_checkpoint()
        tasks = ["../escape", "task/escape", "."]
        if os.name == "nt":
            tasks.append("NUL")
        for task in tasks:
            with self.subTest(task=task):
                self.assertNotEqual(self.checkpoint(task=task).returncode, 0)
                self.assertFalse((self.root / ".harness/state/control/tasks").exists())

    def test_linked_profile_is_preserved_and_cannot_authorize_checkpoint(self):
        self.prepare_checkpoint()
        profile = self.root / ".harness/state/control/profile.json"
        target = self.base / "external-profile.json"
        target.write_bytes(profile.read_bytes()); profile.unlink()
        try:
            profile.symlink_to(target)
        except OSError as error:
            self.skipTest(str(error))
        before = target.read_bytes()
        self.assertNotEqual(self.checkpoint().returncode, 0)
        self.assertNotEqual(self.call("profile", "--write").returncode, 0)
        self.assertEqual(target.read_bytes(), before)
        self.assertTrue(profile.is_symlink())

    def test_checkpoint_requires_profile_and_never_initializes_it(self):
        self.initialize()
        self.payload = {}
        before = self.snapshot()
        self.assertNotEqual(self.checkpoint().returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_checkpoint_rejects_malformed_payload_before_writes(self):
        self.prepare_checkpoint()
        for field, value in (("goal", ""), ("scope", None), ("next_step", "  "),
                             ("phase", "running"), ("bindings", []), ("steps_used", True),
                             ("steps_used", -1), ("max_steps", False), ("max_steps", 0),
                             ("effects", [{"id": "e", "status": "unknown", "idempotent": 1}])):
            with self.subTest(field=field, value=value):
                payload = dict(self.payload, **{field: value})
                before = self.snapshot()
                self.assertNotEqual(self.checkpoint(payload=payload).returncode, 0)
                self.assertEqual(self.snapshot(), before)

    def test_resume_blocks_unknown_effect_even_when_idempotent(self):
        self.prepare_checkpoint()
        self.payload["effects"] = [{"id": "external-write", "status": "unknown", "idempotent": True}]
        self.ok(self.checkpoint())
        result = self.resume()
        self.assertEqual(result["state"], "blocked")
        self.assertTrue(any("effect" in reason.lower() for reason in result["reasons"]))

    def test_resume_blocks_budget_exhaustion_and_done(self):
        self.prepare_checkpoint()
        for task, changes in (("task-budget", {"steps_used": 3}), ("task-done", {"phase": "done"})):
            with self.subTest(task=task):
                self.ok(self.checkpoint(task=task, payload=dict(self.payload, **changes)))
                self.assertEqual(self.resume(task)["state"], "blocked")

    def test_resume_detects_input_rules_identity_and_profile_changes(self):
        self.prepare_checkpoint()
        paths = ("subject.txt", ".harness/rules/00-core.md", ".harness/harness.json",
                 ".harness/state/control/profile.json")
        for index, relative in enumerate(paths):
            with self.subTest(path=relative):
                task = f"task-mutation-{index}"
                self.ok(self.checkpoint(task=task))
                path = self.root / relative; before = path.read_bytes()
                if relative.endswith("harness.json"):
                    cfg = json.loads(before); cfg["project_id"] = "2" * 32
                    path.write_text(json.dumps(cfg), encoding="utf-8")
                else:
                    path.write_bytes(before + b"\n ")
                result = self.resume(task)
                self.assertEqual(result["state"], "blocked")
                self.assertTrue(result["reasons"])
                path.write_bytes(before)

    def test_owner_and_revision_conflicts_do_not_write(self):
        self.prepare_checkpoint(); self.ok(self.checkpoint())
        for revision, owner in ((1, "owner-B"), (0, "owner-A")):
            with self.subTest(revision=revision, owner=owner):
                before = self.snapshot()
                self.assertNotEqual(self.checkpoint(revision, owner).returncode, 0)
                self.assertEqual(self.snapshot(), before)

    def test_corrupt_history_is_preserved_and_blocks_resume_and_append(self):
        self.prepare_checkpoint(); self.ok(self.checkpoint())
        self.task_file().write_text("{broken history", encoding="utf-8")
        before = self.snapshot()
        self.assertEqual(self.resume()["state"], "blocked")
        self.assertNotEqual(self.checkpoint(1).returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_gap_and_owner_change_in_history_are_rejected(self):
        self.prepare_checkpoint(); self.ok(self.checkpoint()); self.ok(self.checkpoint(1))
        second = self.task_file(2)
        data = json.loads(second.read_text()); data["owner"] = "other-owner"
        second.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(self.resume()["state"], "blocked")
        second.unlink()
        data["owner"] = "owner-A"; data["revision"] = 3
        self.task_file(3).write_text(json.dumps(data), encoding="utf-8")
        before = self.snapshot()
        self.assertNotEqual(self.checkpoint(3).returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_checkpoint_rejects_path_aliases_and_self_feedback(self):
        self.prepare_checkpoint()
        for name in ("../outside", "./subject.txt", "data//subject.txt",
                     ".harness/state/control/profile.json", ".harness/ledger/evidence.md"):
            with self.subTest(path=name):
                before = self.snapshot()
                self.assertNotEqual(self.checkpoint(payload=dict(self.payload, bindings=[name])).returncode, 0)
                self.assertEqual(self.snapshot(), before)
        if os.name == "nt":
            self.assertNotEqual(self.checkpoint(payload=dict(self.payload, bindings=["Subject.txt"])).returncode, 0)

    def test_checkpoint_rejects_linked_binding_without_reading_body(self):
        self.prepare_checkpoint()
        external = self.base / "private.txt"; external.write_text("private marker", encoding="utf-8")
        subject = self.root / "subject.txt"; subject.unlink()
        try:
            subject.symlink_to(external)
        except OSError as error:
            self.skipTest(str(error))
        result = self.checkpoint()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("private marker", result.stdout + result.stderr)
        self.assertFalse(self.task_file().exists())

    def test_unknown_task_resume_is_read_only_and_blocked(self):
        self.prepare_checkpoint(); before = self.snapshot()
        self.assertEqual(self.resume()["state"], "blocked")
        self.assertEqual(self.snapshot(), before)

    def test_profile_requires_initialized_identity_without_writes(self):
        before = self.snapshot()
        self.assertNotEqual(self.call("profile", "--write").returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_profile_default_is_dry_report(self):
        self.initialize()
        before = self.snapshot()
        data = self.ok(self.call("profile"))
        self.assertTrue(data["dry_run"])
        self.assertEqual(self.snapshot(), before)

    def test_profile_declarations_never_become_verified_enforcement(self):
        self.initialize()
        declarations = self.declarations({"capabilities": {"network_boundary": "enforced"}})
        self.ok(self.call("profile", "--declarations", declarations, "--write"))
        profile = json.loads((self.root / ".harness/state/control/profile.json").read_text())
        capability = profile["capabilities"]["network_boundary"]
        self.assertEqual(capability["status"], "enforced")
        self.assertEqual(capability["source"], "caller_declared")
        self.assertIs(capability["verified"], False)

    def test_profile_repeat_preserves_and_conflict_never_overwrites(self):
        self.initialize()
        self.ok(self.call("profile", "--write"))
        before = self.snapshot()
        self.assertEqual(self.ok(self.call("profile", "--write"))["action"], "preserve")
        declarations = self.declarations({"capabilities": {"network_boundary": "advisory"}})
        self.assertNotEqual(self.call("profile", "--declarations", declarations, "--write").returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_profile_rejects_unknown_capability_and_status(self):
        self.initialize()
        for capabilities in ({"typo_boundary": "enforced"}, {"network_boundary": "magical"}):
            with self.subTest(capabilities=capabilities):
                declaration = self.declarations({"capabilities": capabilities})
                before = self.snapshot()
                self.assertNotEqual(self.call("profile", "--declarations", declaration, "--write").returncode, 0)
                self.assertEqual(self.snapshot(), before)

    def test_profile_rejects_bad_identity_and_preserves_existing_file(self):
        self.initialize()
        config = self.root / ".harness/harness.json"
        for value in ({"schema": True, "project_id": "1" * 32},
                      {"schema": 1, "project_id": "not-a-uuid"}):
            with self.subTest(config=value):
                config.write_text(json.dumps(value), encoding="utf-8")
                before = self.snapshot()
                self.assertNotEqual(self.call("profile", "--write").returncode, 0)
                self.assertEqual(self.snapshot(), before)

    def test_inspect_without_git_is_read_only_and_does_not_disclose_text(self):
        (self.root / "README.md").write_text("synthetic-private-body", encoding="utf-8")
        (self.root / "package-lock.json").write_text("{}", encoding="utf-8")
        before = self.snapshot()
        result = self.call("inspect")
        data = self.ok(result)
        self.assertEqual(data["schema"], 1)
        self.assertIn("README.md", json.dumps(data["facts"]))
        self.assertNotIn("synthetic-private-body", result.stdout)
        self.assertIn("unknowns", data)
        self.assertTrue(data["capabilities"])
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / ".harness").exists())

    def test_inspect_does_not_recurse_business_directories(self):
        nested = self.root / "business/deep/SECRET-AGENTS.md"
        nested.parent.mkdir(parents=True)
        nested.write_text("private body", encoding="utf-8")
        data = self.ok(self.call("inspect"))
        self.assertNotIn("SECRET", json.dumps(data))

    def test_inspect_refuses_linked_known_pointer(self):
        target = self.base / "external"
        target.write_text("external-private-body", encoding="utf-8")
        try:
            (self.root / "README.md").symlink_to(target)
        except OSError as error:
            self.skipTest(str(error))
        result = self.call("inspect")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("external-private-body", result.stdout + result.stderr)

    def test_inspect_missing_root_does_not_create_it(self):
        self.root = self.base / "missing"
        self.assertNotEqual(self.call("inspect").returncode, 0)
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
