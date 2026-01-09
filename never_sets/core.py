\
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Tuple, Optional

import numpy as np

EARTH_OBLIQUITY_DEG = 23.439281
LatLon = Tuple[float, float]


@dataclass(frozen=True)
class Witness:
    decl_deg: float
    hour_angle_deg: float
    worst_max_dot: float
    worst_max_altitude_deg: float
    best_point_indices: Tuple[int, ...]


@dataclass(frozen=True)
class CoverageResult:
    always_daylight_somewhere: bool
    limit_altitude_deg: float
    limit_dot: float
    witness: Witness
    margin_altitude_deg: float


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


def check_never_sets(
    territory_points: Iterable[LatLon],
    *,
    visibility_limit_deg: float = 0.0,
    decl_step_deg: float = 0.10,
    hour_angle_step_deg: float = 0.10,
    obliquity_deg: float = EARTH_OBLIQUITY_DEG,
    return_multiple_best_points: bool = True,
    tie_tol: float = 1e-12,
) -> CoverageResult:
    pts = list(territory_points)
    if not pts:
        raise ValueError("territory_points must contain at least one (lat, lon) pair.")

    N = np.vstack([latlon_to_unit(lat, lon) for lat, lon in pts])  # (K,3)
    limit_dot = math.sin(math.radians(visibility_limit_deg))

    decls = np.arange(-obliquity_deg, obliquity_deg + 1e-12, decl_step_deg, dtype=float)
    Hs = np.arange(0.0, 360.0, hour_angle_step_deg, dtype=float)

    global_min_max_dot = float("inf")
    w_decl = 0.0
    w_H = 0.0
    best_indices = (0,)

    for decl in decls:
        S = sun_vectors_for_decl(float(decl), Hs)  # (3,H)
        dots = N @ S                                # (K,H)
        max_dots = dots.max(axis=0)                 # (H,)
        idx = int(np.argmin(max_dots))
        min_max_dot = float(max_dots[idx])

        if min_max_dot < global_min_max_dot:
            global_min_max_dot = min_max_dot
            w_decl = float(decl)
            w_H = float(Hs[idx])

            col = dots[:, idx]
            best = float(col.max())
            if return_multiple_best_points:
                idxs = np.where(col >= best - tie_tol)[0]
                best_indices = tuple(int(i) for i in idxs.tolist())
            else:
                best_indices = (int(np.argmax(col)),)

    worst_alt = math.degrees(math.asin(float(np.clip(global_min_max_dot, -1.0, 1.0))))
    always = (global_min_max_dot > limit_dot) or math.isclose(global_min_max_dot, limit_dot, abs_tol=1e-15)

    witness = Witness(
        decl_deg=w_decl,
        hour_angle_deg=w_H,
        worst_max_dot=float(global_min_max_dot),
        worst_max_altitude_deg=float(worst_alt),
        best_point_indices=best_indices,
    )

    return CoverageResult(
        always_daylight_somewhere=bool(always),
        limit_altitude_deg=float(visibility_limit_deg),
        limit_dot=float(limit_dot),
        witness=witness,
        margin_altitude_deg=float(worst_alt - visibility_limit_deg),
    )
