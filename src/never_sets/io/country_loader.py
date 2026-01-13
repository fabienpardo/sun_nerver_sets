from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable, List, Tuple

from ..models.country import CountryDef, CountryPoint

LatLon = Tuple[float, float]


def _parse_point_list(
    raw_points: object,
    *,
    path: Path,
    label_required: bool,
    label_prefix: str,
) -> List[CountryPoint]:
    if not isinstance(raw_points, list) or not raw_points:
        raise ValueError(f"Country file {path} must contain a non-empty list of points.")

    points: List[CountryPoint] = []
    for idx, pt in enumerate(raw_points):
        if not isinstance(pt, dict):
            raise ValueError(f"Point {idx} in {path} must be an object.")
        label = pt.get("label")
        if label is None:
            if label_required:
                raise ValueError(f"Point {idx} in {path} is missing required field 'label'.")
            label = f"{label_prefix} {idx + 1}"
        if not isinstance(label, str):
            raise ValueError(f"Point {idx} in {path} has non-string label.")
        if "lat" not in pt or "lon" not in pt:
            raise ValueError(f"Point {idx} in {path} must contain 'lat' and 'lon'.")

        try:
            lat = float(pt["lat"])
            lon = float(pt["lon"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Point {idx} in {path} has non-numeric lat/lon.") from exc

        if not (math.isfinite(lat) and math.isfinite(lon)):
            raise ValueError(f"Point {idx} in {path} has non-finite lat/lon.")

        points.append(CountryPoint(label=label, lat=lat, lon=lon))
    return points


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
    if "points" not in data and "components" not in data:
        raise ValueError(f"Country file {p} must contain 'points' or 'components'.")

    points: List[CountryPoint] = []
    if "points" in data:
        points.extend(
            _parse_point_list(
                data["points"],
                path=p,
                label_required=True,
                label_prefix="point",
            )
        )

    if "components" in data:
        raw_components = data["components"]
        if not isinstance(raw_components, list) or not raw_components:
            raise ValueError(f"Country file {p} must contain a non-empty list of components.")
        for c_idx, component in enumerate(raw_components):
            if not isinstance(component, dict):
                raise ValueError(f"Component {c_idx} in {p} must be an object.")
            comp_name = component.get("name", f"component-{c_idx + 1}")
            if not isinstance(comp_name, str):
                raise ValueError(f"Component {c_idx} in {p} has non-string name.")
            if "points" not in component:
                raise ValueError(f"Component {c_idx} in {p} is missing required field 'points'.")
            points.extend(
                _parse_point_list(
                    component["points"],
                    path=p,
                    label_required=False,
                    label_prefix=comp_name,
                )
            )

    if not points:
        raise ValueError(f"Country file {p} must contain at least one point.")

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
