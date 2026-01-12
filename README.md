# never_sets

A research-grade Python toolkit for answering a deceptively simple question:

> **Is the Sun above the horizon somewhere within a territory for *every* achievable Sun direction throughout the year?**

`never_sets` evaluates the **“never sets”** condition using rigorous spherical geometry and a full sweep of Sun directions (declination × hour angle). It is built for reproducibility, transparent inputs, and batch processing across many territories.

---

## ✨ Highlights

- **Full-sky sweep** across all achievable Sun directions over a year (not time zones).
- **Configurable visibility threshold** for geometric sunrise or “visible sunrise” with refraction.
- **Batch execution** over territory JSON files with deterministic outputs.
- **Witness geometry** archived for auditing and visualization.
- **Human-readable reports** generated per territory.

---

## 🧠 Method (short version)

Each territory point is represented as a unit vector `nᵢ` on the sphere. Each Sun direction `s` is a unit vector parameterized by declination **δ** and hour angle **H**. For a given direction we compute:

```
 h(s) = max_i (n_i · s)
```

The territory satisfies the “never sets” criterion (for a given grid) if:

```
min_s h(s) > sin(limit_alt)
```

Where `limit_alt` is the altitude threshold in degrees:
- `0.0°` — geometric sunrise (Sun center above the horizon)
- `-0.833°` — common “visible sunrise” approximation (refraction + solar radius)

Sun directions are scanned over the yearly declination band **[-ε, +ε]** with **ε ≈ 23.44°**, and all hour angles **[0, 360)**.

> ⚠️ Results depend on territory sampling. Use boundary/extreme points (W/E/N/S) rather than centroids only.

---

## 📦 Project layout

- `never_sets/core.py` — geometry + grid sweep
- `never_sets/country_store.py` — JSON territory loading
- `never_sets/archive.py` — witness geometry archive
- `never_sets/report.py` — report generation
- `never_sets/batch.py` — batch CLI runner
- `data/countries/*.json` — territory definitions
- `tests/` — unit tests (`unittest`)

---

## 🚀 Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## ⚡ Quick start

Run a batch check for geometric sunrise:

```bash
python -m never_sets.batch --data ./data/countries --out ./out --limit 0.0
```

Run with refraction-adjusted sunrise:

```bash
python -m never_sets.batch --data ./data/countries --out ./out --limit -0.833
```

Outputs (per run):

- `out/summary.json`
- `out/<country_id>/report.md`
- `out/<country_id>/witness.json`

---

## 🗺️ Territory format (JSON)

Each file in `data/countries/*.json` defines a unique `id`, a human-readable `name`,
and one or more `components` with latitude/longitude points in degrees.

```json
{
  "id": "island_example",
  "name": "Island Example",
  "components": [
    {
      "name": "main",
      "points": [
        {"lat": 65.0, "lon": -20.0},
        {"lat": 66.0, "lon": -19.0},
        {"lat": 66.0, "lon": -21.0}
      ]
    }
  ]
}
```

**Best practices:**
- Use **boundary/extreme points** instead of only centroids.
- Split disconnected regions into separate `components`.
- Keep longitudes in `[-180, 180]` and lat/lon in degrees.

---

## 📊 Interpreting outputs

- **`summary.json`** — pass/fail result per territory, with margin and sampling metadata.
- **`witness.json`** — the worst-case Sun direction and witness point.
- **`report.md`** — short human-readable verdict + glossary.

---

## ✅ Tests

```bash
python -m unittest discover -s tests -v
```

---

## License

This repository is intended for research and educational use. See individual files for details.
