#!/usr/bin/env python3
"""Validate the repository contract using only the Python standard library."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$")
REQUIRED = ("SKILL.md", "README.md", "LICENSE.md", "PROVENANCE.md", "AUTHORS.md")


def scalar(frontmatter, key):
    match = re.search(rf"^{re.escape(key)}:\s*([^\r\n]+)$", frontmatter, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else None


def skill_metadata(text):
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    frontmatter = match.group(1)
    legacy = scalar(frontmatter, "version")
    metadata = re.search(r"^metadata:\s*\n((?:[ \t]+[^\n]*\n?)+)", frontmatter, re.MULTILINE)
    nested = None
    if metadata:
        match = re.search(r"^[ \t]+version:\s*([^\r\n]+)$", metadata.group(1), re.MULTILINE)
        nested = match.group(1).strip().strip("\"'") if match else None
    if legacy and nested:
        raise ValueError("use either version or metadata.version, not both")
    return scalar(frontmatter, "name"), legacy or nested, scalar(frontmatter, "description")


def markdown_links(root):
    errors = []
    for file in sorted(root.rglob("*.md")):
        if ".git" in file.relative_to(root).parts:
            continue
        text = file.read_text(encoding="utf-8-sig")
        # Code samples may deliberately contain illustrative Markdown links.
        text = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", text)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            target = target.split(' "', 1)[0].strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (file.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"broken local link in {file.relative_to(root)}: {target}")
    return errors


def validate_repo(root):
    root = Path(root)
    errors = []
    try:
        data = json.loads((root / "registry.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"cannot read registry.json: {exc}"]
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        return ["registry schemaVersion must be 1"]
    entries = data.get("skills")
    if not isinstance(entries, list) or not entries:
        return ["registry must contain a nonempty skills array"]
    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("registry skill entries must be objects")
            continue
        name, version, path = entry.get("name"), entry.get("version"), entry.get("path")
        if not isinstance(name, str) or len(name) > 64 or not NAME_RE.fullmatch(name):
            errors.append(f"invalid skill name: {name!r}")
            continue
        if name in seen:
            errors.append(f"duplicate registry name: {name}")
        seen.add(name)
        if path != f"skills/{name}":
            errors.append(f"invalid registry path for {name}: {path!r}")
            continue
        if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
            errors.append(f"invalid version for {name}: {version!r}")
        if not isinstance(entry.get("license"), str) or not entry["license"].strip():
            errors.append(f"missing license for {name}")
        if entry.get("status") not in {"active", "experimental", "deprecated"}:
            errors.append(f"invalid status for {name}")
        skill_dir = root / path
        if not skill_dir.resolve().is_relative_to(root.resolve()):
            errors.append(f"skill path escapes repository: {path}")
            continue
        for filename in REQUIRED:
            file = skill_dir / filename
            if not file.is_file() or not file.read_text(encoding="utf-8-sig").strip():
                errors.append(f"missing or empty required file: {path}/{filename}")
        skill_file = skill_dir / "SKILL.md"
        if skill_file.is_file():
            try:
                actual_name, actual_version, description = skill_metadata(skill_file.read_text(encoding="utf-8-sig"))
                if actual_name != name:
                    errors.append(f"SKILL.md name mismatch: {name}")
                if actual_version != version:
                    errors.append(f"SKILL.md version mismatch: {name}")
                if not description:
                    errors.append(f"SKILL.md missing description: {name}")
            except ValueError as exc:
                errors.append(f"{path}/SKILL.md: {exc}")
        row = next((line for line in readme.splitlines() if line.startswith("|") and f"]({path}/)" in line), None)
        if not row or version not in [cell.strip().strip("`") for cell in row.split("|")]:
            errors.append(f"README catalog missing or stale for {name}")
    for skill_file in sorted((root / "skills").glob("*/SKILL.md")):
        if skill_file.parent.name not in seen:
            errors.append(f"unregistered skill: {skill_file.parent.name}")
    errors.extend(markdown_links(root))
    return errors


def main():
    errors = validate_repo(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    count = len(json.loads((ROOT / "registry.json").read_text())["skills"])
    print(f"Validated {count} skills, registry, README catalog and local Markdown links")


if __name__ == "__main__":
    main()
