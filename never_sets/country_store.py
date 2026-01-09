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
    data = json.loads(p.read_text(encoding="utf-8"))
    points = [CountryPoint(label=pt["label"], lat=float(pt["lat"]), lon=float(pt["lon"])) for pt in data["points"]]
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
