from __future__ import annotations

from dataclasses import dataclass
from typing import List


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
