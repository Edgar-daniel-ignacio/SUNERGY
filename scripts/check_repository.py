"""Offline repository configuration/evidence checks; never import or execute legacy."""

import ast
import json
from hashlib import sha256
from pathlib import Path

from sunergy.configuration import load_paths, load_sources

ROOT = Path(__file__).resolve().parents[1]


def check_repository(root: Path) -> None:
    paths = load_paths(root)
    sources = load_sources(root)
    for declaration in sources.sources:
        if declaration.status == "available_evidence":
            if not (root / declaration.location).exists():
                raise ValueError(f"Missing declared evidence: {declaration.id}")
    evidence = root / paths.evidence
    provenance = json.loads((evidence / "provenance.json").read_text(encoding="utf-8"))
    document = evidence / provenance["preserved_filename"]
    if sha256(document.read_bytes()).hexdigest() != provenance["sha256"]:
        raise ValueError("Supplied evidence bytes changed")
    inventory = json.loads((evidence / "legacy_inventory.json").read_text(encoding="utf-8"))
    recorded = {entry["path"] for entry in inventory["files"]}
    actual = {p.relative_to(root).as_posix() for p in (root / "legacy").rglob("*") if p.is_file()}
    if recorded != actual:
        raise ValueError("Legacy file inventory changed")
    for entry in inventory["files"]:
        if sha256((root / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"Legacy source changed: {entry['path']}")
    # Prevent accidental coupling to legacy/Dash without importing either tree.
    for path in (root / "backend/src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            if any(name.split(".")[0] in {"legacy", "dash", "CurvaIV"} for name in names):
                raise ValueError(f"Forbidden production import in {path}")
    capture_status = json.loads(
        (root / paths.regression_fixtures / "capture_status.json").read_text(encoding="utf-8")
    )
    if capture_status["status"] != "missing_reference_outputs":
        raise ValueError("Review capture status/check when real reference outputs are added")


if __name__ == "__main__":
    check_repository(ROOT)
    print("Configuration, preserved evidence, legacy hashes, and import boundaries pass")
