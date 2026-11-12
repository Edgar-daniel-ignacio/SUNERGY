---
name: code-simplifier
description: Review or simplify selected code for clarity, consistency, and maintainability while preserving behavior. Use for a focused cleanup of current changes or an explicitly named target at any development stage; broader migrations and behavior changes need their own scope.
---

# Code Simplifier

Make the selected code easier to understand, debug, and change without changing
its observable behavior. Prefer explicit, idiomatic code to fewer lines. Use this
as a focused implementation pass or a read-only review, according to the request.

## Establish the target

- Follow the repository's applicable instructions and current language conventions.
  Inspect actual callers, tests, manifests, and nearby patterns before choosing a
  form; do not impose one language's import, function, or exception style on another.
- Use the user's named files, symbols, diff, or revision range when supplied.
  Otherwise inspect worktree status and staged, unstaged, and relevant untracked
  changes to identify code touched by the current task. A clean worktree does not
  make the latest commit or the whole repository an implicit target. Consult task
  history or ask for a target when no current scope can be established.
- State the bounded target and preserve unrelated edits. Read adjacent code to
  understand contracts; do not sweep it into the cleanup. Review requests produce
  findings or proposals; implement changes when the request authorizes editing.
- Leave preserved evidence and read-only originals untouched. For generated code,
  change the owning source and regenerate only when that is within the task.

## Preserve the contract

Identify the relevant observable contract before rewriting. Depending on the code,
this includes:

- Public names, signatures, accepted inputs, return shapes, ordering, types, units,
  defaults, serialization, and compatibility behavior.
- Exceptions and their timing, validation order, mutation, aliasing, I/O, resource
  lifetimes, short-circuiting, evaluation order, and asynchronous behavior.
- Floating-point operation order and precision, solver/model identities, random
  draw order/state, grids, missing-value handling, and source/provenance records.

An algebraic identity, extracted helper, eager collection, or shared cached value
can change these properties. Do not assume that equal ordinary examples prove
equivalence. Retain an awkward expression when its behavior matters or the evidence
is insufficient. Preserve comments that explain scientific assumptions, units,
compatibility quirks, or consequential decisions.

Keep bug fixes, new features, performance tradeoffs, mathematical/model changes,
and contract redesign separate from simplification. Record a suspected defect with
its evidence; do not silently correct it. Continue independently safe cleanup
within the authorized scope. A broader refactoring workflow may help with module
redesign or migration; use an available `code-refactoring` skill if appropriate,
but it is not required to run this local pass.

## Simplify deliberately

Choose changes that reduce the reader's work:

- Flatten unnecessary nesting when guard clauses preserve execution and cleanup.
- Remove proven redundancy and needless indirection; keep useful seams between
  distinct responsibilities and independently testable operations.
- Name concepts, units, and intermediate results clearly. Extract a helper when it
  gives a coherent operation a useful name, rather than hiding a single expression.
- Consolidate genuinely equivalent logic without merging subtly different
  contracts, introducing speculative configuration, or increasing coupling.
- Replace dense conditionals and clever one-liners with readable control flow.
  Keep concise idioms when they are already clear in the project's language.
- Remove stale or obvious comments; retain the rationale that code alone cannot
  convey. Keep types and documentation aligned with the unchanged contract.

Make a small coherent patch and inspect it before expanding. Reject a proposed
cleanup if it obscures behavior, makes debugging harder, erases domain meaning,
or adds abstractions without a concrete benefit. An unchanged result is valid
when the original is clearer or the preservation evidence is inadequate.

## Verify and hand off

Use checks proportionate to the actual change: existing tests, targeted behavior
comparisons, static/type checks, formatting, and generated-contract checks where
relevant. Exercise meaningful boundaries and failure paths, not only normal output.
For risky transformations, compare original and proposed behavior on the same
controlled inputs in isolated locations; include error and side-effect traces when
they are part of the contract. Keep private inputs and generated results out of
tracked fixtures. Do not manufacture expected outputs, loosen tolerances, or infer
scientific validation from passing software tests or agreement with the old code.

If a check fails, determine whether the patch caused it; restore or narrow the
affected simplification rather than concealing the change. Report unavailable
checks and the remaining uncertainty. Inspect the final diff for unintended API,
math, dependency, generated-file, or unrelated edits.

Report the target, the meaningful clarity improvements (or why none were safe),
the behavior evidence and checks run, and any defects or larger work left separate.
Distinguish verified preservation from an expectation that has not been tested.

## Repository context and source

This workflow is portable across languages, agent hosts, and development stages.
It requires no particular tool name, UI metadata, external service, or companion
skill. In SUNERGY, discover current ownership and evidence boundaries through the
applicable repository guidance; do not freeze an old scaffold layout into this
workflow or modify read-only legacy evidence.

Adapted from the supplied [plugin agent](references/plugin-source.md), retained
byte-for-byte for provenance only; do not load it as workflow instructions. The
workflow above replaces its host-specific activation and JavaScript style rules.
The supplied copy establishes no additional upstream version or license metadata.
