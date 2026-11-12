# Controlled legacy thermal capture

These small redistributable artifacts were independently produced by executing
the original `Temperature_feinman` and `Temperature_NOCT` function AST bodies,
before writing the modern numerical kernels. Inputs are five ordered synthetic
steady-state points; they are not a source weather snapshot or measured evidence.
Two explicit parameter cases per model exercise the UI baseline and an alternate
caller value. All original output values are retained without rounding.

The originals return `None`, mutate the supplied frame by appending `TFeinman` or
`NOCT`, leave original columns intact, and redundantly calculate four times without
a length predicate. Capture preserves those operations. The modern supported
point boundary returns immutable ordered values and validates its restricted
domain; it does not reproduce the full mutable NDH/weather wrapper. Missing
`Poa_global` failures are captured, while modern missing-field failures occur at
the typed boundary. These deliberate boundary differences are not numerical
corrections.

`legacy-faiman-v1` requires explicit positive finite U0/U1 and nonnegative wind
(matching the active callback's positive-coefficient gate). There is no implicit
coefficient default. Baseline 25/6.84 is transcribed from `Feinman_options`.
`legacy-noct-v1` retains `Ta + ((TNMOT - 20)/800) * E`, ignores wind, and restricts
the supported parameter to TNMOT >20 °C. Baseline 43 °C is transcribed from
`NOCT_In`. Neither profile establishes calibrated coefficients, measured cell
temperature, annual-chain reproduction or empirical accuracy.

Sandia remains unavailable. Its six a/b entries have only four deltaT entries;
selectors 5/6 fail for accepted-length frames, and other row counts are ignored.
Next action: capture each exposed selector, accepted length and failure regime
independently, then select an explicit compatibility/corrected profile. Do not
invent missing deltaT values or silently apply the small-input Faiman/NOCT
boundary to Sandia.

Replay from the repository root, after installing the separate capture lock:

```text
.local/legacy-iv-env/Scripts/python.exe scripts/capture_legacy_thermal.py --inputs tests/fixtures/legacy/thermal/captured/inputs.json --output .local/runs/thermal-replay
uv run --locked --offline pytest backend/tests/test_thermal.py
```

Use a new replay output directory each time. Compare `outputs.json` exactly on
the capture host; manifest timestamps/output paths differ by design. The capture
manifest pins source, wrapper, full dependency lock and input/output hashes.
Modern tests use the manifest's explicit temperature tolerance
`abs(actual-reference) <= 1e-12 °C + 1e-12*abs(reference)` for double precision
arithmetic, check record order/columns and reject a deliberately perturbed value.
Cross-platform acceptance requires actual CI results; no historical dependency
environment was supplied.
