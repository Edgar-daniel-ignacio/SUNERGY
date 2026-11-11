---
title: Legacy reproduction contract
role: Independent-reference requirements and compatibility comparison boundaries
retrieve_when: Capturing, porting or comparing a named legacy capability
read_scope: Relevant profile, environment, preservation boundary and comparison policy
authority: Software reproduction contract; separate from scientific or empirical acceptance
verify: Check manifests and actual assertions for every claimed branch and record
review_status: "#to-review"
---

# Legacy reproduction contract

Reproduction compares a named original implementation with a modern implementation
under equivalent effective inputs. The [coverage map](legacy_backend_coverage.md)
owns current capability status. A representative point calculation does not close
the full backend gate, and a reproduced defect is not an accepted scientific
choice. #to-review

## Separate acceptance questions

| Assessment | Required evidence |
|---|---|
| Boundary validity | Explicit fields, units, domains, identity, missing-value and cross-field checks. Parsing success alone is not numerical validity. #to-review |
| Reproduction | Independent original-source outputs, exact boundary/environment identity, complete structure/record checks and justified per-quantity comparison. #to-review |
| Scientific verification | Applicable primary formulations, unit/parameter coherence and independent numerical/physical checks. #to-review |
| Empirical comparison | Original observations, conditions, uncertainty, exclusions and normalization lineage. #to-review |
| Calibration | Uncalibrated baseline, fitted identities/values, objective/bounds/method and separate fitting versus held-out evaluation evidence. #to-review |

## Independent reference contract

`CaptureManifest` in `regression.py` owns the executable metadata contract.
Capture independently from unchanged legacy code, not from the replacement being
judged. Inspect import dependencies and called-function side effects first; full
UI imports and file-mutating helper calls are different risks. Isolated runners
must make any extraction, interception or compatibility intervention inspectable
without changing the numerical body. #to-review

Each capture identifies source revision/files/hashes, exact entrypoint/branch,
wrapper, dependency environment, supplied and effective inputs, raw outputs and
hashes. Record source snapshots/permissions where applicable, units/conversions,
model/fit/solver/settings, grids/endpoints/order, time conventions, missing/nonfinite
behavior, and RNG algorithm/state/draw order for stochastic paths. Unknown
historical metadata remains a limitation, not a license to infer it. #to-review

Preserve original upload bytes and source identity separately from normalized or
fitted data. Capture-time review metadata is historical; do not edit frozen
manifests to report later progress. Current coverage assessment belongs in the
maintained map. New captures use new isolated destinations and deliberately
selected redistributable inputs. #to-review

## Existing reference boundaries

| Profile | What is compared | Scope and intentional boundary differences |
|---|---|---|
| `legacy-iv-r-v1` | Two modules, six ordered conditions and 600 voltage/current points per captured Windows/Linux x86-64 environment; fit arguments/six parameters, De Soto arguments/five parameters, seven solver metrics and exact rounded table. #to-review | Original IV_R numerical return boundary. Modern explicit input/output validation replaces implicit dataframe errors; positive irradiance is required. Plot styling and the discarded reverse-grid computation are captured evidence, not modern returned features. No upstream condition-generation or other-curve claim. #to-review |
| `legacy-faiman-v1`, `legacy-noct-v1` | Four explicit parameter cases across five ordered synthetic points; all temperatures/identities and output-column meanings. #to-review | Immutable point results replace legacy frame mutation/None returns. Coefficients are explicit; supported domain is narrower and documented in TH-02. No annual/weather integration or empirical thermal claim. #to-review |

The [capture registry](../tests/fixtures/legacy/capture_status.json) links immutable
manifests. Each pins source/wrapper/environment/input/output evidence. Existing
capture environments are reconstructed, not the unknown historical runtime.
Synthetic/manual inputs can characterize software; they are not original weather
or measurements. #to-review

IV_R reference selection is deterministic by captured OS/architecture. It does not
choose whichever numbers pass. All four platform references are integrity checked;
unsupported environments fail explicitly. Original Windows/Linux differences are
retained, while same-platform comparisons use the unchanged quantity limits.
#to-review

## Comparison policy

Compare branch/model identity, names, units, identifiers, count/order, shapes,
columns, timestamps and declared grids. Account for every record and failure
boundary. Numeric comparisons use each manifest's quantity-specific tolerance and
rationale, normally `abs(actual-reference) <= atol + rtol*abs(reference)`.
Near-zero floors need a scale in the stated units. #to-review

Do not round, sort, resample, mask numbers, drop records or weaken thresholds to
obtain agreement. Original table rounding is preserved behavior, not comparator
rounding. Unexplained missing/nonfinite values fail. Diagnose source defects,
implementation drift, platform behavior and intentional versioned corrections
separately. Manufacturer tolerance and campaign percentage errors do not supply
software limits. #to-review

Reference-integrity and discrepancy-injection tests establish that the comparison
can reject changed values/units/records/branches. Equation checks and developer
precision diagnostics remain separate assessments. In particular, the selected
MPP audit target and its unmet observation are not an approved scientific
acceptance contract; IV-04 records that limitation. #to-review

## Operation and completion

The supported offline replay and isolated original-capture recipes are in root
[README](../README.md#legacy-reference-replay). `replay.py` and the named tests use
recorded inputs/manifests; routine regression does not regenerate its own oracle.
Capture tooling is an explicit evidence-generation operation, not a production
simulation workflow or a prerequisite to reading documentation. #to-review

Full backend reproduction requires each intended capability to have a supported
input domain, provenance, independent intermediate/final references and successful
numerical/structural/failure comparisons, or an explicit reviewed scope exclusion.
No skipped comparison or unexplained discrepancy counts as complete. Follow the
[ordered remaining work](legacy_backend_coverage.md#ordered-remaining-reproduction-work).
Scientific, empirical and calibration acceptance remain separate; new frontend
functionality waits for the full intended backend reproduction gate. #to-review
