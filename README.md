# never_sets — mini library

A small, documented library to test whether the Sun is **above the horizon (or "visible")**
somewhere within a set of territory points for **all achievable Sun directions over the year**.

## Core idea (theorem-based)

Represent territory points as unit vectors `n_i` on the unit sphere.
Represent Sun direction `s` as a unit vector parameterized by declination δ and hour angle H.

For each Sun direction, compute:
`h(s) = max_i (n_i · s)`.

The "never sets" condition holds (on the sampled grid) if:

`min_s h(s) > sin(limit_alt)`  (or equality within floating tolerance)

Where `limit_alt` is an altitude threshold in degrees:
- `0.0°` strict geometric sunrise (Sun center above horizon)
- `-0.833°` common visible sunrise approximation (refraction + solar radius)

Sun directions `s` are scanned over the yearly declination band `[-ε,+ε]` with `ε≈23.44°`
and all hour angles `[0,360)`.

## What this library is (and is not)

✅ Rigorous geometric check over all achievable Sun directions (not time zones).  
✅ Multiple daylight definitions via `visibility_limit_deg`.  
✅ Batch runs across country definition JSON files.  
✅ Archives witness geometries and generates short per-country Markdown reports.

⚠️ Results depend on territory sampling.
Use extreme boundary points (W/E/N/S) of each territory component, not only centroids.

❌ Does not model topography, weather, or variable refraction.

## Layout

- `never_sets/core.py` — math + grid search
- `never_sets/country_store.py` — load country definitions from JSON
- `never_sets/archive.py` — archive witness geometry to JSON
- `never_sets/report.py` — generate per-country markdown report
- `never_sets/batch.py` — batch CLI runner (writes reports + witness archives + summary.json)
- `data/countries/*.json` — country definitions (points + metadata)
- `tests/` — unit tests (stdlib `unittest`)

## Quick start

From the repo root:

```bash
python -m never_sets.batch --data ./data/countries --out ./out --limit 0.0
python -m never_sets.batch --data ./data/countries --out ./out --limit -0.833
```

Outputs:
- `out/summary.json`
- `out/<country_id>/report.md`
- `out/<country_id>/witness.json`

## Tests

```bash
python -m unittest -v
```
# sun_nerver_sets
