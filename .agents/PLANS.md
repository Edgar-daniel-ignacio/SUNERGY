# Bounded execution plans

Root `AGENTS.md` explicitly routes here. Use an ExecPlan for multi-file, risky,
or staged work. Small isolated edits need only proportionate verification.

## Begin with inspection
1. Read applicable instructions and `git status`; identify unrelated changes.
2. Trace actual owners, entrypoints, inputs, outputs, dependencies, and side effects.
3. Retrieve only relevant architecture/evidence/configuration and primary docs.
4. Record unavailable evidence. Continue independent work without inventing it.

## Write one plan
Use the next available `.agents/plans/NNN_description.md`. Keep it self-contained
and bounded; do not copy stable policy or extensive source evidence into it.
Include:
- Objective, scope, non-goals, and concrete completion criteria.
- Starting revision/worktree state and context/references inspected.
- Decisions with evidence and unresolved questions.
- Ordered implementation steps and explicit ownership if work is delegated.
- Verification commands, expected artifacts, and meaningful failure checks.
- Progress, actual outcomes, deviations, remaining gaps, and handoff.

## Execute
Keep decisions revisable when evidence contradicts them. Update the plan when
scope or findings change; record consequential assumptions as proposals needing
evidence/review, not accepted science. Preserve unrelated changes and evidence.
Use isolated run/temp paths. Delegate only independent bounded work with exclusive
write ownership; the lead owns integration and final checks.

Routine reversible implementation choices within the user's scope do not require
permission. Stop only dependent work at genuine authorization/evidence blockers;
continue safe independent work and describe the precise gap.

## Verify and hand off
Test observable behavior and failure modes, not just file existence. Reproduction,
scientific verification, and empirical evaluation have separate evidence gates.
Record exact commands and results, including failed/unavailable checks and why.
Check the diff for scope creep, secrets, generated/private data, and legacy edits.
Finish with implemented/deferred behavior, evidence limitations, and a bounded
next step. Plans and documentation do not supersede executable contracts.
