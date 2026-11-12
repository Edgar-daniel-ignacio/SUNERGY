"""Behavioral tests for the portable evidence CLIs; synthetic plumbing only."""

from __future__ import annotations

import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import artifact_compare  # noqa: E402
import evidence_io  # noqa: E402
import integrity  # noqa: E402
import test_results  # noqa: E402


class FilesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def put(self, name: str, data: bytes | str | dict | list) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, (dict, list)):
            path.write_text(json.dumps(data), encoding="utf-8")
        elif isinstance(data, bytes):
            path.write_bytes(data)
        else:
            path.write_text(data, encoding="utf-8")

    def invoke(self, entrypoint, *arguments: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return entrypoint(["--root", str(self.root), *arguments])

    def report(self, name: str = "report.json") -> dict:
        return json.loads((self.root / name).read_text(encoding="utf-8"))


class ArtifactTests(FilesTest):
    def setUp(self) -> None:
        super().setUp()
        self.put("input.txt", "shared effective inputs")
        self.put("old", b"unchanged\n")
        self.put("new", b"unchanged\n")
        self.case = {
            "id": "case-1",
            "mode": "bytes",
            "inputs": ["input.txt"],
            "baseline": "old",
            "candidate": "new",
        }

    def run_case(self) -> int:
        self.put("cases.json", {"schema": "artifact-comparison/v1", "cases": [self.case]})
        return self.invoke(
            artifact_compare.main, "--manifest", "cases.json", "--out", "report.json"
        )

    def json_case(self, old, new, **tolerance) -> None:
        self.case["mode"] = "json"
        self.put("old", old)
        self.put("new", new)
        self.case["tolerances"] = [
            {
                "path": "/power",
                "scope": "subtree",
                "abs": 0.01,
                "rel": 0,
                "unit": "W",
                "rationale": "declared budget",
                **tolerance,
            }
        ]

    def test_exact_bytes_and_hash_provenance(self) -> None:
        self.assertEqual(self.run_case(), 0)
        row = self.report()["cases"][0]
        self.assertTrue(row["exact_bytes"])
        self.assertEqual([file["path"] for file in row["files"]], ["input.txt", "old", "new"])
        self.assertEqual(len(row["files"][0]["sha256"]), 64)

    def test_changed_byte_and_trailing_length(self) -> None:
        for value, offset in [(b"Unchanged\n", 0), (b"unchanged\nmore", 10)]:
            self.put("new", value)
            self.assertEqual(self.run_case(), 1)
            self.assertEqual(self.report()["cases"][0]["differences"][0]["byte_offset"], offset)

    def test_missing_output_is_gap(self) -> None:
        (self.root / "new").unlink()
        self.assertEqual(self.run_case(), 1)
        self.assertEqual(self.report()["cases"][0]["missing"], ["new"])

    def test_zero_cases_is_gap(self) -> None:
        self.put("cases.json", {"schema": "artifact-comparison/v1", "cases": []})
        self.assertEqual(
            self.invoke(artifact_compare.main, "--manifest", "cases.json", "--out", "report.json"),
            1,
        )

    def test_quantity_array_tolerance_and_exact_labels(self) -> None:
        self.json_case(
            {"power": [{"id": "A", "value": 2}, {"id": "B", "value": 3}]},
            {"power": [{"id": "A", "value": 2.005}, {"id": "B", "value": 3}]},
        )
        self.assertEqual(self.run_case(), 0)
        spec = self.report()["cases"][0]["tolerances"][0]
        self.assertEqual((spec["numeric_compared"], spec["within"]), (2, 1))
        self.put("new", {"power": [{"id": "B", "value": 2.005}, {"id": "A", "value": 3}]})
        self.assertEqual(self.run_case(), 1)

    def test_array_shape_and_positional_order_fail(self) -> None:
        for new in [{"power": [1, 2, 3]}, {"power": [2, 1]}]:
            self.json_case({"power": [1, 2]}, new)
            self.assertEqual(self.run_case(), 1)

    def test_object_key_order_and_number_outside_scope_fail(self) -> None:
        self.json_case({"id": 7, "power": [1]}, {"power": [1], "id": 7})
        self.assertEqual(self.run_case(), 1)
        self.put("new", {"id": 8, "power": [1]})
        self.assertEqual(self.run_case(), 1)

    def test_baseline_relative_tolerance(self) -> None:
        self.json_case({"power": [10]}, {"power": [11.05]}, abs=0, rel=0.1)
        self.assertEqual(self.run_case(), 1)

    def test_additive_absolute_and_baseline_relative_budget_boundary(self) -> None:
        self.json_case({"power": 100}, {"power": 101.25}, scope="value", abs=0.75, rel=0.005)
        self.assertEqual(self.run_case(), 0)
        self.put("new", {"power": 101.26})
        self.assertEqual(self.run_case(), 1)

    def test_high_precision_tolerance_boundary_does_not_round_to_pass(self) -> None:
        self.json_case({"power": 1}, {"power": 1}, scope="value", abs=0.1)
        self.put("new", '{"power":1.100000000000000000000000000001}')
        self.assertEqual(self.run_case(), 1)

    def test_exact_json_numeric_values_ignore_lexical_format_only(self) -> None:
        self.case["mode"] = "json"
        self.put("old", '{"id":1,"value":1e-999}')
        self.put("new", '{"id":1.0,"value":0.1e-998}')
        self.assertEqual(self.run_case(), 0)
        self.put("new", '{"id":1,"value":0}')
        self.assertEqual(self.run_case(), 1)

    def test_no_universal_absolute_tolerance_cap(self) -> None:
        self.json_case({"power": [1000]}, {"power": [1001]}, abs=2)
        self.assertEqual(self.run_case(), 0)

    def test_misspelled_and_nonnumeric_quantity_paths_invalid(self) -> None:
        for kwargs in [
            {"path": "/powre"},
            {"path": "/label"},
            {"path": "/power", "scope": "value"},
        ]:
            self.json_case({"power": [1], "label": "A"}, {"power": [1], "label": "A"}, **kwargs)
            self.assertEqual(self.run_case(), 2)

    def test_tolerance_validation_and_overlap(self) -> None:
        for kwargs in [
            {"rationale": ""},
            {"unit": ""},
            {"abs": True},
            {"path": ""},
            {"path": "/bad~2"},
            {"scope": "all"},
            {"abs": -1},
            {"abs": 0},
        ]:
            self.json_case({"power": [1]}, {"power": [1]}, **kwargs)
            self.assertEqual(self.run_case(), 2)
        self.json_case({"power": [1]}, {"power": [1]}, abs=1)
        self.case["tolerances"].append({**self.case["tolerances"][0], "path": "/power/0"})
        self.assertEqual(self.run_case(), 2)

    def test_duplicate_keys_nonfinite_and_unknown_mask_invalid(self) -> None:
        self.case["mode"] = "json"
        for raw in ['{"a": 1, "a": 1}', '{"a": NaN}', '{"a": Infinity}']:
            self.put("old", raw)
            self.put("new", raw)
            self.assertEqual(self.run_case(), 2)
        self.case["mask"] = "ignore all"
        self.assertEqual(self.run_case(), 2)

    def test_input_overwrite_and_escape_refused(self) -> None:
        self.assertEqual(self.run_case(), 0)
        self.assertEqual(
            self.invoke(artifact_compare.main, "--manifest", "cases.json", "--out", "old"), 2
        )
        self.case["candidate"] = "../escape"
        self.assertEqual(self.run_case(), 2)

    def test_identical_output_path_is_invalid(self) -> None:
        self.case["candidate"] = "old"
        self.assertEqual(self.run_case(), 2)

    def test_artifact_and_report_aliases_do_not_overwrite_evidence(self) -> None:
        # Windows case aliases are caught through samefile, independently of spelling.
        self.assertEqual(self.run_case(), 0)
        with patch("pathlib.Path.samefile", return_value=True):
            self.assertEqual(self.run_case(), 2)
            with self.assertRaises(evidence_io.InputError):
                evidence_io.write_report(self.root, "report.json", {}, {"old"})


class ResultsTests(FilesTest):
    def put_results(self, name: str, rows: list[tuple[str, str]]) -> None:
        self.put(
            name,
            {
                "schema": "test-results/v1",
                "tests": [{"id": key, "outcome": value} for key, value in rows],
            },
        )

    def run_results(self) -> int:
        return self.invoke(
            test_results.main,
            "--baseline",
            "old.json",
            "--candidate",
            "new.json",
            "--out",
            "report.json",
        )

    def test_identical_results_and_added_pass(self) -> None:
        self.put_results("old.json", [("a", "pass"), ("b", "skip")])
        self.put_results("new.json", [("a", "pass"), ("b", "skip"), ("c", "pass")])
        self.assertEqual(self.run_results(), 0)
        self.assertEqual(self.report()["added"], ["c"])

    def test_disappeared_test_not_inferred_as_rename(self) -> None:
        self.put_results("old.json", [("a", "pass")])
        self.put_results("new.json", [("renamed", "pass")])
        self.assertEqual(self.run_results(), 1)
        self.assertEqual(self.report()["disappeared"], ["a"])

    def test_failures_skips_and_zero_execution(self) -> None:
        self.put_results("old.json", [("a", "pass")])
        for outcome in ["fail", "error", "skip"]:
            self.put_results("new.json", [("a", outcome)])
            self.assertEqual(self.run_results(), 1)
        self.put_results("new.json", [])
        self.assertEqual(self.run_results(), 1)

    def test_existing_failure_does_not_pass(self) -> None:
        self.put_results("old.json", [("a", "fail")])
        self.put_results("new.json", [("a", "fail")])
        self.assertEqual(self.run_results(), 1)
        self.assertEqual(self.report()["new_failures"], [])

    def test_duplicate_ids_and_typed_totals_invalid(self) -> None:
        self.put_results("old.json", [("a", "pass")])
        self.put_results("new.json", [("a", "pass"), ("a", "pass")])
        self.assertEqual(self.run_results(), 2)
        self.put("new.json", {"schema": "test-results/v1", "totals": {"passed": 1}})
        self.assertEqual(self.run_results(), 2)

    def test_unreadable_missing_and_duplicate_sources_invalid(self) -> None:
        self.put_results("old.json", [("a", "pass")])
        self.assertEqual(self.run_results(), 2)
        self.put_results("new.json", [("a", "pass")])
        with patch("pathlib.Path.read_bytes", side_effect=PermissionError("denied")):
            self.assertEqual(self.run_results(), 2)
        self.assertEqual(
            self.invoke(
                test_results.main,
                "--baseline",
                "old.json",
                "--candidate",
                "new.json",
                "--candidate",
                "new.json",
                "--out",
                "report.json",
            ),
            2,
        )

    def test_real_junit_child_outcomes_and_id(self) -> None:
        raw = b"""<testsuites><testsuite name="pytest">
          <testcase classname="unit" name="passed"/>
          <testcase classname="unit" name="bad"><failure/></testcase>
          <testcase classname="unit" name="error"><error/></testcase>
          <testcase classname="unit" name="skip"><skipped/></testcase>
        </testsuite></testsuites>"""
        tests = test_results.parse_junit(raw)
        self.assertEqual(tests[json.dumps(["unit", "bad"])], "fail")
        self.assertEqual(
            test_results.counts(tests),
            {"error": 1, "fail": 1, "pass": 1, "skip": 1, "executed": 3, "total": 4},
        )

    def test_junit_summary_is_checked_but_never_substitutes_for_records(self) -> None:
        raw = b'<testsuite tests="1" failures="0"><testcase name="a"/></testsuite>'
        self.assertEqual(len(test_results.parse_junit(raw)), 1)
        for raw in [
            b'<testsuite tests="1"/>',
            b'<testsuite failures="1"><testcase name="a"/></testsuite>',
            b'<testsuite><testcase name="a" result="Skipped"/></testsuite>',
            b'<testsuite><testcase name="a"><flakyFailure/></testcase></testsuite>',
            b'<testsuite disabled="1"><testcase name="a"/></testsuite>',
        ]:
            with self.subTest(raw=raw), self.assertRaises(evidence_io.InputError):
                test_results.parse_junit(raw)

    def test_xml_entities_duplicate_ids_malformed_and_ambiguous_invalid(self) -> None:
        samples = [
            b'<!DOCTYPE testsuite [<!ENTITY x "hi">]><testsuite/>',
            "<!DOCTYPE testsuite><testsuite/>".encode("utf-16"),
            b'<testsuite><testcase name="x"/><testcase name="x"/></testsuite>',
            b'<testsuite><testcase name="x"><failure/><skipped/></testcase></testsuite>',
            b'<testsuite><testcase name="x" status="unknown"/></testsuite>',
            b"<not-junit/>",
            b"<testsuite>",
        ]
        for raw in samples:
            with self.subTest(raw=raw), self.assertRaises(evidence_io.InputError):
                test_results.parse_junit(raw)


class IntegrityTests(FilesTest):
    def setUp(self) -> None:
        super().setUp()
        self.put("source/a.py", "DO NOT EXECUTE THIS FILE")
        self.put("source/ignored/cache", "cache")
        self.put(
            "selection.json",
            {
                "schema": "integrity-selection/v1",
                "paths": ["source"],
                "exclude": ["source/ignored"],
            },
        )

    def snapshot(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return integrity.main(
                [
                    "snapshot",
                    "--root",
                    str(self.root),
                    "--manifest",
                    "selection.json",
                    "--out",
                    "snapshot.json",
                ]
            )

    def check(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return integrity.main(
                [
                    "check",
                    "--root",
                    str(self.root),
                    "--snapshot",
                    "snapshot.json",
                    "--out",
                    "report.json",
                ]
            )

    def test_snapshot_unchanged_and_excluded_changes(self) -> None:
        self.assertEqual(self.snapshot(), 0)
        self.put("source/ignored/cache", "changed")
        self.assertEqual(self.check(), 0)
        self.assertEqual([row["path"] for row in self.report()["files"]], ["source/a.py"])

    def test_added_deleted_and_changed_even_with_preserved_mtime(self) -> None:
        self.put("source/delete", "gone")
        self.assertEqual(self.snapshot(), 0)
        original = (self.root / "source/a.py").stat()
        self.put("source/a.py", "changed")
        os.utime(self.root / "source/a.py", ns=(original.st_atime_ns, original.st_mtime_ns))
        self.put("source/added", "new")
        (self.root / "source/delete").unlink()
        self.assertEqual(self.check(), 1)
        self.assertEqual(self.report()["added"], ["source/added"])
        self.assertEqual(self.report()["deleted"], ["source/delete"])
        self.assertEqual(self.report()["changed"][0]["path"], "source/a.py")

    def test_missing_selection_empty_snapshot_and_missing_tree_are_gaps(self) -> None:
        self.put(
            "selection.json",
            {"schema": "integrity-selection/v1", "paths": ["missing"], "exclude": []},
        )
        self.assertEqual(self.snapshot(), 1)
        self.assertEqual(self.check(), 2)
        self.put(
            "selection.json",
            {"schema": "integrity-selection/v1", "paths": ["source"], "exclude": []},
        )
        self.assertEqual(self.snapshot(), 0)
        (self.root / "source").rename(self.root / "moved")
        self.assertEqual(self.check(), 1)

    def test_output_in_selection_overwrite_and_corrupt_snapshot_refused(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            status = integrity.main(
                [
                    "snapshot",
                    "--root",
                    str(self.root),
                    "--manifest",
                    "selection.json",
                    "--out",
                    "source/unsafe.json",
                ]
            )
        self.assertEqual(status, 2)
        self.assertEqual(self.snapshot(), 0)
        snapshot = self.report("snapshot.json")
        snapshot["files"][0]["sha256"] = "incomplete hash"
        self.put("snapshot.json", snapshot)
        self.assertEqual(self.check(), 2)

    def test_traversal_overlap_and_unselected_exclusion_invalid(self) -> None:
        for paths, exclusions in [
            (["../outside"], []),
            (["source", "source/a.py"], []),
            (["source"], ["other"]),
            (["source"], ["source"]),
        ]:
            with self.subTest(paths=paths), self.assertRaises(evidence_io.InputError):
                integrity.selection({"paths": paths, "exclude": exclusions})

    def test_symlinks_and_windows_reparse_points_refused(self) -> None:
        for info in [
            SimpleNamespace(st_mode=stat.S_IFLNK),
            SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400),
        ]:
            with (
                patch("pathlib.Path.lstat", return_value=info),
                self.assertRaises(evidence_io.InputError),
            ):
                evidence_io.reject_links(self.root / "source")

    def test_all_bytes_hashed_beyond_one_chunk(self) -> None:
        self.put("source/large", b"x" * (1024 * 1024 + 20))
        self.assertEqual(self.snapshot(), 0)
        with (self.root / "source/large").open("r+b") as stream:
            stream.seek(1024 * 1024 + 19)
            stream.write(b"y")
        self.assertEqual(self.check(), 1)


class StrictIOTests(unittest.TestCase):
    def test_json_number_does_not_underflow_to_zero(self) -> None:
        self.assertEqual(evidence_io.parse_json(b"1e-999", quantities=True), Decimal("1e-999"))

    def test_unusable_json_integer_is_a_controlled_input_error(self) -> None:
        with self.assertRaises(evidence_io.InputError):
            evidence_io.parse_json(b"9" * 5000)

    def test_common_path_validation(self) -> None:
        for value in [
            "/absolute",
            "C:/absolute",
            "a\\b",
            "a/../b",
            "a//b",
            "./a",
            "",
            "NUL.txt",
            "trailing.",
            "trailing ",
            "bad\x00name",
            "a/*",
        ]:
            with self.subTest(value=value), self.assertRaises(evidence_io.InputError):
                evidence_io.relative_name(value)


if __name__ == "__main__":
    unittest.main()
