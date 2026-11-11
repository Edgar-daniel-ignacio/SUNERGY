# Modeling choices and transformation register

Start with the [capability and reproduction map](legacy_backend_coverage.md), then
follow the operation below to its owner. The [curated investigation](legacy-refactorizacion/README.md)
is the primary locator for legacy behavior; its proposals and reported workbook
observations remain supporting evidence. This register records current decisions
and unresolved questions, without copying the investigation or its inventory.
Read [evidence](evidence.md) for provenance and [reproduction](reproduction.md)
for capture commands, executed comparisons and tolerances. [Flowcharts](flowcharts.md)
show the boundaries. A compatibility choice is not an accepted scientific default.

For changes affecting an operation, update its contract, implementation, capture
coverage and this record together. Stable IDs below identify the decision, not a
claim of scientific or empirical acceptance. Missing fields/records fail boundary
validation; no imputation, interpolation, aggregation or calibration is implicit.

## Ownership and authorities

| Concern | Single owner | Meaning of the boundary |
|---|---|---|
| Original bytes and identity | `fetcher.py`; `catalog.py` retains its public snapshot reader | Load a local snapshot with an expected SHA-256; retain source and record identity. Refresh is explicit and creates another snapshot. Acquisition does no fitting or coefficient interpretation. |
| Explicit source normalization | `fetcher.py` | Parse/map declared source field names to `compatibility.py` contracts. Preserve source coefficient units, case IDs/order and original evidence; do not silently fill or convert values. |
| Compatibility input/output schema | `compatibility.py` | Pydantic owns `LegacyIVModule` and `LegacyIVRequest` for `legacy-iv-r-v1`; these source-shaped contracts are distinct from the reserved general simulator contract in `contracts.py`. |
| Modeling and parameterization | `model.py` | `fit_legacy_iv` owns percentage-to-absolute conversions and the legacy overrides. `solve_legacy_iv` owns translation, solver and grid. Typed numerical internals are independent of HTTP and plotting. |
| Thermal point profiles | `thermal.py` / `thermal_contracts.py` | `calculate_thermal` owns the captured Faiman and simplified NOCT equations. Pydantic owns explicit coefficient/point inputs and aligned results; no defaults, acquisition, missing-record filling or mutable NDH bus. |
| Use case and transport | `application.reproduce_legacy_iv`; `api.py` | Orchestrate one explicitly versioned compatibility request; expose results at `/api/v1/compatibility/iv-r`. General `/api/v1/module-iv` remains unavailable. |
| Source metadata / artifact locations | `config/sources.yaml` / `config/paths.yaml`, validated by `configuration.py` | Describe evidence and paths; neither selects model equations nor duplicates request schemas. |
| Runtime settings | Server environment, only where consumed | Credentials stay server-side. No network access is necessary for this local compatibility pathway. |
| Behavior / intended design / scientific support | Legacy source and independent captures / repository contracts and reviewed decisions / primary formulations and evaluation | These authorities answer different questions. Matching executable legacy behavior does not settle a scientific conflict. |

## IV-01 — Source coefficients and reference conditions

**Identity and domain.** Module nameplate points use A and V; source `alpha`,
`beta` and `deltha` use percent/°C. `deltha` is passed as the power coefficient,
not a voltage coefficient. Reference conditions in the selected legacy branch
are 1000 W/m² and 25°C; operating inputs are effective in-plane irradiance
and cell temperature, not ambient temperature. The supported domain and failure
rules are executable in `compatibility.py`; schema validity does not guarantee
that the numerical fit will converge.

**Evidence and transformation.** [C-06](legacy-refactorizacion/03-contratos.md#c-06--el-diccionario-de-placa)
and [D-02](legacy-refactorizacion/10-decisiones-pendientes.md) locate
[`IV_R`](../legacy/Input_File_DIV_Mac_Informe.py), lines 4268–4307. It fits with
`alpha_fit = alpha_source / 100 * Isc`, `beta_fit = beta_source / 100 * Voc`
and unconverted `deltha`. It then supplies the raw numerical `alpha_source`
to De Soto. The two alpha values have different physical units and must remain
separately identifiable. Official [CEC fit documentation](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.ivtools.sdm.fit_cec_sam.html)
requires A/°C and V/°C for alpha and beta, while gamma uses percent/°C.

**Decision, owner and verification.** `model.fit_legacy_iv` preserves both values
under `legacy-iv-r-v1`. A conversion applied once in the fetcher would change
this behavior and conceal its defect. Independently captured fit inputs,
parameters and off-reference conditions distinguish this defect from a porting
regression; a 25°C-only check cannot reveal it. A future corrected model must
have another model ID and its own scientific and empirical checks.

## IV-02 — CEC extraction followed by De Soto translation

**Evidence and effective choices.** The same `IV_R` body fits via
`pvlib.ivtools.sdm.fit_cec_sam`, forces `celltype='monoSi'` and `temp_ref=25`,
uses the first five returned parameters, and discards CEC `Adjust` from the
translation. Supplied material/reference metadata cannot be represented as
effective fit settings. This is a legacy hybrid pathway, not the full CEC model
or proof of the Powell-Hybrid extraction described in the supplied summary.
The [Dobos 2012 primary record](https://www.osti.gov/biblio/1043759) identifies
the CEC six-parameter extraction method; its abstract does not establish
SUNERGY's hybrid as accurate.

**Formulation audit.** Official [De Soto documentation](https://pvlib-python.readthedocs.io/en/v0.13.1/reference/generated/pvlib.pvsystem.calcparams_desoto.html)
defines `a_ref = n Ns Vth_ref` in V, `IL_ref`/`I0_ref` in A, and resistances
in ohms. Translation uses `IL = G/Gref * (IL_ref + alpha * (Tc-Tref))`,
`a = a_ref * Tk/Tref_k`, constant `Rs` and inverse-irradiance `Rsh`.
Thus the raw-alpha use in IV-01 is dimensionally inconsistent with its source
meaning. EgRef=1.121 eV and dEgdT=-0.0002677 K⁻¹ match the selected library's
CEC convention; changing them solely to a material lookup could invalidate the
fit's parameter convention. The official [CEC translation source](https://pvlib-python.readthedocs.io/en/stable/_modules/pvlib/pvsystem.html#calcparams_cec)
additionally scales alpha by `(1-Adjust/100)`; legacy omits that operation.

**Decision and checks.** `model.py` owns these explicit compatibility choices.
Capture the six fit results even though translation uses only five, plus each
case's five translated parameters. Responses retain `supplied_module`,
`supplied_cases`, exact `fit_inputs` and each case's `desoto_inputs`, alongside
effective choices. Repeated legacy condition labels retain their original
positions; a label alone is not unique record identity. Do not reinterpret `nNsVth` as dimensionless
ideality factor. Fit and translation agreement establishes compatibility only.
The [De Soto 2006 publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0038092X05002410)
reports validation of its model against NIST measurements; that does not validate
SUNERGY's altered coefficient chain. Main-paper full equations were unavailable
in this audit; re-derivation remains open.

## IV-03 — Solver, grid, equation and comparison metrics

**Behavior.** `IV_R:4318–4367` solves with Lambert W, samples exactly 100 ordered
voltages from 0 through calculated Voc, and obtains current at those voltages.
It reports five electrical metrics and a table using
`round(100 * abs(simulated - benchmark) / simulated, 2)`; the denominator is
the simulated quantity. Benchmark fields are comparison inputs, not fitting
evidence. Raw outputs must be retained before the legacy table rounding.
The unused inverse-voltage calculation uses a separate fixed current grid;
its existence and omission from the returned curve must remain visible in the
capture method. `CurvaIV.IV`, `IV_CI` and `IV_CI_cor` use different methods or
grids; IV_R coverage does not transfer to them. See curated D-04/D-07.

**Scientific checks and limits.** The [official single-diode equation](https://pvlib-python.readthedocs.io/en/v0.13.1/reference/generated/pvlib.pvsystem.singlediode.html)
gives the independently evaluable residual
`I - IL + I0*expm1((V + I*Rs)/a) + (V + I*Rs)/Rsh` in A. The primary
[De Soto 2007 erratum](https://www.sciencedirect.com/science/article/pii/S0038092X06001691)
corrects Eq. 6a to `Imp + Vmp * dI/dV|mp = 0`. Residual, endpoint and MPP
checks test numerical/equation consistency; they do not validate extraction,
thermal inputs or agreement with measurements. Quantity-specific software
tolerances belong to each capture manifest, not manufacturer power tolerance
or the campaign's percentage error. Exact ID/order/shape/unit checks accompany
numerical comparisons; no sorting or grid replacement is allowed.

An independent arithmetic audit of the six recorded cases in `iv_r/captured`
and `iv_r/captured_alternate` evaluated the residual and analytic implicit
derivative directly from stored parameters/points, without calling the modern
model or pvlib. Maximum absolute equation residual was below 4.0e-14 A;
maximum absolute MPP `dP/dV` was below 5.8e-7 A for the Windows captures. The
Linux alternate STC case later exceeded the unchanged 1e-6 A review target;
IV-04 preserves that unmet result. These finite-case observations
support numerical consistency of these stored curves only. They do not resolve
IV-01/IV-02, establish global solver behavior or constitute empirical evidence.

## IV-04 — Numerical platform identity

**Observed evidence.** Windows and Ubuntu original-source captures use identical
effective fit inputs but differ first in fitted parameters for the preset module.
MPP coordinates also differ for the alternate module. Each platform's original
execution matches the modern implementation under the existing thresholds, and
repeated original executions are byte-identical on that host. Raw references,
workflow/artifact provenance and the [difference report](evidence/iv_r_platform_comparison.json)
are linked from [reproduction](reproduction.md). No Windows output or acceptance
threshold was replaced or relaxed.

**Source audit and interpretation.** PySAM 7.1.0 uses SSC 303; the pinned
[6parsolve source](https://raw.githubusercontent.com/NatLabRockies/ssc/2025.4.16.r1.ssc.303/ssc/cmod_6parsolve.cpp)
invokes a nonlinear solve with maximum 300 iterations and tolerance 1e-7. That
residual criterion is not a per-parameter portability guarantee. pvlib 0.13.1's
[golden-section source](https://raw.githubusercontent.com/pvlib/pvlib-python/v0.13.1/pvlib/tools.py)
compares candidate powers and stops at interior-point separation below 1e-8 V.
This does not prove MPP coordinate accuracy to 1e-8 V. In the alternate STC case,
the logged current shift implies a voltage shift about 1.05e-7 V and a quadratic
power change about 2.85e-14 W, roughly half one ULP at 400 W. Thus power rounding
can leave the optimizer's coordinate branch sensitive while Pmp agrees.
These mechanisms explain plausible sensitivity; exact compiler/libm causality
has not been established. Local SSC reports version 303, build
`Windows 64 bit Visual C++ Aug 8 2025 12:37:54`, native DLL SHA-256
`defd47245c271abdc20a18bc827ea0ad0a833794a6000f3d07d28a700d45ac4d`.
Linux environment/package identities are captured; its separate native build/hash
has not yet been recorded.

**Decision and owner.** `replay.iv_capture_names` selects the fixed reference pair
by OS and architecture, without checking which values pass. Unsupported environments
fail the reproduction gate explicitly; general calculation availability is separate.
Same-platform software compatibility, cross-platform numerical invariance and
scientific/empirical accuracy remain different claims. Future solver/library/native
build changes require a fresh independent capture and discrepancy review.

**Unmet scientific audit target.** The independent Linux `STC-alt` reference has
`abs(Imp + Vmp*dI/dV)` about 1.118e-6 A, above the selected strict `<1e-6 A`
target. The target was retained, with `target_met: false` in the original-source
audit report. Modern numeric outputs and audit outcome reproduce this limitation.
The single-diode residual check still passes separately at 1e-10 A. A green
characterization/reproduction suite therefore does not mean this scientific
target passed; API capability status explicitly reports it unmet. This is an
unmet solver audit target, not proof of a physical defect or a justification for
a new accepted accuracy threshold. A power-precision criterion would require
separate derivation/review and must supplement this preserved result.

## IN-01 — Preset and manual module paths

`Placa_Prueba:982–1015` replaces every supplied argument with fixed 250 W,
30.12 V, 8.30 A, 37.85 V, 8.65 A, 0.01%/°C alpha, -0.31%/°C beta,
-0.5%/°C gamma, 60 cells, 25°C and polySi. `Placa_D1/D2` instead retain
supplied values. Curated D-08 proposes an explicit preset, but that proposal
does not turn discarded manual input into correct behavior. An IV_R request
uses an explicit module; it does not reproduce all dashboard selector branches
or `Placa_Prueba` argument-discard behavior. Capture those producer paths
separately before claiming end-to-end reproduction. Input provenance belongs
to acquisition; choosing a fixed preset belongs to the application/model.

## TH-01 — Sandia thermal selection

`Temperature_sandia:785–800` mutates `Tsandia` only for frames with legacy
accepted lengths. It evaluates `Tm = E*exp(a+b*wind) + Ta`, then
`Tc = Tm + E/1000*deltaT`. Its a/b arrays have six entries, while deltaT has
four; applicable selectors 5/6 fail by indexing. The original
[Sandia SAND2004-3535 report](https://www.osti.gov/servlets/purl/919131),
thermal section pp.17–19, Eqs.11–12 and Table1, supports these equations
and identifies module/mount and wind-height dependence. Its fifth/sixth
deltaT values are 3°C/13°C. This supports a proposed correction, not silent
compatibility repair. Sandia is unavailable in the modern thermal boundary;
its selector/length regimes and failures need separate captures before a
compatibility or corrected profile can be selected. The thermal model owns
parameter selection and cell/back-surface distinction; the fetcher owns
observed wind and metadata. Neither the implemented Faiman/NOCT kernels nor
their captures establish Sandia or annual thermal reproduction.

## TH-02 — Faiman and simplified NOCT

**Legacy and modern transformations.** `Temperature_feinman:805–814` passes
`Poa_global`, air temperature, wind and explicit U0/U1 to pvlib Faiman;
the equation is `T = Ta + E/(U0 + U1*wind)`. `Temperature_NOCT:817–825`
uses `T = Ta + ((TNMOT-20)/800)*E`, reading wind without using it.
The immutable point implementations are
[`thermal.calculate_thermal`](../backend/src/sunergy/thermal.py), selected by
`legacy-faiman-v1` or `legacy-noct-v1` through
[`thermal_contracts.py`](../backend/src/sunergy/thermal_contracts.py).
[`application.request_thermal`](../backend/src/sunergy/application.py) exposes
the validated Python use case without requiring an HTTP route.
E is total incident POA irradiance [W/m²], Ta and T are °C, and wind is m/s.
U0 is W/(m² K); U1 is W/(m² K (m/s)); TNMOT is °C. Parameter interpretation
and calculation belong to the thermal model. Source normalization must supply
these units explicitly; no fitting, imputation or time interpretation occurs.

**Supported boundary and decisions.** Every ordered point requires a unique
record ID, finite nonnegative E/wind and Ta above absolute zero. Faiman
requires explicit finite positive U0/U1 and a finite positive combined loss
factor. NOCT requires explicit TNMOT >20°C. These are restrictions of the
supported modern boundary, not new claims about the full mathematical or
scientifically valid domain; in particular, zero U1 is excluded by this
profile rather than proved unphysical. Outputs must be finite and above
absolute zero. The original functions return `None`, mutate an NDH frame,
append `TFeinman`/`NOCT`, and repeat each calculation four times without a
length predicate. Capture retains these operations, while the modern point
boundary returns ordered values without mutation. Legacy missing irradiance
raises `AttributeError`; the modern missing field fails Pydantic validation.
These explicit boundary changes are separate from numerical compatibility.

**Evidence and verification.** The
[controlled capture](../tests/fixtures/legacy/thermal/README.md) executes both
original AST bodies independently in the isolated locked environment. Four
parameter cases × five synthetic points retain original input columns,
record order, unrounded temperatures, return/mutation behavior and missing-field
failures. Baseline values 25/6.84 and 43°C come from the legacy UI; alternate
coefficients exercise explicit callers. They are not calibrated defaults.
An isolated recapture produced byte-identical `outputs.json` on the capture
host. [Thermal tests](../backend/tests/test_thermal.py) compare kernels using
`abs(actual-reference) <= 1e-12°C + 1e-12*abs(reference)`, reject a 0.01°C
perturbation and reordered IDs, and exercise zero irradiance, reference
conditions, wind cooling/NOCT wind independence, invalid domains and overflow.
The [manifest](../tests/fixtures/legacy/thermal/captured/manifest.json) pins
source, wrapper, inputs, outputs, environment and tolerance provenance.

**Scientific support and limitations.** Official
[Faiman documentation](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.temperature.faiman.html)
requires wind at the coefficient estimation height and identifies context-specific
origins for its default loss factors. No universal U0/U1 or mounting choice
follows. The simplified NOCT equation is dimensionally coherent and returns
TNMOT at E=800 W/m², Ta=20°C; it is not interchangeable with every NOCT/NMOT
model. Labels do not establish measured cell versus module temperature.
These captures cover the point kernels and inspected wrapper behavior, not
annual weather orchestration, measured thermal accuracy or calibration.

## AN-01 — Annual irradiance, power and missing-record behavior

Curated S2–S5/C-01–C-03 and D-01 route to `Solar_pos`, `PE*` and summaries.
The selected `PE:1488–1510` uses `Pmax = Vmax * Imax`; current already includes
`G/1000`. Therefore the two generic expressions `G/1000` and `1/(1000/G)`
are algebraically equivalent where defined, but that alone does not prove
equivalence of whole annual branches. `PE` also stores `nNsVth` [V] in `AF`,
then computes `gamma = AF * k * Tk / q` [V²] before using it in the
dimensionless factor `1 + gamma*log(G/1000)`. This is a dimensional mismatch
under the library's documented parameter meaning. The branch applies the
power coefficient to Vmp and replaces selected non-finite results with zero.
These operations need separate compatibility capture and reviewed corrected
formulations, not a global irradiance-factor fix.
Accepted frame lengths can exclude leap-year or incomplete records.
Preserve that behavior as evidence; any repaired missing-record policy needs
explicit versioning. Annual outputs remain outside implemented IV_R coverage.

## WX-01 — Weather time, POA and effective irradiance

`Primer_Funcion_Clima.obtener_utc_de_coordenadas:26–38` uses today's UTC
offset; `Posicion_Solar.Solar_pos:36–114` combines pvlib position with manual
seasonal terms using `Day` and a legacy default orientation. A raw weather
snapshot is an acquisition artifact. Time-zone interpretation, irradiance
transposition, spectral/reflection assumptions and thermal modeling are
model operations. They must not be hidden in source normalization. A future
weather boundary must preserve timestamps/intervals, DST/leap-day policy,
wind height, irradiance basis and source metadata. No annual snapshot was
provided, and a point IV_R capture does not audit this chain.

## EV-01 — Correction, measurements and bootstrap

The curated [thesis mapping](legacy-refactorizacion/08-tesis-a-codigo.md)
reports examination of a real 30-curve workbook, including 13-minute timing,
860–1024 W/m² irradiance and seven omitted CurveIDs. The preserved summary
reports roughly twelve minutes. These are reported observations from different
evidence artifacts; the original workbook, its hash, exclusion criteria,
permissions and report are absent here. Do not overwrite one account with
the other or treat them as a locally replayed campaign.

`correction_IV:7304–7534` has an M2N branch with a squared log term;
`get_corrected_IV_P2` is another, unconnected implementation. No IEC 60891
conformance is established without the exact edition/formulation and test
conditions. `Temperature_coeffs` and `find_k_sweep` fit against simulated
curves, so their success is not held-out measurement validation.
`Bootstrap:8358…` truncates to the shortest curve and independently resamples
voltage/current/power with NumPy global randomness (3000 × 12 samples).
Capture inputs/order and RNG implementation/state before changing the seed,
alignment or estimator. A controlled seed supports a reproducible new
experiment; it does not recreate an unknown historical draw.

## Assessment and next scientific work

| Gate | Present evidence | What remains |
|---|---|---|
| Boundary validity | Executable Pydantic contracts and explicit ownership | Branch-specific source/measurement/weather boundaries as those paths migrate. |
| Selected legacy reproduction | See current manifests, tests and [reproduction record](reproduction.md) | Complete the [coverage map](legacy_backend_coverage.md); no full-backend claim. |
| Scientific verification | Checked coefficient units, selected equations, primary Sandia thermal formulation and De Soto MPP erratum | Independent extraction/formulation review, domain/limiting tests, reviewed corrected model and model selection. |
| Empirical agreement | Supplied campaign descriptions only | Original records, uncertainty, exclusion criteria and independent comparisons. |
| Calibration | Legacy fitting operations identified | Baseline retention, fitted identities/bounds/objective, fit-data provenance and held-out evaluation. |

Sources above were accessed on 2026-11-10. Official stable pvlib pages resolved
to 0.16.1 during the audit; explicitly versioned 0.13.1 pages establish the same
listed coefficient/equation semantics, not historical environment identity.
The capture manifest and lock establish the actual executed library versions.
The 2018 SAM technical-reference PDF could not be retrieved from the cited
NREL host (DNS failure); it was not used as formulation evidence.
