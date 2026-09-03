#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.json"
NAME_RE = re.compile(r"^name:\s*['\"]?([^'\"\r\n]+)['\"]?\s*$", re.MULTILINE)
VERSION_RE = re.compile(r"^version:\s*['\"]?([^'\"\r\n]+)['\"]?\s*$", re.MULTILINE)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    seen = set()
    for entry in data.get("skills", []):
        name = entry["name"]
        if name in seen:
            fail(f"duplicate registry name: {name}")
        seen.add(name)

        skill_dir = ROOT / entry["path"]
        skill_file = skill_dir / "SKILL.md"
        for required in (skill_file, skill_dir / "LICENSE.md", skill_dir / "PROVENANCE.md"):
            if not required.is_file():
                fail(f"missing required file: {required.relative_to(ROOT)}")

        text = skill_file.read_text(encoding="utf-8-sig")
        name_match = NAME_RE.search(text)
        version_match = VERSION_RE.search(text)
        if not name_match or name_match.group(1).strip() != name:
            fail(f"SKILL.md name mismatch: {name}")
        if not version_match or version_match.group(1).strip() != entry["version"]:
            fail(f"SKILL.md version mismatch: {name}")
        if skill_dir.name != name:
            fail(f"directory name mismatch: {name}")

    if not seen:
        fail("registry contains no skills")
    print(f"Validated {len(seen)} skills")


if __name__ == "__main__":
    main()

