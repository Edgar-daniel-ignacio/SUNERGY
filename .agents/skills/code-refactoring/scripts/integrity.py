"""Hash explicit source selections and check added, deleted and changed files."""

from __future__ import annotations

import argparse
import re
import stat
from pathlib import Path
from typing import Any

from evidence_io import (
    InputError,
    evidence,
    file_evidence,
    inside,
    invalid_report,
    parse_json,
    read_bytes,
    reject_links,
    relative_name,
    require_keys,
    root_path,
    write_report,
)


def under(name: str, parent: str) -> bool:
    return parent == "." or name == parent or name.startswith(parent + "/")


def selection(obj: Any) -> dict[str, list[str]]:
    require_keys(obj, {"paths", "exclude"})
    for label in ("paths", "exclude"):
        if not isinstance(obj[label], list):
            raise InputError(f"selection {label} must be a list")
        for value in obj[label]:
            relative_name(value, allow_dot=label == "paths")
        if len(set(obj[label])) != len(obj[label]):
            raise InputError(f"duplicate {label} entries")
    if not obj["paths"]:
        raise InputError("selection needs at least one path")
    paths = obj["paths"]
    for index, name in enumerate(paths):
        if any(under(name, other) or under(other, name) for other in paths[:index]):
            raise InputError("selected paths must not overlap")
    for name in obj["exclude"]:
        if not any(under(name, parent) for parent in paths):
            raise InputError(f"exclude is outside selected paths: {name}")
        if name in paths:
            raise InputError("an exclude must not remove an entire selected path")
    return {"paths": sorted(paths), "exclude": sorted(obj["exclude"])}


def included(name: str, policy: dict[str, list[str]]) -> bool:
    return any(under(name, base) for base in policy["paths"]) and not any(
        under(name, excluded) for excluded in policy["exclude"]
    )


def inventory(root: Path, policy: dict[str, list[str]]) -> tuple[list[dict[str, Any]], list[str]]:
    files: list[dict[str, Any]] = []
    missing: list[str] = []

    def visit(path: Path, name: str) -> None:
        if any(under(name, excluded) for excluded in policy["exclude"]):
            return
        reject_links(path)
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            files.append(file_evidence(root, name))
        elif stat.S_ISDIR(info.st_mode):
            for child in sorted(path.iterdir()):
                relative = child.name if name == "." else name + "/" + child.name
                visit(child, relative)
        else:
            raise InputError(f"unsupported non-regular file: {name}")

    for name in policy["paths"]:
        path = inside(root, name, allow_dot=True)
        if not path.exists():
            missing.append(name)
        else:
            visit(path, name)
    return sorted(files, key=lambda row: row["path"]), missing


def snapshot_files(value: Any, policy: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        raise InputError("snapshot files must be a list")
    result = {}
    for row in value:
        require_keys(row, {"path", "bytes", "sha256"})
        name = relative_name(row["path"])
        if name in result or not included(name, policy):
            raise InputError(f"duplicate or out-of-selection snapshot file: {name}")
        if type(row["bytes"]) is not int or row["bytes"] < 0:
            raise InputError("file bytes must be a nonnegative integer")
        if not isinstance(row["sha256"], str) or not re.fullmatch("[0-9a-f]{64}", row["sha256"]):
            raise InputError("snapshot needs a complete lowercase SHA-256 hash per file")
        result[name] = row
    return result


def run_snapshot(root: Path, manifest_name: str, out: str) -> dict[str, Any]:
    raw = read_bytes(root, manifest_name)
    manifest = parse_json(raw)
    require_keys(manifest, {"schema", "paths", "exclude"})
    if manifest["schema"] != "integrity-selection/v1":
        raise InputError("expected integrity-selection/v1")
    policy = selection({key: manifest[key] for key in ("paths", "exclude")})
    if included(relative_name(out), policy):
        raise InputError("snapshot output must be outside its selection or explicitly excluded")
    files, missing = inventory(root, policy)
    return {
        "schema": "integrity-snapshot/v1",
        "manifest": evidence(manifest_name, raw),
        "selection": policy,
        "files": files,
        "missing_selected": missing,
        "status": "pass" if files and not missing else "gap",
    }


def run_check(root: Path, snapshot_name: str, out: str) -> dict[str, Any]:
    raw = read_bytes(root, snapshot_name)
    snapshot = parse_json(raw)
    require_keys(
        snapshot, {"schema", "manifest", "selection", "files", "missing_selected", "status"}
    )
    if snapshot["schema"] != "integrity-snapshot/v1" or snapshot["status"] != "pass":
        raise InputError("check requires a complete, passing integrity-snapshot/v1")
    if snapshot["missing_selected"] != []:
        raise InputError("snapshot has missing selections")
    policy = selection(snapshot["selection"])
    for name in (snapshot_name, out):
        if included(relative_name(name), policy):
            raise InputError("snapshot and check output must be outside selection or excluded")
    before = snapshot_files(snapshot["files"], policy)
    if not before:
        raise InputError("snapshot contains zero files")
    files, missing = inventory(root, policy)
    after = {row["path"]: row for row in files}
    added = sorted(after.keys() - before.keys())
    deleted = sorted(before.keys() - after.keys())
    changed = [
        {"path": name, "before": before[name], "after": after[name]}
        for name in sorted(before.keys() & after.keys())
        if before[name] != after[name]
    ]
    return {
        "schema": "integrity-check/v1",
        "snapshot": evidence(snapshot_name, raw),
        "selection": policy,
        "files": files,
        "missing_selected": missing,
        "added": added,
        "deleted": deleted,
        "changed": changed,
        "status": "gap" if added or deleted or changed or missing else "pass",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("snapshot", "check"):
        sub = commands.add_parser(name, help=f"{name} an explicit file selection")
        sub.add_argument("--root", required=True, help="explicit source root directory")
        sub.add_argument("--out", required=True, help="relative output path; parent must exist")
        sub.add_argument("--manifest" if name == "snapshot" else "--snapshot", required=True)
    args = parser.parse_args(argv)
    try:
        root = root_path(args.root)
        source = args.manifest if args.command == "snapshot" else args.snapshot
        report = (
            run_snapshot(root, source, args.out)
            if args.command == "snapshot"
            else run_check(root, source, args.out)
        )
        write_report(root, args.out, report, {source, *(row["path"] for row in report["files"])})
    except (InputError, OSError, RecursionError, TypeError) as exc:
        return invalid_report(exc)
    print(report["status"])
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
