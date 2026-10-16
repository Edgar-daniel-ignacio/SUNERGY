# Architecture and ownership

SUNERGY is a small monorepo. The scaffold supports application development and
explicit boundaries; it contains no migrated PV calculation or validated simulator.

```text
Next.js forms/presentation
       -> same-origin server proxy (health only today)
       -> FastAPI routes -> Python application use cases -> numerical functions
                                    ^                         ^
                         external Pydantic contracts     typed internal data
                                    ^                         ^
                           catalog/weather snapshots and explicit assumptions

FastAPI/Pydantic -> contracts/openapi.json -> generated TypeScript
Legacy source + independent captures -> regression gate (currently missing)
Primary formulations/physical tests -> scientific gate (not performed)
Original measurements -> comparison -> optional calibration (not implemented)
```

## Present owners

| Location | Responsibility and current scope |
|---|---|
| `backend/src/sunergy/contracts.py` | Pydantic external point-request, source record, status contracts. Explicit units; provisional request, no accepted scientific model. |
| `application.py` | Directly callable health/capability and reserved module I–V use cases. |
| `physics.py` | Ordinary typed numerical boundary; raises `SimulationUnavailable`. No legacy, HTTP or plotting dependency. |
| `api.py` | Thin FastAPI transport; health 200, capability states, reserved I–V 501, schema errors 422. |
| `catalog.py` | Exact local snapshot-byte/hash read only; no catalog retrieval/normalization. |
| `configuration.py` | Explicit typed path/source registry loading and unique run-directory allocation. No implicit import-time configuration/network I/O. |
| `regression.py` | Capture metadata and exact-structure/per-quantity comparison plumbing; no real reference captures. |
| `frontend/` | Next.js App Router presentation, visible pending scope, optional health proxy; no numerical engine. |
| `contracts/`, `scripts/` | Generated authoritative OpenAPI export and drift/integrity checks. |
| `docs/evidence/` | Preserved supplied summary, attribution/hash and legacy byte inventory. |

Python packaging lives in root `pyproject.toml`; the wheel packages
`backend/src/sunergy`. Tests and HTTP call the same use cases. YAML contains only
small repository path/source declarations, loaded explicitly by the configuration
module and checked by `scripts/check_repository.py`. Source registry fields marked
planned/missing are not active adapters. UI users never edit YAML.

## Contracts and data flow

FastAPI/Pydantic is the API authority. Export OpenAPI and generate TypeScript after
contract edits; CI checks both artifacts for drift. Generated types provide static
checking, not runtime scientific validation. Next's health control handles
unavailable/malformed upstream responses; frontend builds never contact the API.

The reserved request supports manual specs or an explicit catalog snapshot/record
identity. It takes coordinates and IANA timezone, cell temperature and effective
in-plane irradiance, explicit reference conditions and versioned model selection.
No model is supported yet; all valid requests return 501. Coefficients are named
in A/°C, V/°C, or percent/°C. Original source coefficients remain in original records;
future normalization must record conversions. Never infer Pmp from a Vmp coefficient.
Ambient temperature is not cell temperature. A future weather-driven use case must
add explicit orientation, weather/thermal selection and timestamp/interval
conventions; these are unnecessary for an explicitly supplied point condition.
Measurements are optional and belong to a separate evaluation use case, not a
prerequisite to forward simulation. No upload/calibration endpoint exists yet.

The frontend's server-only `SUNERGY_API_URL` selects the API origin (default
`http://127.0.0.1:8000`). No credentials are required today. Future weather secrets
belong in server environment settings, never requests, public environment
variables, fixtures, source metadata, logs or browser bundles. No generic settings
framework is needed until there are actual settings to consume.

## Storage and provenance

| Class | Location / policy |
|---|---|
| Reviewed/source evidence | `docs/evidence/`; preserve supplied bytes with attribution/hash. New editions get new identities. |
| Small redistributable fixtures | `tests/fixtures/legacy/`; explicit review, capture manifest and hashes required. No golden results today. |
| Original private uploads | Planned `.local/private/`, ignored; preserve bytes/hash, permissions and ownership. |
| Cache | Planned `.local/cache/`, ignored; disposable and never authoritative. Tool caches also ignored. |
| Generated results | `.local/runs/run-*`, ignored; `create_run_directory` allocates isolated names. |

`.gitattributes` retains the observed CRLF legacy representation on Windows and
Unix checkouts so raw preservation hashes remain portable. The supplied summary
disables Git text conversion to preserve its original bytes. No legacy files were
rewritten or renormalized in this task.

Future runs must pin module records, weather snapshots, model/solver identity,
assumptions, input/output hashes, units and time conventions. `retrieve_sam` reads
pvlib-bundled data or a specified file/URL; it is not a continuously updated live
database API. Refresh must explicitly acquire a new versioned snapshot and must
never change saved runs/baselines. The observed legacy catalog is a missing Excel
workbook, not proven to be a pvlib snapshot. Manual specifications remain an
alternative. No live acquisition occurs in current runtime or default tests.

pvlib and PySAM are not installed in the HTTP scaffold because it performs no
physics. The traced CEC fitting calls **already require NREL-PySAM**. The next
independent capture must select/lock compatible pvlib, PySAM/SSC and scientific
dependencies; do not postpone PySAM until full-system modeling or claim this
new lockfile reproduces the unknown historical legacy environment.

## Extension boundaries, not speculative schemas

After relevant reproduction gates, introduce explicit electrical topology for
strings/arrays, inverter/MPPT connections, wiring/losses and batteries. pvlib can
own selected module/solar/thermal calculations, while PySAM may own separately
specified system/performance models; avoid duplicate ownership and test adapters
individually. These responsibilities require evidence before selection.

Technical results must hand energy/power time series, units, interval conventions,
loss boundaries and provenance to a separate economic-assumptions layer. Financing
and cash-flow calculations then consume explicit costs/tariffs/currency/discount
and financing assumptions. No jurisdictional, tariff or financing defaults are
accepted from library examples or the thesis. No financial models exist here.

Map geometry eventually describes placement and coordinate systems; electrical
connectivity remains a separate domain graph. A map package is a presentation
adapter, not the system model. No map library/editor, topology schema, database,
auth, task queue, deployment infrastructure or LLM runtime is introduced now.

Future calibration must keep the uncalibrated baseline, original/normalized
measurements, fitted parameter identities/values, bounds/objective, method/version
and fitting data provenance. Record held-out evaluation separately when available;
goodness of fit alone is not independent validation. No calibration algorithm now.

## Reference decisions

Adapted from CANOE: selective context retrieval, one owner per artifact, traceable
source metadata, stable policy separate from bounded plans, Pydantic at boundaries,
and executable offline verification. Inspected local CANOE `v2.0` revision
`399bb3c8c53712a3fa02dec0f1694419bce5e55a`: `AGENTS.md`, `.agents/PLANS.md`,
`docs/backend_architecture.md`, `config/paths.yaml`, committed `config/sources.yaml`
header/sample and narrow skill trigger conventions. The source registry working
copy differed, so only its committed version informed this scaffold.

[Public CANOE reference](https://github.com/CANOE-main/canoe-transportation/tree/v2.0)
was accessible through a stale web cache; live remote revision could not be verified.
Local HEAD and local origin/v2.0 agreed. Rejected transport/Temoa/SQLite layers,
scenario orchestration, domain policies, tool/skill inventories, YAML-owned UI
inputs, extensive histories/archive machinery and scheduler requirements.

[SUNERGY target](https://github.com/Edgar-daniel-ignacio/SUNERGY/tree/main) was
consulted, but implementation and evidence tracing use the actual local checkout
`ef92cd12fd2c40854c24c1fe7cded9ba351de7df`, including the user's in-progress moves.

Official docs consulted for bounded scaffold choices on 2026-10-15:
[uv projects](https://docs.astral.sh/uv/guides/projects/),
[FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/),
[Pydantic models](https://docs.pydantic.dev/latest/concepts/models/),
[Next.js installation](https://nextjs.org/docs/app/getting-started/installation),
[openapi-typescript](https://openapi-ts.dev/introduction),
[retrieve_sam](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.pvsystem.retrieve_sam.html),
[fit_cec_sam](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.ivtools.sdm.fit_cec_sam.html).
Resolved versions and execution results belong in lockfiles and the task plan.
Current [Starlette TestClient documentation](https://starlette.dev/testclient/)
recommends HTTPX2; the dev dependency uses it to avoid the deprecated HTTPX path.
