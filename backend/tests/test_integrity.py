import importlib.util
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from sunergy.catalog import read_catalog_snapshot
from sunergy.configuration import RepositoryPaths, create_run_directory, load_paths, load_sources

ROOT = Path(__file__).resolve().parents[2]


def test_registry_and_distinct_run_directories(tmp_path: Path) -> None:
    paths = load_paths(ROOT)
    assert load_sources(ROOT).sources
    first = create_run_directory(tmp_path, paths)
    second = create_run_directory(tmp_path, paths)
    assert first != second
    assert first.is_dir() and second.is_dir()
    assert first.is_relative_to(tmp_path)


@pytest.mark.parametrize("bad_path", ["../outside", "/absolute", "."])
def test_paths_cannot_escape_repository(bad_path: str) -> None:
    data = load_paths(ROOT).model_dump()
    data["runs"] = Path(bad_path)
    with pytest.raises(ValidationError):
        RepositoryPaths.model_validate(data)


@pytest.mark.parametrize(
    "bad_path",
    ["legacy", "legacy/new", "docs/evidence", "docs", "tests/fixtures/legacy/new", ".local"],
)
def test_mutable_paths_cannot_overlap_protected_evidence_or_other_data(bad_path: str) -> None:
    data = load_paths(ROOT).model_dump()
    data["runs"] = Path(bad_path)
    with pytest.raises(ValidationError, match="separate"):
        RepositoryPaths.model_validate(data)


def test_catalog_snapshot_tampering_is_visible(tmp_path: Path) -> None:
    path = tmp_path / "synthetic.csv"
    raw = b"id,value\nsynthetic,1\n"
    path.write_bytes(raw)
    digest = sha256(raw).hexdigest()
    assert read_catalog_snapshot(path, expected_sha256=digest) == raw
    path.write_bytes(b"changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        read_catalog_snapshot(path, expected_sha256=digest)


def test_preserved_repository_evidence_and_import_boundaries() -> None:
    spec = importlib.util.spec_from_file_location(
        "repository_check", ROOT / "scripts/check_repository.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check_repository(ROOT)
