# Legacy reproduction contract

Current status: **reference capture missing; parity has not been tested**.
The scaffold supplies contracts/comparison plumbing, not migrated PV calculations
or golden outputs. See [evidence map](evidence.md) for the actual calculation
paths and suspected defects.

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
  selected, small, redistributable legacy captures. There are no golden results.
- [`capture_status.json`](../tests/fixtures/legacy/capture_status.json) records the
  missing-capture state; a status declaration is not a fixture or a passing gate.
- [`backend/src/sunergy/regression.py`](../backend/src/sunergy/regression.py) owns
  the executable capture-manifest and numerical-comparison contract. Its tests
  exercise plumbing using explicitly synthetic values only.
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

## First bounded milestone

Select `Input_File_DIV_Mac_Informe.IV_R` as a candidate for review, independently
capture its CEC/SAM → De Soto → Lambert W pathway with the original 100-point
grid and explicit module/condition inputs, then port only that selected behavior.
Confirm this choice before treating it as the reproduction authority.

`CurvaIV.IV` is a different Newton/100-point path with hardcoded conditions;
`IV_CI_cor` uses 250 points. The summary reports a Powell-Hybrid extraction
pathway and inconsistent 250/255 points. Do not merge these into one baseline.
Record the helper's raw-alpha/material choices and `Placa_Prueba` hardcoding as
defects, with any future corrected mode versioned separately. Annual and
correction captures wait for their branch-specific source inputs and review.
