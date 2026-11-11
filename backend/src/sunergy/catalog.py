"""Local immutable catalog snapshot read boundary; refresh/normalization are deferred."""

from pathlib import Path

from sunergy.fetcher import read_snapshot


def read_catalog_snapshot(path: Path, *, expected_sha256: str) -> bytes:
    """Read exact bytes; reject changed snapshots before any future normalization."""
    return read_snapshot(path, expected_sha256=expected_sha256)
