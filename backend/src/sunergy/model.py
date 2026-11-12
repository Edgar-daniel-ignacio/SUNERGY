"""Deterministic IV_R parameterizer. No acquisition, HTTP, plotting or Pydantic."""

from dataclasses import dataclass
from math import isfinite
from typing import Any

import numpy as np
import pvlib

FIT_NAMES = ("I_L_ref", "I_o_ref", "R_s", "R_sh_ref", "a_ref", "Adjust")
DESOTO_NAMES = (
    "photocurrent",
    "saturation_current",
    "resistance_series",
    "resistance_shunt",
    "nNsVth",
)
METRIC_NAMES = ("i_sc", "v_oc", "i_mp", "v_mp", "p_mp", "i_x", "i_xx")


class LegacyCalculationError(ValueError):
    """A fit failed or a calculation is outside the finite compatibility boundary."""


@dataclass(frozen=True)
class LegacyModuleParameters:
    v_mp_v: float
    i_mp_a: float
    v_oc_v: float
    i_sc_a: float
    alpha_sc_percent_per_c: float
    beta_voc_percent_per_c: float
    gamma_pmp_percent_per_c: float
    cells_in_series: int


@dataclass(frozen=True)
class LegacyCondition:
    condition_id: str
    irradiance_w_m2: float
    cell_temperature_c: float
    comparison: tuple[float, float, float, float, float]


@dataclass(frozen=True)
class LegacyCurve:
    condition_id: str
    translation_inputs: dict[str, float]
    parameters: dict[str, float]
    metrics: dict[str, float]
    voltage_v: tuple[float, ...]
    current_a: tuple[float, ...]
    error_row: tuple[float, ...]


def _finite(values: Any) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in result):
        raise LegacyCalculationError("Nonfinite legacy calculation output")
    return result


def legacy_fit_inputs(module: LegacyModuleParameters) -> dict[str, str | float]:
    """The same effective arguments drive the fit and its provenance."""
    return {
        "celltype": "monoSi",
        "v_mp": module.v_mp_v,
        "i_mp": module.i_mp_a,
        "v_oc": module.v_oc_v,
        "i_sc": module.i_sc_a,
        "alpha_sc": (module.alpha_sc_percent_per_c / 100) * module.i_sc_a,
        "beta_voc": (module.beta_voc_percent_per_c / 100) * module.v_oc_v,
        "gamma_pmp": module.gamma_pmp_percent_per_c,
        "cells_in_series": float(module.cells_in_series),
        "temp_ref": 25,
    }


def fit_legacy_iv(module: LegacyModuleParameters) -> dict[str, float]:
    """Preserve forced monoSi/25°C and convert source percentages only for fitting."""
    try:
        values = pvlib.ivtools.sdm.fit_cec_sam(**legacy_fit_inputs(module))
    except (ValueError, RuntimeError, OverflowError) as error:
        raise LegacyCalculationError("Legacy CEC/SAM fit failed") from error
    result = dict(zip(FIT_NAMES, _finite(values), strict=True))
    if (
        result["I_L_ref"] <= 0
        or result["I_o_ref"] <= 0
        or result["R_s"] < 0
        or result["R_sh_ref"] <= 0
        or result["a_ref"] <= 0
    ):
        raise LegacyCalculationError("Legacy fit returned unsupported diode parameters")
    return result


def solve_legacy_iv(
    module: LegacyModuleParameters,
    fit: dict[str, float],
    condition: LegacyCondition,
) -> LegacyCurve:
    """Original returned grid/metrics; omit the discarded reverse-voltage diagnostic."""
    if condition.irradiance_w_m2 <= 0 or condition.cell_temperature_c <= -273.15:
        raise LegacyCalculationError(
            "Positive irradiance and temperature above absolute zero required"
        )
    translation_inputs = {
        "effective_irradiance": condition.irradiance_w_m2,
        "temp_cell": condition.cell_temperature_c,
        "alpha_sc": module.alpha_sc_percent_per_c,
        "a_ref": fit["a_ref"],
        "I_L_ref": fit["I_L_ref"],
        "I_o_ref": fit["I_o_ref"],
        "R_sh_ref": fit["R_sh_ref"],
        "R_s": fit["R_s"],
        "EgRef": 1.121,
        "dEgdT": -0.0002677,
    }
    try:
        translated = pvlib.pvsystem.calcparams_desoto(**translation_inputs)
        parameters = dict(zip(DESOTO_NAMES, _finite(translated), strict=True))
        metrics = {
            key: float(value)
            for key, value in pvlib.pvsystem.singlediode(method="lambertw", **parameters).items()
        }
        _finite(metrics.values())
        voltage = np.linspace(0.0, metrics["v_oc"], 100)
        current = pvlib.pvsystem.i_from_v(voltage=voltage, method="lambertw", **parameters)
        predicted = np.array([metrics[key] for key in METRIC_NAMES[:5]])
        if np.any(predicted <= 0):
            raise LegacyCalculationError("Legacy relative error table has undefined denominator")
        errors = np.round((np.abs(predicted - np.array(condition.comparison)) / predicted) * 100, 2)
        row = (
            *_finite(errors),
            float(np.round(condition.irradiance_w_m2, 2)),
            float(np.round(condition.cell_temperature_c, 2)),
        )
        return LegacyCurve(
            condition.condition_id,
            translation_inputs,
            parameters,
            metrics,
            _finite(voltage),
            _finite(current),
            row,
        )
    except (ValueError, RuntimeError, OverflowError, ZeroDivisionError) as error:
        raise LegacyCalculationError("Legacy diode calculation failed") from error
