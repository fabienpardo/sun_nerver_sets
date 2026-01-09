\
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Any

from .core import check_never_sets
from .country_store import iter_countries, to_latlon_list
from .archive import archive_witness
from .report import write_report


def run_batch(data_dir: str | Path, out_dir: str | Path, *, limit: float, decl_step: float, hour_step: float) -> Dict[str, Any]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {
        "data_dir": str(Path(data_dir).resolve()),
        "out_dir": str(out_dir.resolve()),
        "visibility_limit_deg": limit,
        "decl_step_deg": decl_step,
        "hour_angle_step_deg": hour_step,
        "countries": [],
    }

    for country in iter_countries(data_dir):
        pts = to_latlon_list(country)
        res = check_never_sets(
            pts,
            visibility_limit_deg=limit,
            decl_step_deg=decl_step,
            hour_angle_step_deg=hour_step,
        )
        write_report(out_dir, country, res)
        archive_witness(out_dir, country, res)
        summary["countries"].append({
            "id": country.id,
            "name": country.name,
            "pass": res.always_daylight_somewhere,
            "worst_altitude_deg": res.witness.worst_max_altitude_deg,
            "margin_deg": res.margin_altitude_deg,
            "witness_decl_deg": res.witness.decl_deg,
            "witness_hour_angle_deg": res.witness.hour_angle_deg,
        })

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch-check 'sun never sets' over country point sets.")
    parser.add_argument("--data", required=True, help="Directory containing country JSON files.")
    parser.add_argument("--out", required=True, help="Output directory.")
    parser.add_argument("--limit", type=float, default=0.0, help="Visibility altitude threshold in degrees.")
    parser.add_argument("--decl-step", type=float, default=0.10, help="Declination step in degrees.")
    parser.add_argument("--hour-step", type=float, default=0.10, help="Hour-angle step in degrees.")
    args = parser.parse_args()

    run_batch(args.data, args.out, limit=args.limit, decl_step=args.decl_step, hour_step=args.hour_step)


if __name__ == "__main__":
    main()
