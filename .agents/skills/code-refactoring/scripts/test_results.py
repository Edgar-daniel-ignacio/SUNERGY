"""Compare explicit per-test JUnit XML or JSON result files without executing tests."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any
from xml.parsers import expat

from evidence_io import (
    InputError,
    evidence,
    invalid_report,
    parse_json,
    read_bytes,
    require_keys,
    root_path,
    text_field,
    write_report,
)

OUTCOMES = {"pass", "fail", "error", "skip"}


def parse_junit(data: bytes) -> dict[str, str]:
    tests: dict[str, str] = {}
    stack: list[str] = []
    suites: list[tuple[dict[str, str], Counter[str]]] = []
    current: dict[str, Any] | None = None

    def refuse(*_args: Any) -> Any:
        raise InputError("DTD and entity declarations are forbidden in test evidence")

    def start(tag: str, attrs: dict[str, str]) -> None:
        nonlocal current
        if not stack and tag not in ("testsuite", "testsuites"):
            raise InputError("expected a JUnit testsuite or testsuites root")
        if (
            stack
            and stack[-1] == "testcase"
            and tag
            not in {
                "failure",
                "error",
                "skipped",
                "system-out",
                "system-err",
                "properties",
            }
        ):
            raise InputError(f"unsupported JUnit testcase result element: {tag}")
        if tag in ("testsuite", "testsuites"):
            if stack and stack[-1] not in ("testsuite", "testsuites"):
                raise InputError("JUnit suites must be direct children of suites")
            suites.append((attrs, Counter()))
        if tag == "testcase":
            if current is not None or not stack or stack[-1] != "testsuite":
                raise InputError("testcase must be a direct child of testsuite")
            name = text_field(attrs.get("name"), "JUnit testcase name")
            identifier = json.dumps([attrs.get("classname", ""), name], ensure_ascii=True)
            flag = attrs.get("status", "run").lower()
            if flag not in ("run", "passed", "failed", "error", "skipped", "notrun", "disabled"):
                raise InputError(f"unsupported JUnit testcase status: {flag}")
            if "result" in attrs:
                raise InputError("JUnit result attributes need an explicit per-test JSON adapter")
            mapped = {
                "passed": "pass",
                "failed": "fail",
                "error": "error",
                "skipped": "skip",
                "notrun": "skip",
                "disabled": "skip",
            }.get(flag)
            current = {"id": identifier, "outcomes": {mapped} if mapped else set()}
        elif tag in ("failure", "error", "skipped"):
            if current is None or stack[-1] != "testcase":
                raise InputError(f"{tag} must be a direct child of testcase")
            current["outcomes"].add({"failure": "fail", "error": "error", "skipped": "skip"}[tag])
        stack.append(tag)

    def end(tag: str) -> None:
        nonlocal current
        if tag == "testcase":
            assert current is not None
            if len(current["outcomes"]) > 1:
                raise InputError(f"conflicting outcomes for test: {current['id']}")
            identifier = current["id"]
            if identifier in tests:
                raise InputError(f"duplicate test id: {identifier}")
            outcome = next(iter(current["outcomes"]), "pass")
            tests[identifier] = outcome
            for _attrs, totals in suites:
                totals[outcome] += 1
            current = None
        elif tag in ("testsuite", "testsuites"):
            attrs, totals = suites.pop()
            if attrs.get("disabled", "0") != "0":
                raise InputError("JUnit disabled suite counts need a per-test JSON adapter")
            for label, measured in {
                "tests": sum(totals.values()),
                "failures": totals["fail"],
                "errors": totals["error"],
                "skipped": totals["skip"],
            }.items():
                if label in attrs:
                    declared = attrs[label]
                    if (
                        not declared.isascii()
                        or not declared.isdecimal()
                        or int(declared) != measured
                    ):
                        raise InputError(f"JUnit {label} summary disagrees with per-test records")
        stack.pop()

    parser = expat.ParserCreate()
    parser.StartDoctypeDeclHandler = refuse
    parser.EntityDeclHandler = refuse
    parser.ExternalEntityRefHandler = refuse
    parser.StartElementHandler = start
    parser.EndElementHandler = end
    try:
        parser.Parse(data, True)
    except expat.ExpatError as exc:
        raise InputError(f"invalid JUnit XML: {exc}") from exc
    return tests


def parse_test_json(data: bytes) -> dict[str, str]:
    obj = parse_json(data)
    require_keys(obj, {"schema", "tests"})
    if obj["schema"] != "test-results/v1" or not isinstance(obj["tests"], list):
        raise InputError("expected test-results/v1 with per-test entries, not totals")
    tests = {}
    for row in obj["tests"]:
        require_keys(row, {"id", "outcome"})
        identifier = text_field(row["id"], "test id")
        outcome = row["outcome"]
        if not isinstance(outcome, str) or outcome not in OUTCOMES:
            raise InputError(f"unsupported outcome for test {identifier}")
        if identifier in tests:
            raise InputError(f"duplicate test id: {identifier}")
        tests[identifier] = outcome
    return tests


def load_results(root: Any, names: list[str]) -> tuple[dict[str, str], list[dict[str, Any]]]:
    tests: dict[str, str] = {}
    sources = []
    for name in names:
        raw = read_bytes(root, name)
        if name.lower().endswith(".xml"):
            more = parse_junit(raw)
            kind = "junit"
        elif name.lower().endswith(".json"):
            more = parse_test_json(raw)
            kind = "per-test-json"
        else:
            raise InputError("test result file must have .xml or .json extension")
        duplicate = tests.keys() & more.keys()
        if duplicate:
            raise InputError(f"duplicate test ids across result files: {sorted(duplicate)}")
        tests.update(more)
        sources.append({**evidence(name, raw), "format": kind, "tests": len(more)})
    return tests, sources


def counts(tests: dict[str, str]) -> dict[str, int]:
    values = Counter(tests.values())
    result = {key: values[key] for key in sorted(OUTCOMES)}
    result["executed"] = result["pass"] + result["fail"] + result["error"]
    result["total"] = len(tests)
    return result


def compare(before: dict[str, str], after: dict[str, str]) -> dict[str, Any]:
    old_counts, new_counts = counts(before), counts(after)
    disappeared = sorted(before.keys() - after.keys())
    added = sorted(after.keys() - before.keys())
    changes = [
        {"id": key, "before": before[key], "after": after[key]}
        for key in sorted(before.keys() & after.keys())
        if before[key] != after[key]
    ]
    failures = sorted(key for key, value in after.items() if value in {"fail", "error"})
    newly_failing = [key for key in failures if before.get(key) not in {"fail", "error"}]
    newly_skipped = sorted(
        key for key, value in after.items() if value == "skip" and before.get(key) != "skip"
    )
    gaps = []
    if not old_counts["executed"] or not new_counts["executed"]:
        gaps.append("baseline and candidate must each execute at least one test")
    if disappeared:
        gaps.append("baseline test ids disappeared")
    if failures:
        gaps.append("candidate contains failing or errored tests")
    if newly_skipped or new_counts["skip"] > old_counts["skip"]:
        gaps.append("candidate has newly skipped tests or skip growth")
    if new_counts["executed"] < old_counts["executed"]:
        gaps.append("executed test count decreased")
    return {
        "baseline_counts": old_counts,
        "candidate_counts": new_counts,
        "disappeared": disappeared,
        "added": added,
        "changes": changes,
        "candidate_failures": failures,
        "new_failures": newly_failing,
        "newly_skipped": newly_skipped,
        "gaps": gaps,
        "status": "gap" if gaps else "pass",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="explicit evidence root directory")
    parser.add_argument("--baseline", required=True, action="append", help="relative XML/JSON file")
    parser.add_argument(
        "--candidate", required=True, action="append", help="relative XML/JSON file"
    )
    parser.add_argument("--out", required=True, help="report path relative to root")
    args = parser.parse_args(argv)
    try:
        root = root_path(args.root)
        before, old_files = load_results(root, args.baseline)
        after, new_files = load_results(root, args.candidate)
        report = {
            "schema": "test-comparison-report/v1",
            **compare(before, after),
            "baseline_files": old_files,
            "candidate_files": new_files,
            "baseline_tests": before,
            "candidate_tests": after,
        }
        write_report(root, args.out, report, set(args.baseline + args.candidate))
    except (InputError, OSError, RecursionError, TypeError) as exc:
        return invalid_report(exc)
    print(report["status"])
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
