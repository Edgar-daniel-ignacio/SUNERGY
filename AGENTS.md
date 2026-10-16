# SUNERGY agent guidance

## Mission and sequence
Build an accessible, scientifically defensible PV technical, economic, and financial
application for small and large developers. Agent-native describes development;
the application does not require an LLM runtime.

First capture independently reproducible legacy outputs, then modernize module
workflows toward numerical parity under equivalent inputs and assumptions. Only
after the relevant gates pass, extend to systems, financial assessment, and layout.
The scaffold is not a validated simulator or a completed migration.

## Before editing
- Inspect `git status`, actual files/imports, dependencies, and applicable scoped
  `AGENTS.md` files (`backend/` and `frontend/`). Preserve unrelated changes.
- For bounded multi-file, risky, or staged work, explicitly read
  [`.agents/PLANS.md`](.agents/PLANS.md) and create/update one task ExecPlan.
- Retrieve context selectively using the routing map below. Do not recursively
  ingest legacy code, plans, catalogs, or documentation. History stays cold.
- Architecture/plans guide work; contradictory runtime/source evidence requires
  revisiting them. Agent proposals are not accepted modeling assumptions.

## Ownership
- Python owns deterministic calculations and application use cases, independently
  of HTTP, plotting, and browser state. Thin FastAPI routes call those use cases.
- Pydantic owns external/API/configuration boundaries; use ordinary typed
  functions and scientific structures internally where suitable.
- Next.js owns forms/presentation/visualization. Never duplicate scientific or
  financial calculations in JavaScript. FastAPI OpenAPI is the API authority;
  generated TypeScript must be refreshed and checked, not edited by hand.
- Environment settings, API requests, model assumptions, and source metadata
  have separate owners. YAML is not a second application schema or a user UI.
- Catalog/weather adapters must preserve source records and immutable snapshots.
  Refresh is explicit; saved runs and baselines retain their original hashes.
- Original measurements, normalized values, and fitted parameters remain distinct.
  Calibration preserves the uncalibrated baseline, fitted parameter identities,
  provenance, and held-out evaluation status. Do not infer validation from fit.

## Evidence and safeguards
- `legacy/` is read-only evidence. Do not reorganize, format, repair, or import its
  UI into production. Inspect side effects before isolated execution.
- Keep schema validation, legacy reproduction, scientific verification,
  measurement comparison, and calibration separate in code, tests, and claims.
- Never manufacture golden outputs or derive them from the implementation tested.
  Compare identifiers/structure exactly; document quantity-specific tolerances.
  No hidden rounding, resampling, dropped records, or threshold relaxation.
- A reproduced defect remains a defect. Version compatibility behavior separately
  from reviewed corrections; neither is a scientifically validated default.
- Use explicit units, coefficient conversions, irradiance/temperature conventions,
  time zones, model/solver identities, grids, and source provenance.
- Read the evidence cautions before physics changes. Do not silently settle the
  annual irradiance term, coefficient semantics, correction/residual equations,
  or curve grid conflicts. Same-library agreement is not independent validation.
- Keep private uploads, secrets, caches, and generated results out of tracked
  evidence/fixtures. Use isolated temporary/run locations, not shared global files.
  Secrets stay server-side and out of logs. Default tests/replay are offline.
- Only deliberately selected redistributable fixtures belong in `tests/fixtures/`.
  Do not add datasets or measurements merely because an ignore exception allows it.
- Do not add auth, databases, queues, deployment systems, or speculative component
  schemas to reserve future functionality. Unimplemented work must fail explicitly.

## Context routing
| Task | Read first |
|---|---|
| Ownership, integration, extension | `docs/architecture.md` |
| Legacy migration, capture, numerical comparison | `docs/reproduction.md` |
| Physics, measurements, scientific claims | `docs/evidence.md`, then relevant supplied-summary sections |
| Source/path declarations | `config/paths.yaml`, `config/sources.yaml` and their named consumers |
| Current scaffold decisions/results | `.agents/plans/001_initial_scaffold.md` |
| Optional reusable procedure | Only a relevant existing `.agents/skills/*/SKILL.md`, if present |

Do not create a skill inventory or persistent memory subsystem. Use available
skills when their actual workflow applies. For independent investigation or
implementation, bounded delegation may help: assign exclusive write ownership,
isolate artifacts, and have the lead verify integration. Small sequential tasks
need no delegation. Do not change global harness settings.

## Essential commands (repository root)
See README for prerequisites and one-time dependency installation.

```text
uv sync --locked
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked python scripts/export_openapi.py --check
uv run --locked python scripts/check_repository.py
uv run --locked uvicorn sunergy.api:app --reload
npm --prefix frontend ci
npm --prefix frontend run api:generate
npm --prefix frontend run api:check
npm --prefix frontend run lint
npm --prefix frontend run typecheck
npm --prefix frontend run build
npm --prefix frontend run dev
```

New-code checks exclude `legacy/`. Update lockfiles intentionally with manifest
changes. Check offline behavior after dependencies are installed.

## Completion
Run proportionate checks, inspect the final diff, and update the ExecPlan with
actual commands/results and evidence gaps. Report implemented versus placeholder
capabilities, limitations, and the next bounded reproduction milestone. Do not
claim parity or scientific validation from scaffold tests.
