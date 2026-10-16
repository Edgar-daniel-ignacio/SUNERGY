# SUNERGY

An evidence-first foundation for a PV technical, economic and financial application
for small and large developers. **This is a runnable development scaffold, not a
validated PV simulator or a completed legacy migration.** Agent-native describes
the development workflow; no LLM runtime is required by the application.

Implemented: importable Python package, FastAPI liveness/capabilities, explicit
unavailable I–V endpoint, Next.js shell/service check, generated API types, source
and path declarations, snapshot-integrity checks, capture/comparison contracts,
offline tests and CI. Calculations, catalog/weather retrieval, measurement ingestion,
calibration, systems, economics/finance and layout remain unimplemented.

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
`export UV_CACHE_DIR="$PWD/.cache/uv"`. A normal Node installation provides npm;
the bundled Codex runtime on the implementation host lacked it, so verification
used a temporary npm CLI without changing system installations.

## Checks and API synchronization

```text
uv run --locked --offline pytest
uv run --locked --offline ruff check .
uv run --locked --offline ruff format --check .
uv run --locked --offline mypy
uv run --locked --offline python scripts/check_repository.py
uv run --locked --offline python scripts/export_openapi.py --check
npm --prefix frontend run api:check
npm --prefix frontend run lint
npm --prefix frontend run typecheck
npm --prefix frontend run build
```

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
backend/src/sunergy/         contracts, use cases, physics placeholder, adapters
backend/tests/              API/boundary, integrity and synthetic comparator tests
frontend/                   Next.js / TypeScript presentation and health control
contracts/openapi.json      generated FastAPI schema
config/                     small typed path/source registries
scripts/                    offline export and repository-integrity checks
docs/architecture.md        ownership, data flow and deferred extension boundaries
docs/evidence.md             runtime trace, scientific limits and open questions
docs/reproduction.md         independent capture requirements and separate gates
docs/evidence/              unchanged supplied summary, attribution and hashes
tests/fixtures/legacy/      explicit missing-reference status; no golden results
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
weather snapshots and independent numerical outputs are unavailable. Its narrow
module I–V/correction campaign does not validate annual yield or a full PV system.

Next bounded milestone: capture the candidate active `IV_R` CEC/SAM → De Soto →
Lambert W path independently, with reviewed module inputs, PySAM/scientific
dependency versions, exact 100-point grid and raw output hashes, before porting it.
See [architecture](docs/architecture.md) for the CANOE principles adapted and the
transport-specific architecture rejected. Agents start with [AGENTS.md](AGENTS.md).
