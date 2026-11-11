---
title: Backend transformation lineage
role: Trace sources through the implemented kernels and observed legacy data chains
retrieve_when: Following a producer-consumer chain or changing a transformation boundary
read_scope: Relevant diagram and linked operation records; not the whole legacy inventory
authority: Diagrams explain named code paths, not execution coverage or scientific approval
verify: Check actual callers, branch conditions and the corresponding assumption and coverage entries
---

# Backend transformation lineage

Each diagram states whether it describes modern implementation or frozen legacy
source. A solid arrow records a transformation in that boundary, not proof that
every input/branch has executed. Modern coverage is owned by the [coverage map](legacy_backend_coverage.md);
meanings and equations are owned by [assumptions](assumptions.md).

## Implemented modern point calculations

```mermaid
flowchart LR
    snapshot["Local original snapshot<br/>source identity and expected hash"] --> fetch["fetcher.py<br/>verify bytes and map inspected fields<br/>retain source values and order"]
    fetch --> ivinput["compatibility.py<br/>explicit module, conditions and comparison inputs"]
    explicit["Direct supplied point request"] --> ivinput
    ivinput --> application["application.reproduce_legacy_iv"]
    subgraph iv["model.py — legacy-iv-r-v1"]
        application --> fit["IV-01 / IV-02<br/>CEC fit conversions and forced settings<br/>retain all six parameters"]
        fit --> translation["De Soto at supplied G / cell temperature<br/>raw-alpha behavior; Adjust omitted"]
        translation --> solver["IV-03<br/>seven solver metrics<br/>100 ordered voltage/current points"]
        solver --> errors["Five benchmark error metrics<br/>legacy denominator and table rounding"]
    end
    errors --> ivoutput["Validated result<br/>supplied/effective inputs, parameters, curves and table"]
    ivoutput --> api["Thin FastAPI compatibility endpoint"]
    thermalinput["thermal_contracts.py<br/>ordered points and explicit Faiman/NOCT parameters"] --> thermalapp["application.request_thermal"]
    thermalapp --> thermal["thermal.calculate_thermal — TH-02<br/>immutable point temperatures"]
    thermal --> thermaloutput["Validated profile, unit, IDs and temperatures"]
```

Source mapping ends before coefficient interpretation. The model owns
fit conversions, overrides, solver/grid and error meaning. Thermal is a direct
Python point use case; this diagram does not implement weather acquisition or an
annual workflow. The reserved general simulator remains unavailable.

## Observed legacy weather-to-electrical chain

```mermaid
flowchart LR
    %% #to-review: corrected weather/POA lineage and catalogue NOCT-to-fit-reference mapping; see WX-01 and IN-02.
    response["Clima / SmartNDH — S1, C-01<br/>weather frames by fetched length<br/>last response metadata"] --> poa["Solar_pos / Solar_pos_e — S2<br/>downstream length gate<br/>pvlib position and explicit/default orientation"]
    poa --> irradiance["Mutated NDH with POA columns"]
    irradiance --> temperature["S3 — TH-01 / TH-02<br/>selected thermal columns<br/>Sandia length/selector rules differ"]
    preset["Preset or manual producer<br/>IN-01: INSERT can discard supplied values"] --> module["C-06 module record"]
    catalog["Catalogue Average NOCT"] --> reference["Slot 9 named temp_ref — IN-02<br/>annual fit reference meaning unresolved"]
    reference --> module
    module --> annual["PE families — S4, AN-01<br/>fit and electrical time series<br/>branch-specific coefficient/cleaning behavior"]
    temperature --> annual
    annual --> summaries["S5 summaries/extrema<br/>labels, selections and errors"]
    summaries --> curves["S6 detailed curve branch<br/>IV_R / VE / CI families<br/>distinct settings, grids and returns"]
    annual --> output["S8 tables, plots and file consumers"]
    curves --> output
```

This is source lineage, not modern annual reproduction. Acquisition
can retain lengths that downstream consumers ignore. Unused manual seasonal
calculations can still require fields/fail, but the returned POA chain consumes
pvlib position. The catalogue temperature mapping and upstream preset/manual
behavior must remain visible before sharing a numerical kernel.

## Observed measurement, correction and statistical chain

```mermaid
flowchart TD
    %% #to-review: corrected upload preservation, effective/reported temperature, method/origin and statistical lineage; see EV-01.
    upload["Original workbook supplied by user"] --> rewrite["guardar_archivo<br/>rewrites Uploaded_.xlsx via pandas<br/>not byte preservation"]
    rewrite --> workbook["Info rows and positional curve sheets<br/>module/sensor linkage must be established"]
    workbook --> sensors["Voc, Irrad1, Temp1, Temp2"]
    sensors --> mean["Sensor mean temperature"]
    mean --> desoto["De Soto translation<br/>initial parameters at sensor mean"]
    desoto --> inferred["Voc-derived Tmod overwrite<br/>uses nNsVth / beta / irradiance ratio<br/>dimensional interpretation unresolved"]
    sensors --> inferred
    inferred --> measured["Measured-origin correction_IV<br/>dispatch M2 or M2N"]
    inferred --> simulation["IV_sim at inferred Tmod"]
    simulation --> simulated["Simulated-origin correction_IV_s<br/>dispatch M2 or M2N<br/>different fit grid / k strategy"]
    workbook --> measured
    mean --> metadata["Reported temperature metadata<br/>retains sensor mean"]
    measured --> comparison["Corrected curves and comparison tables"]
    simulated --> comparison
    metadata --> comparison
    comparison --> aggregate["Promedio aggregates result tables<br/>not sensor selection"]
    comparison --> bootstrap["Bootstrap / Bootstrap2<br/>minimum-length truncation<br/>separate random draws; current 3000 × 12"]
    bootstrap --> intervals["Comprobacion<br/>fixed n=30 / df=29 and t-based interval label<br/>statistical applicability unresolved"]
```

This representative source chain preserves three different temperature
roles and separates correction method from curve origin/fit strategy. It does not
replace the branch-specific code or prove statistical validity. The supplied
summary's reported bootstrap method differs from current source. Original
measurements, historical algorithm identity, RNG state and calibration/evaluation
lineage are still needed; see EV-01 and the original chapters 03/08/10.

## Verification boundary

Independent original-source captures feed the compatibility comparisons described
in [reproduction](reproduction.md). Schema checks, numerical reproduction,
scientific formulation checks, observations and calibration have separate evidence
requirements. Neither these diagrams nor current tests approve a disputed modeling
choice or the full backend.
