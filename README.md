# SUNERGY

An evidence-first foundation for a PV technical, economic and financial application
for small and large developers. **This backend foundation reproduces selected
legacy numerical boundaries; it is not a validated simulator or complete migration.** Agent-native describes
the development workflow; no LLM runtime is required by the application.

Implemented: versioned IV_R compatibility calculation through Python/FastAPI,
Faiman/NOCT thermal point calculations through Python, immutable local source
loading/normalization, independently captured legacy references and offline replay.
The existing Next.js shell/service check and generated API contracts remain.
The general module simulator, live catalog/weather retrieval, annual integrations,
measurement/correction/calibration, systems, economics/finance and layout remain
unimplemented. New frontend functionality stays behind full backend reproduction.

## Run locally

Use Python 3.12 (3.13 is allowed), [uv](https://docs.astral.sh/uv/getting-started/installation/),
and Node.js 24 LTS with npm 11. No Docker or WSL required. Commands below work in
PowerShell and Unix shells from the repository root; no virtualenv activation needed.
Initial dependency installation needs internet; application tests/replay need no
live services or credentials.

```text
uv sync --locked
npm --prefix frontend ci
```

In two terminals:

```text
uv run --locked uvicorn sunergy.api:app --reload
```

```text
npm --prefix frontend run dev
```

Open [frontend](http://localhost:3000), [API docs](http://127.0.0.1:8000/docs),
or [health](http://127.0.0.1:8000/health). The frontend renders with the API stopped;
its optional service check reports availability only. To change the API origin,
set server-only `SUNERGY_API_URL` before starting Next.js, or use
`frontend/.env.local` (ignored). No weather credentials are consumed by the scaffold.

If a restricted Windows environment has an unwritable uv cache, set
`UV_CACHE_DIR` to a writable path, e.g. PowerShell
`$env:UV_CACHE_DIR = Join-Path $PWD '.cache/uv'`; Unix
`export UV_CACHE_DIR="$PWD/.cache/uv"`. A normal Node installation provides npm.

## Checks and API synchronization

```text
uv run --locked --offline pytest
uv run --locked --offline ruff check .
uv run --locked --offline ruff format --check .
uv run --locked --offline mypy
uv run --locked --offline python scripts/check_repository.py
uv run --locked --offline python scripts/replay_backend.py
uv run --locked --offline python scripts/export_openapi.py --check
npm --prefix frontend run api:check
npm --prefix frontend run lint
npm --prefix frontend run typecheck
npm --prefix frontend run build
uv run --locked --offline python scripts/smoke_test.py
uv run --locked --offline python scripts/smoke_test.py --frontend
```

The smoke commands launch and stop their own loopback processes on temporary
ports. The frontend variant requires `npm ci` and a completed frontend build;
it checks the actual FastAPI/Next health proxy and its 503 response after backend
shutdown. CI runs backend, frontend and launch checks on both Windows and Ubuntu,
with matrix fail-fast disabled so both platform results remain visible.

Ruff checks application Python/stubs and `pyproject.toml`. Installed skill examples,
reviewed evidence and legacy code remain outside its scope, including when an
excluded file is passed explicitly. CI retains non-mutating formatting checks.

After Pydantic/API changes, regenerate both tracked contract artifacts:

```text
uv run --locked python scripts/export_openapi.py
npm --prefix frontend run api:generate
```

FastAPI OpenAPI is authoritative; TypeScript is generated, not a competing schema.
`uv build` creates a wheel/source distribution (may fetch the build toolchain on
first use). CI installs locked dependencies, then runs new-code checks. `legacy/`
is excluded from formatting/lint/testing. No legacy UI is imported by the backend.

## Repository map

```text
AGENTS.md                    stable policy and context routing
.agents/PLANS.md             planning procedure
.agents/plans/001_*.md       scaffold decisions and actual verification
backend/src/sunergy/         contracts, use cases, numerical kernels, fetcher/replay
backend/tests/              independent reproduction, equations, boundaries/integrity
frontend/                   Next.js / TypeScript presentation and health control
contracts/openapi.json      generated FastAPI schema
config/                     small typed path/source registries
scripts/                    offline export and repository-integrity checks
docs/README.md              evidence catalogue and selective reading routes
docs/architecture.md        ownership, data flow and deferred extension boundaries
docs/evidence.md             source authority, availability and scientific limits
docs/reproduction.md         independent capture requirements and separate gates
docs/legacy_backend_coverage.md curated evidence → owners → reproduction backlog
docs/assumptions.md          populated operation records and scientific audit
docs/flowcharts.md           implemented and observed-legacy transformation lineage
docs/legacy-refactorizacion/ original-author investigation, locally audited and tagged
docs/evidence/              unchanged supplied summary, attribution and hashes
tests/fixtures/legacy/      controlled original-source IV_R and thermal references
config/legacy-capture/      separate hash-locked original-source capture environment
legacy/                    preserved source evidence and original README/template
```

Ignored `.local/` separates future private uploads, caches and unique generated run
directories. Only small, reviewed, redistributable fixtures should be tracked.

## Evidence and development sequence

First independently capture selected legacy behavior, then reproduce it under
equivalent inputs/assumptions. Only after relevant reproduction gates, extend
module workflows to systems, technical/economic/financial assessment and a future
layout UI. Scientific verification and empirical evaluation remain separate gates.
Schema validation, numerical parity and goodness of fit are not interchangeable.

The apparent legacy dashboard calls helpers in `Input_File_DIV_Mac_Informe.py`;
it does not call the imported `CurvaIV.IV` path. Paths differ in fitting, solving
and curve grids. Read the [evidence map](docs/evidence.md) and
[reproduction contract](docs/reproduction.md) before selecting a baseline.
Suspected defects are recorded, not silently repaired.

The supplied [thesis-derived summary](docs/evidence/pv_physics_engine_evidence_summary_for_agent_research_equations_fixed.md)
is copied unchanged and attributed in adjacent provenance. It is secondary evidence;
the original thesis, campaign data, catalog workbook, historical dependencies,
and weather snapshots are unavailable. Controlled numerical reference outputs now
exist for IV_R and Faiman/NOCT only. The summary's narrow
module I–V/correction campaign does not validate annual yield or a full PV system.

Start at [AGENTS.md](AGENTS.md) and the [evidence catalogue](docs/README.md).
For legacy functionality, follow the relevant original-author chapter and its
audited coverage entry. [Assumptions](docs/assumptions.md) owns modeling meanings;
[flowcharts](docs/flowcharts.md) traces transformations;
[architecture](docs/architecture.md) owns component and configuration boundaries.
[Reproduction](docs/reproduction.md) defines preservation and comparison criteria.
Executable captures establish selected behavior; primary formulations and original
observations answer separate scientific and empirical questions.

The first reproduction milestone passed for two modules/six I–V conditions/600
curve points per captured platform (Windows/Linux x86-64), and four thermal
parameter cases/five points. Original platform differences remain recorded;
replay selects by OS/architecture using unchanged thresholds. The next bounded
milestone is Sandia selector/length/failure capture and annual-summary
characterization, followed by source/weather/time-contract recovery for integrated
annual replay. Full backend reproduction requires every intended coverage row
to pass its reference comparisons or have a reviewed scope exclusion; no new
frontend functionality begins before that gate.

Local development requires the locked scientific packages (including PySAM's
native wheel) and Python 3.12. Capture needs the separate environment, including
Plotly. Tests/replay need no credentials or external services after installation.
Loopback process smoke and frontend build commands are listed above; deployment
packaging/startup verification is recorded in the task plan, with production
hosting, TLS/secrets operation and other platform/build environments still pending.
Scientific verification and empirical evaluation remain incomplete and separate
from software replay. Their scope and unresolved questions are recorded in the
evidence catalogue's owning documents.

## Legacy reference replay

After installing the locked application dependencies, compare modern outputs to
the fixed, independently captured references without network access:

```text
uv run --locked --offline python scripts/replay_backend.py
uv run --locked --offline pytest backend/tests/test_model.py backend/tests/test_thermal.py
uv run --locked --offline python scripts/check_repository.py
```

Replay selects I–V references by captured OS/architecture, verifies source,
environment and artifact identity, and reports case/point comparisons. Thermal
tests compare every captured temperature. These commands do not regenerate the
expected outputs. Their supported scope and comparison rules are in
[reproduction](docs/reproduction.md); missing capabilities are in
[coverage](docs/legacy_backend_coverage.md).

Fresh original-source capture is a separate operation. Inspect the selected
legacy body's side effects and wrapper first. Create the hash-locked capture
environment once (Windows commands below; on Unix use `bin/python` in place of
`Scripts/python.exe`):

```text
uv venv .local/legacy-iv-env --python 3.12
uv pip sync --python .local/legacy-iv-env/Scripts/python.exe config/legacy-capture/requirements.txt --require-hashes
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_iv.py --inputs tests/fixtures/legacy/iv_r/captured/inputs.json --output .local/runs/iv-r-replay
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_iv.py --inputs tests/fixtures/legacy/iv_r/captured_alternate/inputs.json --output .local/runs/iv-r-alternate-replay
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_thermal.py --inputs tests/fixtures/legacy/thermal/captured/inputs.json --output .local/runs/thermal-replay
```

Use a new output directory for each execution; runners refuse replacement. Initial
installation needs network; sync can add `--offline` after dependencies are cached.
Wrappers execute selected unchanged AST bodies in isolated subprocesses with
Python networking blocked. Review the resulting manifests and raw-output hashes
against the same-platform references; timestamps and output paths vary. Never
replace a fixed oracle merely because a modern comparison fails. These limited
kernel captures do not recover the historical runtime or original measurements.
