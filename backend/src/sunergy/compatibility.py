"""Explicit legacy IV_R boundaries; these are compatibility inputs, not accepted physics."""

from typing import Literal

from pydantic import Field, field_validator, model_validator

from sunergy.contracts import BoundaryModel, NonEmpty, SourceRecord
from sunergy.model import DESOTO_NAMES, FIT_NAMES, METRIC_NAMES

LEGACY_IV_MODEL = "legacy-iv-r-v1"
TABLE_COLUMNS = (
    "Condiciones",
    "ISC (Error %)",
    "VOC (Error %)",
    "IM (Error %)",
    "VM (Error %)",
    "POT (Error %)",
    "Irradiancia",
    "T_cell",
)


class LegacyIVModule(BoundaryModel):
    """Source coefficients retain percent/°C; the model owns interpretation."""

    p_mp_w: float = Field(gt=0, description="Retained source rating; unused by IV_R fit")
    v_mp_v: float = Field(gt=0)
    i_mp_a: float = Field(gt=0)
    v_oc_v: float = Field(gt=0)
    i_sc_a: float = Field(gt=0)
    alpha_sc_percent_per_c: float
    beta_voc_percent_per_c: float
    gamma_pmp_percent_per_c: float
    cells_in_series: int = Field(gt=0, strict=True)
    source_reference_temperature_c: float = Field(gt=-273.15)
    source_cell_type: NonEmpty

    @model_validator(mode="after")
    def ordered_points(self) -> "LegacyIVModule":
        if self.v_mp_v >= self.v_oc_v or self.i_mp_a >= self.i_sc_a:
            raise ValueError("MPP voltage/current must be below open/short circuit values")
        return self


class LegacyIVCase(BoundaryModel):
    condition_id: NonEmpty
    effective_irradiance_w_m2: float = Field(gt=0, description="Zero has undefined error table")
    cell_temperature_c: float = Field(gt=-273.15)
    comparison_i_sc_a: float = Field(ge=0)
    comparison_v_oc_v: float = Field(ge=0)
    comparison_i_mp_a: float = Field(ge=0)
    comparison_v_mp_v: float = Field(ge=0)
    comparison_p_mp_w: float = Field(ge=0, description="Comparison input, not necessarily measured")


class LegacyIVRequest(BoundaryModel):
    model_id: Literal["legacy-iv-r-v1"]
    module: LegacyIVModule
    cases: list[LegacyIVCase] = Field(min_length=1)
    source_record: SourceRecord | None = None


class LegacyIVCaseResult(BoundaryModel):
    condition_id: NonEmpty
    desoto_inputs: dict[str, float]
    desoto_parameters: dict[str, float]
    singlediode: dict[str, float]
    voltage_v: list[float] = Field(min_length=100, max_length=100)
    current_a: list[float] = Field(min_length=100, max_length=100)

    @model_validator(mode="after")
    def stage_identity(self) -> "LegacyIVCaseResult":
        if set(self.desoto_parameters) != set(DESOTO_NAMES) or set(self.singlediode) != set(
            METRIC_NAMES
        ):
            raise ValueError("Quantity names must agree with result stage")
        return self


class LegacyIVResponse(BoundaryModel):
    model_id: Literal["legacy-iv-r-v1"] = "legacy-iv-r-v1"
    reproduction_scope: str = "Selected IV_R numerical boundary; full backend reproduction pending"
    scientific_status: str = (
        "Limited equation checks; an original Linux MPP audit target is unmet; "
        "no empirical validation"
    )
    supplied_module: LegacyIVModule
    supplied_cases: list[LegacyIVCase] = Field(min_length=1)
    source_record: SourceRecord | None
    effective_assumptions: dict[str, str | float | int]
    fit_parameters: dict[str, float]
    fit_inputs: dict[str, str | float]
    cases: list[LegacyIVCaseResult] = Field(min_length=1)
    table_columns: list[str]
    table_records: list[list[str | float]]

    @field_validator("fit_parameters")
    @classmethod
    def required_fit_parameters(cls, value: dict[str, float]) -> dict[str, float]:
        if set(value) != set(FIT_NAMES):
            raise ValueError("All six fit parameters must be retained")
        return value

    @model_validator(mode="after")
    def aligned_output(self) -> "LegacyIVResponse":
        labels = [case.condition_id for case in self.supplied_cases]
        if labels != [case.condition_id for case in self.cases]:
            raise ValueError("Result cases must retain supplied labels/order/count")
        if self.table_columns != list(TABLE_COLUMNS) or len(self.table_records) != len(labels):
            raise ValueError("Legacy table columns/order/row count must be preserved")
        for label, row in zip(labels, self.table_records, strict=True):
            if len(row) != len(TABLE_COLUMNS) or row[0] != label:
                raise ValueError("Legacy table must retain row width/label/order")
            if any(not isinstance(value, (float, int)) for value in row[1:]):
                raise ValueError("Legacy table quantities must be numeric")
        return self


class CalculationFailure(BoundaryModel):
    code: Literal["legacy_iv_calculation_failed"] = "legacy_iv_calculation_failed"
    message: str = "The compatibility fit or calculation did not return finite supported outputs."
