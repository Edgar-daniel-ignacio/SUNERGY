"""Local acquisition and lossless source-field normalization; no modeling interpretation."""

import json
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, JsonValue

from sunergy.compatibility import LegacyIVRequest
from sunergy.contracts import BoundaryModel, NonEmpty, SourceRecord

MODULE_FIELDS = (
    "Pmax",
    "Vmax60",
    "Imax",
    "Voc",
    "Isc",
    "alpha",
    "beta",
    "deltha",
    "cells_in_series",
    "temp_ref",
    "cell_type",
)
CONDITION_COLUMNS = ("Condiciones", "Geff", "Tcell", "Isc", "Voc", "Im", "Vm", "Potencia")


class FailureProbe(BoundaryModel):
    id: NonEmpty
    drop_column: NonEmpty


class LegacyIVSourceDocument(BoundaryModel):
    """Only the inspected source layout; no inferred dataset or alternate edition."""

    schema_version: Literal[1]
    capture_id: NonEmpty | None = None
    provenance: NonEmpty
    module: list[tuple[NonEmpty, JsonValue]] = Field(min_length=11, max_length=11)
    condition_columns: list[NonEmpty]
    conditions: list[list[JsonValue]] = Field(min_length=1)
    failure_cases: list[FailureProbe]


def read_snapshot(path: Path, *, expected_sha256: str) -> bytes:
    """Explicit read; no refresh, write, cache fallback or replacement of saved snapshots."""
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("Source snapshot hash mismatch")
    return raw


def normalize_legacy_iv_input(
    data: dict[str, Any],
    *,
    source_record: SourceRecord | None = None,
) -> LegacyIVRequest:
    """Map the inspected capture layout; retain all rows, units and source values.

    Percent-to-absolute conversion, material/reference overrides and fitting belong
    solely to model.py. Reject changed source layout instead of guessing columns.
    """
    document = LegacyIVSourceDocument.model_validate(data)
    if (
        source_record is not None
        and document.capture_id is not None
        and source_record.source_id != document.capture_id
    ):
        raise ValueError("Source capture identity differs from the selected manifest")
    pairs = document.module
    if [pair[0] for pair in pairs] != list(MODULE_FIELDS):
        raise ValueError("Legacy module keys/order differ from the selected capture contract")
    if document.condition_columns != list(CONDITION_COLUMNS):
        raise ValueError("Legacy condition columns/order differ")
    module = dict(pairs)
    cells = module["cells_in_series"]
    if isinstance(cells, bool) or not isinstance(cells, (int, float)) or int(cells) != cells:
        raise ValueError("Legacy series-cell count must be an integer")
    cases = []
    for values in document.conditions:
        if len(values) != len(CONDITION_COLUMNS):
            raise ValueError("Legacy condition row must retain every column")
        cases.append(
            dict(
                zip(
                    (
                        "condition_id",
                        "effective_irradiance_w_m2",
                        "cell_temperature_c",
                        "comparison_i_sc_a",
                        "comparison_v_oc_v",
                        "comparison_i_mp_a",
                        "comparison_v_mp_v",
                        "comparison_p_mp_w",
                    ),
                    values,
                    strict=True,
                )
            )
        )
    return LegacyIVRequest.model_validate(
        {
            "model_id": "legacy-iv-r-v1",
            "module": {
                "p_mp_w": module["Pmax"],
                "v_mp_v": module["Vmax60"],
                "i_mp_a": module["Imax"],
                "v_oc_v": module["Voc"],
                "i_sc_a": module["Isc"],
                "alpha_sc_percent_per_c": module["alpha"],
                "beta_voc_percent_per_c": module["beta"],
                "gamma_pmp_percent_per_c": module["deltha"],
                "cells_in_series": int(cells),
                "source_reference_temperature_c": module["temp_ref"],
                "source_cell_type": module["cell_type"],
            },
            "cases": cases,
            "source_record": source_record,
        }
    )


def load_legacy_iv_input(path: Path, *, expected_sha256: str, source_id: str) -> LegacyIVRequest:
    raw = read_snapshot(path, expected_sha256=expected_sha256)
    record = SourceRecord(
        source_id=source_id, snapshot_sha256=expected_sha256, record_id="manual-module"
    )
    return normalize_legacy_iv_input(json.loads(raw), source_record=record)
