---
title: Legacy audit and backend coverage
role: Reconcile the original investigation and map capabilities to implementation and references
retrieve_when: Recovering legacy behavior, checking a disputed claim or choosing the next backend slice
read_scope: Relevant audit finding or capability; follow the original chapter, symbol and capture
authority: Source-audited reconciliation; static findings and executed coverage remain distinct
verify: Inspect named source and actual reference assertions before extending a claim
---

# Legacy audit and backend coverage

Start with the collaborator's [overview](legacy-refactorizacion/README.md), its
[chapter catalogue](legacy-refactorizacion/README.md#8-índice-de-documentos) and
[index](legacy-refactorizacion/index.json). They preserve the original author's
understanding, terminology, implicit contracts and intended refactor. This document
owns the independent audit and legacy-to-modern coverage, not a replacement
function inventory. Modeling interpretation belongs in [assumptions](assumptions.md).

## Audit scope and confidence

The current audit reviewed chapters 00–11, the overview, index and four diagrams,
then checked consequential claims at their named functions, callbacks and data
consumers. Source identity is the frozen [inventory](evidence/legacy_inventory.json).
Static source findings below do not claim that the full dashboard, original
workbook or annual/correction branches executed.

| Evidence checked | Result and scope |
|---|---|
| All 109 indexed functions | Names, start/end lines and spans match the two main source files; no indexed locator drift or omitted top-level function was found. Reuse chapter 04/index rather than recreate them. |
| Callback/layout reachability | 23 decorated callbacks plus 22 distinct layout factories give 45 static roots; the traced graph reaches 103/109 functions and corroborates the six listed disconnected helpers. This graph does not rule out external direct callers. |
| Counts and source spans | State counts/spans agree with the index. The six largest functions total 7,013/13,516 function-span lines (51.89%), or 47.08% of 14,896 raw lines. Denominators matter. |
| Repeated selector structure | The large curve callback has 84 `Metodo` branches, 28 `Seleccion` branches and 113 return statements of width 13. These are branches, not 113 distinct output ports. |
| Reported duplication/liveness metrics | The 91% duplication, 44 groups/166 blocks and 132 unused assignments remain collaborator-reported measurements; the originating benchmark tools/method artifacts are absent. Their source pointers remain useful, but the exact metrics were not independently reproduced. |
| External modules | Their indexed locations were checked separately; the cited top-level definitions include ten functions and one class. They are outside the main 109-function inventory. |
| Numerical execution | Existing independent IV_R/Faiman/NOCT references establish only the domains below. This context audit adds no new numerical reproduction or empirical-validation claim. |

## What the original chapters uniquely provide

Use 00 for conventions, 01–02 for the system/data story, 03 for implicit boundaries,
04/index for exact function locators, 05–07 for duplication/defects/missing work,
08 for the author's report-to-code account, and 09–11 for proposed organization,
unresolved decisions and historical implementation order. Proposals in the last
three chapters are valuable design input, not accepted contracts or proof of
scientific validity. Their own frontmatter narrows retrieval.

## Consequential findings and corrections

The original chapters retain local tagged corrections. This table is the compact
cross-chapter disposition; follow the cited source/operation for details.

| Claim or seam | Audited conclusion | Trace / consequence |
|---|---|---|
| Counts, IDs and overview language | The panel contains 24 functions but 23 callbacks. Some README ID examples are invalid; duplication percentages use differing denominators. Unsupported statements that the physics is sound are interpretations. | Original README/01/04/05 and the index; current audit preserves the valid locators and separates measured/reported/proposed claims. |
| Weather acquisition and length filtering | `Clima` returns `SmartNDH`, supports direct supplied arguments and creates keys for fetched lengths. TMY forces 60-minute requests. Downstream POA/Sandia/writers impose length gates; acquisition does not universally discard nonstandard lengths. Metadata describe the last fetched response, not every year. | `Primer_Funcion_Clima.Clima:64–183`, `SmartNDH:43–56`; C-01 and WX-01. Separate source records, temporal interpretation and downstream filtering. |
| Import versus execution side effects | Full helper import requires UI/plotting dependencies. CSV deletion and upload rewriting occur inside called helpers, not proven import-time deletion. | Helper top-level AST and writer/upload bodies; isolated capture must inspect both dependencies and selected call effects. |
| Catalog reference temperature | The catalogue selector places `Average NOCT` in slot 9; `Placa_D1/D2` name it `temp_ref`; annual PE consumes it as fit reference temperature. Detailed IV_R instead forces 25 °C. | Dashboard `render_content:969–1080`, helper `Placa_D1/D2:1017–1057`, `PE:1390`; IN-02. This semantic mismatch is not repaired by field normalization. |
| Preset versus discarded manual input | A displayed 250 W preset is legitimate behavior. The silent-input problem is the INSERT path's reuse of `Placa_Prueba`, which replaces the supplied fields. | B-06, preset defaults/callback branches and IN-01; keep preset identity separate from manual-input preservation. |
| Thermal contracts and reachability | Sandia has six a/b entries but four deltaT entries; the UI exposes 1–4. Direct helper/externally supplied selectors 5–6 remain an out-of-domain failure risk. Unsupported lengths are ignored; missing POA can fail immediately. Faiman/NOCT lack Sandia's length predicate. | `Temperature_sandia:785–800`, `Sandia_options:762–783`, thermal callback; TH-01/02. Capture exposed selectors and helper failure regimes separately. |
| Annual equations | `PE` already applies irradiance in current before multiplying Vmp×Imp. D-01's algebraic wording does not justify another factor. Stored `nNsVth` and temperature-coefficient meanings need scientific review. | `PE:1488–1508`, AN-01 and IV-01; no corrected default selected. |
| Compound missing-column condition | Only the literal `NOCT` operand is always truthy; the complete condition still depends on Sandia/Faiman columns. The branch reading all three temperatures is normally supplied by thermal selection `[1,2,3]`; other PE_NOCT branches use different selections. | B-08; characterize missing-NOCT inputs and reachable callers instead of asserting unconditional application failure. |
| Float/list arithmetic | IV_CI2 reads pandas scalars. NumPy scalar subtraction can dispatch successfully over a list, unlike plain Python float subtraction. The asserted TypeError is dtype-dependent. | B-09 and `IV_CI2`; no measurement/function execution is available to establish the actual failure for the original workbook. |
| UI failure/default scope | The malformed fallback is a real arity defect for cleared/unknown selection; the default is `SELEC`. Bootstrap table style defects affect five returns. Missing-correction zeroes are callback outputs, not initial store data. | B-11/12/13 and the actual callbacks; do not turn conditional symptoms into startup facts. |
| Correction method versus curve origin | Both `correction_IV` and `_s` support M2/M2N. `_s` identifies simulated-curve inputs, not the normalized method; their fitting grids/coefficient/k strategies differ. | Chapters 08–10, `correction_IV:7304–7534`, `correction_IV_s:7609…`; EV-01. Method, origin and fit strategy are separate axes. |
| Effective versus reported temperature | IV_CI_cor first uses sensor average for translation, then overwrites Tmod with a Voc-derived value for corrections/simulation, while output metadata retain the sensor average. | `IV_CI_cor:5957–6015` and repeated branches; EV-01 and the correction lineage diagram. Sensor averaging alone is not the effective correction contract. |
| Statistical/report linkage | Source bootstrap uses 3,000 × 12 and minimum-length truncation; the summary reports 4,000 × 15 and 255 positions. `Comprobacion` fixes n=30 / df=29. A displayed 95% label does not validate the statistic or historical method linkage. | Bootstrap/Bootstrap2/Comprobacion and summary §4.10; EV-01. Preserve RNG/sample/ordering rules before any controlled alternative. |
| Design equivalence and estimates | `Solar_pos_e(tilt=None)` equivalence is proposed, not current behavior; `float(None)` fails. Refactor line/function totals and coverage predictions are estimates. | Chapter 09; preserve dimensions-as-data intent without adopting hypothetical contracts/counts. |
| Workbook identity and preservation | Earlier workbook observations are collaborator-reported because originals are absent. Positional sheet consumption can misassociate or fail. `guardar_archivo` rewrites the workbook, so preserving original bytes is a deliberate modern safeguard. | C-05/R-03/R-04, upload helper and EV-01; retain author observations without inferring source availability or identity. |

## Capability-to-implementation coverage

Repository module paths below are relative to `backend/src/sunergy/`; original
function/contract IDs resolve through chapter 04/index. Scope is the intended
legacy backend, including unresolved failure/correction decisions. Browser styling
and Dash stores explain callers but are not migrated numerical features.

| Capability | Legacy boundary / inputs | Modern owner and present coverage | Next evidence or work |
|---|---|---|---|
| Module/preset/catalogue records | S0/S4, C-06; `Placa_Prueba`, `Placa_D1/D2`, catalogue workbook fields. | Fetcher supports the inspected manual capture layout; no workbook adapter. IN-01/02 retain preset and reference-temperature distinctions. | Producer-specific references; catalogue edition/hash/license and field semantics. |
| Weather | S1, C-01; `Clima`/SmartNDH, site/year/interval and response metadata. | No modern acquisition or raw-response normalization. | Original response snapshots and per-response provenance/time contract. |
| Solar geometry / POA | S2; `Solar_pos`/`Solar_pos_e`, weather index and orientation. | No modern integration or reference. WX-01 distinguishes returned pvlib geometry from unused manual terms. | Timestamp/length/orientation characterization and recorded inputs. |
| Thermal | S3; `Temperature_sandia`, `Temperature_feinman`, `Temperature_NOCT`. | `thermal.py` / `thermal_contracts.py`: Faiman/NOCT point profiles, four parameter cases × five synthetic points. Legacy mutable wrappers are outside that numerical boundary. | Sandia UI 1–4, length gates and direct-helper failures; annual integration and empirical applicability. |
| Annual electrical series | S4, C-02/03; `Factor_Idealidad`, PE families and selectors. | No modern annual workflow. AN-01/IN-02 identify effective parameter/temperature concerns. | Branch-specific captures of parameters, filtering, columns and all records; do not infer annual parity from IV_R. |
| Summaries/extrema/condition generation | S5; resume/min/max helpers and consumed labels. | Unimplemented. Source-confirmed dictionary-rounding and Voc-column defects remain separate from intended selection rules. | Synthetic frame characterization of ties, labels, branches, errors and consumers. |
| IV_R | S6, F-058; ordered module and supplied comparison-condition rows. | `model.py`, `compatibility.py`, application/API: two modules/six conditions/600 points per captured Windows/Linux x86-64 environment; fit/translation/solver/grid/table references. | Upstream condition generation and broader inputs; no full dashboard, scientific or empirical claim. |
| Other detailed I–V | S6; IV_R1/2/VE and CI/simulation families. | Unimplemented profiles. VE hardcodes a different gamma; grids and return schemas vary. | Independent branch-specific captures before sharing kernels or changing grids. |
| Measurement normalization / correction | C-05, S6/S7; Info records, positional sheets, both method/origin families. | No modern ingestion/evaluation/correction. EV-01 retains effective-temperature and fit-provenance chains. | Original bytes/permissions/module linkage and intermediate sensor/inferred/fitted values, then M2/M2N captures. |
| Representative curve / statistics | S7; Bootstrap/Bootstrap2/Comprobacion. | Unimplemented. Current source and reported historical method differ. | Exact input lengths/order, legacy RNG state/draw order, fixed n/df and historical algorithm identity. |
| Legacy I/O and presentation | C-02–05, S0/S8; file bus, upload rewriting and callbacks. | Explicit modern calls/results and isolated run paths replace selected incidental I/O. No general dashboard migration. | Inspect side effects and define observable boundaries; capture conditional failures before compatibility/correction decisions. |

Current capture identities live in [the registry](../tests/fixtures/legacy/capture_status.json)
and manifests; executable comparisons live in the named model/thermal tests and
replay owner. Frozen manifest review text describes capture time, not current
approval. The [reproduction contract](reproduction.md) owns acceptance semantics.

## Ordered remaining reproduction work

1. Characterize Sandia's exposed selectors/lengths and separate helper failure
   regimes, plus annual summary/condition-generation helpers with synthetic frames.
   These are pending work, not missing-weather blockers.
2. Recover recorded weather responses, time metadata and catalogue evidence where
   used; compare source normalization, POA and thermal intermediates before annual
   integration. Manual module input bypasses only the catalogue dependency.
3. Capture S4/S5 supported combinations and the remaining I–V variants, retaining
   module identity, branch-specific coefficients, columns, ordering and failures.
   Review corrections separately from compatibility.
4. Recover original report/workbook, permissions and module/sensor linkage; then
   capture measurement normalization and correction with effective-temperature,
   coefficient/fit and output-metadata provenance intact.
5. Resolve current-versus-reported bootstrap identity and capture original RNG,
   truncation/draw order and fixed statistical assumptions before any alternative.

6. Close the intended full backend coverage or obtain explicit reviewed exclusions
   before new frontend functionality. Scientific support, empirical evaluation
   and calibration remain separate assessments.
