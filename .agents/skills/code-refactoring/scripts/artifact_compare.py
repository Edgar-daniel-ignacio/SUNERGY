"""Compare declared artifact pairs; reports evidence, never scientific validity."""

from __future__ import annotations

import argparse
from decimal import Decimal
from fractions import Fraction
from typing import Any

from evidence_io import (
    InputError,
    evidence,
    inside,
    invalid_report,
    parse_json,
    read_bytes,
    relative_name,
    require_keys,
    root_path,
    text_field,
    write_report,
)


def pointer_parts(value: Any) -> tuple[str, ...]:
    if not isinstance(value, str) or not value.startswith("/"):
        raise InputError("quantity paths must be non-root JSON Pointers beginning with /")
    result = []
    for token in value[1:].split("/"):
        index = 0
        while index < len(token):
            if token[index] == "~":
                if index + 1 == len(token) or token[index + 1] not in "01":
                    raise InputError(f"invalid JSON Pointer escape: {value}")
                index += 1
            index += 1
        result.append(token.replace("~1", "/").replace("~0", "~"))
    return tuple(result)


def quantity_tolerances(items: Any) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise InputError("tolerances must be a list")
    result = []
    for item in items:
        require_keys(item, {"path", "scope", "abs", "rel", "unit", "rationale"})
        parts = pointer_parts(item["path"])
        if item["scope"] not in ("value", "subtree"):
            raise InputError("tolerance scope must be value or subtree")
        for bound in ("abs", "rel"):
            number = item[bound]
            if isinstance(number, bool) or not isinstance(number, (int, Decimal)):
                raise InputError(f"{bound} must be a finite nonnegative JSON number")
            if not Decimal(number).is_finite() or number < 0:
                raise InputError(f"{bound} must be a finite nonnegative JSON number")
        for label in ("unit", "rationale"):
            text_field(item[label], label)
        if item["abs"] == item["rel"] == 0:
            raise InputError("a tolerance needs a positive abs or rel value")
        for previous in result:
            other = previous["parts"]
            if (
                parts == other
                or (previous["scope"] == "subtree" and parts[: len(other)] == other)
                or (item["scope"] == "subtree" and other[: len(parts)] == parts)
            ):
                raise InputError("tolerance paths must not overlap")
        result.append({**item, "parts": parts, "numeric_compared": 0, "within": 0})
    return result


def display_pointer(parts: tuple[str, ...]) -> str:
    return "".join("/" + token.replace("~", "~0").replace("/", "~1") for token in parts)


def compare_json(old: Any, new: Any, specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    differences: list[dict[str, Any]] = []

    def difference(path: tuple[str, ...], reason: str) -> None:
        differences.append({"path": display_pointer(path), "reason": reason})

    def walk(left: Any, right: Any, path: tuple[str, ...]) -> None:
        if type(left) is not type(right):
            difference(path, "type differs")
        elif isinstance(left, dict):
            if list(left) != list(right):
                difference(path, "object keys or their order differ")
            for key in left:
                if key in right:
                    walk(left[key], right[key], (*path, key))
        elif isinstance(left, list):
            if len(left) != len(right):
                difference(path, "array length differs")
            for index, (a, b) in enumerate(zip(left, right, strict=False)):
                walk(a, b, (*path, str(index)))
        elif isinstance(left, Decimal):
            matched = next(
                (
                    spec
                    for spec in specs
                    if path == spec["parts"]
                    or (spec["scope"] == "subtree" and path[: len(spec["parts"])] == spec["parts"])
                ),
                None,
            )
            if matched is None:
                if left != right:
                    difference(path, "number differs without a quantity tolerance")
            else:
                matched["numeric_compared"] += 1
                # Relative tolerance is relative to the baseline quantity, not the candidate.
                delta = abs(Fraction(left) - Fraction(right))
                limit = Fraction(matched["abs"]) + Fraction(matched["rel"]) * abs(Fraction(left))
                if delta > limit:
                    difference(path, "quantity exceeds declared tolerance")
                elif delta:
                    matched["within"] += 1
        elif left != right:
            difference(path, "value differs")

    walk(old, new, ())
    for spec in specs:
        if not spec["numeric_compared"]:
            raise InputError(f"tolerance matched no comparable numeric values: {spec['path']}")
    return differences


def run(root: Any, manifest_name: str) -> tuple[dict[str, Any], set[str]]:
    raw = read_bytes(root, manifest_name)
    manifest = parse_json(raw)
    require_keys(manifest, {"schema", "cases"})
    if manifest["schema"] != "artifact-comparison/v1" or not isinstance(manifest["cases"], list):
        raise InputError("expected artifact-comparison/v1 with a cases list")
    protected = {manifest_name}
    cases = []
    seen = set()
    for case in manifest["cases"]:
        require_keys(case, {"id", "mode", "inputs", "baseline", "candidate"}, {"tolerances"})
        identifier = text_field(case["id"], "case id")
        if identifier in seen:
            raise InputError(f"duplicate case id: {identifier}")
        seen.add(identifier)
        if case["mode"] not in ("bytes", "json"):
            raise InputError("case mode must be bytes or json")
        inputs = case["inputs"]
        if not isinstance(inputs, list) or not inputs or len(set(inputs)) != len(inputs):
            raise InputError("each case needs a nonempty, unique list of shared input paths")
        names = [relative_name(name) for name in [*inputs, case["baseline"], case["candidate"]]]
        baseline_path, candidate_path = (inside(root, name) for name in names[-2:])
        if names[-1] == names[-2] or (
            baseline_path.exists()
            and candidate_path.exists()
            and baseline_path.samefile(candidate_path)
        ):
            raise InputError("baseline and candidate must be distinct output paths")
        protected.update(names)
        specs = quantity_tolerances(case.get("tolerances", []))
        if case["mode"] == "bytes" and specs:
            raise InputError("byte mode does not accept tolerances")
        row: dict[str, Any] = {"id": identifier, "mode": case["mode"], "files": []}
        contents = []
        missing = []
        for name in names:
            try:
                data = read_bytes(root, name)
            except FileNotFoundError:
                missing.append(name)
                continue
            except InputError as exc:
                # Unsafe paths are invalid, not merely absent output evidence.
                if "not a regular readable file" not in str(exc):
                    raise
                missing.append(name)
                continue
            row["files"].append(evidence(name, data))
            contents.append(data)
        if missing:
            row.update(status="gap", missing=missing)
        else:
            left, right = contents[-2:]
            row["exact_bytes"] = left == right
            if case["mode"] == "bytes":
                row["differences"] = (
                    []
                    if left == right
                    else [
                        {
                            "byte_offset": next(
                                (
                                    i
                                    for i, (a, b) in enumerate(zip(left, right, strict=False))
                                    if a != b
                                ),
                                min(len(left), len(right)),
                            ),
                            "reason": "bytes differ",
                        }
                    ]
                )
            else:
                row["differences"] = compare_json(
                    parse_json(left, quantities=True), parse_json(right, quantities=True), specs
                )
                row["tolerances"] = [
                    {key: value for key, value in spec.items() if key != "parts"} for spec in specs
                ]
            row["status"] = "different" if row["differences"] else "match"
        cases.append(row)
    report = {
        "schema": "artifact-comparison-report/v1",
        "manifest": evidence(manifest_name, raw),
        "cases": cases,
        "status": "pass" if cases and all(row["status"] == "match" for row in cases) else "gap",
    }
    return report, protected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="explicit evidence root directory")
    parser.add_argument("--manifest", required=True, help="manifest path relative to root")
    parser.add_argument("--out", required=True, help="new report path relative to root")
    args = parser.parse_args(argv)
    try:
        root = root_path(args.root)
        report, protected = run(root, args.manifest)
        write_report(root, args.out, report, protected)
    except (InputError, OSError, ArithmeticError, RecursionError, TypeError) as exc:
        return invalid_report(exc)
    print(report["status"])
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
