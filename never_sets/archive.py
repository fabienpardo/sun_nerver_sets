from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from .core import CoverageResult
from .country_store import CountryDef


def archive_witness(
    out_dir: str | Path,
    country: CountryDef,
    result: CoverageResult,
    *,
    extra: Optional[Dict[str, Any]] = None
) -> Path:
    out_dir = Path(out_dir)
    cdir = out_dir / country.id
    cdir.mkdir(parents=True, exist_ok=True)

    payload: Dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "country": {
            "id": country.id,
            "name": country.name,
            "notes": country.notes,
            "points": [ {"label": p.label, "lat": p.lat, "lon": p.lon} for p in country.points ],
        },
        "result": {
            "always_daylight_somewhere": result.always_daylight_somewhere,
            "limit_altitude_deg": result.limit_altitude_deg,
            "limit_dot": result.limit_dot,
            "margin_altitude_deg": result.margin_altitude_deg,
        },
        "witness": {
            "decl_deg": result.witness.decl_deg,
            "hour_angle_deg": result.witness.hour_angle_deg,
            "worst_max_dot": result.witness.worst_max_dot,
            "worst_max_altitude_deg": result.witness.worst_max_altitude_deg,
            "best_point_indices": list(result.witness.best_point_indices),
            "best_point_labels": [ country.points[i].label for i in result.witness.best_point_indices ],
        }
    }
    if extra:
        payload["extra"] = extra

    out_path = cdir / "witness.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path
