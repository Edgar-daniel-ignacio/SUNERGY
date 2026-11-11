# Selected fixtures only

`legacy/capture_status.json` records partial coverage and links independent
original-source IV_R and Faiman/NOCT captures. Inputs are deliberately selected
manual/synthetic cases, not weather snapshots or empirical measurements.
New captures require `CaptureManifest` from `sunergy.regression`, reviewed
source/input/output hashes, provenance, redistribution rights, and documented
per-quantity tolerances. Capture independently from the chosen legacy function;
never generate expected values using the new implementation.

Only intentionally reviewed files in this directory are candidates for tracking.
Do not place private uploads, credentials, original user measurements, full
catalogs, or generated runs here. Synthetic data in backend unit tests tests
comparison plumbing and is never scientific evidence. The original-source outputs
here are valid software reproduction references only for their declared boundaries;
see [reproduction](../../docs/reproduction.md) for replay, tolerances and gaps.
