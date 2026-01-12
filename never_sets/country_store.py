from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Iterable

LatLon = Tuple[float, float]


@dataclass(frozen=True)
class CountryPoint:
    label: str
    lat: float
    lon: float


@dataclass(frozen=True)
class CountryDef:
    id: str
    name: str
    points: List[CountryPoint]
    notes: str = ""


def load_country(path: str | Path) -> CountryDef:
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Country file {p} contains invalid JSON.") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Country file {p} must contain a JSON object.")
    if "id" not in data:
        raise ValueError(f"Country file {p} is missing required field 'id'.")
    if "points" not in data:
        raise ValueError(f"Country file {p} is missing required field 'points'.")

    raw_points = data["points"]
    if not isinstance(raw_points, list) or not raw_points:
        raise ValueError(f"Country file {p} must contain a non-empty list of points.")

    points: List[CountryPoint] = []
    for idx, pt in enumerate(raw_points):
        if not isinstance(pt, dict):
            raise ValueError(f"Point {idx} in {p} must be an object.")
        if "label" not in pt:
            raise ValueError(f"Point {idx} in {p} is missing required field 'label'.")
        if "lat" not in pt or "lon" not in pt:
            raise ValueError(f"Point {idx} in {p} must contain 'lat' and 'lon'.")

        label = pt["label"]
        if not isinstance(label, str):
            raise ValueError(f"Point {idx} in {p} has non-string label.")

        try:
            lat = float(pt["lat"])
            lon = float(pt["lon"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Point {idx} in {p} has non-numeric lat/lon.") from exc

        if not (math.isfinite(lat) and math.isfinite(lon)):
            raise ValueError(f"Point {idx} in {p} has non-finite lat/lon.")

        points.append(CountryPoint(label=label, lat=lat, lon=lon))

    return CountryDef(
        id=str(data["id"]),
        name=str(data.get("name", data["id"])),
        points=points,
        notes=str(data.get("notes", "")),
    )


def iter_countries(data_dir: str | Path) -> Iterable[CountryDef]:
    d = Path(data_dir)
    for p in sorted(d.glob("*.json")):
        yield load_country(p)


def to_latlon_list(country: CountryDef) -> List[LatLon]:
    return [(pt.lat, pt.lon) for pt in country.points]
