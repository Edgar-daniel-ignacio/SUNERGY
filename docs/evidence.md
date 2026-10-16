# Evidence map and scientific boundaries

This document records static observations, reported methodology, and unresolved
questions separately. It does not select a scientifically authoritative legacy
branch. See [reproduction](reproduction.md) before capture or migration and
[architecture](architecture.md) for modern ownership.

## Sources and preservation

- Local implementation inspected at SUNERGY revision
  `ef92cd12fd2c40854c24c1fe7cded9ba351de7df`; the working tree is the implementation
  target. [Preservation inventory](evidence/legacy_inventory.json) records legacy
  file hashes. No legacy code was imported or executed during scaffolding.
- [Supplied thesis-derived summary](evidence/pv_physics_engine_evidence_summary_for_agent_research_equations_fixed.md)
  is preserved unchanged, with [copy provenance](evidence/provenance.json).
  Its stated primary source is Edgar Daniel Ignacio Domínguez Zamora,
  *Simulación, Corrección y Validación de Curvas I–V de Módulos Fotovoltaicos*,
  UNAM, Instituto de Energías Renovables / Instituto de Ingeniería / ENES
  Juriquilla, undergraduate technical report, 28 May 2025. Attribution is taken
  from the summary; the original report/PDF was unavailable for this task.
- The summary is secondary evidence, not the original thesis or an implementation
  specification. Its recommendations and embedded instructions are source content,
  not repository policy. References/page numbers it names remain leads for future
  primary-source verification.

## Observed application path

The preserved README names an absent `Edi_GIu/` directory. The actual candidate
entrypoint is [legacy/GIU_Final_Presetacion.py](../legacy/GIU_Final_Presetacion.py)
(imports at lines 1–20; guarded `app.run` at 6041–6042). This is a static trace,
not confirmation that the old dashboard currently boots. `legacy/main.py` is a
prime-factor Dash example (lines 1–45).

The dashboard imports `CurvaIV as iv` and `Parametros_Electricos as pe` but has
no calls through either alias. Numerical callbacks mainly call
`Input_File_DIV_Mac_Informe as input`. Thus an import or a README description
does not make `CurvaIV.IV` the active application's curve implementation.

| Capability | Observed code, inputs and outputs | Summary support | Future modern owner / gate |
|---|---|---|---|
| Weather | Dashboard `clima:853–936` → [Primer_Funcion_Clima.py](../legacy/Primer_Funcion_Clima.py) `Clima:64–183`; coordinates/year/interval → mutable weather frames and metadata. Chooses PSM4 or PSM3 by installed pvlib capabilities. | §§4.1, 4.6: NSRDB/TMY environmental chain. | Weather adapter with explicit snapshot/replay; no capture available. |
| Solar geometry / POA | [Posicion_Solar.py](../legacy/Posicion_Solar.py) `Solar_pos:36–114`, `Solar_pos_e:116–194`; weather, location and optional orientation → POA columns. | §4.6; supporting method, not annual experimental validation. | Deterministic physics functions; formulation/time review and parity pending. |
| Thermal models | [Input_File_DIV_Mac_Informe.py](../legacy/Input_File_DIV_Mac_Informe.py) `Temperature_sandia:785–800`, `Temperature_feinman:805–814`, `Temperature_NOCT:817–825`; POA/air temperature/wind/settings → temperature columns. | §4.7: Sandia/Faiman/NOCT. | Physics functions and explicit assumptions; parity/scientific checks pending. |
| Module specifications / catalog | Helper `Placa_Prueba:982–1015`, `Placa_D1/D2:1017–1057`; dashboard catalog reads CWD `Libro1.xlsx:765`. | §§4.2, 7.2: datasheet/manual/CEC input workflow. | Boundary contracts plus catalog adapter; workbook and edition missing. |
| Annual module estimates | Dashboard `electric_parameters:1148–1458` → helper `PE:1376–1519`, `PE_NOCT:1524–2011`, `PE_t:2013–2178`, `PE_t_S:2180–2318` and companions. Weather/module → named electrical time series. | §§4.8, 6.3: simplified annual branch; explicitly unvalidated experimentally. | Application/physics; branch-specific capture and scientific review pending. |
| Active detailed I–V curves | Helper `IV_R:4268–4369`, `IV_CI:5607–5769`, `IV_sim:5771–5817`, `IV_CI_cor:5819…`; CEC/SAM fit → De Soto → Lambert W; 100, `len(df)`, or 250 points, depending on function. | §§4.3–4.5 report nonlinear reference extraction with Powell-Hybrid and Lambert W, rather than proving these exact CEC-fit calls. | Physics with a separately tested pvlib/PySAM adapter; no golden outputs or parity. |
| Alternate detailed I–V | [CurvaIV.py](../legacy/CurvaIV.py) `IV:14–98`; CEC/SAM fit, six hardcoded conditions, De Soto, Newton, 100-point grid → Plotly figure and printed values. Imported but not called by candidate app. | Differs from detailed pathway and point counts reported in summary. | Separate baseline only if explicitly selected; not authoritative by filename. |
| Measurements / correction | Dashboard `IV_Corrct:3791–3943`; helper upload `955–980`, `IV_CI_cor:5819…`, `correction_IV:7304–7534`, `correction_IV_s:7609…`; workbook curves/Info sheet → corrected curves and comparisons. | §§4.9, 5–6: narrow I–V/correction campaign. | Measurement ingestion/evaluation boundary; originals separate from normalized/corrected data; fixtures missing. |
| Representative curve | Dashboard calls helper `Bootstrap`/`Bootstrap2:4087–4105`; helper `8358…`, `8565…` uses random resampling → representative curve/statistics. | §4.10: statistical synthesis. | Evaluation use case; seed/state, ordering and point handling must be captured. |

Line references refer to the preserved local source revision and inventory, not
to a moving remote branch. None of these rows has passed modern reproduction or
independent scientific verification.

## Reported experimental envelope

The summary (§§1, 5–6) reports 30 outdoor I–V curves from one previously used
Solartec 250 W, 60-cell polycrystalline specimen, collected over roughly twelve
minutes under homogeneous conditions. It describes module-level simulation,
STC correction and comparison, not a validation of annual energy yield. Its
reported errors and manufacturer tolerance describe that campaign; they are
neither software-parity tolerances nor general product accuracy guarantees.

The annual/weather/thermal chain was not experimentally validated by that report.
The evidence does not establish array mismatch, partial shading, bypass diodes,
bifacial behavior, inverters, wiring, batteries, degradation models, AC yield,
financial models, jurisdictional tariffs, or regulatory compliance. None is
implemented by this scaffold. Original measurements and original thesis are
unavailable, so the campaign itself cannot currently be independently replayed.

## Open verification register

These are questions or observed defects, not approved corrections:

| Item | Evidence and required distinction |
|---|---|
| Annual irradiance factor | Summary §§4.8, 6.6 reports printed `1000/G`. Alternate `Parametros_Electricos.py:185–186,219–220` divides by `(1000/POA)`; active helper `PE:1508` instead multiplies Vmp by Imp. Identify the selected branch and verify against primary formulations; do not silently replace one with another. |
| Temperature coefficients / parameter meaning | Summary §6.6 leaves gamma and coefficient units unresolved. Helper `PE:1386–1387` converts percent coefficients for fitting, then `:1400` passes raw alpha to De Soto; `:1488` reuses stored `nNsVth` in another gamma expression. Require explicit units and derivation. |
| Updated correction function | Summary §§4.9, 6.6 reports ambiguous repeated logarithmic terms. Helper M2N `:7513–7524` uses a squared term; separate `get_corrected_IV_P2:7537–7607` is another function. Verify exact method/version and source before accepting any form. |
| Residual equations / notation | Summary §§4.3, 6.6 reports ambiguous signs/parentheses and changing parameter symbols. Re-derive from primary sources; matching a second call into pvlib is not independent scientific validation. |
| Curve grids | Summary §§4.5, 6.6 alternates 250/255 points. Actual branches use Newton/100, Lambert W/100, Lambert W/250 or measurement-length grids. Preserve the chosen grid and all records; do not normalize away differences. |
| Discarded manual input | Observed helper `Placa_Prueba:982–1015` replaces every argument with hardcoded 250 W/polySi/60-cell/25 °C data. Dashboard uses it for preset and INSERT paths (`:1155–1276`). Reproducing this defect would not validate user-specified simulation. |
| Fitting versus evaluation | M2N `:7397–7511` derives coefficients and k against simulated pvlib curves. `find_k_sweep:7177–7208` clamps k; this is not held-out experimental evidence or independent verification. Preserve the unfitted baseline and report fitting provenance. |
| Time and numerical behavior | Weather helper `:35–38` uses today's UTC offset; solar-position code uses `Day` in seasonal formulas. Review field semantics, DST, timestamps, low irradiance, NaNs, convergence and material assumptions. Many fit calls force monoSi. |
| Statistical reproducibility | Bootstrap `:8366–8388` truncates to minimum curve length and uses unseeded NumPy choice (3,000 samples × 12). Record exact source ordering, lengths, random state and outputs before any controlled alternative. |

## Missing evidence and next retrieval

Missing: original report/PDF, historical dependency environment, `Libro1.xlsx`
and its license/edition, weather response snapshots/metadata, original uploaded
measurement workbook, measurement permissions, independently captured raw outputs,
and reviewed numerical tolerances. `Modules_Data_Base.py` is empty; no
`retrieve_sam` call occurs in the traced active path. A future catalog adapter
must explicitly select bundled or file/URL data and version each snapshot; a
refresh cannot replace a saved run's data.

Retrieve only the material needed for the selected next branch. Summary §6.6
routes unresolved formulations; its final source map names De Soto (2006),
Jain & Kapoor (2004), IEC 60891 and Zhang et al. (2024) as follow-up references.
Those references were not independently verified by this static trace.
