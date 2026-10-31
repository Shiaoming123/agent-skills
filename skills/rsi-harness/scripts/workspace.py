#!/usr/bin/env python3
"""Inspect explicit projects and retain bounded recovery records; never execute steps."""
import argparse
import hashlib
from itertools import islice
import json
import os
from pathlib import Path, PurePosixPath
import re

CAPABILITIES = ("event_hooks", "path_isolation", "network_boundary", "process_termination",
                "pause_resume", "cost_metering", "immutable_evaluator")
POINTERS = {
    "instructions": ("AGENTS.md", "CLAUDE.md"),
    "entrypoints": ("README.md", "Makefile", "justfile", "package.json", "pyproject.toml",
                    "Cargo.toml", "go.mod", "CMakeLists.txt", "build.gradle"),
    "lockfiles": ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock",
                  "poetry.lock", "Cargo.lock", "go.sum"),
    "architecture": ("ARCHITECTURE.md", "docs/architecture.md", "docs/ARCHITECTURE.md"),
    "ci": (".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml"),
}


def reject_links(path):
    for part in (path, *path.parents):
        if part.is_symlink() or (part.exists() and getattr(part.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError("Link/reparse paths are unsupported")


def project_root(value):
    path = Path(value).absolute()
    reject_links(path)
    if not path.is_dir():
        raise ValueError("Project root must be an existing directory")
    return path.resolve()


def capabilities():
    return {name: {"status": "unavailable", "source": "not_verified", "verified": False,
                   "reason": "No host adapter has been verified by this tool"}
            for name in CAPABILITIES}


def inspect(root):
    facts = {}
    for group, names in POINTERS.items():
        facts[group] = []
        for name in names:
            path = root / name
            reject_links(path)
            if path.is_file():
                facts[group].append(name)
    workflows = root / ".github/workflows"
    reject_links(workflows)
    if workflows.is_dir():
        # Bounded pointers only; no business tree or file bodies are inspected.
        for path in islice(workflows.iterdir(), 20):
            reject_links(path)
            if path.is_file() and path.suffix in (".yaml", ".yml"):
                facts["ci"].append(path.relative_to(root).as_posix())
    return {"schema": 1, "root": str(root), "facts": facts,
            "unknowns": ["Pointer existence does not verify instructions, commands or architecture",
                         "Generated sources, protected scope and host enforcement require confirmation",
                         "CI discovery is limited to 20 directory entries"],
            "capabilities": capabilities()}


def read_json(path):
    reject_links(path)
    return json.loads(path.read_text(encoding="utf-8"))


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def identity(root):
    config = read_json(root / ".harness/harness.json")
    if (not isinstance(config, dict) or type(config.get("schema")) is not int
            or config["schema"] != 1 or not isinstance(config.get("project_id"), str)
            or not re.fullmatch(r"[0-9a-f]{32}", config["project_id"])):
        raise ValueError("Existing schema=1 and 32-hex project_id are required")
    return config["project_id"]


def create_file(path, payload):
    reject_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    reject_links(path)
    # Exclusive publication prevents overwrite; this is not a lock or crash transaction.
    with path.open("xb") as stream:
        stream.write(payload)


def profile(root, declarations=None, write=False):
    project_id = identity(root)
    result = inspect(root)
    result["project_id"] = project_id
    if declarations:
        declared = read_json(Path(declarations).absolute())
        if (not isinstance(declared, dict) or set(declared) != {"capabilities"}
                or not isinstance(declared["capabilities"], dict)
                or set(declared["capabilities"]) - set(CAPABILITIES)):
            raise ValueError("Declarations must name only the seven known capabilities")
        for name, status in declared["capabilities"].items():
            if status not in ("supported", "enforced", "advisory", "unavailable"):
                raise ValueError("Unsupported capability status")
            result["capabilities"][name] = {
                "status": status, "source": "caller_declared", "verified": False,
                "reason": "Caller declaration only; no host enforcement was verified"}
    target = root / ".harness/state/control/profile.json"
    reject_links(target)
    payload = encoded(result)
    action = "create"
    if target.exists():
        if not target.is_file() or target.read_bytes() != payload:
            raise ValueError("Existing profile differs; preserved without overwrite")
        action = "preserve"
    elif write:
        create_file(target, payload)
    return {"action": action, "dry_run": not write, "profile": result,
            "target": target.relative_to(root).as_posix()}


def windows_alias(name):
    device = name.split(".")[0].upper()
    return (name.rstrip(" .") != name or device in {"CON", "PRN", "AUX", "NUL"}
            or re.fullmatch(r"(?:COM|LPT)[1-9]", device))


def relative_file(root, name, check_disk=True):
    if (not isinstance(name, str) or not name or name == "." or "\\" in name or ":" in name
            or PurePosixPath(name).is_absolute() or PurePosixPath(name).as_posix() != name
            or ".." in PurePosixPath(name).parts):
        raise ValueError("Bindings must be canonical relative project files")
    folded = name.casefold()
    if (".git" in [p.casefold() for p in PurePosixPath(name).parts]
            or folded == ".harness/knowledge/index.md"
            or any(folded == p or folded.startswith(p + "/") for p in
                   (".harness/state", ".harness/ledger", ".harness/evals/runs"))):
        raise ValueError("State, ledger and derived files cannot be recovery inputs")
    path = root
    for part in PurePosixPath(name).parts:
        if os.name == "nt":
            if windows_alias(part):
                raise ValueError("Windows path aliases are unsupported")
            if check_disk and path.is_dir() and part not in {p.name for p in path.iterdir()}:
                raise ValueError("Binding path must use exact existing case")
        path = path / part
        if check_disk:
            reject_links(path)
    return path


def file_hash(path):
    reject_links(path)
    with path.open("rb") as stream:
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Checkpoint payload must be an object")
    for field in ("goal", "scope", "next_step"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            raise ValueError(f"{field} must be nonempty text")
    if payload.get("phase") not in ("active", "verifying", "done"):
        raise ValueError("Invalid checkpoint phase")
    bindings = payload.get("bindings")
    if (not isinstance(bindings, list) or not bindings or any(not isinstance(p, str) for p in bindings)
            or len(bindings) != len(set(bindings))):
        raise ValueError("bindings must be a nonempty unique file array")
    for field, minimum in (("steps_used", 0), ("max_steps", 1)):
        if type(payload.get(field)) is not int or payload[field] < minimum:
            raise ValueError(f"{field} must be an integer >= {minimum}, not bool")
    effects = payload.get("effects")
    if not isinstance(effects, list):
        raise ValueError("effects must be an array")
    seen = set()
    for effect in effects:
        if (not isinstance(effect, dict) or not isinstance(effect.get("id"), str)
                or not effect["id"].strip() or effect["id"] in seen
                or effect.get("status") not in ("unknown", "confirmed")
                or type(effect.get("idempotent")) is not bool):
            raise ValueError("Invalid or duplicate effect declaration")
        seen.add(effect["id"])


def task_folder(root, task):
    if not isinstance(task, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", task):
        raise ValueError("Task ID must contain only letters, digits, underscores and hyphens")
    if os.name == "nt" and windows_alias(task):
        raise ValueError("Task ID must not be a Windows device alias")
    folder = root / ".harness/state/control/tasks" / task
    reject_links(folder)
    return folder


def history(root, task):
    folder = task_folder(root, task)
    if not folder.exists():
        return []
    records = []
    for path in sorted(folder.iterdir()):
        reject_links(path)
        if not path.is_file() or path.name != f"{len(records) + 1:06d}.json":
            raise ValueError("Checkpoint history has a gap or unexpected entry")
        record = read_json(path)
        if (not isinstance(record, dict) or type(record.get("schema")) is not int
                or record["schema"] != 1 or record.get("task") != task
                or type(record.get("revision")) is not int or record["revision"] != len(records) + 1
                or not isinstance(record.get("owner"), str) or not record["owner"].strip()
                or "\n" in record["owner"] or "\r" in record["owner"]
                or not isinstance(record.get("project_id"), str)
                or not re.fullmatch(r"[0-9a-f]{32}", record["project_id"])):
            raise ValueError("Checkpoint history schema, identity or owner is invalid")
        if records and any(record[key] != records[0][key] for key in ("owner", "project_id")):
            raise ValueError("Checkpoint history changes owner or project identity")
        validate_payload(record.get("payload"))
        fingerprint = record.get("fingerprint")
        if (not isinstance(fingerprint, dict) or set(fingerprint) != {"config", "profile", "bindings", "rules"}
                or not isinstance(fingerprint["bindings"], dict) or not isinstance(fingerprint["rules"], dict)
                or set(fingerprint["bindings"]) != set(record["payload"]["bindings"])):
            raise ValueError("Invalid checkpoint fingerprint")
        digests = [fingerprint["config"], fingerprint["profile"]]
        for group in ("bindings", "rules"):
            for name, value in fingerprint[group].items():
                relative_file(root, name, check_disk=False)
                if group == "rules" and not (name.startswith(".harness/rules/") and name.endswith(".md")):
                    raise ValueError("Invalid rule fingerprint path")
                digests.append(value)
        if any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) for value in digests):
            raise ValueError("Invalid checkpoint digest")
        records.append(record)
    return records


def current_fingerprint(root, payload):
    profile_path = root / ".harness/state/control/profile.json"
    current_profile = read_json(profile_path)
    if (not isinstance(current_profile, dict) or type(current_profile.get("schema")) is not int
            or current_profile["schema"] != 1 or current_profile.get("project_id") != identity(root)):
        raise ValueError("Profile project identity is missing or mismatched")
    rules = root / ".harness/rules"
    reject_links(rules)
    return {"config": file_hash(root / ".harness/harness.json"), "profile": file_hash(profile_path),
            "bindings": {name: file_hash(relative_file(root, name)) for name in payload["bindings"]},
            "rules": {path.relative_to(root).as_posix(): file_hash(path)
                      for path in sorted(rules.glob("*.md"))}}


def checkpoint(root, task, source, expected_revision, owner):
    if not owner.strip() or "\n" in owner or "\r" in owner:
        raise ValueError("Owner must be nonempty single-line text; it is not a lock")
    payload = read_json(Path(source).absolute())
    validate_payload(payload)
    records = history(root, task)
    project_id = identity(root)
    if expected_revision != len(records):
        raise ValueError("Revision conflict; existing records preserved")
    if records and (records[0]["owner"] != owner or records[0]["project_id"] != project_id):
        raise ValueError("Owner or project identity conflict; existing records preserved")
    record = {"schema": 1, "task": task, "project_id": project_id, "owner": owner,
              "revision": len(records) + 1, "payload": payload,
              "fingerprint": current_fingerprint(root, payload)}
    create_file(task_folder(root, task) / f"{record['revision']:06d}.json", encoded(record))
    return record


def resume(root, task):
    result = {"state": "blocked", "task": task, "reasons": []}
    try:
        records = history(root, task)
        if not records:
            raise ValueError("No checkpoint exists for this task")
        record = records[-1]
        result.update(revision=record["revision"], owner=record["owner"], payload=record["payload"])
        if record["project_id"] != identity(root):
            result["reasons"].append("Project identity changed")
        if record["fingerprint"] != current_fingerprint(root, record["payload"]):
            result["reasons"].append("Input, rules, config or profile fingerprint changed")
        if any(effect["status"] == "unknown" for effect in record["payload"]["effects"]):
            result["reasons"].append("Unknown effect requires manual reconciliation; never replayed")
        if record["payload"]["steps_used"] >= record["payload"]["max_steps"]:
            result["reasons"].append("Step budget exhausted")
        if record["payload"]["phase"] == "done":
            result["reasons"].append("Task is already done; no continuation")
        if not result["reasons"]:
            result["state"] = "ready"
    except (OSError, ValueError) as error:
        result["reasons"].append(str(error))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    sub = commands.add_parser("inspect")
    sub.add_argument("root")
    sub = commands.add_parser("profile")
    sub.add_argument("root")
    sub.add_argument("--declarations", type=Path)
    sub.add_argument("--write", action="store_true")
    sub = commands.add_parser("checkpoint")
    sub.add_argument("root")
    sub.add_argument("--task", required=True)
    sub.add_argument("--input", required=True, type=Path)
    sub.add_argument("--expected-revision", required=True, type=int)
    sub.add_argument("--owner", required=True)
    sub = commands.add_parser("resume")
    sub.add_argument("root")
    sub.add_argument("--task", required=True)
    args = parser.parse_args(argv)
    try:
        root = project_root(args.root)
        if args.command == "inspect":
            result = inspect(root)
        elif args.command == "profile":
            result = profile(root, args.declarations, args.write)
        elif args.command == "checkpoint":
            result = checkpoint(root, args.task, args.input, args.expected_revision, args.owner)
        else:
            result = resume(root, args.task)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
