# 001 — Evidence-first initial scaffold

## Objective and limits
Implement a packaged Python/FastAPI backend and bootable Next.js shell, concise
agent guidance, preserved evidence, and executable verification foundations.
No legacy migration/calibration, full-system/financial model, auth, database,
queue, deployment, or map editor. Completion requires imports/config checks,
health/failure tests, generated API synchronization, frontend checks/build, and
an explicit reproduction gap register. No parity or scientific-validation claim.

## Starting evidence
- Local SUNERGY HEAD: `ef92cd12fd2c40854c24c1fe7cded9ba351de7df`.
- Existing work: root README/.env.example deleted, untracked copies under legacy;
  preserve those copies. New root README documents the new scaffold.
- No manifests/instructions; all Python code is in legacy. README's Edi_GIu paths
  are stale. Static investigation only; legacy UI imports have side effects.
- Supplied thesis-derived summary is accessible; copy bytes unchanged, record hash
  and attribution. Its embedded recommendations are evidence, not task authority.
- CANOE local v2.0 `399bb3c8c53712a3fa02dec0f1694419bce5e55a` inspected;
  public cached page differs and live remote SHA is unverified. Details in architecture.
- Official Next.js, FastAPI, Pydantic, uv, pvlib and openapi-typescript docs consulted
  only for scaffold choices. Resolve dependencies/lock and test on this host.

## Decisions
- Simple monorepo: root uv project packages backend/src/sunergy, separate npm
  frontend. No monorepo scheduler. Pydantic API/config contracts; ordinary internal
  numerical types. FastAPI OpenAPI -> generated TypeScript with drift checks.
- Minimal health/capability APIs and explicit unavailable simulation use case;
  no fabricated physics. A reserved module request documents current units and
  provenance boundaries without claiming supported model behavior.
- Small YAML path/source registries have explicit consumers/planned status.
- Preserve legacy byte hashes. Regression manifests/comparator are plumbing only;
  no golden outputs can be captured without reviewed source inputs/dependencies.
- Active dashboard calculations differ from standalone CurvaIV and thesis pathway;
  evidence map must distinguish these before selecting a baseline.

## Steps and ownership
1. Lead: inspect worktree/thesis/framework docs, write policy/protocol/plan.
2. Read-only agents: trace legacy runtime; inspect bounded CANOE references.
3. Frontend agent: exclusive frontend/ ownership, npm lock/checks and boot shell.
4. Lead: backend/config/tests/scripts/CI; preserve evidence and build reproduction
   foundation. Evidence agent may own docs/evidence.md and docs/reproduction.md.
5. Lead: integrate docs/README, inspect generated contract, run checks and live
   smoke checks, inspect final diff and preservation hashes.

## Implemented
- Root/scoped agent policy, procedural planning, README and targeted architecture,
  scientific evidence map and reproduction contract. Root policy 106 lines;
  planning protocol 40 lines. Optional skill compatibility without a new catalog.
- Packaged backend: health/capabilities, reserved typed point request with 501,
  numerical placeholder, local catalog-byte integrity, typed source/path loading,
  unique protected run directories, capture manifest and comparator.
- Frontend: responsive Next shell with explicit pending scope, optional health
  control/proxy, accessible disclosure panels; no calculation/measurement form
  suggests currently implemented simulation. Server origin is server-only config.
- Both lockfiles, generated OpenAPI/TypeScript, focused checks and CI for Windows/
  Ubuntu backend and Ubuntu frontend. CI is configured, not remotely executed.
- Summary copied unchanged: SHA-256
  `d4354abf4bba2177b0b27a1fd3c12dddc22c917bad28508f842ce9da01033c06`,
  51,719 bytes; attribution/limits in adjacent provenance. All 25 legacy files
  retain inspected bytes. Existing legacy README/template copies preserved;
  pre-existing root .env.example deletion remains. New root README is intentional.
- `.gitattributes` preserves observed legacy CRLF on either OS and disables text
  conversion for the supplied summary. No legacy rewrite/renormalization performed.

## Verification and actual outcomes (2026-10-15)
Python host: 3.12.12, uv 0.9.10. Locked FastAPI 0.143.2, Pydantic 2.14.1,
Starlette 1.8.0, Uvicorn 0.54.0; dev HTTPX2 2.13.1, pytest 9.1.1,
Ruff 0.17.1, mypy 1.20.2. These are scaffold versions, not historical legacy versions.

Commands were run from root with `UV_CACHE_DIR=<repo>/.cache/uv`:

| Command | Result |
|---|---|
| `uv sync`, then `uv sync --locked --offline` | Lock/environment created; offline synchronization passes after initial downloads. |
| `uv run --locked --offline pytest` | 27 passed; API 200/422/501, explicit capability states, zero coordinates, units/nonfinite rejection, snapshot tampering, protected run paths and synthetic comparator failure cases. |
| `uv run --locked --offline ruff check .` | Pass. |
| `uv run --locked --offline ruff format --check .` | Pass; 23 files formatted; legacy excluded. |
| `uv run --locked --offline mypy` | Pass; 13 source files checked. |
| `uv run --locked --offline python scripts/export_openapi.py --check` | Pass. |
| `uv run --locked --offline python scripts/check_repository.py` | Pass: config, supplied bytes, all legacy hashes, import boundary, missing-reference state. |
| `uv build --offline` | Wheel and sdist built. Wheel contains only sunergy package/metadata; sdist restricted to modern package/build inputs (13 members). Direct wheel-path import of application health passed. |
| `uv lock --check --offline` | Pass after final packaging changes. |
| `git diff --check` | Pass (Git only notes future README line-ending conversion). |

Frontend checks used Node 24.19.0, temporary official-registry npm 11.12.0 CLI
at `C:\Users\rashi\AppData\Local\Temp\sunergy-npm-11.12.0\package\bin\npm-cli.js`.
The normal `npm` command was absent; no global installation was changed.
Pinned Next 16.4.2 / React 19.3.1 / TypeScript 5.9.3 / ESLint 9.39.4 /
openapi-typescript 7.13.0. TS5.9 and ESLint9 match current tooling peer ranges;
latest TS7/ESLint10 would conflict. Package engine reflects resolved Node peers;
README/CI recommend Node24 LTS.

| Equivalent npm command (temporary CLI on this host) | Result |
|---|---|
| `npm --prefix frontend ci --offline --cache frontend/.npm-cache --no-audit --no-fund` | Equivalent to agent's `npm ci --offline --cache .npm-cache --no-audit --no-fund` from frontend; pass, 368 cache-only packages. |
| `npm --prefix frontend run api:generate` / `api:check` | Pass; deliberately altered generated file caused exit 1, then original restored and check passed. |
| `npm --prefix frontend run lint` | Pass. |
| `npm --prefix frontend run typecheck` | Pass, Next route types plus tsc. |
| `npm --prefix frontend run build` (with `NEXT_TELEMETRY_DISABLED=1`) | Pass; static root and dynamic health proxy, no backend/live resource required. |

Live checks: Uvicorn on loopback:8000 and built Next on loopback:3100;
root HTTP200 with pending-capability text, API health200 and proxy health200 with
matching service/version. A separate frontend with unreachable configured backend
returned503. Browser inspection confirmed the rendered shell and visible limits.
Verification servers were task-owned and stopped after checks.

## Failures, review and resolutions
- Sandbox network prevented initial package downloads; approved escalated installs
  succeeded. Repository-local caches avoided unwritable default cache paths.
- Windows sandbox socket-pair initialization stalled TestClient before application
  execution; rerunning unchanged offline tests outside sandbox passed. Sandboxed
  Next server bound but did not serve requests; outside-sandbox restart passed.
- First path test exposed Windows rooted `/absolute` handling; validator now checks
  anchors. Independent review caught mutable/evidence overlap and comparator formula
  mismatch. Both fixed, with rejection/boundary tests and final checks passing.
- HTTPX path emitted Starlette's deprecation warning; consulted current Starlette
  docs and switched to recommended HTTPX2. Final tests have no warnings.
- Frontend sandbox install hit EPERM. One lint attempt overlapped reinstall and
  failed on a transient missing dependency; sequential reinstall/lint passed.
- No approval-review rejection or remaining scaffold implementation blocker.
- Final ignore checks exclude private uploads, frontend secrets, node_modules and
  caches; reviewed fixture CSV is intentionally not ignored (git check-ignore exit1).

## Evidence gaps and next bounded milestone
No golden outputs/migrated calculations: parity **not run**, scientific verification
**not performed**, empirical comparison/calibration **not implemented**. Missing:
original thesis, Libro1.xlsx/edition/license, historical dependencies, weather and
measurement snapshots, and reviewed quantity tolerances. Remote reference SHAs
could not be live-verified; local inspected revisions are recorded above.

Independently capture candidate `Input_File_DIV_Mac_Informe.IV_R` with reviewed
module inputs, explicit effective inputs/coefficient/material behavior, pvlib and
PySAM/SSC environment, exact Lambert W/100-point grid and raw output hashes.
Review capture/tolerances before porting only that branch. Keep documented defects
in explicit compatibility cases; future scientific corrections require evidence
and a separately versioned/tested model. Annual/correction branches need their
own missing inputs. No modeling ambiguities were settled by intuition here.
