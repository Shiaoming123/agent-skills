#!/usr/bin/env python3
"""Import a pinned, user-supplied RSI release locally; never download or execute it."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import tempfile
import zipfile

SKILL = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_lock():
    return json.loads((SKILL / "runtime-source.json").read_text(encoding="utf-8"))


def reject_links(path):
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError(f"Refusing link or reparse point: {item}")


def archive_files(archive, lock):
    raw = archive.read_bytes()
    if sha(raw) != lock["archive_sha256"]:
        raise ValueError("Archive SHA256 does not match runtime-source.json; nothing imported")
    files = {}
    prefix = "rsi-harness/"
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for item in z.infolist():
            if item.filename != item.orig_filename:
                raise ValueError("Archive path was normalized or truncated by ZIP reader")
            if not item.filename.startswith(prefix + "scaffold/") or item.is_dir():
                continue
            name = item.filename[len(prefix):]
            rel = PurePosixPath(name)
            if (rel.is_absolute() or rel.as_posix() != name or ".." in rel.parts
                    or ":" in name or "\\" in name or name in files
                    or stat.S_ISLNK(item.external_attr >> 16)):
                raise ValueError(f"Unsafe or duplicate archive path: {name}")
            files[name] = z.read(item)
    if sha(files.get("scaffold/rsi", b"")) != lock["cli_sha256"]:
        raise ValueError("CLI SHA256 does not match the pinned release")
    if not any(name.startswith("scaffold/templates/") for name in files):
        raise ValueError("Runtime templates are missing")
    return files


def install_runtime(archive, target, dry_run=False):
    archive, target = Path(archive).absolute(), Path(target).absolute()
    reject_links(archive)
    reject_links(target)
    if target == Path(target.anchor):
        raise ValueError("Cannot import at a filesystem root")
    lock = load_lock()
    files = archive_files(archive, lock)
    marker = json.dumps({"version": lock["version"], "archive_sha256": lock["archive_sha256"],
                         "files": {name: sha(data) for name, data in sorted(files.items())}},
                        sort_keys=True, indent=2).encode("utf-8") + b"\n"
    result = {"action": "create", "target": str(target), "files": len(files),
              "version": lock["version"], "dry_run": dry_run}
    if target.exists():
        if not target.is_dir():
            raise ValueError("Runtime destination exists and is not a directory; preserved")
        actual = {}
        for path in target.rglob("*"):
            reject_links(path)
            if path.is_file():
                actual[path.relative_to(target).as_posix()] = sha(path.read_bytes())
        expected = {name: sha(data) for name, data in files.items()}
        expected["IMPORT.json"] = sha(marker)
        if actual != expected:
            raise ValueError("Existing runtime differs or is incomplete; preserved, no overwrite")
        result["action"] = "preserve"
        return result
    if dry_run:
        return result
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".rsi-import-", dir=target.parent) as tmp:
        stage = Path(tmp) / "runtime"
        stage.mkdir()
        for name, data in files.items():
            out = stage / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            if out.name == "rsi" or out.suffix == ".sh":
                out.chmod(0o755)
        (stage / "IMPORT.json").write_bytes(marker)
        reject_links(target)
        if target.exists():
            raise ValueError("Runtime destination appeared during import; preserved")
        # shortcut: single installer; no transaction with unrelated filesystem writers.
        os.rename(stage, target)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--dest", type=Path, default=SKILL / "assets/runtime")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(install_runtime(args.archive, args.dest, args.dry_run), ensure_ascii=False))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Not imported: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
