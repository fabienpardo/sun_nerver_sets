\
from __future__ import annotations

import json
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
        raise ValueError(f"malformed JSON in {p}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"expected object in {p}")
    if "id" not in data:
        raise ValueError(f"missing id in {p}")
    if "points" not in data:
        raise ValueError(f"missing points list in {p}")
    points_raw = data["points"]
    if not isinstance(points_raw, list) or not points_raw:
        raise ValueError(f"missing points list in {p}")
    points = []
    for pt in points_raw:
        if not isinstance(pt, dict):
            raise ValueError(f"invalid point entry in {p}")
        if not {"label", "lat", "lon"}.issubset(pt.keys()):
            raise ValueError(f"missing point fields in {p}")
        points.append(CountryPoint(label=pt["label"], lat=float(pt["lat"]), lon=float(pt["lon"])))
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
