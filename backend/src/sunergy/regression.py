"""Independent-capture contract and strict comparison plumbing, not a parity claim."""

from pathlib import PurePosixPath

from pydantic import AwareDatetime, Field, JsonValue, field_validator, model_validator

from sunergy.contracts import BoundaryModel, NonEmpty, Sha256


class Artifact(BoundaryModel):
    path: NonEmpty
    sha256: Sha256
    provenance: NonEmpty

    @field_validator("path")
    @classmethod
    def contained_artifact(cls, value: str) -> str:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or "\\" in value or ":" in value:
            raise ValueError("Artifact path must be a contained portable relative path")
        return value


class QuantityTolerance(BoundaryModel):
    unit: NonEmpty
    absolute: float = Field(ge=0)
    relative: float = Field(ge=0, lt=1)
    rationale: NonEmpty


class CaptureManifest(BoundaryModel):
    """Required metadata for a later independently executed legacy reference capture."""

    capture_id: NonEmpty
    captured_at: AwareDatetime
    source_revision: str = Field(pattern=r"^[a-f0-9]{40}$")
    source_files: list[Artifact] = Field(min_length=1)
    entrypoint: NonEmpty
    python_version: NonEmpty
    platform: NonEmpty
    dependencies: dict[str, NonEmpty] = Field(min_length=1)
    dependency_lock: Artifact
    inputs: list[Artifact] = Field(min_length=1)
    outputs: list[Artifact] = Field(min_length=1)
    # Null is explicit: a point IV capture may have no weather/catalog/time series.
    catalog_snapshot: Artifact | None
    weather_snapshot: Artifact | None
    measurement_snapshot: Artifact | None
    units_and_coefficients: dict[str, NonEmpty] = Field(min_length=1)
    time_convention: NonEmpty
    model_solver_grid: dict[str, JsonValue] = Field(min_length=1)
    random_seed: int | None
    randomness_notes: NonEmpty
    capture_method: NonEmpty
    tolerances: dict[str, QuantityTolerance] = Field(min_length=1)
    review_status: NonEmpty


class QuantitySeries(BoundaryModel):
    unit: NonEmpty
    values: list[float] = Field(min_length=1)


class ComparisonOutput(BoundaryModel):
    identifiers: list[NonEmpty] = Field(min_length=1)
    quantities: dict[str, QuantitySeries] = Field(min_length=1)

    @model_validator(mode="after")
    def aligned_records(self) -> "ComparisonOutput":
        if len(set(self.identifiers)) != len(self.identifiers):
            raise ValueError("Identifiers must be unique")
        if any(len(series.values) != len(self.identifiers) for series in self.quantities.values()):
            raise ValueError("Every quantity must retain all records in identifier order")
        return self


def compare_outputs(
    reference: ComparisonOutput,
    candidate: ComparisonOutput,
    tolerances: dict[str, QuantityTolerance],
) -> list[str]:
    """No rounding, sorting, dropping, or resampling. Return every observed mismatch."""
    problems: list[str] = []
    if reference.identifiers != candidate.identifiers:
        problems.append("identifiers/order differ")
    names = set(reference.quantities)
    if names != set(candidate.quantities):
        problems.append("quantity names differ")
    if names != set(tolerances):
        problems.append("tolerance quantity names differ")
    for name in sorted(names & set(candidate.quantities) & set(tolerances)):
        expected = reference.quantities[name]
        actual = candidate.quantities[name]
        tolerance = tolerances[name]
        if expected.unit != actual.unit or expected.unit != tolerance.unit:
            problems.append(f"{name}: units differ")
            continue
        if len(expected.values) != len(actual.values):
            problems.append(f"{name}: record count differs")
            continue
        for index, (left, right) in enumerate(zip(expected.values, actual.values, strict=True)):
            if abs(right - left) > tolerance.absolute + tolerance.relative * abs(left):
                problems.append(f"{name}[{index}]: {right!r} != reference {left!r}")
    return problems
