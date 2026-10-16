"""Export the authoritative API schema without starting HTTP or loading legacy code."""

import argparse
import json
from pathlib import Path

from sunergy.api import app

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "contracts/openapi.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = json.dumps(app.openapi(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != content:
            raise SystemExit("OpenAPI is stale: uv run python scripts/export_openapi.py")
        print("OpenAPI matches FastAPI contracts")
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(content, encoding="utf-8", newline="\n")
        print("Exported contracts/openapi.json")


if __name__ == "__main__":
    main()
