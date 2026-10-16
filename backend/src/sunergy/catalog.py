"""Local immutable catalog snapshot read boundary; refresh/normalization are deferred."""

from hashlib import sha256
from pathlib import Path


def read_catalog_snapshot(path: Path, *, expected_sha256: str) -> bytes:
    """Read exact bytes; reject changed snapshots before any future normalization."""
    content = path.read_bytes()
    if sha256(content).hexdigest() != expected_sha256:
        raise ValueError("Catalog snapshot hash mismatch")
    return content
