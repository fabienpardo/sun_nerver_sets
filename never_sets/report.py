from __future__ import annotations

from pathlib import Path
from .core import CoverageResult
from .country_store import CountryDef


def render_markdown_report(country: CountryDef, result: CoverageResult) -> str:
    status = "PASS" if result.always_daylight_somewhere else "FAIL"
    w = result.witness

    lines = [
        f"# Report: {country.name}",
        "",
        f"- **ID:** `{country.id}`",
        f"- **Verdict:** **{status}**",
        f"- **Visibility limit (altitude):** `{result.limit_altitude_deg:.3f}°`",
        f"- **Worst-case max altitude:** `{w.worst_max_altitude_deg:.3f}°`",
        f"- **Margin:** `{result.margin_altitude_deg:.3f}°`",
        "",
        "## Witness (worst case on sampled grid)",
        f"- Declination: `{w.decl_deg:.3f}°`",
        f"- Hour angle: `{w.hour_angle_deg:.3f}°`",
        f"- min over grid of max dot: `{w.worst_max_dot:.6f}`",
        "",
        "## Points (anchors)",
    ]
    for i, pt in enumerate(country.points):
        mark = " ← best at witness" if i in w.best_point_indices else ""
        lines.append(f"- {i:02d}. **{pt.label}** (lat `{pt.lat:.4f}`, lon `{pt.lon:.4f}`){mark}")

    if country.notes:
        lines += ["", "## Notes", country.notes]

    lines.append("")
    lines.append("> Reminder: results depend on the adequacy of the territory point sampling.")
    return "\n".join(lines)


def write_report(out_dir: str | Path, country: CountryDef, result: CoverageResult) -> Path:
    out_dir = Path(out_dir)
    cdir = out_dir / country.id
    cdir.mkdir(parents=True, exist_ok=True)
    p = cdir / "report.md"
    p.write_text(render_markdown_report(country, result), encoding="utf-8")
    return p
