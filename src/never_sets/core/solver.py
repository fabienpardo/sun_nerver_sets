from __future__ import annotations

import math
from typing import Iterable, Optional, Tuple

import numpy as np

from .geometry import EARTH_OBLIQUITY_DEG, LatLon, latlon_to_unit
from ..models.result import CoverageResult, Witness


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
    if decl_step_deg <= 0:
        raise ValueError("decl_step_deg must be positive.")
    if hour_angle_step_deg <= 0:
        raise ValueError("hour_angle_step_deg must be positive.")
    if not (0.0 <= obliquity_deg <= 90.0):
        raise ValueError("obliquity_deg must be between 0 and 90 degrees.")
    if not (-90.0 <= visibility_limit_deg <= 90.0):
        raise ValueError("visibility_limit_deg must be between -90 and 90 degrees.")
    if tie_tol < 0:
        raise ValueError("tie_tol must be non-negative.")

    for lat, lon in pts:
        if not (math.isfinite(lat) and math.isfinite(lon)):
            raise ValueError("territory_points must contain finite latitude/longitude values.")
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("territory_points must have latitude within [-90, 90].")
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("territory_points must have longitude within [-180, 180].")

    N = np.vstack([latlon_to_unit(lat, lon) for lat, lon in pts])  # (K,3)
    limit_dot = math.sin(math.radians(visibility_limit_deg))

    decls = np.arange(-obliquity_deg, obliquity_deg + 1e-12, decl_step_deg, dtype=float)
    Hs = np.arange(0.0, 360.0, hour_angle_step_deg, dtype=float)

    h = np.deg2rad(Hs)
    cos_h = np.cos(h)
    sin_h = np.sin(h)
    d = np.deg2rad(decls)
    cd = np.cos(d)
    sd = np.sin(d)

    sun_vectors = np.stack(
        [
            cd[:, None] * cos_h[None, :],
            cd[:, None] * sin_h[None, :],
            np.broadcast_to(sd[:, None], (decls.size, Hs.size)),
        ],
        axis=1,
    )  # (D,3,H)

    dots = np.einsum("kq,dqh->dkh", N, sun_vectors)  # (D,K,H)
    max_dots = dots.max(axis=1)  # (D,H)
    hour_idx_per_decl = np.argmin(max_dots, axis=1)  # (D,)
    min_max_per_decl = max_dots[np.arange(decls.size), hour_idx_per_decl]

    decl_idx = int(np.argmin(min_max_per_decl))
    hour_idx = int(hour_idx_per_decl[decl_idx])

    global_min_max_dot = float(min_max_per_decl[decl_idx])
    w_decl = float(decls[decl_idx])
    w_H = float(Hs[hour_idx])

    col = dots[decl_idx, :, hour_idx]
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
