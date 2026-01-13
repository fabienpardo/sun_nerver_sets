from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


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
