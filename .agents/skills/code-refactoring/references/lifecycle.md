# Refactoring lifecycle

Read the section for the current stage/track. These are jobs with evidence-based
entry and exit criteria, not mandatory named commands, folders or a linear ceremony.
Skip satisfied work after checking that its inputs and scope still match.

## Understanding and feasibility

**Entry:** selected task/scope, with uncertainty about the system or evidence.

- Recover intent from the user and maintained decisions before mining code. Identify
  off-limits data/files, callers outside scope, previous attempts and bespoke build
  tooling. Ask only when the next action depends on a missing answer.
- Inspect entrypoints, CI/build manifests, dependency locks and target toolchain.
  Separate source buildability, test-runner availability and service/environment
  availability. A missing legacy runtime may leave recorded-output checks possible;
  missing target tooling prevents a target-build claim, not planning.
- Reuse inventories, compiler graphs, maps, documentation and tests. Extend only
  consequential edges: calls, callbacks/dispatch, configuration, storage/file/state
  joins and external consumers. Record unresolved edges; no inbound edge alone
  establishes dead code. Existing machine-readable graphs beat new heuristic scans.
- Recover rules as conditions → observable outcomes, including errors, ordering,
  mutation, identifiers and units. Reuse IDs or symbols and source citations rather
  than imposing a naming scheme. Priority reflects consequence, not code size.
- Distinguish static inference, observed execution and an accepted contract. Record
  actual reviewer decisions with their scope: an inaccurate description differs
  from correctly documented but unwanted behavior. Never infer human sign-off.
- Assess risk from coupling, oracle/test gaps, sensitive data, domain uncertainty
  and reversibility. Size/duplication metrics are comparative clues, not schedules
  or evidence that an abstraction is correct.

**Exit:** enough understanding to choose the next slice, plus explicit unknowns and
their affected decisions. Full-system mapping is unnecessary for a supported seam.

## Planning and track selection

Choose by the actual change; mixed programs can use different tracks per phase.

| Track | Preserve/establish | Main evidence |
|---|---|---|
| Same-stack uplift | Supported behavior across named runtime/library versions | Exact environments, code-specific deltas, old/new test outcomes and behavior comparisons |
| Incremental refactor/translation | Selected contracts across structure/language changes | Characterization, independent captures where needed, mapping and caller integration |
| Architectural/process redesign | Required capabilities and explicit new contracts through changed boundaries | Domain/data flow, decisions and failure/transition model, acceptance tests plus preserved behavior |
| Rehost/replace without code change | Operational compatibility and ownership | Environment/vendor, integration, data/cutover evidence; no invented rewrite phase |

Use the current task record for goal, constraints, contracts, phases/dependencies,
pilot, prerequisites, exit evidence and recovery point. Criteria are testable
conditions, not optimistic labels. Respect current user decisions even when older
plans disagree. Propose scope/accepted-behavior changes explicitly.

Order by actual dependencies, not a universal leaf-first rule:

- A harness unable to run on the target is a prerequisite.
- A shared dependency/schema used by old and new consumers may need an adapter,
  dual support, coordinated change or deliberate break. Identify all consumers.
- An irreversible data/protocol transition needs a recovery/compatibility strategy
  before cutover. Do not add deployment infrastructure to a code-only task.
- Pilot a representative unit with real deltas, integration and failures. Record a
  repeatable recipe after it succeeds; use discoveries to revise the plan.

An optional contract record can fit in an existing plan:

```text
Boundary/rule: observed behavior + source/conditions
Preserve: inputs, outputs, failures, state/I/O, relevant domain conventions
Target/deviations: what changes, rationale, decision owner/authorization
Oracle and checks: identities, exact structure, justified numerical tolerances
Open questions: affected decisions + next investigation
```

## Version uplift

**Entry:** explicit source/target versions and supported baseline or honest gap.

1. Build a code-specific delta list from official migration/release documentation
   and actual use sites. Include syntax/API/configuration, dependency/toolchain and
   **silent behavioral** changes: defaults, serialization, numerical behavior,
   resource lifetimes, exceptions and ordering. Mark relevance confirmed, inferred,
   ruled out or unresolved. A generic release-note dump is not a plan.
2. Measure source tests before edits. Preserve per-test reports and hashes, including
   existing failures/skips and test-file identities. Typed totals or a green target
   cannot establish what ran before. Migrate the harness first if required.
3. Run the pilot in isolated source/target environments with equivalent inputs.
   Characterize silent deltas at affected use sites. Mentioning a delta/filename
   in a test is a navigation link, not assertion coverage.
4. Record versions, relevant sites, ordered transformations, shared-root changes,
   commands, surprises, validation and rollback in the pilot recipe/playbook.
   Separate mechanical edits from behavioral corrections; retain the baseline.
5. Batch units only with satisfied dependencies and validated recipes. New deltas
   become recipe gaps: stop the affected dependent work, investigate, update the
   plan/recipe and retry a representative unit before widening the batch. Recheck
   affected completed units. Do not guess a fix across every consumer.
6. Integrate migrated units and run affected application/package tests/contracts.
   Passing isolated units does not establish shared build compatibility.

**Exit:** intended versions actually build/run within tested scope, outcome/behavior
differences are explained, changed tests reviewed and integration checked. Missing
old versions/services remain explicit limitations, not substituted successes.

## Incremental replacement

**Entry:** selected seam with an observable contract and preservation oracle,
or the task is first satisfying an explicit capture prerequisite.

- Trace both sides. Specify input domain, outputs/errors, side effects, precision,
  time/randomness and external callers. Replace accidental structure where safe:
  preserving behavior does not require perpetuating an internal filesystem bus.
- Add characterization where consequential coverage is missing. Numerical parity
  needs independently captured references before replacement; hand-derived values
  or replacement-generated expectations are different evidence.
- Implement a cohesive use case in target idioms at the owning layer. Separate
  deterministic domain work, I/O, transport and presentation by actual responsibility.
  Avoid legacy-shaped wrappers or speculative frameworks without a concrete need.
- Compare identical inputs, inspect deviations and exercise a real consumer.
  Include mutations, lazy evaluation, labels used as keys, rounding and exceptions.
  Wiring an unused path or honoring discarded input is a behavior change.
- Retire obsolete production paths only after resolving consumers/transition.
  Preserve source-of-record evidence and captures per policy. A compatibility
  reproduction of a defect remains a documented defect.

**Exit:** the named behavior is implemented, checked and connected at its claimed
boundary. Other branches/modules are separate pending work.

## Architectural redesign

**Entry:** explicit goal/constraints and enough behavior/data understanding to
justify changed boundaries. Existing diagrams can contain unaccepted proposals.

- Define capabilities, owners and contracts before choosing services/packages.
  Compare the simplest viable design with alternatives. Include relevant concurrency,
  idempotency, failure propagation, resource limits, domain/provenance conventions and
  data transition. Do not reserve hypothetical functionality with infrastructure.
- Map old rules/capabilities to target use cases, deliberate retirements and new
  behavior. Define runnable acceptance criteria for each vertical slice. A schema,
  stub, folder tree or pending test is scaffolding, not implementation.
- Implement one real use case through required owners: domain logic/calculation,
  boundary validation, adapters, transport and presentation as scoped. Regenerate
  derived interfaces from their owner; do not maintain parallel schemas.
- Exercise end-to-end success/failure, compatibility and integration. Review and
  repair the integrated change, update design/decision records when findings change
  assumptions, then implement the next pending use case. One service's tests cannot
  complete a multi-capability program.
- Before switching consumers, establish readiness, compatibility/parallel period
  if needed, observability and recovery. Select staged versus atomic transition
  using actual consumer/data constraints rather than a default pattern.

**Exit:** implemented and integrated capabilities satisfy named acceptance criteria;
scaffolded, deferred, unverified and intentionally removed scope remains visible.

## Orchestration and resume

Portable roles are **investigate**, **implement**, **verify** and **integrate**.
One agent can perform them sequentially. Independent review helps with high-risk
contracts/shared boundaries; it is not a required platform feature or approval.

```text
Unit / stage / track:
Goal and contract/rule/delta links:
Dependencies and current source/contract/data/environment identities:
Read scope; exclusive write scope; shared changes requested from lead:
Checks and expected evidence locations:
Stop condition / unresolved-decision boundary:
Return: attempted actions, changed files, actual commands/results, evidence,
        gaps/deviations, state and next action.
```

Use existing task rows; no workflow engine or special file schema is required.
Reject dependency cycles, unresolved IDs and overlapping write scopes before
scheduling. Unknown/out-of-scope dependencies need evidence, not an assumption that
they are complete. Serialize shared manifests/contracts/generated outputs or isolate
and integrate deliberately. Choose concurrency from capacity and independence.

Track pending, ready, running, blocked, failed, completed or invalidated units, with
stage/evidence attached. Separate attempted command, successful build, executed
tests, matching behavior and integrated result. Aborted, missing and unattempted
units remain in coverage. A worker returning no result is not a completed unit.

On resume/status:

1. Read the record; inspect checkout/dirty work and expected outputs, including
   processes/resources left by the task. Do not trust completion markers alone.
2. Match contract, source/content, data, toolchain and command identities to recorded
   evidence. Check hashes/results as warranted; file presence/mtime is insufficient.
   Matching identities permit reuse only at the originally evidenced strength;
   hashes cannot supply missing execution records or upgrade a historical claim.
3. Invalidate only dependent evidence affected by changed inputs, failures or missing
   artifacts. Preserve unrelated valid work; compare tests to retained originals.
4. Diagnose implementation, harness/environment, evidence gap or deliberate difference.
   Resolve the owning cause, rerun affected checks and update the record. Repeated
   retries without new evidence are not progress; state the precise blocker.
5. Report current coverage, invalid/stale/blocked units and one concrete next eligible
   action with reason. Honor requested scope; no automatic full restart or rollout.

## Integration and handoff

The lead reviews returned patches/evidence, owns shared interfaces and runs affected
integration checks after combining changes. Check API/data compatibility, failure
behavior and generated contract drift. A bounded clarity pass (optionally using
`code-simplifier`) must not mix in new behavior.

Review security/operational changes at the affected surface: input boundaries,
secrets, file/network access, dependencies and resource behavior. Use specialized
audit workflows when task/risk calls for them, not as a mandatory final ceremony.
Substantiate findings, distinguish not scanned/not judged from clean, apply scoped
corrections and verify residual gaps. Do not patch frozen source evidence.

For release/cutover in scope, name target, readiness checks, compatibility/data
transition, monitoring, rollback trigger/procedure and recovery point. Complete a
reviewable change before requesting any still-required external authorization.
Refactoring alone does not authorize publication, deployment or messaging others.
Clean up task-owned processes/resources; preserve artifacts needed for replay.

Handoff names implemented versus scaffolded/deferred scope, source-to-target owners,
accepted differences and authorization, actual commands/results, test/comparison
coverage, known defects, gaps and next action. Link raw artifacts rather than copying
volatile inventories. Implementation, integration, verification and release are
different states; a handoff document cannot substitute for any of their evidence.

## Adapted plugin routines

The supplied code-modernization plugin informed this workflow. Its original tree
is not a runtime dependency. This table documents the functional adaptation rather
than requiring its command names or folder conventions.

| Original routine | Portable form |
|---|---|
| Preflight, assess, map, extract-rules, review | Scoped feasibility, reuse of graphs/evidence, explicit behavior contracts and recorded decisions |
| Brief and intent | Existing task plan with criteria, dependency order, pilot and authorization scope |
| Uplift, deltas, migrate workflow | Code-specific version deltas, source/target baseline, pilot recipe, dependency-aware units and recipe-gap loop |
| Transform | Characterization, cohesive replacement, caller integration and explicit deviations |
| Reimagine/scaffold | Capability/architecture design followed through actual use-case implementation, integration and verification; scaffolding remains interim |
| Verify, compare, baseline-diff, uplift-checks | Independent/negative checks, per-test outcomes, declared artifact comparisons and hash-based test/source integrity; see [tooling](tooling.md) |
| Shard builder, rule renderer/trace | Bounded unit assignments and contract-to-assertion/result matrix using established IDs; lexical references stay locators, not proof |
| Status, workflow journals, report | Current task record and artifact identities, selective invalidation, concrete next action and readable evidence handoff |
| Hardening/review | Scoped substantiated findings, corrective iteration and residual gaps; full audits remain conditional |

Workflow engine calls, plugin slash-command registration, live panes, hooks,
telemetry and global harness settings are not ported. Diagrams/rendered reports
remain optional presentation artifacts, not workflow prerequisites. Fixed case or
worker quotas, mtime freshness, presence-only completion and universal proof labels
are replaced by contract-specific evidence and explicit coverage limits.
