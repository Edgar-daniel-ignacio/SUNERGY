import pytest
from pydantic import ValidationError

from sunergy.regression import (
    Artifact,
    CaptureManifest,
    ComparisonOutput,
    QuantitySeries,
    QuantityTolerance,
    compare_outputs,
)


def output(values: list[float], *, unit: str = "A") -> ComparisonOutput:
    # All numbers in these tests are synthetic comparator examples, never golden outputs.
    return ComparisonOutput(
        identifiers=[f"point-{index}" for index in range(len(values))],
        quantities={"current": QuantitySeries(unit=unit, values=values)},
    )


def tolerances() -> dict[str, QuantityTolerance]:
    return {
        "current": QuantityTolerance(
            unit="A",
            absolute=1e-8,
            relative=1e-7,
            rationale="Synthetic plumbing-test threshold only",
        )
    }


def test_quantity_comparison_checks_zero_and_relative_error() -> None:
    assert compare_outputs(output([0, 8]), output([1e-9, 8.0000001]), tolerances()) == []
    differences = compare_outputs(output([0, 8]), output([1e-6, 8.01]), tolerances())
    assert len(differences) == 2


def test_tolerance_is_additive_and_scaled_to_reference() -> None:
    threshold = {
        "current": QuantityTolerance(
            unit="A", absolute=0.75, relative=0.005, rationale="Synthetic formula boundary example"
        )
    }
    assert compare_outputs(output([100]), output([101.25]), threshold) == []
    assert compare_outputs(output([100]), output([101.26]), threshold)


def test_structure_units_and_threshold_coverage_are_exact() -> None:
    reference = output([1, 2])
    reordered = output([1, 2])
    reordered.identifiers.reverse()
    assert "identifiers/order differ" in compare_outputs(reference, reordered, tolerances())
    assert "current: units differ" in compare_outputs(
        reference, output([1, 2], unit="mA"), tolerances()
    )
    differences = compare_outputs(reference, output([1]), tolerances())
    assert (
        "identifiers/order differ" in differences and "current: record count differs" in differences
    )
    assert "tolerance quantity names differ" in compare_outputs(reference, reference, {})


def test_missing_quantities_and_nonfinite_values_fail() -> None:
    reference = output([1])
    candidate = ComparisonOutput(
        identifiers=["point-0"], quantities={"voltage": QuantitySeries(unit="V", values=[1])}
    )
    assert "quantity names differ" in compare_outputs(reference, candidate, tolerances())
    with pytest.raises(ValidationError):
        output([float("inf")])
    with pytest.raises(ValidationError):
        ComparisonOutput(identifiers=["a", "b"], quantities=reference.quantities)


def test_missing_capture_and_unsafe_artifact_cannot_be_accepted() -> None:
    with pytest.raises(ValidationError):
        CaptureManifest.model_validate({"status": "missing_reference_outputs"})
    with pytest.raises(ValidationError):
        Artifact(path="../private.csv", sha256="a" * 64, provenance="synthetic")
