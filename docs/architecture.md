---
title: Backend architecture and ownership
role: Current layer, interface, configuration and artifact ownership
retrieve_when: Changing an owner, application use case, integration seam or storage boundary
read_scope: Relevant boundary and its direct producers and consumers
authority: Maintained design; code and tests establish implemented behavior
verify: Check named modules and contracts; use the coverage map for reproduction status
---

# Backend architecture and ownership

Python owns calculations and application use cases; FastAPI transports requests;
Next.js presents results. The implemented backend contains selected compatibility
point calculations, not an annual or full-system simulator. The [coverage map](legacy_backend_coverage.md)
owns capability status; this document owns placement and boundaries.

## Current owners

All module paths below are relative to `backend/src/sunergy/`.

| Owner | Responsibility and boundary |
|---|---|
| `fetcher.py` | Verify local snapshot bytes against an expected hash and map the inspected legacy input layout. Preserve source values, identity and order; no coefficient interpretation, fitting or missing-value fill. |
| `catalog.py` | Existing catalogue-byte reader delegates to the same fetcher snapshot owner. No live catalogue acquisition or workbook adapter is implemented. |
| `model.py` | IV_R parameterization: fit conversions and forced settings, De Soto translation, Lambert W grid/metrics and legacy error calculation. Ordinary typed internals; no HTTP, plotting, acquisition or legacy imports. |
| `thermal.py` | Explicit Faiman/NOCT point parameters and ordered immutable numerical results. No weather acquisition, timestamp interpretation or annual orchestration. |
| `compatibility.py`, `thermal_contracts.py` | Pydantic boundaries for supported compatibility inputs/results. Units, required fields, finite domains and cross-field structure are validated here. |
| `application.py` | Directly callable use cases coordinate validated inputs and numerical owners. HTTP and Python callers use the same calculations. |
| `api.py` | Thin transport: compatibility IV_R results, schema/calculation errors, health and capability responses. The reserved general simulator remains unavailable. |
| `contracts.py`, `physics.py` | Shared external shapes and the explicitly unavailable general module-IV seam. Its provisional schema is not an accepted scientific model or evidence of implemented calculation. |
| `configuration.py` | Explicit loading of typed repository path/source declarations and isolated run-directory allocation. No import-time configuration or network acquisition. |
| `regression.py`, `replay.py` | Capture metadata/integrity, exact structural and per-quantity comparisons, and explicit platform/reference selection. They establish software compatibility within a recorded boundary. |

## Acquisition versus modeling

Normalization ends at faithful source parsing, field mapping, identity, units and
record preservation. The model owns interpretations such as percent-to-absolute
conversion, fit reference conditions, material overrides and solver/grid selection.
No default, imputation, aggregation or calibration may hide in source normalization.
The operation records in [assumptions](assumptions.md) explain the actual choices.

Original source records, normalized inputs, fitted parameters and comparison inputs
are distinct. The IV_R compatibility request intentionally retains source-percent
coefficients because the legacy consumers interpret them inconsistently. The
modern boundary does not silently repair that inconsistency.

## Configuration and contract authority

| Concern | Authoritative home | Consumer / limit |
|---|---|---|
| Artifact paths | `config/paths.yaml`, validated by `configuration.py` | Repository integrity and isolated run allocation. It does not select equations or user inputs. |
| Source identity, availability and refresh | `config/sources.yaml`, validated by `configuration.py` | Evidence declarations; a `planned` source is not an implemented adapter. Captures additionally pin exact snapshots in their manifests. |
| Runtime settings | Server environment where actually consumed | The frontend's server-only `SUNERGY_API_URL` selects the health-proxy origin. No weather credentials are consumed by the supported point workflows. |
| Requests and results | Owning Pydantic contracts; FastAPI OpenAPI for HTTP | Exported OpenAPI generates TypeScript. Do not add a competing YAML or handwritten frontend schema. |
| Modeling behavior | Explicit versioned profile and its Python owner | Assumptions document meaning/support; they do not execute or approve a model. No scientifically accepted default is inferred from compatibility. |

FastAPI/Pydantic owns `contracts/openapi.json`; frontend types are generated from
it. Next.js has no scientific or financial calculations. Supported development,
launch and synchronization commands belong in [README](../README.md), not in the
modeling evidence.

## Storage and provenance

| Artifact class | Location and ownership |
|---|---|
| Original source evidence | `legacy/` remains byte-preserved and read-only. Curated investigation and supplied evidence have distinct authority described in [evidence](evidence.md). |
| Reviewed software references | `tests/fixtures/legacy/` contains deliberately selected redistributable original-source captures, manifests and hashes. It is not a home for private measurements or full catalogues. |
| Private uploads and caches | Ignored `.local/private/` and `.local/cache/` are reserved locations, not implemented ingestion/acquisition services. |
| Generated runs | Ignored `.local/runs/run-*`; `create_run_directory` allocates separate destinations. Reference snapshots must not be replaced by refresh or cache reuse. |

The application lock owns application dependencies. The separate capture lock owns
the inspected legacy environment. Manifests identify actual source, wrapper,
environment, inputs and outputs. A reconstructed environment does not establish
the unknown historical runtime.

## Extension boundaries

Annual/weather/measurement integrations are not implemented by the point kernels.
Systems, financial assessment and layout require their own contracts after the
prerequisite gates. No database, auth, queue, generic component schema or alternate
UI is reserved for hypothetical future work.

The useful CANOE practices here are source/model separation, selective retrieval,
explicit artifact ownership, assumptions and provenance. Transport-specific paths,
scenario configuration and SQLite/Temoa infrastructure do not belong in SUNERGY.
The task record retains the comparison history.
