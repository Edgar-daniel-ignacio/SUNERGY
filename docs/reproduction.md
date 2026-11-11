# Legacy reproduction contract

Current status: **selected IV_R and Faiman/NOCT numerical boundaries captured,
implemented and compared; full backend reproduction remains incomplete**.
The [coverage map](legacy_backend_coverage.md) reconciles the curated investigation
with actual owners, evidence gaps and dependency order. [Assumptions](assumptions.md)
and [flowcharts](flowcharts.md) explain the implemented transformations and science
limits. A representative successful run does not close the full backend gate.

## Distinct gates

| Gate | Question | Required evidence |
|---|---|---|
| Input/schema validation | Are boundary inputs structurally valid, typed and explicit? | Pydantic and boundary tests; no physical-accuracy claim. |
| Reproduction | Does the modern implementation reproduce one named legacy branch under equivalent inputs/assumptions? | Independently captured legacy artifacts, manifest, exact structure checks and reviewed quantity-specific tolerances. |
| Scientific verification | Are equations, units, physical assumptions and numerical behavior defensible? | Primary formulations, independent references/implementations where appropriate, limiting cases and meaningful physical tests. |
| Measurement comparison | How do predictions compare with empirical observations? | Original measurement provenance, normalization history, conditions, uncertainty and comparison method. |
| Calibration | Which explicit parameter changes are justified by fitting evidence? | Preserved uncalibrated run, fitted identities/values, objective/bounds, measurement links and held-out evaluation status. Good fit alone is not independent validation. |

A reproduced bug remains a bug. Keep a compatibility model/version separate from
any reviewed corrected model and test both explicitly. Neither missing evidence
nor exact numerical agreement authorizes a scientifically validated default.

## Capture and artifact locations

- [`tests/fixtures/legacy/`](../tests/fixtures/legacy/) is reserved for deliberately
  selected, small, redistributable original-source captures with manual/synthetic
  inputs. These are software references, not weather or measurement evidence.
- [`capture_status.json`](../tests/fixtures/legacy/capture_status.json) records the
  partial coverage and manifest paths; integrity checks validate every recorded
  source, wrapper, environment lock, input and output hash before replay.
- [`backend/src/sunergy/regression.py`](../backend/src/sunergy/regression.py) owns
  the executable capture-manifest and numerical-comparison contract. Its tests
  exercise comparison plumbing separately from the real captures compared by
  `sunergy.replay` and the model/thermal tests.
- [`legacy_inventory.json`](evidence/legacy_inventory.json) records source-file
  preservation hashes; it is not a numerical baseline.
- [Unchanged supplied summary](evidence/pv_physics_engine_evidence_summary_for_agent_research_equations_fixed.md)
  and [copy provenance](evidence/provenance.json) are attributed source evidence,
  not golden outputs. Private uploads, caches and generated results use separate
  ignored locations documented in [architecture](architecture.md).

## Minimum independent capture record

The next capture must record these items, extending the manifest deliberately
where a selected branch requires more detail:

1. Source revision, exact entrypoint/function/branch and hashes of inspected
   source files, plus any controlled capture wrapper and invocation. Record dirty
   source changes explicitly rather than substituting a remote revision.
2. Python, platform/architecture, pvlib, PySAM/SSC, NumPy, SciPy and pandas versions
   and a reproducible dependency environment. CEC `fit_cec_sam` requires PySAM;
   full-system PySAM integration being deferred does not remove that requirement.
3. Exact supplied and effective inputs, with keys/order/identifiers: manual module
   specifications or catalog record, coordinates where relevant, orientation,
   weather/temperature states, thermal parameters and model/material choices.
4. Catalog/weather/measurement snapshot identity, origin, license/permission,
   retrieval date, raw bytes and content hashes, relevant metadata, normalization
   transforms and normalized-artifact hashes. Manual specifications remain a
   supported alternative to a catalog. A refresh creates a new snapshot.
5. Units and every coefficient conversion; irradiance/reference conventions,
   temperature basis, timezone/UTC offset/DST, timestamp alignment, interval and
   leap-day policy. Keep original measurements separate from derived values.
6. Model identity, fit inputs/outputs, solver method/settings/tolerances, numerical
   constants, convergence/failure handling and the exact voltage/current grid,
   point count, endpoints, ordering and output schema. Preserve NaNs/infinities
   and missing-record behavior as evidence; review how comparisons handle them.
7. Seeds and RNG implementation/state for stochastic paths, input ordering and
   sample dimensions. If absent historically, mark the limitation rather than
   claiming deterministic reproduction.
8. Unrounded raw output artifacts and hashes, quantity/unit definitions, capture
   provenance/review status, comparator settings and an honest evidence-gap list.

Capture outputs independently from the legacy implementation before the modern
calculation is written. Never generate golden values from the modern code being
tested. No capture runner or legacy execution is included in this task.

## Safe capture procedure for the next task

Inspect side effects first. Legacy dashboard imports construct Dash/layout,
configure cufflinks/notebook output and suppress warnings; weather imports load
`.env`. Callbacks can request live weather. Helpers delete CWD `g_*.csv`,
`PE_*.csv`, `PE2_*.csv` and overwrite `Uploaded_.xlsx` (see evidence map).

Use a separate legacy environment and isolated process/working directory with
controlled inputs, explicit temporary output paths and blocked live acquisition
during replay. Preserve the source and original upload bytes. Do not import the
legacy UI into the new backend or silently patch its dependencies/calculations.
Any necessary wrapper/interception must be inspectable and recorded, and must
not alter numerical behavior. Keep credentials out of captures, logs and fixtures.

## Comparison policy

Identifiers, branch/model identity, units, column names, timestamps, shapes,
ordering and grid coordinates agree exactly unless the contract explicitly
defines a numerical grid comparison. Every expected record must be accounted
for. Numeric quantities use documented per-quantity absolute/relative tolerances,
chosen from precision, units and measured platform/library behavior. State the
formula, typically `abs(actual - expected) <= atol + rtol * abs(expected)`.
For near-zero values the absolute term must have a defensible scale; unexplained
NaNs, non-finite values, shape changes or missing records fail comparison.

There is no accepted universal tolerance yet. The thesis campaign's percent
errors and manufacturer tolerance are not software-parity tolerances. Do not
round, resample, drop records, change assumptions or loosen thresholds to obtain
a pass. Report discrepant quantities and largest differences with provenance;
decide explicitly whether the cause is implementation drift, platform behavior,
source defect or an intentional versioned modeling change.

## Implemented preservation boundaries and replay

| Profile | Independently executed evidence | Modern numerical coverage | Explicit limits |
|---|---|---|---|
| `legacy-iv-r-v1` | `iv_r/captured` and `iv_r/captured_alternate`: two modules, four plus two ordered conditions, 600 voltage/current points. | Exact effective fit inputs, all six fit parameters, De Soto arguments/parameters, seven single-diode metrics, every returned point and exact rounded table. | Original `IV_R` function boundary; no upstream preset/annual/callback, other curve branch or empirical claim. |
| `legacy-faiman-v1`, `legacy-noct-v1` | `thermal/captured`: four parameter cases across five ordered synthetic points. | Every temperature, identifier/order and output-column identity; independent equation/limiting-case checks. | Point kernels; original mutation/None return captured but modern immutable output is deliberate. No Sandia or annual integration. |

Both scripts execute unchanged selected AST bodies with real scientific libraries,
without importing modern SUNERGY or full legacy UI/helpers. This avoids unrelated
imports, CWD CSV deletion and upload handling. Fresh subprocesses/temp CWDs and
blocked Python networking isolate execution. Inspectable wrappers and source hashes
are in each manifest. Independent repeat executions were byte-identical on the
capture host. Historical dependencies remain unknown; the environment is explicitly
reconstructed with Python 3.12, pvlib 0.13.1 and PySAM 7.1.0.

I–V has separate immutable Windows x86-64 and Linux x86-64 references. The Linux
pair lives at `iv_r/captured_linux` and `iv_r/captured_alternate_linux`. Both use the
same supplied/effective inputs and existing tolerances. Default replay selects
only by OS/architecture; an unsupported platform fails explicitly, with no numerical
fallback. Integrity checks cover all four I–V manifests on both platforms. Counts
are six conditions/600 points **per platform**, not additional scientific samples.

Initial Ubuntu CI disagreed with the Windows oracles. An isolated original-source
capture on [the diagnostic CI run](https://github.com/Edgar-daniel-ignacio/SUNERGY/actions/runs/42965809075)
then matched the modern Ubuntu implementation under the unchanged thresholds;
repeated original captures were byte-identical. The frozen Linux artifacts were
downloaded from artifact `13830512913` (published ZIP SHA-256
`cebb90afba356b7e5bed888ba0ba18d2f637b50e2122425ab116a5d220e0b15a`),
whitelist-imported without path/content edits, and verified against source/wrapper/
lock/input/output hashes. Temporary CI capture steps were removed: normal CI
compares fixed independent references and never regenerates its oracle.

The [platform difference report](evidence/iv_r_platform_comparison.json) preserves
fit, translated parameter, solver/grid and discarded-diagnostic differences,
including largest absolute/relative differences. Regenerate a report to a fresh
ignored path with `uv run --locked --offline python scripts/compare_iv_platforms.py --output .local/runs/iv-platform-audit.json`.
Original rounded tables and failure records agree exactly between platforms.
This establishes same-platform compatibility, not platform-invariant numbers.
See [IV-04](assumptions.md#iv-04--numerical-platform-identity) for the solver audit.

Install the application with `uv sync --locked`. Replay modern comparisons offline:

```text
uv run --locked --offline python scripts/replay_backend.py
uv run --locked --offline pytest backend/tests/test_model.py backend/tests/test_thermal.py
uv run --locked --offline python scripts/check_repository.py
```

The CLI checks capture integrity, branch/solver identity and installed scientific
core versions, then reports each module's cases, point count and differences.
The thermal tests replay its independent capture through the same callable point
kernel used by `application.request_thermal`.

For fresh original-source captures, create the separate environment once (Windows;
on Unix replace `Scripts/python.exe` with `bin/python`):

```text
uv venv .local/legacy-iv-env --python 3.12
uv pip sync --python .local/legacy-iv-env/Scripts/python.exe config/legacy-capture/requirements.txt --require-hashes
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_iv.py --inputs tests/fixtures/legacy/iv_r/captured/inputs.json --output .local/runs/iv-r-replay
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_iv.py --inputs tests/fixtures/legacy/iv_r/captured_alternate/inputs.json --output .local/runs/iv-r-alternate-replay
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_thermal.py --inputs tests/fixtures/legacy/thermal/captured/inputs.json --output .local/runs/thermal-replay
```

Use new output directories for every run; runners refuse replacement. Initial
installation requires network, subsequent sync can add `--offline` once cached.
Compare replay `outputs.json` hashes to their references; capture timestamps/output
paths vary. `.gitattributes` preserves raw fixture/wrapper/lock bytes on checkout.
Full capture metadata remains inside each manifest rather than copied here.

The I–V API accepts `LegacyIVRequest` at `/api/v1/compatibility/iv-r` and returns
supplied/effective inputs and numerical outputs. `fetcher.normalize_legacy_iv_input`
maps the capture layout to this request; `load_legacy_iv_input` additionally checks
snapshot hash and attaches source identity. Conditions may have repeated labels;
their ordered record positions remain authoritative. Zero irradiance is rejected
because the original relative-error table has undefined denominators. Missing raw
columns originally raise KeyError/AttributeError; modern schema failures return
422, calculation failures return 400. These are intentional boundary changes.
Plot formatting and the computed-but-discarded reverse grid are retained in capture
evidence and omitted from the modern returned numerical boundary.

I–V manifests use additive absolute/relative tolerances: current 1e-9 A/1e-9,
voltage 1e-8 V/1e-9, power 1e-7 W/1e-9, saturation current 1e-20 A/1e-9,
resistance 1e-9 ohm/1e-9 and Adjust 1e-9 percent/1e-9. Each manifest explains the
quantity precision and near-zero floor. Original rounded table values compare
exactly. Thermal temperature uses 1e-12 °C/1e-12. These controlled-domain software
thresholds are applied unchanged within each captured platform. Windows-to-Linux
oracle differences are retained separately; other platforms/builds remain
unverified. They are not measurement/manufacturer tolerances.

Tests deliberately perturb current, tiny saturation current, units, record order,
grid length, required quantities and table structure; the gate must fail. Output
contracts independently reject missing/misaligned stages. Equation residual and
MPP derivative tests use direct arithmetic, distinct from reproduction tests.

## Next bounded milestones and full backend gate

Next capture Sandia's accepted-length/selector/failure regimes and characterize
annual S4/S5 summaries with synthetic frames, then obtain reviewed weather/time
snapshots for integrated replay. Follow the [ordered coverage backlog](legacy_backend_coverage.md#ordered-remaining-reproduction-work).
IV_R/thermal success does not justify dropping untested branches from scope.

`CurvaIV.IV` is a different Newton/100-point path with hardcoded conditions;
`IV_CI_cor` uses 250 points. The summary reports a Powell-Hybrid extraction
pathway and inconsistent 250/255 points. Do not merge these into one baseline.
Record the helper's raw-alpha/material choices and `Placa_Prueba` hardcoding as
defects, with any future corrected mode versioned separately. Annual and
correction captures wait for their branch-specific source inputs and review.

Full backend reproduction requires every intended inventory row to have explicit
domains, provenance, intermediate/final references, successful numerical and
structure/failure comparisons, or a reviewed scope exclusion. No skipped comparison,
missing record or unexplained discrepancy counts as passed. Scientific verification,
measurement comparison and calibration retain their separate gates. New frontend
functionality starts only after that full backend gate; existing generated interface
consistency does not constitute new frontend functionality.
