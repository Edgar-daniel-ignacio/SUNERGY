# Evidence-First Technical Summary: PV Module Physics Engine for Downstream Agent Research

**Primary source:** Edgar Daniel Ignacio Domínguez Zamora, *Simulación, Corrección y Validación de Curvas I‑V de Módulos Fotovoltaicos*, UNAM, Instituto de Energías Renovables / Instituto de Ingeniería / ENES Juriquilla, undergraduate technical report, 28 May 2025.  
**Purpose of this summary:** consolidate the thesis evidence that is most useful for a later deep-research analysis of a physics-informed assistant for small residential and commercial PV developers in Mexico.  
**Evidence rule used here:** the thesis is treated as the authority. The separately supplied synthesized report was reviewed only to identify omissions, overextensions, and places where source material had been silently “corrected” or supplemented. This document does **not** design the agentic framework and does **not** import Mexican interconnection, electrical-code, inverter-sizing, or installation requirements that are absent from the thesis.

---

## 1. Executive synthesis

The thesis develops a Python software methodology, named **SunLier**, for estimating the electrical behavior of crystalline-silicon photovoltaic modules from relatively accessible inputs, principally manufacturer datasheet values and environmental conditions. Its core technical contribution is a module-level physics workflow built around the **single-diode equivalent circuit**, the **De Soto five-parameter model**, environmental translation of those parameters, and **Lambert W**-based solution of the single-diode equation to generate full current-voltage (I–V) curves. It also implements semi-empirical translation equations for faster, longer-duration calculations and integrates module-temperature models (Faiman, Sandia, and NOCT), solar-resource data from NREL/NSRDB, and I–V correction procedures used to translate outdoor measurements toward Standard Test Conditions (STC).

For the intended downstream project, the strongest evidence in the thesis is therefore **not** a complete PV-system design engine. It is a candidate **deterministic module-electrical submodel**: given a crystalline-silicon module’s reference electrical data and a specified irradiance/temperature state, it can infer the five single-diode parameters at reference conditions, translate them to the operating condition, and generate the module I–V characteristic and key electrical points. That is a meaningful physics anchor for questions about expected module voltage, current, maximum-power behavior, and sensitivity to temperature and irradiance.

The thesis itself draws an important boundary that must be preserved. Its methodology has two branches: (1) an **annual / long-horizon performance branch** using simplified translation equations and climate data, and (2) a **detailed I–V simulation branch** using the single-diode model. Only the I–V branch and the I–V correction workflow were experimentally validated in the report. The annual simulation branch was included as a foundation for future work and was explicitly **not validated**. Any downstream project that uses the annual branch for energy yield, design extremes, or expected production must therefore treat it as provisional until independently checked.

The validation is useful but narrow. Thirty outdoor I–V curves were measured on one previously used **Solartec 250 W, 60-cell polycrystalline module** over roughly twelve minutes while module temperature and irradiance changed. The simulation was run under the same environmental conditions; both simulated and measured curves were corrected to STC and compared with the manufacturer datasheet. The representative simulated curves remained within the manufacturer’s ±3% tolerance for all five principal electrical parameters under both correction methods. Average simulation-versus-corrected-measurement error was reported as **2.06%** with the older correction method and **2.41%** with the updated method. The updated correction method, however, brought measured maximum power much closer to the datasheet and achieved four of five parameters within tolerance versus three of five for the older method. The thesis interprets the remaining discrepancy, especially in maximum-power current, as evidence of light module degradation that the pristine simulation does not represent.

This evidence supports the proposition that the thesis methodology can provide a deterministic, auditable estimate of **module-level DC behavior under homogeneous operating conditions**, but it does not establish a validated engine for full arrays, partial shading, mismatch, bypass-diode behavior, modern bifacial or non-standard cell architectures, inverter operation, AC-side performance, conductor/protection sizing, structural design, commissioning, or Mexican regulatory compliance. Those are separate research and validation layers.

A second critical finding from reviewing the source is that several equations and definitions in the thesis contain internal inconsistencies or likely transcription/formulation issues. These must be re-derived from the cited primary literature or tested against a reference implementation before production use. Most notably: the annual maximum-power equation is printed with an inverse irradiance factor $1000/G$; the coefficient $\gamma$ is described inconsistently as a voltage-at-MPP coefficient and a maximum-power coefficient; the updated correction function $f(G)$ is printed with two first-order logarithmic terms rather than an explicitly squared term; the report alternates between 250 and 255 I–V points; and notation shifts among $I_{ph}/I_L$, $I_s/I_0$, $R_h/R_{sh}$, and $\eta/a$. These do not invalidate the conceptual workflow, but they make source verification a prerequisite for software reuse.

---

## 2. Problem context and scope of the original report

The thesis begins from a practical engineering problem: PV module nameplate parameters are specified at controlled reference conditions, while real modules operate under continuously changing irradiance and temperature. The difference matters for technology selection, system dimensioning, and field evaluation. Physical-mathematical models can bridge this gap, but some approaches require difficult-to-obtain parameters or specialist knowledge. The project therefore seeks a methodology that balances **physical fidelity, computational cost, and accessibility of inputs**.

The stated general objective is to evaluate an integrated methodology for simulating and correcting PV-module I–V curves using previously validated models and procedures, implemented in Python and compared against experimental measurements. The specific objectives are to compare simulated and measured I–V curves over different irradiance and temperature conditions, correct both measured and simulated curves to STC, and identify the strengths and limitations of the integrated method.

The software is described as applicable to **monocrystalline and polycrystalline photovoltaic modules**, using basic information such as datasheet parameters. This general software ambition should not be confused with the empirical validation envelope: the experimental campaign involved only one older polycrystalline module. The report therefore establishes implementation feasibility and a first validation case, not broad empirical validation across module technologies.

The thesis distinguishes two modelling resolutions:

1. **Detailed equivalent-circuit modelling**, especially the single-diode model, for obtaining a full I–V curve under a particular operating state. This has higher computational burden but gives a more complete electrical representation.
2. **Simplified empirical or semi-empirical translation equations**, intended for longer periods such as days, months, or a year. These estimate key electrical quantities directly from environmental inputs and reference electrical values without reconstructing a full I–V curve at every time step.

That distinction is particularly useful for downstream research. The thesis is effectively proposing a **multi-fidelity computation strategy**: use lower-cost equations to screen or characterize many operating states, then use the detailed single-diode solver for conditions where a full electrical curve is needed. The source does not turn this into an autonomous workflow, but the computational division itself is explicit.

---

## 3. Physical and mathematical foundation

### 3.1 I–V behavior and critical electrical points

A PV module’s I–V curve describes output current as a function of terminal voltage for a specific irradiance and temperature. The thesis focuses on the following key quantities:

- $I_{sc}$: short-circuit current, at approximately zero terminal voltage;
- $V_{oc}$: open-circuit voltage, at zero output current;
- $(V_{mp}, I_{mp})$: the maximum-power operating point;
- $P_{max}=V_{mp}I_{mp}$;
- fill factor, $FF=(V_{mp}I_{mp})/(V_{oc}I_{sc})$.

The source emphasizes the contrasting environmental sensitivities of current and voltage. Increasing irradiance primarily raises current. Increasing module/cell temperature reduces open-circuit voltage and maximum power, while short-circuit current typically changes only slightly upward. This is why temperature and effective irradiance are the key environmental state variables throughout the methodology.

### 3.2 Double-diode and single-diode equivalent circuits

The literature review discusses both the double-diode and single-diode equivalent circuits. The double-diode model represents additional recombination behavior and requires more parameters. The thesis notes that, although this can provide greater granularity, the **single-diode model is generally sufficient for crystalline silicon under normal operating conditions** and is much more tractable for the intended software.

The single-diode equation is represented conceptually as:

$$
I = I_{ph} - I_s\left[\exp\left(\frac{V+IR_s}{\eta V_t}\right)-1\right] - \frac{V+IR_s}{R_h}
$$

with:

- $I_{ph}$: photogenerated current;
- $I_s$: reverse saturation current;
- $R_s$: series resistance;
- $R_h$ or $R_{sh}$: shunt resistance;
- $\eta$: diode ideality factor;
- $V_t$: thermal voltage term.

For implementation, the thesis later uses De Soto notation in which the five reference parameters are commonly written $I_{L,ref}$, $I_{0,ref}$, $R_{s,ref}$, $R_{sh,ref}$, and $a_{ref}$, where $a$ incorporates the ideality/thermal-voltage scaling. A downstream implementation should normalize these notational variants into one canonical schema.

### 3.3 Homogeneous-condition scaling assumption

The single-diode methodology assumes **homogeneous conditions**: cells in a module, and modules in a system if scaled upward, are treated as having uniform electrical behavior and being exposed to the same climatic conditions. Under this assumption, cell-to-module or module-to-array scaling can be performed using series/parallel relationships for voltage, current, and equivalent resistances.

This assumption is central to the model’s validity envelope. It means the thesis model is not, by itself, a validated partial-shading or mismatch model. It does not explicitly resolve cell strings, bypass-diode activation, localized hot spots, soiling gradients, uneven rear-side irradiance, or per-module temperature differences. These effects would need separate modelling if the downstream tool is expected to diagnose or design systems under non-uniform conditions.

---

## 4. Core computational methodology

This is the most transferable part of the thesis and the most important evidence for a deterministic physics engine.

### 4.1 Overall software structure

SunLier was developed in Python using scientific and PV-oriented libraries including **pvlib, SciPy, pandas, NumPy, matplotlib, Plotly, and Leaflet-related mapping functionality**. The thesis explicitly states that pvlib calculation functions used by the project were not accepted blindly: for examples such as module-temperature models, the equations were implemented manually and compared to pvlib outputs to check consistency.

The software methodology is divided into two linked branches.

#### Branch A — annual / long-horizon simulation

The workflow shown in the thesis begins with:

1. location (latitude and longitude);
2. module electrical parameters, either entered manually, selected from a CEC database, or represented by the thesis reference module;
3. module inclination and orientation;
4. selection of one or more module-temperature models (Faiman, Sandia, NOCT);
5. choice of TMY or a specific meteorological year / period;
6. NREL climate-data download;
7. calculation of effective irradiance and module temperature;
8. evaluation of semi-empirical translation equations;
9. tabular output of time-dependent electrical quantities.

The annual-flow diagram in the thesis is particularly important because it establishes that **coordinates, orientation, tilt, module datasheet inputs, climate data, and thermal modelling were already conceived as connected input stages**. However, this branch was not experimentally validated in the thesis and therefore should not be treated as established production-grade yield modelling.

#### Branch B — detailed I–V simulation

The I–V branch has three user-facing modes:

- **Standard Test / Prueba Estándar:** simulate the selected module at representative environmental conditions identified from the long-horizon simulation;
- **Specific Values / Valores Específicos:** generate an I–V curve for user-specified temperature and irradiance;
- **I–V Comparison / Comparación I–V:** load a measured I–V curve, simulate the same environmental condition, and calculate error relative to measurement.

All modes converge on the same physics chain:

1. obtain the five single-diode variables using De Soto;
2. translate the variables to the required irradiance and temperature;
3. obtain electrical parameters with Lambert W;
4. generate the I–V curve;
5. optionally compare against the translation-equation result or a measured curve.

The flowchart on PDF page 53 makes this sequence explicit and is the clearest source-level depiction of the deterministic computational core.

### 4.2 Reference inputs from a manufacturer datasheet

The key engineering advantage of the De Soto approach in this thesis is that manufacturers usually do **not** provide $I_L$, $I_0$, $R_s$, $R_{sh}$, and $a$ directly, but they do provide observable reference points at STC. The thesis constructs the hidden equivalent-circuit parameters from accessible nameplate information, principally:

- $I_{sc,ref}$;
- $V_{oc,ref}$;
- $I_{mp,ref}$;
- $V_{mp,ref}$;
- $P_{max,ref}$ as a consistency quantity;
- temperature coefficients such as $\alpha_{sc}$ and $\beta_{oc}$, with additional coefficients used by the simplified translation branch.

For the eventual downstream research, this is a high-value feature: it aligns the deterministic core with inputs that small developers can realistically provide from datasheets rather than requiring laboratory extraction of diode parameters.

### 4.3 Five-parameter extraction at reference conditions: De Soto formulation

The detailed solver seeks five reference parameters:

$$
\{I_{L,ref}, I_{0,ref}, a_{ref}, R_{s,ref}, R_{sh,ref}\}.
$$

The thesis closes the nonlinear system using five physical constraints derived from the single-diode model:

1. **Short-circuit constraint:** enforce the diode equation at $V=0$, $I=I_{sc,ref}$.
2. **Open-circuit constraint:** enforce the equation at $I=0$, $V=V_{oc,ref}$.
3. **Maximum-power coordinate constraint:** enforce the equation at $I=I_{mp,ref}$, $V=V_{mp,ref}$.
4. **Maximum-power slope constraint:** require $dP/dV=0$ at the MPP, equivalently $I_{mp}+V_{mp}(dI/dV)=0$.
5. **Temperature-perturbed open-circuit constraint:** evaluate an adjacent state at $T_2=T_{ref}+2$ and use the module’s open-circuit-voltage and short-circuit-current temperature response plus semiconductor band-gap and saturation-current scaling to provide the final independent relationship.

The fifth condition is important because it couples the reference extraction to thermal behavior rather than solving purely from the four obvious I–V landmarks. The thesis expresses the auxiliary relationships as:

$$
T_2=T_{ref}+2
$$

$$
V_{oc,2}=V_{oc,ref}+\beta_{oc}(T_2-T_{ref})
$$

$$
a_2=a_{ref}\frac{T_2}{T_{ref}}
$$

$$
I_{L,2}=I_{L,ref}+\alpha_{sc}(T_2-T_{ref})
$$

plus a temperature-dependent band-gap expression and a temperature-scaled reverse-saturation current.

The thesis then solves the coupled equations numerically using a **Powell-Hybrid root-finding method**. It describes the solver as using iterative root finding from an initial value until convergence, combining Newton-type behavior with a more robust hybrid strategy. The practical output of this stage is a module-specific reference parameter set that can be cached and reused for many environmental states.

**Implementation caution:** the exact algebra printed in several of the De Soto equations has sign/parenthesis and notation ambiguities in the thesis PDF. A production implementation should therefore use the thesis to preserve the workflow and variable dependencies, but it should re-derive the exact residual equations from De Soto (2006) or a trusted reference implementation rather than transcribing the thesis equations verbatim.

### 4.4 Translation of the five parameters to operating irradiance and temperature

Once the five reference parameters are known, the thesis applies De Soto-style environmental translation. The central dependency structure is:

- convert reference and cell temperatures to kelvin;
- update semiconductor band gap with temperature;
- scale the modified ideality/thermal-voltage term $a$ with absolute temperature;
- scale photogenerated current $I_L$ approximately linearly with effective irradiance and adjust it with $\alpha_{sc}$;
- scale reverse saturation current $I_0$ strongly with temperature through a cubic temperature factor and an exponential band-gap term;
- scale shunt resistance inversely with effective irradiance;
- hold series resistance $R_s$ constant in the De Soto formulation used by the thesis.

The source writes, in substance:

$$
T_{ref,K}=T_{ref}+273.15,\qquad T_{cell,K}=T_{cell}+273.15
$$

$$
E_g=E_{g,ref}\left[1+dE_{g}/dT\,(T_{cell,K}-T_{ref,K})\right]
$$

$$
a=a_{ref}\left(\frac{T_{cell,K}}{T_{ref,K}}\right)
$$

$$
I_L=\frac{G_{eff}}{G_{ref}}\left[I_{L,ref}+\alpha_{sc}(T_{cell,K}-T_{ref,K})\right]
$$

$$
I_0=I_{0,ref}\left(\frac{T_{cell,K}}{T_{ref,K}}\right)^3
\exp\left(\frac{E_{g,ref}}{kT_{ref,K}}-\frac{E_g}{kT_{cell,K}}\right)
$$

$$
R_{sh}=R_{sh,ref}\frac{G_{ref}}{G_{eff}},\qquad R_s=R_{s,ref}.
$$

This stage is the bridge from manufacturer reference behavior to site/operating behavior. For the intended future application, it is also the most direct location at which trustworthy environmental inputs become deterministic electrical-state outputs.

### 4.5 Lambert W solution and I–V curve construction

The single-diode equation is implicit in current and voltage. The thesis contrasts iterative approaches such as Newton–Raphson with the use of the **Lambert W function**, citing Jain and Kapoor (2004) as an exact analytical route for the single-diode equation. The stated advantage is avoiding repeated iterative solution when many I–V points or many curves must be generated.

The methodology uses the translated five-parameter set as input to Lambert-W-based expressions for the key electrical quantities and for current as a function of voltage. It then constructs the curve by:

1. determining $V_{oc}$ for the specified environmental state;
2. creating a uniformly spaced voltage list from 0 to $V_{oc}$;
3. evaluating the corresponding current at each voltage using the Lambert W solution;
4. plotting / returning the paired voltage-current arrays.

The detailed software description says generated curves use **250 points** based on the curve tracer used as a reference. In the later statistical validation chapter, however, each measured/corrected curve is described as having **255 points**. This is a source inconsistency that should be reconciled from the original code/data before reproducing the workflow. It does not affect the physics, but it matters for exact validation replication.

### 4.6 Effective irradiance and solar-resource inputs

The annual branch uses **effective irradiance**, rather than raw horizontal irradiance, to better approximate the radiation available to the module. The thesis states that this accounts for surface inclination and solar geometry, and also mentions air mass in determining effective irradiance. pvlib is used for geometry-related calculations and its outputs were checked for consistency.

NREL resources cited include:

- **NSRDB**, with historical direct, diffuse, and global irradiance plus meteorological variables such as ambient temperature and wind;
- **TMY**, representing a statistically typical meteorological year.

The thesis states that NSRDB/global-irradiance data carry typical errors of roughly **5–10%** and explicitly cautions that annual energy simulations represent probable/expected behavior rather than exact future operation. This uncertainty statement is important for any future physics-informed tool: deterministic equations do not make uncertain meteorological inputs deterministic truths.

### 4.7 Module-temperature estimation

Because temperature strongly affects voltage and power, the software integrates three temperature models.

#### Faiman

$$
T_m=T_a+\frac{G}{U_0+U_1v}
$$

Inputs are ambient temperature, in-plane irradiance, wind speed, and empirical convection/heat-loss coefficients $U_0$ and $U_1$. The thesis notes that estimating these coefficients can be a barrier for a typical user.

#### Sandia

$$
T_m=E\exp(a+bW_s)+T_a
$$

$$
T_c=T_m+\frac{E}{E_0}\Delta T
$$

This approach uses irradiance, ambient temperature, wind speed, mounting-dependent coefficients, and a cell-to-module temperature difference term. The thesis characterizes it as more complex and dependent on installation configuration.

#### NOCT

$$
T_m=T_a+\left(\frac{NOCT-20}{800}\right)G
$$

This is the simplest of the three and can often be used directly from a datasheet, but the thesis calls it the least precise under real operating conditions.

The key evidence boundary is that the thesis **checked its implementations of these formulas against pvlib**, but did not perform an independent multi-site field validation of the annual thermal/yield chain. Thus, “implemented and cross-checked” is supported; “experimentally validated thermal engine” is not.

### 4.8 Fast translation equations for long-horizon calculations

For annual or long-duration simulation, the thesis uses lower-cost semi-empirical equations to estimate $I_{sc}$, $V_{oc}$, $I_{max}$, $V_{max}$, and $P_{max}$ from STC values, module temperature, irradiance, and empirical coefficients. The equations avoid solving a full single-diode curve at every time step and therefore represent the low-cost branch of the multi-fidelity approach.

The reported forms for current and voltage are, schematically:

$$
I_{sc}=I_{sc0}[1+\alpha(T_{mod}-25)]\left(\frac{G}{1000}\right)
$$

$$
V_{oc}=V_{oc0}[1+\beta(T_{mod}-25)]\left[1+\delta\ln\left(\frac{G}{1000}\right)\right]
$$

$$
I_{max}=I_{max0}[1+\alpha(T_{mod}-25)]\left(\frac{G}{1000}\right)
$$

$$
V_{max}=V_{max0}[1+\gamma(T_{mod}-25)]\left[1+\delta\ln\left(\frac{G}{1000}\right)\right].
$$

The thesis then prints the following maximum-power form:

$$
P_{max}=P_{max0}[1+\gamma(T_{mod}-25)]
\left[1+\delta\ln\left(\frac{G}{1000}\right)\right]
\left(\frac{1000}{G}\right).
$$

**This final factor is a high-priority verification item.** As printed, power contains $1000/G$, which is counterintuitive for a direct irradiance-response equation and differs from the silent revision made in the supplied secondary summary. The evidence-first approach is to preserve what the thesis actually prints and explicitly require downstream research to check the cited NREL / source equations and the original SunLier code before using this branch. The annual branch was not validated anyway, so no production conclusion should rest on this expression without re-derivation.

The coefficient $\gamma$ also needs verification. In one part of the thesis it is described as the temperature coefficient of voltage at maximum power, while in the methodology it is described as the temperature coefficient of maximum power. Those are not interchangeable parameters in a production input schema.

### 4.9 I–V curve correction to Standard Test Conditions

The correction workflow is a **measurement normalization / diagnostics method**, distinct from forward design simulation. Its purpose is to translate an I–V curve measured at $(G_1,T_1)$ toward reference conditions $(G_2,T_2)$, allowing comparison with a datasheet or reference curve.

The thesis implements two versions of “Method 2”:

- the older method associated with **IEC 60891:2009**;
- an “updated Method 2” described as a 2021 update and implemented using formulations discussed in later literature, especially Zhang et al. (2024).

The older method uses a relatively simple irradiance scaling for current and linear/logarithmic correction terms for voltage. The updated method adds more variables and a nonlinear irradiance-dependent voltage correction, as well as a temperature-adjusted series-resistance term.

The updated current relationship is presented as:

$$
I_2=I_1\frac{G_2}{G_1}
\frac{1+\alpha_{rel}(T_{m2}-25)}{1+\alpha_{rel}(T_{m1}-25)}.
$$

Its voltage equation uses $r_{s1}$, $\kappa$, $\kappa_2$, $\beta_{rel}$, and an empirical irradiance function $f(G)$. The thesis prints:

$$
f(G)=B_2\ln\left(\frac{1000}{G}\right)+B_1\ln\left(\frac{1000}{G}\right)+1.
$$

The PDF image confirms that both logarithmic terms are printed with the same first power. This is another high-priority source-verification item: a downstream implementation should verify the intended expression directly against the cited updated correction literature / current IEC standard rather than adopting either the thesis expression or the altered expression in the prior synthesized report without checking.

For the eventual developer-assistance use case, I–V correction has value primarily as a **commissioning, QA, or diagnostics capability** when field measurements are available. It is not required for every forward design calculation, and it should not be conflated with inverter sizing, protection design, or regulatory compliance.

### 4.10 Statistical validation: TLC/CLT and bootstrapping

The thesis uses the Central Limit Theorem and bootstrapping to form statistically representative I–V curves from repeated outdoor measurements. This is part of the evidence for model validation, not an essential runtime component for a developer who only wants a forward deterministic estimate.

The validation method is:

1. start from 30 curves in each comparison group;
2. align the curves point by point (reported as 255 positions in this section);
3. at each position, form the 30-value sample;
4. draw 4,000 bootstrap samples of size 15 with replacement;
5. calculate the mean for each resample;
6. treat the distribution of resampled means as approximately normal;
7. use its mean as the representative value at that curve position;
8. repeat across all positions to reconstruct a representative I–V curve;
9. calculate 95% confidence intervals using a Student-t expression and the bootstrap-derived standard deviation.

This statistical layer reduced sensitivity to individual measurements and provided a more stable comparison against the manufacturer tolerance. For a future product, it is most relevant if the tool later accepts repeated field I–V traces for QA or degradation assessment. It is not evidence that bootstrapping is needed for ordinary pre-installation design.

---

## 5. Experimental validation and the results that matter for reuse

### 5.1 Validation setup

The physical module was a previously used **Solartec polycrystalline 250 W module with 60 series cells**, nominally $V_{oc}=37.85\,V$, $V_{mp}=30.12\,V$, $I_{sc}=8.65\,A$, and $I_{mp}=8.30\,A$. The report notes that the module had already been used in real applications.

The outdoor campaign used an I–V curve tracer, thermocouples on the rear of the module, a PV pyranometer, a solar gnomon, a motorized support for orientation/inclination, and expanded-polystyrene insulation. The module was initially cooled toward STC, insulated at the rear, aligned approximately normal to solar incidence, and then measured as it heated under outdoor conditions.

Thirty I–V curves were obtained in roughly twelve minutes. Conditions were not controlled at STC; the measurement campaign deliberately spanned a changing thermal and irradiance state. This is useful for demonstrating environmental translation, but it is a narrow and highly correlated validation sample rather than 30 independent site/day/module experiments.

### 5.2 What the results establish

The results provide three forms of evidence.

#### A. Simulated curves remain close to manufacturer STC values after correction

For the simple average of 30 simulated curves corrected to STC:

- older method: $V_{oc}=36.74\,V$, $I_{sc}=8.83\,A$, $P=243.70\,W$, with errors of 2.94%, 2.07%, and 2.52% relative to the datasheet;
- updated method: $V_{oc}=37.17\,V$, $I_{sc}=8.83\,A$, $P=248.28\,W$, with errors of 1.79%, 2.08%, and 0.69%.

The representative simulated curves generated with the bootstrap/CLT procedure placed **all five parameters** $(V_{oc},I_{sc},P_{max},V_{mp},I_{mp})$ inside the manufacturer ±3% tolerance under both correction methods.

This is the strongest validation evidence for using the detailed single-diode simulation as a preliminary deterministic module model.

#### B. Simulation reproduces measured electrical behavior with low single-digit error

Comparing simulation against corrected measurement, the thesis reports average percent error of **2.06% for the older correction method and 2.41% for the updated method** across the selected comparison metrics. This supports the statement that the simulator tracks the measured module reasonably well in the tested environmental range.

A subtle but important interpretation point is that the updated correction method is **not uniformly superior on every validation metric**. It improves the normalization of measured power to the datasheet substantially, yet the mean simulation-versus-measurement error quoted by the thesis is slightly higher (2.41% vs. 2.06%). A downstream report should therefore say that the updated correction appears better for certain STC-normalization outputs, especially measured power, rather than asserting unconditional algorithmic superiority.

#### C. Real-module degradation is not represented by the simulation

For measured representative curves, the older correction matched three of five key parameters within ±3%, whereas the updated correction matched four of five; $I_{mp}$ remained outside the band. The thesis attributes this to **light degradation / prior module use**. The simulation, built from nameplate parameters, assumes an undegraded module and therefore cannot reproduce physical wear automatically.

The thesis does **not** experimentally identify the degradation mechanism. It does not establish that solder fatigue, corrosion, encapsulant browning, or any other specific failure mode caused the discrepancy. Those causal mechanisms appeared in the supplied secondary synthesis but are not supported by this source. The supported conclusion is only that the observed mismatch is consistent with light degradation and that future work should incorporate degradation modelling and use new/reference modules for validation.

### 5.3 Why the experimental results should remain a compact part of the downstream evidence base

For the intended product research, the individual sweep tables and all experimental numerical detail are not central product inputs. Their value is evidentiary: they show that the detailed simulation produced plausible module-level behavior under one outdoor validation campaign and expose the model’s inability to represent degradation. The deep-research LLM should use these results to set **confidence boundaries**, not to tune future systems to the specific 250 W Solartec module.

---

## 6. Validity envelope, limitations, and unresolved technical issues

### 6.1 Explicit limitations stated by the thesis

The conclusion recommends several improvements:

- use controlled conditions / a solar simulator to reduce irradiance and temperature variability;
- repeat validation with new or minimally degraded modules;
- use a laboratory-characterized reference/control module;
- treat simulation as an orientation / preliminary-analysis tool and corroborate important technical or commercial decisions with experimental evidence;
- incorporate degradation models in future work;
- validate the methodology on more modules;
- maintain critical professional interpretation of results.

The thesis explicitly says the methodology has **implicit error** and does not include module degradation.

### 6.2 Validation scope is much narrower than the possible product scope

The detailed I–V engine was validated on:

- one module model;
- one polycrystalline technology;
- one previously used module specimen;
- one outdoor measurement session;
- 30 rapidly consecutive curves;
- a limited irradiance/temperature envelope;
- homogeneous, unshaded conditions.

This does not establish accuracy across all modern PV modules, mounting arrangements, Mexican climates, or system configurations. The software’s stated applicability to mono/poly crystalline modules is broader than the experimental evidence.

### 6.3 Annual simulation is architecturally present but experimentally unvalidated

The annual branch is highly relevant to future site-specific planning because it links coordinates, NREL climate data, orientation/tilt, effective irradiance, thermal models, and electrical translation. Nevertheless, the thesis explicitly says that validating annual simulation would require a different experiment and was outside the report scope. It must therefore be labelled **implemented / conceptual but unvalidated by this thesis**.

Any future use for annual energy production, P50/P90, financial modelling, system sizing, or code-required temperature extremes needs independent validation against established tools and field datasets.

### 6.4 The homogeneous single-diode model omits important real-system effects

The thesis model does not provide evidence for:

- partial shading and moving shadows;
- cell/module mismatch;
- bypass-diode activation;
- multiple submodule electrical strings;
- soiling and non-uniform contamination;
- snow;
- bifacial rear-side irradiance;
- spectral-response differences among modern technologies;
- angle-of-incidence optical-loss models beyond the general effective-irradiance treatment;
- degradation progression;
- DC wiring losses;
- inverter MPPT/control behavior;
- inverter efficiency/clipping;
- AC system losses;
- battery integration;
- conductor, overcurrent, grounding, isolation, or surge-protection design;
- structural or roof-load engineering.

These are not “minor missing features” if the target is a complete installer/developer guide; they are distinct engineering layers outside the thesis validation.

### 6.5 No Mexican regulatory or interconnection model is contained in the thesis

The thesis discusses **IEC 61853** and **IEC 60891** as standards for PV module measurement, performance evaluation, and I–V correction. It does not establish the Mexican interconnection rules, CFE procedures, CRE requirements, NOM electrical design rules, permitting workflows, utility paperwork, or inverter certification requirements needed for a real project in Mexico.

Accordingly, the thesis can contribute a physics engine to a later developer-assistance system, but **regulatory compliance must be independently researched from current Mexican primary sources**. It should not be inferred from the thesis or from the earlier synthesized report.

### 6.6 Source equations and notation require verification before reuse

The most important technical ambiguities to hand off to deep research are:

| Issue | What the thesis says | Why it must be checked |
|---|---|---|
| Annual $P_{max}$ irradiance factor | Equation 17/27 multiplies by $1000/G$ | Counterintuitive for forward power-vs-irradiance response; prior synthesis silently changed it. Verify against cited source/code. |
| $\gamma$ definition | Described in different places as a Vmp temperature coefficient and as a Pmax temperature coefficient | These are distinct datasheet quantities. A production schema cannot conflate them. |
| Updated $f(G)$ correction | PDF prints $B_2\ln(1000/G)+B_1\ln(1000/G)+1$ | Two same-order log terms appear redundant. Verify against the cited Zhang / IEC formulation. |
| Single-diode residual equations | Some signs/parentheses are ambiguous in typesetting | Re-derive from De Soto rather than literal transcription. |
| I–V point count | Software section says 250; statistical section says 255 | Reconcile original tracer/export/code behavior. |
| Weather-year range | Flowchart and prose show different year ranges | Likely software/data-version mismatch; not a physics issue but matters for reproducibility. |
| Parameter notation | $I_{ph}/I_L$, $I_s/I_0$, $R_h/R_{sh}$, $\eta/a$ alternate | Canonicalize units and definitions before software integration. |
| Temperature-coefficient units | Datasheet table presentation is terse/ambiguous | Confirm whether values are fractional, percent per °C, or absolute-unit coefficients before numerical use. |

This table is one of the most important corrections to the supplied secondary evidence report. Where that report silently normalized or “fixed” equations, this summary preserves the thesis as evidence and turns inconsistencies into explicit verification tasks.

---

## 7. What is directly reusable as a deterministic physics anchor

Without designing the eventual agent, the thesis supports the following reusable evidence components.

### 7.1 High-confidence, thesis-validated core

**Detailed module I–V simulation under homogeneous irradiance and temperature**, consisting of:

- a five-parameter single-diode representation;
- extraction of reference parameters from standard datasheet electrical points through a De Soto-style nonlinear system;
- numerical reference-parameter solution with a hybrid root solver;
- translation of the hidden diode parameters to a specified operating $G_{eff}$ and $T_{cell}$;
- analytical / explicit Lambert-W-based solution of the I–V relationship;
- calculation of $I_{sc}$, $V_{oc}$, $I_{mp}$, $V_{mp}$, and $P_{max}$;
- generation of a full I–V trace;
- optional comparison with field I–V measurements.

This is the closest thing in the thesis to a deterministic “physics service” that can sit underneath probabilistic reasoning.

### 7.2 Useful but only partially established support functions

The thesis also provides methods that are useful inputs to that core but not fully validated end to end in the report:

- effective-irradiance computation from location/orientation and solar geometry using pvlib;
- NREL/NSRDB and TMY weather ingestion;
- Faiman, Sandia, and NOCT module-temperature estimates;
- long-horizon semi-empirical translation equations;
- CEC database / manual datasheet selection workflow.

These should be treated as **candidate supporting modules**, not as experimentally proven parts of the thesis validation.

### 7.3 Diagnostic / QA capability rather than primary design physics

IEC-style correction of measured I–V curves to STC, together with repeated-curve statistical synthesis, is valuable when a project has field measurements. It can support:

- post-installation comparison with nameplate behavior;
- quality assurance;
- module-level performance screening;
- evidence that a module may have degraded relative to its reference state.

The thesis does not establish a complete automatic fault classifier or degradation model, so diagnostic claims should remain conservative.

---

## 8. Corrections to the supplied secondary synthesis

The previously supplied evidence report contained useful extraction of many equations and results, but it also blurred the boundary between thesis evidence and an imagined future product. The following corrections should guide the next deep-research stage.

1. **Do not treat the thesis as an end-to-end validated PV project engine.** Only the detailed I–V simulation/correction branch was experimentally validated. The annual branch was explicitly left for future validation.
2. **Do not describe the engine as “infallible,” exact in practical operation, or a complete deterministic anchor for project engineering.** It is a validated preliminary module model with documented error and important omitted physics.
3. **Do not attribute Mexican regulations to the thesis.** NOM, CFE, CRE, inverter interconnection, conductor sizing, disconnects, and permitting workflows must be researched separately from current primary sources.
4. **Do not import system-level inverter/string calculations as if they were thesis outputs.** The thesis models module electrical behavior and only discusses homogeneous scaling conceptually.
5. **Do not claim the three temperature models were field-validated by this thesis.** Their equations were implemented and checked against pvlib; annual performance was not experimentally validated.
6. **Do not silently correct thesis equations.** The previous synthesis changed the annual $P_{max}$ irradiance factor and changed the form of the updated $f(G)$ function. Those changes may ultimately prove physically correct, but they are external corrections, not faithful retrieval.
7. **Do not add generic coefficient values unless independently sourced.** The thesis gives model forms and qualitative input requirements; several numerical defaults in the prior synthesis were not established by this report.
8. **Do not diagnose specific degradation mechanisms from this experiment.** The thesis attributes the discrepancy to light degradation / prior use, but does not identify solder fatigue, corrosion, browning, or other failure mechanisms.
9. **Do not overstate the updated correction method.** It improves measured STC normalization, especially maximum power, but the reported average simulation-versus-measurement error is slightly higher under the updated method.
10. **Keep the experimental results in proportion.** They validate the methodology within one test envelope; they are not product requirements or representative module performance values for Mexico.

---

## 9. Evidence gaps that the subsequent deep-research query should resolve

The next research stage can use this thesis as a seed, but should independently establish the following before any real developer-facing deployment.

### 9.1 Reconstruct and verify the physics engine from primary technical sources

- Re-derive the five-parameter system directly from De Soto, Klein & Beckman (2006) or an authoritative implementation.
- Confirm all parameter units, temperature coefficients, initialization constraints, convergence checks, and physically valid parameter bounds.
- Verify the exact Lambert W expressions used for current/voltage and their numerical stability across very low irradiance, high temperature, and cold high-voltage conditions.
- Establish failure handling when the nonlinear reference-parameter extraction does not converge or produces non-physical values.
- Test the solver against pvlib and at least one other trusted PV modelling package over a systematic irradiance-temperature matrix.

### 9.2 Validate the long-horizon environmental chain

- Verify the semi-empirical electrical translation equations and specifically resolve the $P_{max}$ irradiance term and $\gamma$ definition.
- Validate effective-irradiance calculations, transposition, angle-of-incidence effects, air-mass/spectral corrections, albedo, horizon/shading inputs, and time conventions.
- Establish which weather datasets have robust coverage and current support for Mexico and quantify uncertainty by region.
- Validate Faiman, Sandia, and NOCT/NMOT temperature models for relevant Mexican rooftop and small-commercial mounting configurations.
- Benchmark annual and monthly energy estimates against established reference software and measured systems.

### 9.3 Extend beyond the homogeneous module model where required

Research whether the target user needs deterministic treatment of:

- modern half-cell and multi-busbar module topology;
- bypass diodes and substring behavior;
- partial shading and mismatch;
- bifacial modules;
- n-type TOPCon/HJT and other technologies outside the thesis validation;
- degradation and soiling;
- DC string/array scaling and wiring losses;
- inverter MPPT, efficiency, clipping, and operating limits;
- storage if within product scope.

The important principle is to add these as separately validated layers rather than hiding them inside LLM reasoning.

### 9.4 Research Mexican regulatory and development requirements independently

The thesis is not evidence for the regulatory layer. The deep-research stage should retrieve current, primary Mexican requirements governing small distributed PV, including the applicable electrical installation standard, utility interconnection procedures, distributed-generation rules, equipment certifications, metering/commercial schemes, inspection/verification requirements, and any state/municipal permitting differences relevant to residential and small commercial projects. Each requirement should be versioned and traceable to an official source because this layer can change independently of the physics model.

### 9.5 Establish the human-in-the-loop and assurance boundary

The thesis itself recommends professional interpretation and experimental corroboration for important decisions. Deep research should therefore determine which calculations can safely be automated deterministically, which require warnings or confidence bounds, which require a licensed/qualified professional, and which field checks are needed before energization. This is an assurance question, not a conversational-agent design question.

---

## 10. Conclusions for downstream project research

The thesis provides a credible and practically useful starting point for a **module-level deterministic physics engine**, especially because it is built around inputs that are usually available to real developers: manufacturer STC electrical parameters, thermal coefficients, environmental irradiance and temperature, and site information. Its detailed branch converts these accessible inputs into hidden single-diode parameters, translates them to operating conditions, and reconstructs the I–V curve with a computationally efficient Lambert W approach. Within the limited outdoor validation campaign, simulated curves reproduced manufacturer and measured behavior with low single-digit error, supporting continued investigation of this methodology as a deterministic anchor.

The strongest transferable insight is the modelling architecture rather than the specific experimental values: **datasheet → reference single-diode parameters → environmental translation → explicit I–V solution → key electrical states**, supplemented by **site/weather → effective irradiance and temperature**. That chain is physically interpretable, auditable, and compatible with a future system in which probabilistic reasoning is not allowed to invent electrical behavior.

At the same time, the thesis should be used as a starting evidence base, not as a finished project-development engine. Its annual branch is unvalidated, its empirical validation is limited to one used module and one outdoor session, it assumes homogeneous operation, it does not model degradation, and it does not contain inverter, array, protection, construction, safety, or Mexican regulatory engineering. Several printed equations and parameter definitions also require primary-source verification before implementation.

For the subsequent deep-research LLM, the correct stance is therefore:

- **retain** the single-diode / De Soto / environmental-translation / Lambert W chain as the principal candidate deterministic module model;
- **retain** the thesis’s accessible-input philosophy and its two-resolution (fast annual vs. detailed I–V) computational structure;
- **retain** the validation results only as evidence of plausibility and a preliminary error envelope;
- **treat as provisional** the annual weather/thermal/translation branch until benchmarked;
- **verify** all exact equations and units against primary literature/reference implementations;
- **research independently** all system-level design, modern-module behavior, inverter, safety, and Mexican regulatory requirements;
- **avoid** turning the thesis’s validation statistics or the specific Solartec module into product assumptions.

This yields a much cleaner handoff: the thesis contributes a physically grounded, inspectable module-electrical kernel and a set of tested computational ideas, while the later deep-research stage determines what must surround that kernel for a reliable real-world PV developer tool in Mexico.

---

## Source map for follow-up research

The following sections of the thesis are the highest-signal places to revisit:

- **PDF pp. 18–20:** problem context and objectives; explicit statement that only the I–V branch is validated.
- **PDF pp. 23–38:** modelling literature, single-diode basis, Lambert W, De Soto, semi-empirical translation equations, NREL data, temperature models, IEC-related correction background.
- **PDF pp. 39–53:** core software methodology, annual simulation flow, detailed I–V simulation workflow, five-parameter extraction, parameter translation, Lambert W curve construction.
- **PDF pp. 54–60:** measurement, correction, validation, bootstrap/CLT methodology.
- **PDF pp. 61–88:** experimental data and curve-by-curve validation details; useful if reproducing the experiment, otherwise lower priority for product research.
- **PDF pp. 89–95:** consolidated results and comparison tables.
- **PDF pp. 96–98:** conclusions, limitations, and future-work recommendations.
- **PDF pp. 99 onward:** bibliography and appendices; primary citations to De Soto (2006), Jain & Kapoor (2004), IEC 61853, IEC 60891-related methods, NREL resources, and temperature-model literature.

### Key primary references named by the thesis

1. W. De Soto, S. Klein, and W. Beckman (2006), *Improvement and validation of a model for photovoltaic array performance*, Solar Energy 80(1), 78–88.
2. A. Jain and A. Kapoor (2004), *Exact analytical solutions of the parameters of real solar cells using Lambert W-function*, Solar Energy Materials and Solar Cells 81(2), 269–277.
3. IEC 61853 series, for module performance testing / energy rating.
4. IEC 60891:2009, for temperature and irradiance correction of measured I–V characteristics.
5. C. Zhang et al. (2024), *Enhanced I–V curve correction for PV diagnosis under diverse environmental and fault conditions*, Solar Energy 273.
6. NREL resources used by the thesis for PV performance modelling, NSRDB/TMY data, and implementation references.

