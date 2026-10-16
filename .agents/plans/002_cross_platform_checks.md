# 002 — Cross-platform checks and launch verification

## Objective and scope
Fix the pushed scaffold's Ruff failure and verify application launch on Windows
and Linux CI without changing legacy, skills, evidence, contracts or PV behavior.
Keep CI check-only. Add bounded executable process-level health/proxy verification;
do not introduce deployment infrastructure or claim scientific/legacy parity.

## Inspection and cause
- Starting revision: `6830dd1937c5f1e4fc2f18eb6cef81ca4e8ef80c`; clean worktree.
- Read root/scoped guidance, planning protocol, manifests, CI, architecture and
  existing checks. Reference run: `38837863338`; Windows job `116770912144`
  and Ubuntu job `116772037181` logs both show 27 tests passed and lint passed.
- Ruff 0.17.1 format discovers skill Markdown code examples: five failing files
  under each of `.agents/skills` and `.claude/skills` on CI. Locally only one
  copy was selected by local Ruff discovery. These are not application-source
  formatting errors.
- A rerun's Windows matrix job was cancelled after the Ubuntu failure; frontend
  Ubuntu job passed. Preserve existing skill sources instead of mass formatting.
- Checked official Ruff configuration documentation for include/force-exclude.

## Decisions and execution
1. Scope root Ruff discovery to Python/stubs and pyproject, explicitly exclude
   both skill locations and preserve existing exclusions. Enforce exclusions for
   explicit file arguments as well, protecting legacy from tracked-file commands.
2. Keep formatter `--check` in CI. Disable matrix fail-fast and check frontend
   on both Windows/Ubuntu, using existing Node24/Python3.12 locked dependencies.
3. Add a standard-library smoke command: launch actual Uvicorn; optionally launch
   built Next with server-only backend origin; verify health, capabilities, proxy,
   and 503 after backend shutdown. Use loopback, bounded waits, temporary logs,
   task-owned process cleanup and no external services/credentials.
4. Document commands and run locked backend/frontend checks and live smoke tests.
   Inspect final diff and preservation hashes. Lead owns all writes; no delegation.

## Verification and outcomes (2026-10-15, local Windows host)
- `uv sync --locked --offline` and `uv lock --check --offline`: passed; no lockfile
  or dependency changes. Local sandbox denied Hatchling cache installation;
  approved outside-sandbox synchronization succeeded.
- `uv run --locked --offline ruff format .`: formatted only the newly added smoke
  script; existing application sources and all skill/evidence/legacy files unchanged.
- `uv run --locked --offline ruff format --check .`: passed, 14 Python files.
- `uv run --locked --offline ruff check .`: passed. `--show-files` contains modern
  backend/tests/scripts and pyproject only. Explicit excluded legacy/skill arguments
  select no files. Deliberately unformatted application stdin still fails the check.
- `uv run --locked --offline mypy`: passed, 14 source files.
- `uv run --locked --offline pytest`: 27 passed.
- `uv run --locked --offline python scripts/check_repository.py`: passed, including
  original evidence and legacy byte hashes.
- `uv run --locked --offline python scripts/export_openapi.py --check`: passed.
- `uv build --offline`: wheel and source distribution built.
- Frontend `npm ci --offline --cache frontend/.npm-cache --no-audit --no-fund`,
  `api:check`, `lint`, `typecheck` and `build`: passed. Used the prior temporary
  official npm11.12 CLI with Node24.19; no global installation changes. Retained
  existing ESLint9 deprecation notice/peer compatibility; no tooling upgrade scope.
- `uv run --locked --offline python scripts/smoke_test.py`: actual Uvicorn process
  starts, health/capabilities pass, malformed simulation request returns422.
- `uv run --locked --offline python scripts/smoke_test.py --frontend`: actual built
  Next process starts, root renders pending notice, proxy health200 matches backend,
  stopping backend produces proxy503 while root remains200. Processes cleaned up.
- CI YAML parsed: both backend and frontend have Windows/Ubuntu matrices with
  `fail-fast: false`; formatter remains check-only. `git diff --check` passed.
- No live Linux runtime was available locally. Updated remote CI has not run for
  these uncommitted changes; the previous run proves only pre-fix Linux tests/lint
  and frontend build passed, not the new launch check or remaining backend steps.

## Handoff
Changes are ready for review/commit/push. Both-platform success requires the next
GitHub run to pass all four jobs. Independent legacy output capture remains the
next modeling milestone; PV behavior is untouched.
