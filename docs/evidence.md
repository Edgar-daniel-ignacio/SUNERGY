---
title: Evidence provenance and limits
role: Source authority, availability and the scope of scientific and empirical claims
retrieve_when: Selecting evidence or making a scientific, empirical or provenance claim
read_scope: Relevant source record and its limitations; follow the named operation if needed
authority: Source assessment, not a model specification or approval
verify: Inspect original artifacts and exact source references; do not infer validity from prose or fit
review_status: "#to-review"
---

# Evidence provenance and limits

The collaborator's [curated investigation](legacy-refactorizacion/README.md) is the
primary map of legacy intent, functionality and dependencies. The [audit and coverage map](legacy_backend_coverage.md)
checks its consequential claims against source. [Assumptions](assumptions.md) owns
operation-level interpretation and scientific support; this file owns the strength
and availability of the evidence itself. #to-review

## What each source can establish

| Source | Establishes | Does not establish |
|---|---|---|
| Frozen legacy implementation and [hash inventory](evidence/legacy_inventory.json) | Exact preserved code and statically observable operations. #to-review | Author intent, successful execution of every branch, historical environment or scientific correctness. #to-review |
| Collaborator investigation and `index.json` | Original-author understanding, detailed locators, implicit contracts, observed design intent and proposals. The current audit validates the index and qualifies specific claims. #to-review | A source-review label does not mean the entire application ran; absent benchmark tools limit reproduction of reported duplication metrics. #to-review |
| [Supplied thesis-derived summary](evidence/pv_physics_engine_evidence_summary_for_agent_research_equations_fixed.md) and [copy provenance](evidence/provenance.json) | The report and methods as described by the supplied secondary account; unchanged bytes and attribution. #to-review | The original thesis, raw observations, an executable specification, or agreement with the current source where methods differ. #to-review |
| Independent legacy captures | Original-function results for named inputs, source/environment/solver identities and returned boundaries. See [reproduction](reproduction.md). #to-review | Full dashboard/annual reproduction, platform-invariant numbers, physical accuracy or empirical validation. #to-review |
| Primary formulations and technical documentation | Equation definitions, units, applicability and library semantics within their stated scope; linked in the relevant assumption entry. #to-review | Validation of SUNERGY's mixed coefficient/fit chains or campaign conclusions without the original data. #to-review |

Code, author intent, scientific formulation and measured observations answer
different questions. When they conflict, retain both accounts, identify the exact
branch/conditions and state what would resolve the difference. Do not choose an
accepted assumption by document age, majority agreement or a second call to the
same library. #to-review

## Supplied report and empirical envelope

The supplied summary attributes its source to Edgar Daniel Ignacio Domínguez
Zamora, *Simulación, Corrección y Validación de Curvas I–V de Módulos Fotovoltaicos*,
UNAM, 28 May 2025. Attribution is taken from that summary; the original report/PDF
is not present in this checkout. Preserve the supplied file's bytes; metadata and
routing live in its provenance record and [catalogue](README.md). #to-review

The summary describes 30 outdoor I–V curves from one previously used Solartec
250 W, 60-cell polycrystalline specimen. The collaborator reports inspecting a
30-curve workbook, IDs with gaps and varying irradiance/sensor temperatures.
Those original records are not supplied here. The accounts differ in duration
and the description of environmental homogeneity; neither can currently be
replayed or independently confirmed from original measurements. #to-review

The reported campaign concerns module I–V simulation/correction, not annual yield,
full PV systems or finance. Reported percentage errors, confidence labels and
manufacturer tolerances are not software-reproduction limits or general product
accuracy guarantees. Source-algorithm differences—including bootstrap sample rules
and effective correction temperature—must be resolved before attributing current
outputs to what the report evaluated. See EV-01 in [assumptions](assumptions.md).
#to-review

## Availability and unresolved evidence

Available: frozen source, the curated author investigation, the supplied secondary
summary, selected manual/synthetic-input original-source captures, and primary
references for specific formulations. Windows/Linux x86-64 same-platform I–V
comparisons exist; cross-platform numerical invariance and other environments are
not established. Current implementation/capture scope belongs in [coverage](legacy_backend_coverage.md).
#to-review

Not supplied: original thesis/report and measurement workbook, measurement
permissions/uncertainty and module linkage, original catalogue workbook with
edition/license, recorded weather response/time metadata, and the historical
runtime environment. The collaborator's earlier access is valuable reported
evidence, but does not make those artifacts available in this checkout. Retrieve
only what the selected next capability requires. #to-review

The retained platform-comparison report is a limited developer diagnostic. Its
selected MPP stationarity target is not a collaborator-approved accuracy standard
or a universal scientific acceptance gate. Keep its unmet observation visible;
use it only for that numerical investigation, not as a normal modeling input or
production prerequisite. #to-review
