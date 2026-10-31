#!/usr/bin/env python3
"""One isolated candidate, frozen grading contract, advisory comparison only."""
import argparse
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

# A plain CLI preview must not create a local helper bytecode cache.
sys.dont_write_bytecode = True
from import_runtime import reject_links, sha

LOG_LIMIT = 1024 * 1024


def file_path(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Expected explicit absolute path")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("Expected absolute path without traversal")
    reject_links(path)
    return path.resolve()


def relative_file(root, name):
    if not isinstance(name, str) or not name:
        raise ValueError("Empty subject path")
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts or rel.as_posix() != name or ":" in name or "\\" in name:
        raise ValueError("Noncanonical subject path")
    if any(p.casefold() == ".git" for p in rel.parts):
        raise ValueError("Git metadata is not a subject input")
    reserved = {"CON", "PRN", "AUX", "NUL", *{f"COM{i}" for i in range(1, 10)}, *{f"LPT{i}" for i in range(1, 10)}}
    cursor = root
    for part in rel.parts:
        if part.endswith((".", " ")) or part.split(".")[0].upper() in reserved:
            raise ValueError("Ambiguous subject path")
        if os.name == "nt" and cursor.is_dir():
            matches = [p.name for p in cursor.iterdir() if p.name.casefold() == part.casefold()]
            if matches and part not in matches:
                raise ValueError("Subject path case must match disk")
        cursor = cursor / part
    path = root / rel
    reject_links(path)
    if path.exists() and not path.is_file():
        raise ValueError("Subject input must be a file")
    return path


def load_policy(path):
    reject_links(path)
    spec = json.loads(path.read_bytes())
    if not isinstance(spec, dict) or type(spec.get("schema")) is not int or spec["schema"] != 1:
        raise ValueError("Expected policy schema 1")
    if spec.get("isolated") is not True:
        raise ValueError("Explicit isolated-copy declaration required; it is not a sandbox")
    roots = [file_path(spec.get(name)) for name in ("baseline", "candidate")]
    if any(not r.is_dir() for r in roots) or roots[0].is_relative_to(roots[1]) or roots[1].is_relative_to(roots[0]):
        raise ValueError("Subject roots must be existing, disjoint, non-nested directories")
    grader = file_path(spec.get("grader"))
    inputs = spec.get("inputs")
    if not isinstance(inputs, list) or not inputs or len(inputs) != len(set(inputs)):
        raise ValueError("Expected nonempty distinct shared inputs")
    shared = [grader, *[file_path(v) for v in inputs], path.resolve(),
              Path(__file__).resolve(), Path(__file__).with_name("import_runtime.py").resolve(),
              Path(sys.executable).resolve()]
    if grader.suffix != ".py" or any(not p.is_file() for p in shared):
        raise ValueError("Python grader and shared files must exist")
    if any(p.is_relative_to(r) for p in shared for r in roots):
        raise ValueError("Policy, grader and shared inputs must be outside both subjects")
    names = spec.get("subject_files")
    if not isinstance(names, list) or not names or any(not isinstance(n, str) for n in names) or len(names) != len(set(names)):
        raise ValueError("Expected distinct subject_files")
    for r in roots:
        for n in names:
            relative_file(r, n)
    if type(spec.get("trials")) is not int or not 1 <= spec["trials"] <= 5:
        raise ValueError("trials must be 1..5")
    for key, low, high in (("timeout_seconds", 0, 30), ("min_delta", 0, 1)):
        v = spec.get(key)
        if type(v) not in (int, float) or not math.isfinite(v) or not low < v <= high:
            raise ValueError(f"Invalid {key}")
    if type(spec.get("deterministic")) is not bool:
        raise ValueError("deterministic must be an explicit boolean declaration")
    return spec, roots, grader, shared


def fingerprint(spec, roots, shared):
    result = {}
    for path in shared:
        reject_links(path)
        result[str(path)] = sha(path.read_bytes())
    for root in roots:
        for name in spec["subject_files"]:
            path = relative_file(root, name)
            result[str(path)] = sha(path.read_bytes()) if path.is_file() else None
    return result


def grade(grader, root, timeout):
    started = time.monotonic()
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        proc = subprocess.Popen([sys.executable, "-B", "-X", "utf8", str(grader)],
            cwd=root, env=dict(os.environ, RSI_SUBJECT_ROOT=str(root), PYTHONDONTWRITEBYTECODE="1"),
            stdout=out, stderr=err, shell=False,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        reason = "completed"
        while proc.poll() is None:
            if max(os.fstat(out.fileno()).st_size, os.fstat(err.fileno()).st_size) > LOG_LIMIT:
                reason = "output_limit"
            elif time.monotonic() - started >= timeout:
                reason = "timeout"
            if reason != "completed":
                proc.kill()
                break
            try:
                proc.wait(timeout=0.02)
            except subprocess.TimeoutExpired:
                pass
        proc.wait(timeout=5)
        out.seek(0); err.seek(0)
        stdout, stderr = out.read(LOG_LIMIT + 1), err.read(LOG_LIMIT + 1)
        if max(len(stdout), len(stderr)) > LOG_LIMIT:
            reason = "output_limit"
        run = {"exit_code": proc.returncode, "reason": reason,
               "elapsed_seconds": time.monotonic() - started,
               "stdout_sha256": sha(stdout[:LOG_LIMIT]), "stderr_sha256": sha(stderr[:LOG_LIMIT]),
               "score": None}
        if reason != "completed" or proc.returncode != 0:
            run["reason"] = reason if reason != "completed" else "grader_error"
            return run
        try:
            value = json.loads(stdout)
            score = value["score"]
            if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError("Invalid score")
            run["score"] = score
        except (ValueError, TypeError, KeyError):
            run["reason"] = "invalid_grade"
        return run


def compare(policy, execute=False, output=None):
    spec, roots, grader, shared = load_policy(policy)
    if output is not None:
        output = output.absolute()
        reject_links(output)
        if not execute or output.exists() or any(output.resolve().is_relative_to(r) for r in roots):
            raise ValueError("Output requires execution, a new file, and a location outside both subjects")
    binding = fingerprint(spec, roots, shared)
    report = {"schema": 1, "action": "dry-run", "binding": binding,
              "trials": spec["trials"], "timeout_seconds": spec["timeout_seconds"],
              "automatic_promotion": False, "isolation": "caller_declared_not_enforced",
              "environment": {"python": platform.python_version(), "platform": platform.platform(),
                              "executable_sha256": sha(Path(sys.executable).read_bytes())}}
    if execute:
        report.update(action="compare", runs=[], decision="invalid")
        scores = {"baseline": [], "candidate": []}
        for trial in range(spec["trials"]):
            for index in ((0, 1) if trial % 2 == 0 else (1, 0)):
                label = ("baseline", "candidate")[index]
                run = grade(grader, roots[index], spec["timeout_seconds"])
                run.update(subject=label, trial=trial + 1)
                report["runs"].append(run)
                try:
                    unchanged = fingerprint(spec, roots, shared) == binding
                except (OSError, ValueError):
                    unchanged = False
                if not unchanged:
                    report["reason"] = "binding_changed"
                    return report
                if run["reason"] != "completed":
                    report["reason"] = run["reason"]
                    return report
                scores[label].append(run["score"])
        deltas = [b - a for a, b in zip(scores["baseline"], scores["candidate"])]
        report["paired_deltas"] = deltas
        report["decision"] = ("equivalent" if all(d == 0 for d in deltas) else
            "candidate_preferred" if all(d >= spec["min_delta"] for d in deltas) else
            "baseline_preferred" if all(d <= -spec["min_delta"] for d in deltas) else "inconclusive")
        if not spec["deterministic"]:
            report["decision"] = "inconclusive"
        report["meaning"] = "Observed under this declared grading contract; not an intelligence or statistical significance claim"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = compare(args.policy.absolute(), args.execute, args.output)
        payload = json.dumps(result, ensure_ascii=False, allow_nan=False)
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            reject_links(args.output.absolute())
            with args.output.open("x", encoding="utf-8", newline="\n") as file:
                file.write(payload + "\n")
        print(payload)
        return 2 if result.get("decision") == "invalid" else 0
    except (OSError, ValueError, TypeError) as error:
        print(f"Comparison not completed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
