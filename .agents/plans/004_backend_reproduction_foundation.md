# 004 — Evidence-led backend reproduction foundation

## Objective and acceptance

Operationalize the curated `docs/legacy-refactorizacion/` investigation in the
existing Python/FastAPI scaffold. Implement an independently captured, explicitly
versioned compatibility slice before claiming reproduction. Preserve source and
scientific uncertainty. Complete when offline captures/replay, modern comparisons,
boundary/failure tests, contextual routing and generated API contracts pass; open
a succinct collaborator PR. Full S1–S7/backend parity and new frontend features
are outside this bounded implementation and remain gated by the coverage map.

## Starting state and context

- HEAD `cef03c2b9f73558c715d489f499d55ce26824a4c`, branch
  `docs/legacy-refactorizacion`. Existing untracked plan 003 and
  `.agents/skills/code-refactoring/` are relevant user-provided work: preserve and
  include in the reviewable foundation. The skill core/plan 003 remain unchanged;
  its routing reference gains links to the consolidated canonical records.
- Read root/backend/frontend instructions, `.agents/PLANS.md`, the requested skill
  and its SUNERGY reference, canonical architecture/evidence/reproduction docs,
  actual contracts/use cases/configuration/comparator/tests/CI and manifests.
- Curated investigation is the primary locator. Delegated systematic chapter
  assessment covers 00–11/index; verify consequential claims at their symbols.
- Existing scaffold has no calculations/captures, only schema and comparator tests.
  Historical dependency environment, workbook/catalog, original thesis and weather
  and measurement snapshots remain unavailable.

## Decisions and preservation contract

- First slice: active helper `Input_File_DIV_Mac_Informe.IV_R`, CEC/SAM fit →
  De Soto translation → Lambert W, original ordered 100-point curves, MPP and
  rounded comparison table. Structural modernization, with an explicit restricted
  external boundary; no silent mathematical corrections.
- Preserve forced monoSi/25°C fitting, percent-to-absolute fitting conversions,
  raw-alpha De Soto use and discarded CEC Adjust in a named compatibility profile.
  Do not represent it as a scientifically accepted general point simulator.
- Capture exact inspected function AST in a separate process/environment; never
  import full helper/UI or execute its CWD deletion/upload side effects. Wrapper
  and all interventions must be inspectable and hashed. Capture before porting.
- Source normalization ends at faithful source-field mapping; coefficient
  interpretation and fitting belong to the model/parameterizer. No imputation,
  resampling, hidden record drops or grid unification.
- Add only useful snapshot/normalization boundaries and actual numerical
  capabilities; do not reserve speculative weather/measurement/system schemas.
- CANOE reference is limited to configuration ownership, selective retrieval,
  assumption records, diagrams and immutable provenance; no transport machinery.

## Steps and exclusive ownership

1. Lead: plan, contracts/model/fetcher/application/API, integration and verification.
2. `curated_reconciliation`: `docs/legacy_backend_coverage.md` only; systematic
   evidence reconciliation and dependency-ordered reproduction inventory.
3. `legacy_capture`: isolated `scripts/capture_legacy_iv.py`, capture environment
   files, `tests/fixtures/legacy/iv_r/`, `backend/tests/test_legacy_capture.py` only.
   Independently execute legacy; send exact stage contract before modern port.
4. `scientific_audit`: `docs/assumptions.md`, `docs/flowcharts.md` only; primary
   formulations, ownership and separate evidence gates.
5. Lead: canonical routing/docs/config/status/integrity updates; regenerate OpenAPI
   and TypeScript; independent patch/contract review, complete checks and PR.
6. Continue independently actionable captured backend branches where feasible;
   document precise blockers for data-dependent paths. Full frontend gate is all
   required backend inventory rows, not one representative curve success.

## Verification

Run capture with explicit isolated output path; replay recorded inputs offline.
Check source/wrapper/environment/input/output hashes and exact structures, labels,
ordering, grid counts, units and quantities. Explain per-quantity tolerances from
precision; inject meaningful discrepancies into scratch candidates and require
failure. Check invalid inputs and fitting/nonfinite failures separately.

Run locked offline pytest, Ruff lint/format, mypy, repository integrity, OpenAPI and
TypeScript drift, frontend lint/typecheck/build if available, and process smoke.
Inspect final diff, source preservation, secrets/private data and package behavior.
Record actual results here; no skip or unavailable check counts as reproduction.

## Progress, outcomes and gaps

- Initial reconciliation: curated harness claim 'no Dash needed' does not hold for
  full helper import; inspected AST extraction is a bounded alternative. Curated
  D-01 irradiance prose conflates algebraically equivalent operations and is not
  an accepted equation. Workbook observations remain collaborator-reported until
  original bytes/provenance are supplied.
- Systematically assessed curated chapters 00–11, diagrams and index; preserved the
  originals. `docs/legacy_backend_coverage.md` links every capability/implicit
  contract to actual owners and remaining evidence, without a second function
  inventory. Added populated `docs/assumptions.md` and `docs/flowcharts.md`; updated
  architecture/evidence/reproduction/README/root routing and source registry.
- Independent original-source IV_R captures precede the port. Main preset:
  four conditions; alternate manual/synthetic module: two conditions. All six
  retain 100 voltage/current points, CEC arguments/six fit parameters, De Soto
  arguments/five parameters, seven electrical metrics and exact rounded table.
  Original missing-column errors and discarded reverse-grid diagnostics are also
  preserved. Repeat original executions are byte-identical on the capture host.
- `model.py` and `compatibility.py` implement `legacy-iv-r-v1`, directly callable
  through `application.reproduce_legacy_iv` and HTTP compatibility endpoint.
  General `/api/v1/module-iv` remains explicitly 501. Raw-alpha, forced monoSi/25°C
  and omitted Adjust are preserved; positive-irradiance/finite schema boundaries,
  immutable returns and clear errors are deliberate external contract changes.
- Continued independently actionable thermal work: captured unchanged Faiman/NOCT
  functions before porting, four explicit parameter cases × five synthetic points.
  Pure typed `thermal.py`, Pydantic boundaries and `application.request_thermal`
  reproduce the selected numerical kernels. Original frame mutation/None returns
  and failures are recorded separately. Independent recapture byte-identical.
- `fetcher.py` owns expected-hash reads and validated source layout/field mapping;
  no coefficient interpretation or hidden data fill. Existing catalog reader now
  delegates to that one snapshot-byte owner. Application/native scientific
  dependencies are intentionally locked; capture has a separate hash-locked
  environment including real Plotly. Neither is an established historical runtime.
- Replay validates source/wrapper/lock/input/output/snapshot hashes, selected
  branch/solver and scientific core versions, required quantities, exact order/
  structure/units and quantity-specific numerical tolerances. Mutation tests
  detect changed current, saturation current, units, record/grid/table/quantity
  defects, wrong branch and changed evidence. Capture runners refuse overwrites.
- Independent reviewer identified and lead fixed (1) unit comparison inheriting
  candidate units from the reference, (2) missing output alignment/required-key
  validation, and (3) OpenAPI 422 schema collision. Calculation failures now use
  400; malformed requests retain FastAPI HTTPValidationError 422. Regenerated both
  authoritative contract artifacts and checked drift.
- Scientific register records checked raw-alpha unit mismatch, forced fit material,
  omitted Adjust, annual gamma dimensional mismatch, Sandia deltaT/selector defect,
  measurement evidence conflicts and RNG requirements. Primary official pvlib
  definitions, Sandia SAND2004-3535 and De Soto 2007 erratum support bounded checks;
  full 2006 equations and original empirical evidence remain unavailable.
- Equation-only checks: six curves' single-diode residual <4e-14 A and MPP
  stationarity <5.8e-7 A in independent arithmetic audit. Tests use 1e-10 A residual
  and 1e-6 A MPP thresholds, separate from software parity tolerances/empirical
  accuracy. Faiman/NOCT independent hand/reference/zero-irradiance checks pass.

## Actual verification (Windows / Python 3.12.12)

- `uv lock`, `uv sync --locked`: succeeded after scoped network access; exact
  scientific core pvlib 0.13.1 / NREL-PySAM 7.1.0 / NumPy 2.3.4 / pandas 2.3.3 /
  SciPy 1.16.3. Capture lock includes full hash-checked dependency closure.
- Original capture commands in `docs/reproduction.md`: both IV captures and thermal
  executed, repeated into fresh ignored paths; all output hashes identical.
  `uv pip sync --python .local/legacy-iv-env/Scripts/python.exe config/legacy-capture/requirements.txt --require-hashes --offline`: passed.
- `uv run --locked --offline pytest -q`: **85 passed**, no skipped comparisons.
  Initial HTTP runs stalled at Windows socketpair creation under the restricted
  sandbox; faulthandler established the cause. Scoped loopback-enabled rerun passes;
  only verified stalled test processes were stopped. No harness settings changed.
- `uv run --locked --offline ruff check .`, `ruff format --check .`, `mypy`:
  passed, 26 Python files; no legacy formatting or lint changes.
- `uv run --locked --offline python scripts/replay_backend.py`: both modules pass,
  4+2 cases / 400+200 points / no differences. Thermal 16 focused checks pass within
  the full suite. Hash and branch/unit/discrepancy rejection tests also pass.
- `uv run --locked --offline python scripts/check_repository.py`: passed source,
  summary and all three capture-manifest integrity checks/import boundaries.
- `uv run --locked --offline python scripts/export_openapi.py --check` and
  `node frontend/scripts/generate-api.mjs --check`: passed after generation.
- Node 24.22.1 / existing lock-matching frontend dependencies: ESLint, Next typegen
  + `tsc --noEmit`, and production `next build` passed. npm executable/old temporary
  npm CLI unavailable, so executed the exact package-script targets with Node:
  `node node_modules/eslint/bin/eslint.js . --max-warnings 0`,
  `node node_modules/next/dist/bin/next typegen`,
  `node node_modules/typescript/bin/tsc --noEmit`,
  `node node_modules/next/dist/bin/next build` from frontend. Build needed scoped
  normal local-config/child-process permissions; no frontend functionality added.
- `uv run --locked --offline python scripts/smoke_test.py --frontend`: passed
  real Uvicorn/compatibility calculation, built Next page/proxy, and backend-offline
  handling. Found/fixed Windows launcher-only shutdown leaving a child/log handle:
  smoke cleanup now targets only its owned process tree. Repeat smoke passed.
- `uv build --offline`: wheel and sdist built. Separate `.local/wheel-check-004`
  environment installation used an export of locked runtime requirements plus the
  built wheel. Initial offline resolution found a cold/incomplete cache; scoped
  dependency installation succeeded. Isolated Python `-I` imports from installed
  `site-packages`, not editable source, and replays both captures (6 cases/600
  points) successfully. Deployment still requires initial dependency availability;
  no production hosting was introduced.

## Remaining scope and handoff

- Next bounded work: Sandia accepted-length/selector/failure captures and annual
  summary characterization with synthetic inputs. These are pending implementation,
  not externally blocked or implicitly excluded. Next obtain reviewed weather/time
  metadata for integrated POA/annual replay; catalog mode needs original workbook.
- Measurement/correction/campaign claims require original report/workbook,
  permissions and sensor/module linkage. Bootstrap requires original RNG state,
  draw/order/truncation controls. Other I–V profiles require their own captures.
- Full backend gate remains every intended coverage row independently reproduced
  (or reviewed exclusion), no skipped/unexplained discrepancies. Scientific,
  empirical and calibration gates remain separate. New frontend work is gated.
- Python 3.12/native-wheel dependencies, offline replay and local process startup
  are demonstrated; production hosting/operation and cross-platform numerical
  acceptance remain unverified. CI Windows/Ubuntu checks provide the next evidence.
- PR is stacked on `docs/legacy-refactorizacion` (open collaborator PR #1) so its
  diff isolates this implementation instead of repeating the curated investigation.
- Final inspection: canonical/skill local links resolve, staged whitespace check
  passes with explicit CR-at-EOL recognition for byte-preserved capture artifacts;
  no legacy/curated/supplied-summary bytes changed, no private/generated run files
  staged. The user-provided skill and plan 003 are included; only skill routing
  references changed to connect the new canonical context.
- Opened PR #2: https://github.com/Edgar-daniel-ignacio/SUNERGY/pull/2. Connector
  creation lacked integration permission; used existing authenticated Git access
  without logging credentials. PR attached to the chat, repository clean after
  implementation commit `082371e`.
- First CI run `42965383301`: Windows backend and Ubuntu frontend passed; Ubuntu
  reproduction against Windows numerical captures failed strict thresholds. No
  tolerance/reference relaxation. Diagnosing with independently repeated unchanged
  original-source captures on Ubuntu before deciding platform acceptance. Temporary
  CI capture/upload step preserves outputs and same-platform comparisons.
- Diagnostic run `42965809075`, Ubuntu job `130342643771`: original captures
  executed twice with byte-identical outputs; modern Ubuntu comparisons to those
  originals passed existing thresholds. This isolates the observed failure as
  Windows/Linux oracle differences, not observed same-platform refactor drift.
- Imported six unchanged JSON artifacts directly at their captured paths from
  published ZIP `13830512913`, SHA-256
  `cebb90afba356b7e5bed888ba0ba18d2f637b50e2122425ab116a5d220e0b15a`.
  Whitelist-only extraction and every source/wrapper/lock/input/output hash passed;
  no original Windows source/output/tolerance replaced. Removed the temporary
  capture/upload CI steps so routine tests cannot generate their own oracle.
- Replay now selects Windows/Linux x86-64 references by OS/architecture only;
  unsupported environments fail explicitly. Added platform selection checks and
  all-reference integrity tests. `scripts/compare_iv_platforms.py` generates the
  retained original-source platform difference report; scientific mechanisms and
  exact remaining compiler/native-build uncertainty are recorded as IV-04.
- Current local full suite: **88 passed**. All five capture manifests validate on
  Windows; selected numerical comparisons still use the unchanged thresholds.
  Final Windows/Ubuntu CI rerun follows this integration commit.
- Subsequent CI `42966647478`: all selected Linux reproduction comparisons passed;
  the independent scientific stationarity check exposed original Linux STC-alt at
  about 1.118e-6 A against the fixed strict 1e-6 A review target. Kept that target
  and failed audit outcome, rather than loosening it or changing the legacy solver.
  The source audit explains near-flat rounded-power optimization sensitivity but
  does not establish a physical defect or an accepted alternative accuracy bound.
- Split equation-residual/endpoints from MPP audit characterization. Tests require
  modern derivative values and target outcomes to reproduce the independent
  reference, while API/report/docs explicitly state the target is unmet and
  scientific verification incomplete. No skipped/xfail comparisons and no numerical
  reproduction threshold changed. Local final suite **90 passed**; Ruff/format,
  mypy, regenerated OpenAPI/TypeScript drift and all artifact integrity checks pass.
