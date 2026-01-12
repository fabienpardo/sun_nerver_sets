from __future__ import annotations

from pathlib import Path
from .core import CoverageResult
from .country_store import CountryDef


def render_markdown_report(country: CountryDef, result: CoverageResult) -> str:
    status = "PASS" if result.always_daylight_somewhere else "FAIL"
    verdict_icon = "✅" if result.always_daylight_somewhere else "❌"
    w = result.witness
    limit = result.limit_altitude_deg
    limit_desc = (
        "0.000° = geometric sunrise (Sun center above horizon)."
        if abs(limit) < 1e-9
        else "-0.833° ≈ common visible sunrise (refraction + solar radius)."
        if abs(limit + 0.833) < 1e-9
        else "Custom threshold for visible Sun altitude."
    )
    interpretation = (
        "Margin ≥ 0° means the territory satisfies the “never sets” condition "
        "for the chosen visibility limit."
    )
    plain_verdict = (
        "At least one point in this territory has the Sun above the horizon for every achievable Sun direction."
        if result.always_daylight_somewhere
        else "There exists at least one achievable Sun direction where all points are below the visibility limit."
    )

    lines = [
        f"# Report: {country.name}",
        "",
        f"- **ID:** `{country.id}`",
        f"- **Verdict:** **{status}** {verdict_icon}",
        f"- **Plain-language verdict:** {plain_verdict}",
        f"- **Visibility limit (altitude):** `{result.limit_altitude_deg:.3f}°` ({limit_desc})",
        f"- **Worst-case max altitude:** `{w.worst_max_altitude_deg:.3f}°` (highest Sun altitude achievable at the worst Sun direction)",
        f"- **Margin:** `{result.margin_altitude_deg:.3f}°` (worst-case max altitude minus the visibility limit)",
        "",
        "## Interpretation",
        f"- {interpretation}",
        "",
        "## Witness (worst case on sampled grid)",
        f"- Declination: `{w.decl_deg:.3f}°` (tilt of the Sun relative to Earth's equator for this direction)",
        f"- Hour angle: `{w.hour_angle_deg:.3f}°` (Sun direction relative to local noon)",
        f"- min over grid of max dot: `{w.worst_max_dot:.6f}` (minimum across sampled directions of the max dot)",
        "",
        "## Points (anchors)",
        f"- Input points: `{len(country.points)}` (add extreme boundary points for higher confidence)",
    ]
    best_indices_set = set(w.best_point_indices)
    for i, pt in enumerate(country.points):
        mark = " ← best at witness" if i in best_indices_set else ""
        lines.append(f"- {i:02d}. **{pt.label}** (lat `{pt.lat:.4f}`, lon `{pt.lon:.4f}`){mark}")

    if country.notes:
        lines += ["", "## Notes", country.notes]

    lines += [
        "",
        "## Glossary",
        "- **Visibility limit:** Altitude threshold used to define “visible” Sun.",
        "- **Worst-case max altitude:** Highest Sun altitude achievable at the most challenging Sun direction.",
        "- **Margin:** Worst-case max altitude minus the visibility limit.",
        "- **Declination:** Sun’s angle north/south of Earth’s equatorial plane.",
        "- **Hour angle:** Sun’s angular distance from local noon.",
        "",
        "> Reminder: results depend on the adequacy of the territory point sampling. "
        "Use extreme boundary points (W/E/N/S) and split separated regions into components.",
    ]
    return "\n".join(lines)


def write_report(out_dir: str | Path, country: CountryDef, result: CoverageResult) -> Path:
    out_dir = Path(out_dir)
    cdir = out_dir / country.id
    cdir.mkdir(parents=True, exist_ok=True)
    p = cdir / "report.md"
    p.write_text(render_markdown_report(country, result), encoding="utf-8")
    return p
