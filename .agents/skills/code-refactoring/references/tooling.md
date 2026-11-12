# Portable evidence tools

Use these optional Python standard-library CLIs when the selected contract needs
deterministic file, numerical, test-result, or integrity comparisons. They inspect
already captured evidence; they do not run source, tests, shell commands, models,
or an LLM. Python 3.12+ is sufficient. Copy the entire `scripts/` directory together
when reusing the tools outside this skill; there is no install or project import.

All tools require an explicit `--root` and `--out`. Every other file path and
`--out` are canonical forward-slash paths relative to that root. Output parent
directories must already exist. Absolute paths, `..`, Windows device names,
symlinks, and Windows reparse points in any visited component are refused. An
excluded integrity subtree is not visited. There is no implicit discovery or
ignore list. Inputs are never overwritten, including an existing output alias
that is a hard link to an input. Reports are replaced atomically after a complete
comparison; on invalid input no new report is written, so an older report at the
same path must not be reused. Use distinct run directories and check exit codes.

Exit codes are shared:

| Exit | Meaning |
|---|---|
| `0` | This tool's documented comparison criteria passed. |
| `1` | A difference or evidence gap was found; read the JSON report. |
| `2` | Input, schema, path, or output was unusable; read the JSON error on stdout. |

Unknown JSON fields, duplicate keys, nonfinite numbers, and malformed data fail
closed. Hashes use SHA-256 over all file bytes, with byte counts. No file mtime is
used. Reports identify their input files by hash and contain data rather than an
overall refactoring, scientific, or validation verdict. Record the tool revision,
commands, environment, producer runs and evidence hashes in the existing task
record. A hash identifies bytes; it does not authenticate their origin or prove
that those bytes came from independent runs. Keep selected files quiescent during
capture/check: these tools do not provide a filesystem transaction or defend
against concurrent adversarial path replacement.

## Artifact comparison

```text
python PATH_TO_SKILL/scripts/artifact_compare.py --root RUN_DIR --manifest cases.json --out comparison.json
```

The manifest declares every case and shared effective input file. `inputs` must
be a nonempty list of unique file paths. Capture zero-argument/environment-driven
cases with a real, recorded conditions file rather than omitting their conditions.
The baseline and candidate output files must be distinct: identical path strings
and known aliases to the same physical file (hard links or Windows case aliases)
are invalid, while identical bytes in separate files are allowed. The tool hashes every
input and both outputs but cannot establish that a producer actually used them.

```json
{
  "schema": "artifact-comparison/v1",
  "cases": [
    {
      "id": "nominal-curve",
      "mode": "json",
      "inputs": ["inputs/nominal.json"],
      "baseline": "baseline/curve.json",
      "candidate": "candidate/curve.json",
      "tolerances": [
        {
          "path": "/power_w",
          "scope": "subtree",
          "abs": 0.0001,
          "rel": 0.000001,
          "unit": "W",
          "rationale": "Example only: replace with the reviewed quantity-specific budget."
        }
      ]
    }
  ]
}
```

Choose mode explicitly:

- `bytes`: every byte must match, including line endings and trailing content;
  the report gives the first differing byte offset. Tolerances are forbidden.
- `json`: decode UTF-8 JSON (an optional BOM is accepted), preserve object key
  order and array length/order, compare types and nonnumeric values exactly.
  JSON numbers are exact decimal values: `1` and `1.0`, or `-0` and `0`, compare
  equal as numbers. Whitespace, escapes with the same decoded string, and numeric
  spelling may differ. `exact_bytes` separately records byte identity. Use byte
  mode when lexical representation is part of the contract.

In JSON mode there is no default numerical tolerance. Each declaration names one
non-root JSON Pointer (`~0` escapes `~`, `~1` escapes `/`) with either `value` for
one numeric leaf or `subtree` for numeric leaves below a quantity array/object.
For example, `/power_w` with `subtree` handles every sample in the power array;
`/power_w/0` with `value` handles only the first sample. There are no wildcards,
masks, sorting, resampling, record dropping or approved-difference switches.
Array elements are compared at their original indices. Nonnumeric fields inside
a tolerance scope remain exact, as do all numbers outside it. Numeric identifiers
must remain outside quantity tolerance scopes: the tool cannot infer whether a
number is a measurement or an identifier. Prefer arrays containing only the named
quantity over tolerating a whole record that also contains numeric identifiers.

Each tolerance requires finite nonnegative `abs` and `rel`, at least one positive,
plus nonempty `unit` and `rationale`. Units are recorded, never converted. There
is no global numerical cap: a reviewer must justify the actual quantity budget.
The exact rational comparison is
`abs(candidate - baseline) <= abs + rel * abs(baseline)`, avoiding binary
float conversion and decimal-context rounding. Overlapping declarations or a
declaration that matches no comparable numeric leaf are invalid (including a
misspelled path). Reports retain declared bounds as exact decimal strings when
they were JSON decimals, plus numeric comparison and within-budget change counts.

A missing input/output is a gap. Shape, order, exact-field and out-of-budget
differences fail. An empty case list is a gap. Empty byte artifacts can match;
the reviewer must establish whether empty output is meaningful for that case.
Invalid JSON/nonfinite values fail even if both files have identical bytes.
Files are fully read into memory for artifact and test-result parsing; the tools
do not silently truncate inputs or result lists. Very large evidence needs an
explicit streaming format/adapter designed for its contract.

## Test-result comparison

```text
python PATH_TO_SKILL/scripts/test_results.py --root RUN_DIR --baseline baseline/results.xml --candidate candidate/results.xml --out tests.json
```

Repeat `--baseline` and `--candidate` for explicitly selected result files from
one run on each side. Directories, logs, Markdown totals and guessed result paths
are not accepted. File extensions select `.xml` JUnit or `.json` per-test adapter
format. Duplicate IDs within or across files are invalid even when outcomes agree;
do not combine retries or repeated runs as though they were disjoint tests.

JUnit supports a `testsuite`/`testsuites` root and direct `testcase` children of
`testsuite`. Test IDs are the JSON-encoded pair `[classname, name]`, with an empty
class name if absent; names are never normalized, shortened or inferred renamed.
A testcase without an outcome child passes; `failure`, `error`, and `skipped`
children map to `fail`, `error`, and `skip`. Documented testcase status attributes
`run`, `passed`, `failed`, `error`, `skipped`, `notrun`, and `disabled` are accepted;
conflicting statuses/children fail. Optional suite totals for tests, failures,
errors and skipped are checked against parsed per-test records and never replace
them. DTD/entity declarations are refused by the XML parser, including UTF-16
documents. Unsupported result children, testcase `result` attributes, nonzero
suite `disabled` counts, namespaces and other dialects require an explicit adapter.
Some runners count successful subtests in suite totals while omitting their
per-test records; such reports are refused rather than assigning that aggregate
count to executable test IDs. Preserve the raw report and use a runner-specific
adapter only when its per-test execution evidence can be recovered.

An adapter must write per-test records from the real runner's raw results:

```json
{
  "schema": "test-results/v1",
  "tests": [
    {"id": "module::test_boundary[param]", "outcome": "pass"},
    {"id": "module::test_unavailable_backend", "outcome": "skip"}
  ]
}
```

Allowed outcomes are exactly `pass`, `fail`, `error`, `skip`. Pin and inspect
the adapter, retain/hash the original runner output, and record its command in
the task record. To compare an adapter with JUnit, use the exact JUnit ID string
format above. Neither JSON nor XML authenticates a runner execution by itself;
synthetic test records only verify the parser/comparison plumbing.

The report lists full per-test maps, changes, added/disappeared IDs, candidate and
new failures, newly skipped IDs, parsed counts, and hashed result files. Exit 0
requires executed tests on both sides, no disappeared baseline IDs, no candidate
failures/errors (including pre-existing failures), no newly skipped tests or skip
growth, and no drop in executed count. Added passing tests and previously failing
tests that now pass are recorded without failing. Unchanged baseline skips are
visible and do not independently fail this regression check; they remain excluded
from executed coverage. A zero-executed baseline/candidate is a gap.

This compares reported outcomes and identities. It cannot establish adequate
assertions, unchanged test code, exercised branches, clean builds, runner exit
status, fresh execution, or scientific validity. Pair it with the relevant source
inventory, raw commands/results, contract review and discrepancy/canary evidence.

## Source and test integrity

```json
{
  "schema": "integrity-selection/v1",
  "paths": ["legacy/module", "tests/compatibility"],
  "exclude": ["legacy/module/generated"]
}
```

```text
python PATH_TO_SKILL/scripts/integrity.py snapshot --root PROJECT_DIR --manifest selection.json --out run/source-before.json
python PATH_TO_SKILL/scripts/integrity.py check --root PROJECT_DIR --snapshot run/source-before.json --out run/source-after.json
```

Each selected path is one file or a recursively traversed directory. A selected
`.` means the whole explicit root. Paths may not overlap. Exclusions are exact
file/directory paths with subtree semantics, not globs; they must fall within a
selection and must not remove an entire selected path. There are no automatic
build/cache/hidden-file exclusions. Review and record every exclusion, especially
when checking legacy preservation or unchanged tests. A selected symlink/reparse
point is invalid; an explicitly excluded subtree is not inspected or attested.

Snapshot stores the selection policy, manifest identity, and sorted relative file
names, complete hashes and byte counts. Missing selected paths or an inventory
with zero files is a gap, and a gap snapshot cannot be checked as a valid baseline.
`check` reuses the snapshot's selection, lists every added/deleted/changed file,
and fails for any difference or missing selected path. Snapshot/check outputs must
be outside the selected trees or explicitly excluded. This prevents the inventory
from changing itself. No source is imported or run; no Git command is required.
Hashes detect changed content even when file mtimes are preserved. Files are
hashed in chunks to EOF. Permissions, mtimes, empty directory identities, links,
and changes outside the selection/excluded trees are not part of this inventory.

The snapshot must be retained with independently recorded hash/revision evidence.
Editing the snapshot can forge its claimed baseline; hashing the snapshot in a
later check identifies what was checked but cannot establish its earlier origin.

## Verification and adaptation record

Run persistent synthetic behavioral tests and targeted style checks from a
checkout containing Python and Ruff (Ruff is optional tooling, not a dependency
of the CLIs):

```text
python -B -m unittest discover -s PATH_TO_SKILL/scripts/tests -v
ruff check --isolated --select E,F,I,UP,B --line-length 100 PATH_TO_SKILL/scripts
ruff format --isolated --check --line-length 100 PATH_TO_SKILL/scripts
```

The tests exercise positive matches and meaningful injected discrepancies,
negative parsing/schema/containment cases, missing/zero evidence, precision
boundaries, JUnit summaries/entities/duplicates, disappearing tests and skip/fail
growth, full-file hashes, explicit exclusions and link/reparse-point refusal.
These are tool tests, not legacy parity or scientific verification cases.

The supplied `code-modernization` package was selectively inspected as design
input. These compact implementations adapt its useful operational ideas rather
than importing its scripts, Claude API/runtime, hooks, HTML dashboard, or command
workflow. Its README declares Apache 2.0, but the supplied package has no root
license file or independently identified upstream revision. No upstream code was
transplanted wholesale; retain this provenance limitation before any broader
redistribution or closer source adaptation.

| Supplied capability | Portable counterpart or deliberate boundary |
|---|---|
| `compare.py`: paired artifact cases, hashing, discrepancy detection | `artifact_compare.py`: declared cases and hashes; adds ordered JSON quantity scopes and exact rational comparison; omits masks, global caps and approved-difference passes. |
| `baseline_diff.py`: per-test runner results and regressions | `test_results.py`: explicit JUnit/per-test JSON, duplicates and summary disagreement fail; no Markdown/log totals, fuzzy renames or ignored flaky failures. |
| `uplift_checks.py`: inspect test-file changes | `integrity.py`: explicit source/test selections, complete hashes and added/deleted/changed file lists; no percentage threshold excuses changes. |
| `proof_pack.py`: source untouched check and evidence aggregation | `integrity.py` replaces mtime inference with byte identity; aggregation remains a bounded task-record review, with each evidence gate separate. |
| `trace_rules.py`: rule mentions and executed-test linkage | Keep a procedural mapping from contract/rule to actual test ID, assertions, raw run and outcome. A static rule mention locates evidence; it does not prove coverage. No heuristic coverage verdict is provided. |
| `proof_pack.py`: universal verdict and fixed fresh-case count | Omitted. Choose cases from the selected contract and risks; report exactly what ran and what it cannot establish. |
