from __future__ import annotations

import math
from typing import Tuple

import numpy as np

EARTH_OBLIQUITY_DEG = 23.439281
LatLon = Tuple[float, float]


def latlon_to_unit(lat_deg: float, lon_deg: float) -> np.ndarray:
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    clat = math.cos(lat)
    return np.array([clat * math.cos(lon), clat * math.sin(lon), math.sin(lat)], dtype=float)


def sun_vectors_for_decl(decl_deg: float, hour_angles_deg: np.ndarray) -> np.ndarray:
    d = math.radians(decl_deg)
    cd, sd = math.cos(d), math.sin(d)
    h = np.deg2rad(hour_angles_deg)
    return np.vstack([cd * np.cos(h), cd * np.sin(h), np.full_like(h, sd)])
