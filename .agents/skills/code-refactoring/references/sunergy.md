# SUNERGY evidence routing

Use these as starting locations, not a fixed inventory or accepted design. Paths
and status can change: inspect current files/symbols and follow their references.
Repository paths below resolve from the SUNERGY root. If an index or document is
missing, search by the selected capability, symbol, caller or artifact name and
apply the same evidence assessment. Do not rebuild a whole inventory to proceed.

## Choose the relevant context

| Question | Read/search first | Then verify only what the task needs |
|---|---|---|
| Where does the change belong? | [AGENTS.md](../../../../AGENTS.md), scoped backend/frontend guidance, [architecture](../../../../docs/architecture.md) | Actual imports, use cases, external contracts and generated consumers. |
| What does legacy do? | [Reconciled coverage](../../../../docs/legacy_backend_coverage.md), then [collaborator overview](../../../../docs/legacy-refactorizacion/README.md); query [index.json](../../../../docs/legacy-refactorizacion/index.json) by symbol, file or state | Cited function/callers; data path in `02-historia-del-dato.md`, boundary in `03-contratos.md`, local conventions in `00-convenciones.md`. |
| Who owns a transformation or assumption? | Relevant stable ID in [assumptions](../../../../docs/assumptions.md) and [flowcharts](../../../../docs/flowcharts.md) | Actual contract/model/fetcher, independent capture and separate scientific/empirical status. Update these together when behavior changes. |
| Is it implemented/reachable? | Relevant entries in `04-inventario.md`, `06-lo-que-esta-roto.md`, `07-lo-que-falta.md` in that documentation directory | Current body, callback/dispatch and producer/consumer paths; distinguish broken, unused, never connected, absent and modern placeholder. |
| What changes have been proposed? | `09-refactor-propuesto.md`, `10-decisiones-pendientes.md`, `11-por-donde-empezar.md` | Scope and approval of each decision; compare with current owners and reproduction gates. |
| Can numerical parity be claimed? | [Reproduction contract](../../../../docs/reproduction.md), current `tests/fixtures/legacy/capture_status.json`, actual capture artifacts | Capture provenance/inputs/environment; [regression owner](../../../../backend/src/sunergy/regression.py) and its tests are comparison plumbing, not captured reference values. |
| Are the mathematics/measurements supported? | [Evidence map](../../../../docs/evidence.md), then relevant sections of the supplied summary it links; collaborator `08-tesis-a-codigo.md` when relevant | Exact implemented branch and primary formulation; original measurements and conditions if available. Thesis descriptions and fit quality do not establish general accuracy. |
| Where are source inputs/settings? | `config/paths.yaml`, `config/sources.yaml` and named consumers | Availability, snapshot identities, units, secrets boundary and side effects; declarations marked planned are not adapters. |

For example, query an existing index without loading all of it:

```powershell
$index = Get-Content docs/legacy-refactorizacion/index.json -Raw | ConvertFrom-Json
$index.funciones | Where-Object { $_.name -eq 'IV_R' }
rg -n 'def IV_R|IV_R\(' legacy/Input_File_DIV_Mac_Informe.py legacy/GIU_Final_Presetacion.py
```

This is an optional locator for the current index format, not a required parser or
runtime dependency. Resolve cited line ranges against the current symbol. Reuse
Spanish identifiers/sections without translating the entire documentation set.

## Interpret the collaborator's evidence

The overview explicitly describes static analysis, not a successful run. Labels
`medido` and `verificado` may refer to AST counts or source review, not executed
outputs. Check what was measured, whether its raw artifact/tool is available, and
the scope of the claim. `propuesta` is a design option; `indeterminable` identifies
a gap. A document marked complete can still describe unfinished software.

The contracts chapter describes assumptions at existing boundaries; its missing
contract section and target designs describe changes. Evaluate each clause, not
just the chapter title. Stage/function/contract IDs help navigation but are not
universal or necessarily complete; external modules and modern code need their
own evidence paths.

## Consequential checks

- **Architecture proposals:** the collaborator's Dash-oriented refactor is scoped
  differently from the existing Python/FastAPI/Next scaffold. Reuse behavior and
  data-flow evidence; select current owners from repository policy and actual code.
  Do not repair frozen `legacy/` or add a second UI as a side effect of adopting it.
- **Numerical recommendations:** grid unification, coefficient normalization,
  correction variants, a fixed bootstrap seed and suggested tolerances are choices
  to assess, not accepted defaults. See the open verification register in the
  evidence map and reproduction requirements before physics work. A change making
  a stochastic path deterministic still changes behavior; retain original RNG
  implementation/state and inputs when establishing a controlled baseline.
- **Capture feasibility:** the proposed harness must be checked against actual
  imports and dependencies. Helpers can import Dash/plotting, delete CWD CSVs or
  overwrite uploads. CEC fitting needs PySAM as well as pvlib. Inspect before
  isolated execution; the current application lock is not a legacy environment.
- **Evidence strength:** raw source hashes prove preservation, not execution or
  parity. A synthetic NDH or comparator example is not original weather/measurement
  evidence. Missing workbook, catalog, historical environment or capture artifacts
  should constrain only the branches and claims that rely on them.

Use [docs/reproduction.md](../../../../docs/reproduction.md) for the capture record
and comparison policy rather than duplicating it here. Preserve all records and
chosen grids; never hide mismatches by rounding, sorting, resampling, numeric masks
or relaxed thresholds. A compatibility reproduction of a defect remains a defect.

## Workflow provenance

This skill adapts the supplied `code-modernization` plugin's methods: bounded
slices, source-cited behavior, characterization, explicit differences and
independent verification. The local plugin README declares Apache 2.0 but its
referenced root LICENSE and upstream revision were not supplied. These are newly
written instructions; no plugin code, assets, hooks or report generators are
included. The original tree is not required to run this skill.
