# 003 — Evidence-led code-refactoring skill

## Objective and completion

Create `.agents/skills/code-refactoring/` from the useful methods in the supplied
code-modernization plugin. The skill must reuse and assess existing understanding,
support uneven documentation, distinguish preservation from deliberate changes,
and run in Codex without plugin hooks or a new application dependency.
Complete when structure/link checks and independent representative task trials
pass, with observed limitations recorded. Scope is skill creation and validation;
no production/legacy refactor, captures, evidence-document corrections, dependency
changes, or global harness changes.

## Starting state and inspected context

- HEAD `cef03c2b9f73558c715d489f499d55ce26824a4c`, branch
  `docs/legacy-refactorizacion`; only pre-existing untracked change is
  `.agents/skills/code-modernization/`. Preserve it byte-for-byte.
- Read root/scoped AGENTS, `.agents/PLANS.md`, architecture, reproduction, evidence,
  initial scaffold plan, manifests, comparator and repository checker.
- Read collaborator README/conventions and selected contracts, missing-work,
  proposed-refactor, decisions and starting-point sections. Index is a locator,
  not evidence that code executes or a complete project inventory.
- Apply installed skill-creator guidance and its UI metadata reference. Inspect
  plugin commands/agents/scripts without executing its hooks or workflows.

## Decisions and unresolved evidence

- Separate new discoverable skill; keep original plugin untouched. Concise core
  workflow plus SUNERGY-specific evidence routing, loaded selectively.
- Use task-scoped claim/contract/validation records in the existing ExecPlan or
  response, not a parallel analysis database or rigid mandatory report suite.
- Static documentation is neither independent output capture nor accepted science.
  Proposed contracts may mix current behavior with changed behavior; classify per
  claim. Current code is evidence of behavior, not approval of its correctness.
- Reuse existing capture/comparison ownership rather than importing a generic text
  comparator with masks and global tolerance limits.
- Verify upstream provenance/license before any direct code/text reuse. No
  executable upstream code is needed unless inspection establishes a clear benefit.

## Steps and ownership

1. Lead: evidence selection, plan, draft skill/resources and integration checks.
2. `assess_upstream`: read-only plugin capabilities/dependencies/provenance review.
3. Independent agents: use the finished draft without creation history on bounded
   SUNERGY tasks spanning detailed/conflicting evidence and incomplete/absent docs.
   No shared-file writes or legacy execution; temporary outputs only if needed.
4. Lead: assess actual responses against sources and task scope; revise only for
   observed problems. Validate final skill, links, preservation and diff.

## Verification strategy

- Bundled skill-creator `quick_validate.py` for frontmatter/name/placeholders.
- Check relative skill links and repository routes, YAML, absence of stale runtime
  dependencies; read final instructions for useful activation and concise loading.
- Blind forward trials: select concrete source/contracts and require actionable
  validation decisions, explicit missing evidence and scope preservation. Include
  at least one documentary contradiction and one unfinished/undocumented module.
- Offline repository integrity check for legacy/evidence hashes; relevant existing
  tests only if trials need executable evidence. No application-wide build needed
  for Markdown/YAML-only changes. Inspect final diff and untracked contents.

## Progress and outcomes

- Inspection complete. Created `SKILL.md`, one selectively loaded SUNERGY routing
  reference and `agents/openai.yaml`; no scripts or runtime dependencies needed.
  Core is about 960 words. Original plugin remains separate and untouched.
- Upstream read-only assessment corroborated reuse of source-cited behavior,
  bounded slices, characterization, negative checks and independent review.
  Did not port Claude Workflow/hook APIs, telemetry, fixed output trees, universal
  tolerance caps, mtime preservation checks, arbitrary fresh-case counts or the
  `PROVEN` verdict. README declares Apache 2.0; full root license/revision absent.
  New instructions use the methods without copied plugin code/assets/text.
- Initial parent-directory creation was denied by the protected `.agents` path;
  authorized scoped directory creation succeeded through sandbox escalation.
- Initial checks passed:
  - `.venv/Scripts/python.exe C:/Users/rashi/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/code-refactoring`
  - `.venv/Scripts/python.exe scripts/check_repository.py`
  - One-off Python/YAML/link inspection: all 9 relative links resolve within repo;
    UI metadata valid, default automatic discovery, no tool/runtime dependencies.
  - PowerShell index lookup and `rg` example in reference: locates `IV_R`/F-058
    and actual callers without emitting the full index.
- Three fresh-context forward trials: agents receive the skill, realistic requests
  and resource/scope boundaries, not expected findings or creation conversation.
  All three trials completed; lead source/artifact review and reruns passed.

## Forward-test evidence

### Unfinished catalog assessment — passed

Request: assess refactoring the legacy module catalog into the backend, starting
from `Modules_Data_Base.py` and the collaborator inventory; no implementation.
Agent used the skill and selected raw docs/source in a fresh context, read-only.

- Found and hash-checked the empty module, instead of inferring its functionality
  or requiring a matching inventory entry. Traced workbook filtering/selection via
  dashboard and helper to `Placa_D1`/`Placa_D2`; kept static reachability distinct
  from executed behavior.
- Distinguished current immutable byte reader and identity schemas from missing
  parsing/normalization/acquisition; did not present schema-valid requests as a
  working simulation or assume CEC UI label identifies a pvlib snapshot.
- Flagged raw `Average NOCT` flowing to `temp_ref` and an unsupported selectable
  filter combination as consequential changes, not ordinary naming cleanup.
  Lead checked producer `GIU_Final_Presetacion.py:969…` and dictionary builder
  `Input_File_DIV_Mac_Informe.py:1017…`; temperature lineage confirmed.
- Proposed one local snapshot/selected-record characterization with exact record,
  field/order and failure checks. Missing workbook constrained replay while leaving
  mapping/contract investigation available. No files changed or legacy executed.
- Skill usability: no setup dependency or blocking ambiguity reported.

### Conflicting I–V evidence and consolidation plan — passed

Request: plan a reusable backend calculation consolidating `IV_R`/`IV_CI_cor`,
using collaborator contracts/recommendations and preserving user results.

- Reused C-05/C-06 and indexed functions, then traced actual numerical boundaries
  and callers. Kept 100-point `IV_R` distinct from active 250-point `IV_CI_cor`;
  identified the latter's unreachable post-return code rather than treating the
  whole indexed range as executable. Lead confirmed active grids and the return.
- Separated positional module/alpha/material/reference-temperature compatibility
  from proposed corrections and rejected adopting D-07 tolerances without review.
  Recognized the proposed Dash return contract differs from the backend owner.
- Found the no-Dash harness claim contradicted by actual imports and the unused
  reverse solve's potential failure behavior. Proposed independent `IV_R` capture
  first, before numerical extraction, leaving full measurement/correction migration
  gated on original workbook and its own captures.
- Did not let annual-irradiance/bootstrap disputes block the forward-only slice;
  kept explicit 501/unavailable behavior. Named exact structure, numerical,
  side-effect and intentional-change checks. No parity or scientific claim.
- No files changed/legacy execution. Remaining practical capture-wrapper design
  depends on the selected environment; skill correctly surfaces it but does not
  automate it. This is a capture task limitation, not a reason to add a general
  runner to the skill.

### Implemented modern structural refactor — passed

Request: extract per-quantity comparison from `compare_outputs` into a private
helper, preserving signature, exact messages/order, additive tolerance and input
mutation behavior. Agent could write only `.local/skill-validation/structural/`.

- Copied modern package files and the existing five regression tests; retained
  untouched before copy. Produced a small helper-extraction patch plus twelve
  additional synthetic contract cases, all confined to ignored scratch space.
- Pytest session asserts package/contracts/regression import from the candidate
  directory, so passing production imports cannot mask a broken scratch patch.
- 17 cases passed, covering exact messages/order, unit/count precedence, threshold
  equality and additive/reference-scaled tolerance, negative/zero inputs, mutation,
  aliasing and the public signature. These exercise comparator behavior, not PV
  or legacy numerical outputs.
- Negative control changes additive tolerance to `max(atol, rtol*abs(reference))`
  in a separate mutant. The 100→101.25 boundary raises the preservation assertion
  (expected exit 1); candidate/before/production stay unchanged.
- Agent Ruff lint/format and mypy checks passed. Initial isolated isort package
  recognition required explicit first-party config; a new test's optional inspect
  annotation needed narrowing before mypy passed. No production change resulted.
- Lead reviewed candidate, diff, import assertions, contract tests and negative
  control. Independently reran the 17 tests and mutant, confirming the results.

Commands run from `.local/skill-validation/structural/` with
`$env:PYTHONPATH = Join-Path (Get-Location) 'candidate'` and existing installed tools:

```powershell
C:/Users/rashi/SUNERGY/.venv/Scripts/python.exe -B -m pytest --confcutdir=tests -o cache_dir=artifacts/lead-pytest-cache --basetemp=artifacts/lead-pytest-temp tests -q
C:/Users/rashi/SUNERGY/.venv/Scripts/python.exe -B artifacts/run_negative_control.py
C:/Users/rashi/SUNERGY/.venv/Scripts/ruff.exe check --isolated --target-version py312 --line-length 100 --select E,F,I,UP,B --config 'lint.isort.known-first-party=["sunergy"]' candidate tests
C:/Users/rashi/SUNERGY/.venv/Scripts/ruff.exe format --check --isolated --target-version py312 --line-length 100 candidate tests
C:/Users/rashi/SUNERGY/.venv/Scripts/python.exe -B -m mypy --no-incremental --cache-dir artifacts/mypy-cache candidate/sunergy tests
```

## Final verification and handoff — 2026-11-10

- Final `quick_validate.py`: valid. All 9 local Markdown links resolve; UI YAML
  has no extra dependencies or explicit-only restriction. Reference lookup example
  executed successfully. No new executable helper warranted ongoing maintenance.
- Final `scripts/check_repository.py`: passes configuration, preserved evidence,
  all legacy hashes and import boundaries. Full application builds not needed for
  this Markdown/YAML-only deliverable. No numerical/simulation code migrated.
- `git diff --exit-code` and `git diff --check`: pass; no tracked files changed.
  SHA-256 inventories before/after forward trials match for all 104 supplied
  plugin files. New deliverables are only this plan and three skill files; scratch
  code/logs/patch stay ignored in `.local/skill-validation/structural/`.
- One wording refinement distinguishes synthetic comparator plumbing examples
  from general tests with synthetic inputs; no trial revealed a workflow blocker.
  No additional rules or scripts were added solely to fit a trial answer.
- Limitations: trials are selected cases, not an exhaustive behavioral evaluation
  or real legacy migration. No independent legacy capture, scientific verification,
  measurement evaluation or calibration gate passed. Source/routes must be checked
  when future tasks run; raw artifacts may remain unavailable.
- Ready to use as `$code-refactoring`. Next skill milestone is applying it to a
  real bounded task; next reproduction candidate remains reviewed independent
  `IV_R` capture with selected inputs/environment, not a refactor performed here.
