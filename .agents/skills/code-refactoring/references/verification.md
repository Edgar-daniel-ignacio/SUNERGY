# Verification and evidence

Choose checks for the claim. No universal test count, coverage percentage,
tolerance or report verdict proves a refactor correct.

## Acceptance matrix

Relate consequential contracts/rules/version deltas to conditions and results in
the existing task record:

| Contract/claim | Expected behavior and conditions | Check and actual artifact | Status/gap |
|---|---|---|---|
| Boundary, rule, invariant or delta | Inputs, errors, structure, state/I/O and environment | Assertion/test IDs, comparison case, capture identity, command/result hashes | Passed, failed, missing, stale or justified not-applicable |

Reuse identifiers/symbols; do not assign a rule card to every line. A lexical
mention or mapping table is a locator. Inspect assertions and executed outcomes
before claiming coverage. Resolve critical gaps with meaningful checks or explicit
limitations, not renamed tests, removed skip markers or weakened criteria.

Keep claims separate:

- **Schema/boundary:** accepted/rejected shapes and values at external interfaces.
- **Structural preservation:** selected observable behavior including errors,
  mutation, order and relevant resource/state effects.
- **Version compatibility:** actual old/new runtime/library behavior and tests.
- **Legacy reproduction:** a named branch under equivalent effective inputs with
  independently captured reference artifacts/provenance.
- **Domain/scientific verification:** defensible rules/equations, units, assumptions,
  limiting cases and appropriate independent evidence. Same-library agreement is
  not independent scientific verification.
- **Measurement evaluation/calibration:** original observations, transformations,
  uncertainty and comparison; calibration retains uncalibrated results, fitted
  parameter identities, objective/bounds and held-out status. Fit is not validation.

## Baselines and controlled execution

Retain code/test identity, dependency/toolchain identity, command, effective inputs
and raw results before changes requiring comparison. Inspect imports/runners and
cleanup scripts before execution. Isolate copies/processes/paths, preserve originals
and prevent unintended live I/O. A read-only comparator does not make its producer
safe to run.

Choose normal, boundary, error, empty/large, ordering, concurrent or stochastic cases
according to the contract. Fresh cases challenge assumptions outside development
cases; select by uncovered behavior, not an arbitrary count or distinct-output
quota. Different inputs may legitimately have equal outputs. Record refused or
out-of-domain cases and reasons; do not silently drop them from a passing total.

For numerical/stochastic work pin relevant RNG implementation/state, sample sizes,
input order, solver/version/settings, constants, grids/endpoints, units/coefficient
conversions, timezones/timestamp/interval conventions and source identities. A seeded
alternative differs from an unknown historical random stream. Missing originals or
environment limit reproduction; replacement outputs cannot become the baseline.

## Test outcomes and test integrity

Retain machine-readable runner results/logs. Verify the actual command and selected
source/environment, and whether tests executed rather than merely collected. For
uplift compare per-test identities/outcomes on the intended versions.

Investigate failures/errors, newly failing tests, passing tests now skipped,
disappeared tests, execution drops and changed/deleted test files. Equal totals can
hide a replaced test. Existing failures need explicit disposition; do not silently
accept them as product behavior. Harness-only projects/dry runs are not feature
coverage. A green new suite cannot replace the old test inventory unnoticed.

Intentional renamed tests/new contracts may change IDs/expectations. Map them with
rationale and decision evidence; never guess equivalence from class totals. Review
weakened assertions alongside the production diff. Aggregate counts or typed tables
alone do not establish preservation. For portable per-test/integrity reports see
[tooling.md](tooling.md); unsupported formats need a documented adapter preserving
IDs/outcomes or remain an explicit gap.

## Application artifacts

Compare independently obtained reference/candidate artifacts from identical supplied
and effective inputs. Check hashes/identities before interpreting differences.
Compare identifiers, count/order, shapes, units, schemas, time and grids according
to contract. Numerical values may use declared per-quantity absolute/relative
tolerances with units/rationale, e.g. `abs(actual-reference) <= atol + rtol*abs(reference)`.
Near-zero cases need a meaningful absolute scale. Default to exact comparison.

Do not round, sort, resample, hide nonfinite values, drop records or loosen thresholds
to create agreement. Isolate legitimately variable nonnumeric fields under an
explicit contract and test their semantics separately, rather than broadly masking
numbers/identifiers. Accepted deviations remain reported differences with a decision
and affected criteria; they are not silently equal.

Use a project's domain-aware capture/comparator owner when present. Generic helpers
in [tooling.md](tooling.md) inspect declared files/JSON scopes; they cannot establish
scientific meaning, source authenticity or which fields are identifiers. If old
execution/captures are unavailable, report trace/characterization evidence honestly;
it cannot close a gate requiring independent reproduction.

## Challenge and independent review

When confidence depends on a new comparator or critical characterization check,
inject a meaningful discrepancy in scratch, confirm failure, restore and rerun.
Choose relevant record loss, order/unit drift, threshold/formula or mutation errors,
not a cosmetic break. Never modify frozen baselines or originals.

Give independent reviewers the request, contracts, raw artifacts and patch, not a
desired verdict. Ask about missing branches, ownership, unjustified differences and
assertion strength. With no worker API, do a distinct review pass and disclose its
independence limitation. Findings require evidence, not majority votes or automatic
acceptance based on a severity label.

## Diagnose and report

Separate implementation bugs, baseline defects, intentional changes, environment
drift and harness/evidence failures. Fix the owning cause, retain the prior record
and rerun affected checks. A baseline refresh creates a new reviewed identity; it
does not erase discrepancies or retroactively validate old runs.

For each claimed gate report actual commands/versions/input identities, executed
cases/outcomes, skips/missing/stale evidence, relevant discrepancies, changed tests
or contracts, authorized deviations, remaining coverage and next action. Helpers
return differences/gaps; the agent still assesses scope/evidence. A finite pass
does not certify universal equivalence, scientific accuracy or approval to release.
