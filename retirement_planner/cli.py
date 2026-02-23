from __future__ import annotations

import argparse
import json
from pathlib import Path

from .charts import plot_account_values, plot_spending_sources
from .engine import run_plan
from .schema import ValidationError, validate_plan


SCENARIOS = ("worst", "average", "best")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local retirement plan projections.")
    parser.add_argument("--input", required=True, help="Path to plan JSON")
    parser.add_argument("--output", required=True, help="Output directory for PNG charts")
    parser.add_argument(
        "--scenario",
        choices=SCENARIOS,
        default=None,
        help="Run only one scenario. Default runs worst, average, and best.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        validate_plan(data)
    except ValidationError as exc:
        raise SystemExit(f"Validation failed: {exc}") from exc

    scenarios = [args.scenario] if args.scenario else list(SCENARIOS)

    for scenario in scenarios:
        result = run_plan(data, scenario)
        path1 = plot_account_values(result, output_dir, scenario)
        path2 = plot_spending_sources(result, output_dir, scenario)
        print(f"[{scenario}] wrote {path1}")
        print(f"[{scenario}] wrote {path2}")

    return 0
