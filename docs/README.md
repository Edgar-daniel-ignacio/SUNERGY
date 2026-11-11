---
title: Evidence catalogue and reading routes
role: Catalogue of maintained context and original supporting evidence
retrieve_when: Starting a backend task or locating the owner of a contextual claim
read_scope: This catalogue, then the relevant document or original chapter only
authority: Retrieval aid; does not establish runtime behavior, modeling approval, or scientific validity
verify: Check linked owners, source identities, and current evidence before relying on a claim
review_status: '#to-review'
---

# Evidence catalogue

#to-review — This catalogue gives each document one purpose. Repository policy
belongs to [AGENTS.md](../AGENTS.md); this frontmatter and the chapter metadata
help select context. They do not approve assumptions or override instructions.

## Maintained context

| Question | Read | Unique responsibility and boundary |
|---|---|---|
| Where does a calculation, contract, source or setting belong? | [Architecture](architecture.md) | Current ownership and integration boundaries. It does not turn provisional interfaces or future designs into implemented models. #to-review |
| What does a legacy capability do, and how thoroughly has it been reconciled? | [Legacy coverage and audit](legacy_backend_coverage.md) | Checked collaborator claims, source-to-modern mapping, reproduction coverage and gaps. It links the original inventory rather than replacing it. #to-review |
| Which evidence supports a scientific or empirical claim? | [Evidence and provenance](evidence.md) | Source identity, availability, strength, reported campaign scope and conflicting accounts. It does not define model equations or prove empirical validity. #to-review |
| What does a parameter or transformation mean? | [Assumptions](assumptions.md) | Named operation records: units, conditions, legacy interpretation, support, uncertainty and review status. A documented choice is not automatically an approved scientific default. #to-review |
| How do inputs cross normalization, modeling and output boundaries? | [Flowcharts](flowcharts.md) | Transformation lineage and implemented, conditional or deferred paths. Diagram labels link to owning records; they are not a second specification. #to-review |
| What must a numerical port preserve, and what evidence establishes agreement? | [Reproduction](reproduction.md) | Named preservation boundaries, capture provenance, comparison requirements and separate evidence gates. It does not equate compatibility with scientific or empirical acceptance. #to-review |

## Original legacy investigation

#to-review — The collaborator's [overview](legacy-refactorizacion/README.md) is
the primary starting point for legacy functionality. Its chapter catalogue routes
conventions, data history, implicit contracts, function inventory, defects, gaps,
report mapping, proposals and pending decisions. Read the relevant chapter and
the [reconciled findings](legacy_backend_coverage.md), then inspect the cited
source or capture when the conclusion affects implementation.

#to-review — Original author knowledge is valuable evidence of intent and system
structure. Static source analysis, an executed result, a proposal, a human decision
and scientific support establish different things. Reconciliation preserves those
distinctions and flags conflicts; it does not replace the original account silently.

| Locator | Use | Limit |
|---|---|---|
| [Function/state index](legacy-refactorizacion/index.json) | Locate an S-state or F-function and its referenced C-contract IDs. Use the author's README to find contract/risk details in 03, defects in 06 and decisions in 10. | No B/D/R identifiers are enumerated. Status labels are static author classifications, qualified in 04; membership does not prove execution or coverage. #to-review |
| [Original diagrams](legacy-refactorizacion/diagrams/) | Recover the author's data-flow, file/state and branch relationships. | Read each diagram's scope and the audit before treating a proposed or descriptive path as implemented modern behavior. #to-review |

## Supporting artifacts

| Evidence | What it uniquely supplies | Interpretation |
|---|---|---|
| [Supplied thesis-derived summary](evidence/pv_physics_engine_evidence_summary_for_agent_research_equations_fixed.md) and [provenance](evidence/provenance.json) | Preserved secondary source, attribution, original-copy identity and hash. | Immutable supplied bytes are intentionally exempt from added frontmatter and review tags. Catalogue/provenance metadata describes their role; the original thesis and measurement campaign are separate evidence. #to-review |
| [Legacy preservation inventory](evidence/legacy_inventory.json) | Exact source-file identities and preservation hashes. | Hash agreement establishes unchanged bytes, not successful execution or scientific correctness. #to-review |
| [Capture status and manifests](../tests/fixtures/legacy/capture_status.json) | The selected reference branches, environments, original inputs/outputs and provenance. | Captures support their declared software boundary. Synthetic conditions are not empirical observations, and capture-time review text is not current human approval. #to-review |
| [Platform comparison](evidence/iv_r_platform_comparison.json) | Derived differences and diagnostic outcomes from the original Windows/Linux I–V references. | Read the limits in assumptions IV-04 and reproduction. Same-platform agreement does not imply platform-invariant numbers or scientific acceptance. #to-review |

## Commands, task history and maintenance

#to-review — Installation, application launch, quality checks and API generation
belong in the [root README](../README.md). Exact task attempts, local workarounds,
temporary routines and command results belong in [ExecPlans](../.agents/plans/),
read only when their history affects the selected task. Their presence does not
make an optional procedure or preliminary check part of the scientific evidence.

#to-review — When a claim changes, update its owning record and direct links.
Avoid copying capability tables, equations or command lists into additional files.
Visible `#to-review` markers identify agent-edited entries awaiting human review;
automated validation does not remove that review requirement. The editing policy
is defined in [AGENTS.md](../AGENTS.md).
