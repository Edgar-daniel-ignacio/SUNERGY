# SUNERGY agent guidance

## Mission and sequence
Build an accessible, scientifically defensible PV technical, economic and financial
application for small and large developers. Agent-native describes development;
the application does not require an LLM runtime.

Reproduce named legacy functionality under equivalent inputs and assumptions,
with an audit of its scientific and empirical basis. Independent captures precede
numerical replacement. New frontend functionality waits for the full intended
backend reproduction gate. A scaffold, compatible defect or good fit is not a
validated simulator. Systems, finance and layout follow their prerequisite gates.

## Protected guidance and working scope
- Do not edit any `AGENTS.md` or `.agents/PLANS.md` unless the user explicitly
  requests changes to that file. General implementation, cleanup, documentation,
  skill instructions and a discovered inconsistency do not authorize instruction
  edits. Record a proposed correction in the task handoff and continue unaffected
  work. Task-specific ExecPlans remain editable under the authorized task.
- Before editing, inspect `git status`, actual files/imports, dependencies and the
  applicable scoped guidance in `backend/` or `frontend/`. Preserve unrelated work.
- For multi-file, risky or staged work, read `.agents/PLANS.md` and maintain one
  task ExecPlan. Stable policy belongs here; task progress and command logs do not.
- Use the existing task branch. Create another branch or PR only when requested;
  follow the user's existing commit, push and merge authorization without inventing
  a separate review workflow. Do not change global harness settings.

## Context routing
Use [docs/README.md](docs/README.md) to choose a document when the route is unclear.
Read only the relevant section and direct dependencies. Frontmatter describes
purpose, read scope, authority and verification; it does not create instructions,
approve a model or require loading every referenced file.

| Task | Read first, then verify |
|---|---|
| Legacy capability, execution path or implicit contract | Relevant chapter/ID from `docs/legacy-refactorizacion/README.md` or `index.json`, then its audited entry in `docs/legacy_backend_coverage.md` and named source/callers. |
| Current reproduction coverage or next backend slice | Relevant capability in `docs/legacy_backend_coverage.md`; capture/comparison boundary in `docs/reproduction.md`, then manifests, tests and actual implementation. |
| Module, interface, configuration or artifact ownership | Relevant boundary in `docs/architecture.md`; named contracts, producers/consumers and `config/paths.yaml` / `config/sources.yaml`. |
| Conversion, equation, default, fitting, time or RNG choice | Relevant operation in `docs/assumptions.md`, its chain in `docs/flowcharts.md`, then exact legacy/modern owner and cited formulation. |
| Scientific or empirical claim / source availability | Relevant source in `docs/evidence.md`, then the supplied-summary or collaborator section and primary/original evidence it names. |
| Setup, launch, supported checks or API generation | Root `README.md`, actual manifests/scripts and scoped guidance. Operational recipes are not modeling evidence. |
| Historical rationale or previous task results | Only the relevant `.agents/plans/` record when current owners leave a consequential question unresolved. History is not current authority. |
| Reusable workflow | Applicable skill from session metadata and only its needed references. No skill inventory or persistent memory subsystem. |

The collaborator's curated investigation is the primary starting map of legacy
intent and behavior. Preserve its terminology and source links; do not restart
reverse engineering. Verify consequential claims against the named code, captures
and scientific/original evidence. Source establishes implemented behavior, the
author's account helps recover intent, and scientific support requires its own
evidence. A conflict must be recorded with its scope; neither prose nor a green
test resolves all three authorities. Broad ingestion is reserved for a requested
audit, not routine edits. Never recursively ingest `legacy/` or plans by default.

## Documentation maintenance and review
The core maintained Markdown set is catalogued in `docs/README.md`. Give each
core document frontmatter stating its role, retrieval scope, authority and what
to verify. Keep one owner per fact/contract; link supporting evidence rather than
copying inventories, equations or status tables across documents.

For agent-authored substantive additions or changes to core `docs/` evidence,
place a literal `#to-review` beside each changed paragraph, list item, table row
or diagram entry/caption. A file-wide marker alone is insufficient. Keep tags out
of headings, equations, code and rendered diagram labels; use an adjacent note or
Mermaid comment. For routing-metadata edits, use `review_status: "#to-review"` in
frontmatter. Mechanical formatting/link repairs need no substantive tag.

Do not tag unchanged source history or remove existing tags without explicit
human authorization. A request to edit is not approval of the resulting wording;
passing checks is not human review or scientific acceptance. Review tags do not
block the rest of an authorized task. Preserve immutable supplied documents and
capture bytes; describe their role through catalogue/provenance metadata instead.
Keep optional diagnostics, preliminary scaffold recipes and task chronology out
of core modeling evidence; retain relevant observations with their limitations
and route operational details to README or the task record.

## Ownership
- Python owns deterministic calculations and application use cases independently
  of HTTP, plotting and browser state. Thin FastAPI routes call those use cases.
- Pydantic owns external/API/configuration boundaries. Use ordinary typed functions
  and scientific structures internally where suitable. Boundary validity is not
  scientific verification.
- Next.js owns forms/presentation/visualization. Never duplicate scientific or
  financial calculations in JavaScript. FastAPI OpenAPI is the API authority;
  regenerate and check TypeScript consumers instead of editing them by hand.
- Source metadata, artifact paths, runtime settings, requests and modeling choices
  have separate owners. YAML is not a second application schema or a user UI.
- Fetchers preserve originals, identities and immutable snapshots, then perform
  explicit source normalization. Models own interpretation, conversions, defaults,
  imputation, aggregation and fitting when those operations are actually selected.
  Refresh is explicit; saved runs and references retain their original hashes.
- Measurements, normalized values and fitted parameters stay distinct. Calibration
  preserves the uncalibrated baseline, parameter identities, provenance and held-out
  evaluation status. Do not infer validation from fit.

## Evidence safeguards
- `legacy/` is read-only: no reorganization, formatting, repair or production UI
  imports. Inspect import dependencies and execution side effects before isolated
  runs. Default tests/replay remain offline after dependency installation.
- Keep schema validation, reproduction, scientific verification, measurement
  comparison and calibration separate in code, tests and claims. A reproduced
  defect remains a defect; reviewed corrections need a separate versioned behavior.
- Never manufacture golden outputs from the replacement being tested. Compare all
  identifiers, structure, ordering, units and records exactly; justify quantity-
  specific numerical tolerances. No hidden rounding, resampling, dropped records
  or threshold relaxation. Same-library agreement is not independent validation.
- Declare coefficient conversions, irradiance/temperature conventions, time zones,
  model/solver identities, grids and provenance. Do not silently settle the annual
  equations, coefficient semantics, correction/residual forms or grid conflicts.
- Keep secrets, private uploads, caches and generated runs out of tracked evidence.
  Use isolated paths; secrets remain server-side and out of logs. Only deliberately
  selected redistributable references belong in `tests/fixtures/`.
- Do not add auth, databases, queues, deployment systems or speculative component
  schemas for future functionality. Unimplemented work must fail explicitly.

## Checks by changed boundary
Run proportionate checks from the repository root. Installation and launch recipes
live in README; they are not prerequisites for reading evidence. Do not run every
frontend/build/capture command for a documentation edit or regenerate an oracle as
part of an ordinary regression test.

| Change | Verification |
|---|---|
| Python behavior | Focused `uv run --locked --offline pytest <test-path>`; broader backend suite when integration warrants it. |
| Python implementation | `uv run --locked --offline ruff check .`, `ruff format --check .` and `mypy` through the same `uv run --locked --offline` prefix. |
| Evidence, source/path declarations | `uv run --locked --offline python scripts/check_repository.py`; check changed links, frontmatter, source claims and review tags. |
| Captured numerical boundary | Relevant tests and `uv run --locked --offline python scripts/replay_backend.py`; distinguish supported compatibility replay from scientific/empirical acceptance. |
| API or frontend interface | README's API generation/drift and affected frontend checks. No new frontend functionality before the backend gate. |

New-code checks exclude `legacy/`. Change lockfiles intentionally with manifests.
Delegate only independent bounded work with exclusive write ownership; the lead
reviews evidence and integration. Completion requires the applicable interface to
work, checks/results and gaps recorded in the ExecPlan, final diff inspected, and
implemented versus placeholder scope and next reproduction milestone reported.
