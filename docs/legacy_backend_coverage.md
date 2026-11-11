# Legacy backend coverage and evidence reconciliation

Start with the collaborator's [curated overview](legacy-refactorizacion/README.md)
and use its [index](legacy-refactorizacion/index.json) to locate a capability,
function (`F-`), implicit contract (`C-`) or issue (`B-`/`D-`). This document connects
that investigation to current backend ownership and executable reproduction.
It does not replace the original chapters or make their proposals authoritative.
For capture requirements and acceptance rules, use [reproduction](reproduction.md);
for scientific limits, use [evidence](evidence.md).

## Evidence assessment

The curated investigation is dated 2026-11-02. Its overview explicitly says the
system was **not executed**. `medido` means static AST analysis; `verificado`
means reviewed source, unless a specific raw execution artifact establishes more.
The analysis repository's benchmark scripts and detailed bug report are not part
of this checkout. The preserved source inventory, rather than moving line numbers
or document dates, identifies the implementation under review.

The following assessment covers each chapter. Existing source links and IDs remain
useful; no translated copy or second function inventory is needed.

| Curated evidence | Enduring finding and application | Qualification / owner |
|---|---|---|
| [00: conventions](legacy-refactorizacion/00-convenciones.md) | Names, units, thermal selectors, file/index conventions and function states route targeted inspection. | Row-count filtering and mutation differ by function; verify each producer/consumer. An imported alternate path is not the active callback path. |
| [01: overview](legacy-refactorizacion/01-el-sistema-en-una-pagina.md) | Three input families (weather, module, measurements), three output families (annual, curves, comparison), dependency leads. | `pvlib 0.11.0` describes the analysis machine, not an established historical runtime. Claims that physics is sound are interpretations, not scientific verification. |
| [02: data history](legacy-refactorizacion/02-historia-del-dato.md) | S0–S8 transformation chain, mutation and file side effects identify boundaries and ordering. | Backend is concerned with source acquisition and S1–S7 calculations; Dash presentation is evidence, not a migration target. |
| [03: contracts](legacy-refactorizacion/03-contratos.md) | C-01–C-06 document assumptions of existing producers/consumers; C-07 identifies missing boundaries. | These are descriptive implicit contracts. Proposed normalization, named-sheet lookup and module/measurement checks deliberately change behavior and need separately tested profiles. C-04 stores include result dictionaries, despite its generalization that they transport only paths/small parameters. |
| [04: inventory](legacy-refactorizacion/04-inventario.md) | Stable function IDs and external-module section enable selective retrieval. | Main 109-function list excludes external weather/POA functions. Counts and reachability are static, not evidence of successful runs or full coverage. |
| [05: duplication and disconnection](legacy-refactorizacion/05-lo-que-no-sirve.md) | Repeated PE, curve, summary and module-two paths identify candidate shared kernels. | Similarity does not establish equivalence: compare effective arguments, grids, labels, failure modes and consumers before unification. Do not delete frozen legacy code. |
| [06: defects](legacy-refactorizacion/06-lo-que-esta-roto.md) | B-01–B-13 are concrete characterization leads; B-04/B-06/B-07/B-08/B-09 affect backend behavior. | Its execution row is explicitly empty. Its heading says four data-corrupting defects but lists five. Preserve each defect independently; do not treat the proposed patches as approved scientific changes. |
| [07: missing work](legacy-refactorizacion/07-lo-que-falta.md) | Distinguishes never connected, presently unreachable, broken and absent functionality. | A modern API/test scaffold now exists. Legacy captures, isolated runs and particular numerical ports must be assessed from actual artifacts, not this historical absence list. |
| [08: report-to-code](legacy-refactorizacion/08-tesis-a-codigo.md) | Conceptual map of annual, I–V, correction and bootstrap paths; identifies limitations of the annual evidence. | Workbook values and campaign details are collaborator-reported observations. Original workbook/report are unavailable here; no empirical replay or independent confirmation follows from this chapter. See discrepancies below. |
| [09: proposed refactor](legacy-refactorizacion/09-refactor-propuesto.md) | Reuse pure calculations, explicit boundaries, dimensions as data, and separation of presentation. | Its intended target is a cleaned Dash application. Current policy selects Python/FastAPI/Next. Function-count/line-count targets and hypothetical coverage are not reproduction gates. |
| [10: pending decisions](legacy-refactorizacion/10-decisiones-pendientes.md) | D-01–D-08 identify irradiance, coefficients, M2N, grids, workbook, RNG, tolerances and preset issues. | Recommendations remain proposals. Preserve selected legacy behavior in a named compatibility profile; review corrections independently. Refer to IDs in chapter 10 (README examples do not consistently use the same numbering). |
| [11: starting plan](legacy-refactorizacion/11-por-donde-empezar.md) | Independently freeze outputs before replacement; manual module and saved weather can bypass missing live sources. | The suggested full helper import needs Dash/plotting dependencies and source inspection. Its minimal harness and proposed sample tolerances are not an executable baseline. Unknown historical dependencies constrain historical claims, not all fresh controlled captures. |
| [Diagrams](legacy-refactorizacion/diagrams/) and index | Useful original data-flow, file-bus, combination and measurement locators. | Diagram statements such as “all paths covered” describe a proposed design outcome. Current implemented/proposed paths are maintained in the canonical transformation diagrams. |

## Capability-to-implementation inventory

Scope is the observed legacy backend, including broken paths that require explicit
compatibility or correction decisions. Browser controls, Plotly styles and Dash
stores explain callers; they are not numerical backend requirements. A captured
kernel with synthetic conditions establishes controlled software behavior, not
the original campaign or a successful dashboard run.

| Stable capability | Curated / raw source boundary | Inputs, outputs and dependencies | Modern owner and current evidence / blocker |
|---|---|---|---|
| `module_record` | S0/S4, C-06; F-038–040 `Placa_Prueba`, `Placa_D1`, `Placa_D2` | Ordered 11 nameplate fields → mapping; numerical constants added. Workbook selector reads missing `Libro1.xlsx`. | Fetcher preserves raw record/order/units; model owns coefficient interpretation. Manual records allow capture without catalog. B-06 preset discards every supplied field. Catalog edition/hash/license remain missing. |
| `weather` | S1, C-01; `Primer_Funcion_Clima.Clima:64–183`, dashboard `clima:853–936` | Site/year/interval → frames and metadata; pvlib PSM4/PSM3, credentials, current-date timezone lookup. | Fetcher owns explicit acquisition, original response, versioned immutable snapshot and source-only normalization. No captured response is present. Obtain reviewed raw response/time metadata or supplied historical snapshot before annual replay. |
| `poa` | S2; `Posicion_Solar.Solar_pos:36–114`, `Solar_pos_e:116–194` | Weather/site/orientation → in-place `Poa_*` additions; pvlib, timezonefinder. | Model owns geometry/transposition, orientation assumptions and time interpretation. Separate pure replacement requires inspected timestamp alignment and snapshots. Default tilt/azimuth, `Day` semantics and air-mass behavior require review. |
| `thermal` | S3; F-033–035 `Temperature_sandia:785–800`, `Temperature_feinman:805–814`, `Temperature_NOCT:817–825` | `Poa_global`, `temp_air`, wind plus selected parameters → `Tsandia`, `TFeinman`, `NOCT` mutation; pvlib/NumPy. | `thermal.calculate_thermal` and `thermal_contracts.py` implement captured Faiman/NOCT point profiles: four parameter cases × five synthetic points, 16 focused tests and byte-identical original replay. Original mutation/return/failure evidence is retained; modern immutable/validated boundaries are deliberate differences. Sandia selector/length captures and actual-weather/empirical validation remain pending. |
| `annual_electrical` | S4; F-044–051 `Factor_Idealidad`, `PE*`; C-02/03 | Module + POA/thermal series → named electrical series and parameters. CEC fit/PySAM, De Soto, custom translation, filtering/cleaning. | Model owns parameter derivation/equations; application orchestrates; file I/O stays in adapters. Requires captured effective inputs, each supported thermal combination and module branch. No annual parity follows from detailed I–V parity. |
| `annual_summary` | S5; F-052 `resume_df:3100–4149`, F-053 `resume_IV:4675–5603` | Annual frames/selection → extrema and curve-condition rows with original ordering/ties/labels. | Model/application summary owner, pending port. Synthetic annual frames can characterize B-04 wrong Voc and B-07 `round(dict, 2)` failures without original weather. Compatibility summaries and corrected summaries need separate identities. |
| `iv_r` | S6, F-058 `IV_R:4268–4368`; dashboard `electric_parameters:4182…` PE branch | Ordered legacy module + condition table including comparison values → CEC fit, De Soto values, 100-point Lambert W curve, MPP and rounded error table. | `model.py`, `compatibility.py` and `application.reproduce_legacy_iv` implement `legacy-iv-r-v1`. Two independent module captures/six conditions/600 points pass stage and final comparisons; replay/limits in [reproduction](reproduction.md). Capturing the helper does not cover S5 condition generation, other curve variants or dashboard wiring. |
| `iv_r_variants` | S6, F-059–061 `IV_R1`, `IV_R2`, `IV_R_VE` | Module/conditions → curves/tables. Module-two variants and user-specific conditions have distinct effective fit arguments/return schemas. | Model can reuse proven numerical kernels only after preserving each profile. VE forces gamma `-0.36`; IV_R uses supplied `deltha`. No automatic parity transfer across variants. |
| `measurement_comparison` | S6, C-05; F-062–064 `IV_CI`, `IV_sim`, `IV_CI2`; dashboard CI branches | Measurement workbook (`Info` + positional curve sheets), module → measured/simulated curves, errors; pandas/openpyxl/fit/solver. | Fetcher preserves original workbook and sheet/record identities; model owns sensor averaging, fitting and comparison conventions. Workbook, permissions and module linkage missing. B-09 float−list and B-10 unwritten CSV need failure captures/explicit correction decisions. |
| `correction` | S7, F-070–080 `IV_CI_cor`, `Rs_e`, `Temperature_coeffs`, `correction_IV`, `correction_IV_s`, `minimos*` | Measured curves/conditions/target/module → fitted coefficients, corrected curves and comparison tables. | Model owns correction/fitting/extrapolation, evaluation owns reported errors. M2/M2N formulation, fit/target provenance, grids and workbook need branch-specific capture. Alternative F-076 `get_corrected_IV_P2` is uncalled, not default authority. |
| `representative_curve` | S7, F-083–085 `Bootstrap`, `Bootstrap2`, `Comprobacion` | Ordered corrected curves → stochastic representative curve/statistics/tolerance table; NumPy legacy RNG, SciPy trimming, 3,000×12 resampling. | Evaluation owner, unimplemented. Capture RNG implementation/state and all source lengths/order before any deterministic alternative. Legacy truncates to shortest curve; no implicit modern truncation/resampling is acceptable. ±3% is campaign comparison policy, not software-parity tolerance. |
| `alternate_historical_kernels` | Imported `CurvaIV.IV` and `Parametros_Electricos.*`; ch04 external list | Separate Newton/100-point/hardcoded-conditions and alternate annual equations. | Historical evidence, no calls from the traced dashboard aliases. Do not use these as substitute oracles for active helpers. If selected for a distinct compatibility use case, capture and name separately. |
| `legacy_io_and_presentation` | C-02–05; F-032/036/037/041/043/068/069 and S8 | CWD glob deletion, CSV index inheritance, fixed upload overwrite, result dictionaries, duplicated callbacks. | Isolated capture wrapper records necessary side effects; modern application uses explicit run directories and returns data. No new frontend work until the full backend gate. Preserve legacy source bytes. |

## Consequential discrepancies checked against source

Static findings below were rechecked in the preserved source at task start
(`cef03c2b9f73558c715d489f499d55ce26824a4c`). Execution status is established by
capture manifests and tests, not by this section.

- **Annual irradiance:** `PE:1508` uses `Vmax_F * Imax_F`; `Imax_F:1499` already
  carries `G/1000`. Chapter 10 D-01's alternatives conflate `G/1000` with division
  by `1000/G` (algebraically equal) and do not establish an extra irradiance factor.
  The supplied summary also reports an inverse factor. Reconcile the selected
  full branch and primary equation before any scientific correction.
- **Coefficient semantics:** `IV_R:4273–4285` fits with percent-to-absolute
  conversions (`alpha/100 * Isc`, `beta/100 * Voc`), forced `monoSi`, `temp_ref=25`.
  `IV_R:4302` passes raw `Placa["alpha"]` to De Soto. Preserve both effective
  values in compatibility records; a normalized coefficient contract must not
  silently correct this inconsistency.
- **VE is a separate profile:** `IV_R_VE:4574–4586` forces gamma `-0.36`, while
  `IV_R` uses the supplied value. VE returns De Soto parameters; IV_R returns
  rounded relative-error columns. A common function name for “I–V” is insufficient
  to establish interchangeable behavior.
- **Thermal length and selector behavior:** Sandia loops only over the four
  recognized annual lengths. Faiman/NOCT repeat their calculation four times and
  have no length predicate. Sandia has six `a/b` entries but only four `deltaT`
  entries; selectors 5/6 index beyond the latter for accepted-length frames.
  These are compatibility/failure cases, not supported scientific parameter sets.
- **Preset and summary defects:** `Placa_Prueba:984–994` discards all arguments;
  `resume_df:3128–3129` reads `Vmax_F` for its Voc values; `:3267` and `:3524`
  call `round` on dictionaries. These corroborate B-06/B-04/B-07 statically.
- **Measurements and metadata:** `IV_CI_cor:5893…5960` reads `Info` by name and
  curve sheets by position, uses `Voc`, `Irrad1`, `Temp1`, `Temp2`, and averages
  sensors as `(T1 + T2)/2`. Chapter 08 later lists `Voc` among ignored fields,
  contradicting its own table and source. Preserve identifiers and mapping in a
  future adapter; no identity can be inferred from row position alone.
- **Campaign evidence:** chapter 08 reports 30 curves, CurveIDs 1–37 with gaps,
  irradiance 860–1024 W/m², sensors up to about 63 °C and 13 minutes. The supplied
  summary describes roughly twelve minutes and homogeneous conditions. Neither
  report supplies raw records here. The inclusion/exclusion criteria, raw
  sensor/curve pairing and applicability of homogeneity remain unverified.
- **Bootstrap:** `Bootstrap:8366…8388` truncates arrays to the shortest curve,
  then makes separate unseeded `np.random.choice` draws for voltage/current/power.
  A fixed seed proposal is insufficient unless the RNG algorithm, state, draw
  order, curve ordering and NumPy version are also controlled.
- **Callback identities:** the two `electric_parameters` and two
  `Voltaje_Corriente_Selector` definitions are decorated before reassignment.
  Source lookup by bare name loses one registered callable. Baseline identity
  includes function location/callback branch and effective arguments.

## Ordered remaining reproduction work

1. **Complete selected module/point capture profiles.** Preserve intermediate fit
   and De Soto parameters, exact grids, curves, return schemas and failures.
   Characterize IV_R module-two/VE differences before sharing their kernels.
2. **Complete thermal and capture annual-summary boundaries independently.** Faiman
   and NOCT point kernels are captured/compared; Sandia remains pending. Synthetic
   conditions/frames are sufficient for software characterization and expose
   Sandia selector/length behavior, B-04/B-07, ties, labels and missing columns.
   Label them synthetic; they do not replace original weather or measurements.
3. **Obtain source snapshots and settle time contracts for annual replay.** Need
   original weather response/metadata, interval/timezone/leap-day conventions,
   chosen POA/thermal inputs and catalog record if used. Manual module data avoids
   only the catalog blocker. Implement and compare S1-normalization → S2 → S3
   intermediates before claiming the S4 annual chain.
4. **Capture and port S4/S5 branches.** Enumerate seven thermal selections, one/two
   modules, source modes and callback conditions actually supported; preserve
   numerical cleaning, failures, ties and source-record count. Review annual
   coefficient/gamma interpretation separately from compatibility.
5. **Recover the original measurement workbook/report and permissions.** Verify
   sheet order, CurveID mapping, excluded curves, sensors/uncertainty and module
   identity. Then capture CI, M2/M2N, coefficient fitting and extrapolation at
   intermediate and final stages. Synthetic workbook tests cannot establish the
   reported empirical campaign.
6. **Capture representative-curve statistics with controlled original RNG state.**
   Separate compatibility truncation/draw order from any reviewed alignment,
   resampling, seeded-generator or confidence-interval changes.
7. **Close full backend gate before new frontend functionality.** All intended
   capabilities must have explicit supported input domains, source provenance,
   independent references and successful comparisons (including failure behavior),
   or an explicit reviewed scope exclusion. No silently untested branch, skipped
   comparison, missing record or unresolved material discrepancy can count as
   complete reproduction. Scientific, empirical and calibration gates retain
   their separate statuses.

When changing a row's status, update its implementation/contract, assumption and
transformation links, reference manifest, comparator/tests and reproduction
record together. Task command logs belong in the current ExecPlan; durable
ownership and evidence belong in the canonical documents.
