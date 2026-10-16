"""Explicit repository configuration loading; never search CWD or read secrets on import."""

import tempfile
from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field, field_validator, model_validator

from sunergy.contracts import BoundaryModel, NonEmpty


class RepositoryPaths(BoundaryModel):
    evidence: Path
    regression_fixtures: Path
    private_uploads: Path
    cache: Path
    runs: Path

    @field_validator("*")
    @classmethod
    def relative_contained_path(cls, value: Path) -> Path:
        if value.anchor or ".." in value.parts or value == Path("."):
            raise ValueError("Repository paths must be nonempty contained relative paths")
        return value

    @model_validator(mode="after")
    def separate_mutable_data_from_evidence(self) -> "RepositoryPaths":
        immutable = [Path("legacy"), self.evidence, self.regression_fixtures]
        mutable = [self.private_uploads, self.cache, self.runs]
        for index, path in enumerate(mutable):
            for other in immutable + mutable[index + 1 :]:
                if path.is_relative_to(other) or other.is_relative_to(path):
                    raise ValueError("Mutable paths must be separate from evidence and each other")
        return self


class SourceDeclaration(BoundaryModel):
    id: NonEmpty
    status: Literal["available_evidence", "missing", "planned"]
    location: NonEmpty
    description: NonEmpty
    consumer: NonEmpty
    refresh: NonEmpty


class SourceRegistry(BoundaryModel):
    sources: list[SourceDeclaration] = Field(min_length=1)

    @field_validator("sources")
    @classmethod
    def unique_sources(cls, value: list[SourceDeclaration]) -> list[SourceDeclaration]:
        if len({source.id for source in value}) != len(value):
            raise ValueError("Source identifiers must be unique")
        return value


def load_paths(root: Path) -> RepositoryPaths:
    return RepositoryPaths.model_validate(yaml.safe_load((root / "config/paths.yaml").read_text()))


def load_sources(root: Path) -> SourceRegistry:
    return SourceRegistry.model_validate(yaml.safe_load((root / "config/sources.yaml").read_text()))


def create_run_directory(root: Path, paths: RepositoryPaths) -> Path:
    """Every future run gets a unique write directory; no shared result filenames."""
    run_root = (root / paths.runs).resolve()
    if not run_root.is_relative_to(root.resolve()):
        raise ValueError("Run directory escapes repository root")
    protected = [root / "legacy", root / paths.evidence, root / paths.regression_fixtures]
    if any(
        run_root.is_relative_to(path.resolve()) or path.resolve().is_relative_to(run_root)
        for path in protected
    ):
        raise ValueError("Resolved run directory overlaps protected evidence")
    run_root.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="run-", dir=run_root))
