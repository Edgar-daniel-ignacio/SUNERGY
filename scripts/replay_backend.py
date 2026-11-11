"""Replay independently captured IV_R cases against the modern backend, offline."""

import argparse
import json
from pathlib import Path

from sunergy.replay import replay_iv_capture

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, action="append")
    args = parser.parse_args()
    manifests = args.manifest or [
        ROOT / "tests/fixtures/legacy/iv_r/captured/manifest.json",
        ROOT / "tests/fixtures/legacy/iv_r/captured_alternate/manifest.json",
    ]
    results = []
    for path in manifests:
        result, problems = replay_iv_capture(ROOT, path)
        results.append(
            {
                "manifest": str(path.relative_to(ROOT)),
                "cases": len(result.cases),
                "curve_points": sum(len(case.voltage_v) for case in result.cases),
                "passed": not problems,
                "differences": problems,
            }
        )
    print(json.dumps(results, indent=2))
    if any(not result["passed"] for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
