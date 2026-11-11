---
title: Modeling choices and transformation register
role: Operation-level meanings, conversions, assumptions, support and unresolved decisions
retrieve_when: Changing parameter interpretation, an equation, defaults, fitting or time and RNG semantics
read_scope: Named operation and its direct source and implementation dependencies
authority: Explicit compatibility decisions and pending scientific interpretation; not blanket model approval
verify: Check exact source branch, units, primary formulation and independent evidence for the proposed change
---

# Modeling choices and transformation register

Each operation records meaning/units, source behavior, modeling interpretation,
owner and verification limits. The [legacy audit](legacy_backend_coverage.md) owns
cross-chapter findings; [architecture](architecture.md) owns component/configuration
placement. The [evidence assessment](evidence.md) distinguishes author reports,
source execution, scientific formulations and observations. No entry is an accepted
scientific default merely because it is documented.

## IV-01 — Source coefficients and reference conditions

**Meaning and source.** Nameplate current/voltage are A/V; source alpha, beta and
deltha are labeled percent/°C. `IV_R:4268–4307` fits with
`alpha_fit = alpha_source/100*Isc`, `beta_fit = beta_source/100*Voc` and unconverted
power coefficient deltha. It then supplies the raw alpha number to De Soto,
which expects A/°C. These effective values must remain distinct. [Versioned CEC
fit documentation](https://pvlib-python.readthedocs.io/en/v0.13.1/reference/generated/pvlib.ivtools.sdm.fit_cec_sam.html)
defines the absolute alpha/beta and percent gamma inputs.

**Choice, owner and coverage.** `model.fit_legacy_iv` preserves the fitting
conversion and `solve_legacy_iv` preserves raw-alpha translation under
`legacy-iv-r-v1`. The fetcher preserves source values instead of silently repairing
them. Off-reference captured conditions expose this inconsistency; reference-only
agreement cannot validate it. A corrected coefficient chain requires separate
versioned behavior and scientific/empirical review.

## IV-02 — CEC extraction followed by De Soto translation

**Behavior.** IV_R forces monoSi and 25 °C for fitting, then uses five of six fitted
parameters with De Soto, omitting CEC Adjust. This hybrid is neither a complete
CEC model nor proof of the report's described extraction procedure. Source
material/reference values remain supplied metadata, not effective fit choices.
`model.py` owns the chain; responses retain supplied module/cases, exact effective
fit/translation inputs and all six fit results.

**Formulation and limits.** [De Soto documentation](https://pvlib-python.readthedocs.io/en/v0.13.1/reference/generated/pvlib.pvsystem.calcparams_desoto.html)
defines a_ref=n*Ns*Vth_ref in V, IL/Io in A and resistances in ohms. It translates
`IL=G/Gref*(IL_ref+alpha*(Tc-Tref))`, a with absolute temperature, constant Rs and
inverse-irradiance Rsh. EgRef=1.121eV/dEgdT=-0.0002677K⁻¹ follow the fitted CEC
parameter convention; material-specific replacement is not automatically valid.
The [CEC translation](https://pvlib-python.readthedocs.io/en/v0.13.1/_modules/pvlib/pvsystem.html#calcparams_cec)
also applies Adjust. Do not reinterpret nNsVth as a dimensionless ideality factor.

The [Dobos extraction record](https://www.osti.gov/biblio/1043759) and [De Soto
publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0038092X05002410)
support their stated methods, not SUNERGY's altered chain. Full original-paper
re-derivation and independent extraction verification remain open. Captured fit
and translation agreement establishes compatibility only.

## IV-03 — Solver, grid and comparison meaning

IV_R solves with Lambert W, evaluates 100 ordered voltages from 0 through calculated
Voc, and returns curve/MPP plot data plus five error metrics. The library supplies
seven single-diode metrics; the modern response retains all seven. The error table
uses `round(100*abs(simulated-benchmark)/simulated,2)`, with simulated values in the
denominator. Benchmark values are comparison inputs, not necessarily observations.
The unused inverse grid is retained in capture evidence but omitted from the modern
returned numerical boundary. Other curve functions use different methods/grids.

The [single-diode equation](https://pvlib-python.readthedocs.io/en/v0.13.1/reference/generated/pvlib.pvsystem.singlediode.html)
gives residual `I-IL+Io*expm1((V+I*Rs)/a)+(V+I*Rs)/Rsh` in A. The [De Soto
erratum](https://www.sciencedirect.com/science/article/pii/S0038092X06001691)
gives the MPP condition `Imp+Vmp*dI/dV=0`. Direct arithmetic can check numerical
consistency; it does not validate coefficient extraction, temperature inputs or
agreement with measurements. Comparison limits belong to capture manifests, not
manufacturer tolerances or reported campaign errors.

## IV-04 — Numerical platform identity

#to-review — IV-04 changes the earlier treatment of the MPP target: it is a limited developer diagnostic, not an approved scientific accuracy criterion.

Original Windows/Linux captures have identical effective fit inputs but small
fit/MPP-coordinate differences. `replay.iv_capture_names` chooses fixed references
by captured OS/architecture, with no numerical fallback. Source/environment
identity and unchanged quantity limits establish selected same-platform
compatibility; they do not establish platform-invariant output.

The retained [platform diagnostic](evidence/iv_r_platform_comparison.json) records
source differences and an unmet selected MPP stationarity target. That target is
an agent-selected finite-case diagnostic, not a collaborator-approved scientific
accuracy standard or a production prerequisite. Its failed observation remains
visible; neither matching it nor passing characterization tests approves the
model. Detailed experiment/native-build history belongs in the task record, not
in standing model acceptance.

## IN-01 — Preset and manual module identity

`Placa_Prueba:982–1015` returns fixed 250 W/polySi/60-cell/25 °C data regardless of
arguments. A declared preset is valid functionality; silently discarding INSERT
manual values is a separate defect. `Placa_D1/D2` retain supplied values. The
current IV_R request uses explicit module input and does not reproduce those
upstream selector/producer paths. Fetching preserves original identity; selecting
a preset belongs to application/model behavior.

## IN-02 — Catalogue NOCT versus fit reference temperature

#to-review — IN-02 adds a consequential interpretation conflict: catalogue NOCT becomes the annual electrical fit reference temperature.

Dashboard `render_content:969–1080` places `Average NOCT` in record slot 9;
`Placa_D1/D2:1017–1057` call it `temp_ref`; annual `PE:1390` passes it to CEC fitting.
Detailed IV_R instead forces 25 °C. Source field identity, nominal operating thermal
temperature and electrical fit reference temperature are distinct meanings. The
mapping is statically confirmed; actual workbook values/edition are unavailable.

Preserve the source field through acquisition and expose this interpretation at
parameterization. Do not silently relabel NOCT as STC or correct the annual fit
while claiming structural parity. Producer-specific capture and catalogue review
are needed before an accepted alternative. No modern catalogue adapter exists.

## TH-01 — Sandia temperature and selector domain

#to-review — TH-01 narrows the earlier selector-failure claim to distinguish exposed UI values from direct helper inputs.

`Temperature_sandia:785–800` computes module `Tm=E*exp(a+b*wind)+Ta`, then cell
`Tc=Tm+E/1000*deltaT`, only for four accepted frame lengths. The a/b arrays contain
six entries but deltaT four. `Sandia_options:762–783` exposes selectors 1–4; direct
helper or externally supplied 5/6 need separate failure characterization. Missing
POA can fail before any temperature result.

[Sandia SAND2004-3535](https://www.osti.gov/servlets/purl/919131), pp. 17–19,
Eqs. 11–12/Table 1, supports the formulation and mounting/wind-height dependence.
Its additional deltaT values are evidence for a proposed correction, not permission
to change compatibility. Modern Sandia/annual integration remains unimplemented.
The model owns parameter/cell-versus-module interpretation; acquisition preserves
observed wind and metadata.

## TH-02 — Faiman and simplified NOCT

The supported `thermal.calculate_thermal` point profiles retain Faiman
`T=Ta+E/(U0+U1*wind)` and legacy NOCT `T=Ta+((TNMOT-20)/800)*E`.
E is incident POA W/m², temperatures are °C and wind m/s. U0 is W/(m²K), U1 is
W/(m²K(m/s)); NOCT ignores wind. Explicit parameter inputs are not calibrated or
universal defaults. [Faiman documentation](https://pvlib-python.readthedocs.io/en/v0.13.1/reference/generated/pvlib.temperature.faiman.html)
requires wind at the coefficient-estimation height.

`thermal_contracts.py` requires ordered unique records, finite nonnegative E/wind,
physical ambient temperatures, positive explicit U0/U1 or TNMOT>20°C. These are
supported-boundary restrictions, not proof that zero U1 or every excluded value is
unphysical. The original Faiman/NOCT helpers mutate frames, return None and repeat
four times without Sandia's length predicate; modern results are immutable.
[Captures](../tests/fixtures/legacy/thermal/README.md) preserve those differences.

The four parameter cases/five synthetic points establish numerical point-kernel
coverage. Reference/zero-irradiance/wind checks support equation consistency, not
measured cell temperature, mounting applicability or annual reproduction. The
simplified NOCT expression is not every NOCT/NMOT model.

## AN-01 — Annual electrical parameters and missing records

`PE:1488–1510` computes Pmax=Vmax*Imax; current already contains G/1000.
G/1000 and division by 1000/G are algebraically equal where defined, but that does
not prove equivalence of full annual branches. PE stores nNsVth[V] in AF, then
forms AF*k*Tk/q[V²] before a dimensionless logarithmic factor; it also uses a
power-coefficient field in Vmp and replaces selected nonfinite values with zero.
These require branch-specific capture and reviewed interpretation.

Accepted downstream frame lengths can omit leap-year/incomplete series. Preserve
original record/selection behavior and identify any corrected missing-record
policy explicitly. Annual fitting also depends on the catalogue reference issue
IN-02. No annual numerical parity follows from the detailed IV_R point path.

## WX-01 — Weather, time and POA lineage

#to-review — WX-01 corrects acquisition versus downstream filtering, last-response metadata, and which geometry calculations actually feed POA.

`Clima:64–183` returns SmartNDH with source-length buckets and the last fetched
frame/metadata. TMY forces 60-minute requests; specific-year calls can request
multiple intervals. Downstream POA/Sandia/writers impose their own length gates.
A future acquisition adapter must preserve each response, metadata, timestamps,
intervals and source identity separately; the hybrid return is not a complete
per-year metadata snapshot.

`Solar_pos:36–112` computes manual Day/EoT terms, but those values are unused or
overwritten in the returned POA chain. Actual solar zenith/azimuth and airmass
come from pvlib position, with default tilt=latitude/azimuth=180. Unused earlier
calculations can still require fields or fail. `Solar_pos_e` requires explicit
numeric orientation; a None default is proposed behavior, not current equivalence.
Review time zones, DST/leap-day, index alignment and wind height from recorded
responses; do not hide those interpretations in normalization.

## EV-01 — Measurements, correction and statistical synthesis

**Source identity.** Earlier workbook observations are author-reported; originals,
permissions and module/sensor linkage are absent here. Positional sheet/Info-row
association is an implicit contract. Legacy upload rewrites the workbook through
pandas, so preserving original bytes is a deliberate modern safeguard, not a claim
about legacy behavior. See C-05 and [evidence](evidence.md).

#to-review — Effective-temperature correction: sensor mean and reported metadata differ from the Voc-derived Tmod used in correction/simulation.

**Effective temperature.** `IV_CI_cor:5947–6015` reads Voc/Irrad1/Temp1/Temp2.
It first translates De Soto at sensor mean `(T1+T2)/2`, then forms
`delta_source=nNsVth*k*(Tmean+273.15)/q` and overwrites Tmod using Voc, beta and
log(irradiance ratio). Corrections and IV_sim consume that inferred Tmod, while
reported temperature metadata retain the sensor mean. The delta expression has
the same dimensional concern as AN-01. Preserve sensor, inferred and reported
values separately; no validated temperature correction is established.

#to-review — The method/origin and fitting paragraphs correct the earlier function mapping and distinguish measured inputs, simulated references and their fit objectives.

**Method and origin.** Both `correction_IV:7304–7534` and
`correction_IV_s:7609…` dispatch M2/M2N. The latter handles simulated curve columns,
not the normalized method alone. Measured M2N uses Temperature_coeffs, a 400–1100
fit grid and optimized/clamped k; simulated M2N omits that coefficient call, uses
a 200–1100 grid and ri_2/100. Both use a squared logarithmic irradiance term in fG.
These method/origin/fit axes cannot be merged by suffix or formula similarity.
No IEC 60891 conformity follows without exact edition/formulation/conditions.

**Fitting and evaluation.** Temperature_coeffs derives coefficients from simulated
curves. find_k_sweep fits k using measured voltage/current corrected against a
simulated STC power curve: it minimizes the standard deviation of absolute
pointwise power differences, then clamps k. This mixed fit is not held-out
measurement validation. Keep the uncalibrated result, fit inputs/objective/bounds,
parameter identities and independent evaluation status.
The `Promedio` choice aggregates result tables, not sensor-temperature selection.
No modern measurement/correction/calibration use case is implemented.

#to-review — Statistical identity changes: current sampling differs from the report, and the returned power/spread estimators and fixed n/df need separate review.

**Bootstrap and reported method.** Current Bootstrap/Bootstrap2 truncate to minimum
length and draw separately for voltage/current/power using global NumPy randomness
(3,000 samples × 12). The supplied summary §4.10 reports 4,000 × 15 and 255 positions.
The returned P3 is meanV × meanI. Vstd/Istd/Pstd are 5%-trimmed means of
within-resample sample standard deviations (ddof=1), not standard deviations of
resampled means. `Comprobacion` uses those spreads with fixed n=30 / df=29 and a
95% t label. Historical algorithm linkage and statistical applicability remain
unresolved; a label is not validation of confidence coverage. Capture exact
order/lengths/RNG state and estimator before changing alignment, seed or sample
rules.
