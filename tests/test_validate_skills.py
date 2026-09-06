"""Repository-level fixtures test observable failures, not implementation text."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("validate_skills", Path(__file__).resolve().parents[1] / "scripts/validate-skills.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "skills/example-skill"
        self.package.mkdir(parents=True)
        self.entry = {"name": "example-skill", "path": "skills/example-skill", "version": "0.1.0", "license": "MIT", "status": "active"}
        self.write_registry([self.entry])
        (self.root / "README.md").write_text("| [example-skill](skills/example-skill/) | `0.1.0` | MIT |\n")
        for filename in validator.REQUIRED:
            (self.package / filename).write_text("Documented package content.\n")
        self.write_skill('metadata:\n  version: "0.1.0"')

    def write_registry(self, entries):
        (self.root / "registry.json").write_text(json.dumps({"schemaVersion": 1, "skills": entries}))

    def write_skill(self, version):
        (self.package / "SKILL.md").write_text(f"---\nname: example-skill\ndescription: A scoped example.\n{version}\n---\n\nUse the example.\n")

    def errors(self):
        return validator.validate_repo(self.root)

    def test_valid_nested_version(self):
        self.assertEqual(self.errors(), [])

    def test_legacy_version_remains_compatible(self):
        self.write_skill("version: 0.1.0")
        self.assertEqual(self.errors(), [])

    def test_conflicting_version_locations_rejected(self):
        self.write_skill("version: 0.1.0\nmetadata:\n  version: 0.2.0")
        self.assertTrue(any("not both" in x for x in self.errors()))

    def test_missing_provenance_rejected(self):
        (self.package / "PROVENANCE.md").unlink()
        self.assertTrue(any("PROVENANCE.md" in x for x in self.errors()))

    def test_path_traversal_rejected(self):
        self.write_registry([{**self.entry, "path": "../outside"}])
        self.assertTrue(any("invalid registry path" in x for x in self.errors()))

    def test_duplicate_entry_rejected(self):
        self.write_registry([self.entry, self.entry])
        self.assertTrue(any("duplicate" in x for x in self.errors()))

    def test_stale_readme_rejected(self):
        (self.root / "README.md").write_text("| [example-skill](skills/example-skill/) | `0.0.1` | MIT |\n")
        self.assertTrue(any("README catalog" in x for x in self.errors()))

    def test_unregistered_skill_rejected(self):
        other = self.root / "skills/unregistered"
        other.mkdir()
        (other / "SKILL.md").write_text("# Unregistered\n")
        self.assertTrue(any("unregistered skill" in x for x in self.errors()))

    def test_broken_reference_rejected(self):
        (self.package / "README.md").write_text("[Missing method](references/missing.md)\n")
        self.assertTrue(any("broken local link" in x for x in self.errors()))

    def test_version_mismatch_rejected(self):
        self.write_skill("metadata:\n  version: 0.2.0")
        self.assertTrue(any("version mismatch" in x for x in self.errors()))

    def test_code_example_link_not_treated_as_real_resource(self):
        (self.package / "README.md").write_text("```markdown\n[Example](example.md)\n```\n")
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()
