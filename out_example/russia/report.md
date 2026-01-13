# Report: Russia (Russian Federation)

- **ID:** `russia`
- **Verdict:** **FAIL** ❌
- **Plain-language verdict:** ❌ There exists at least one achievable Sun direction where all points are below the visibility limit.

## At a glance
- **Visibility limit (what counts as “Sun visible”):** `0.000°` (0.000° = geometric sunrise (Sun center above horizon).)
- **Worst-case max altitude:** `-25.746°` (highest Sun altitude achievable at the *hardest* Sun direction)
- **Margin:** `-25.746°` (worst-case max altitude − visibility limit)

## How to read this report
- Imagine sweeping the Sun across all physically achievable directions.
- At each direction, find the **single best point** in the territory (highest Sun altitude).
- The **worst-case max altitude** is the *lowest* of those best-case values.
- The **margin** tells you how far above/below your visibility limit the worst case is.

## Interpretation
- If the margin is **≥ 0°**, then *at least one point* in the territory keeps the Sun above the visibility limit for **every achievable Sun direction**. If the margin is **< 0°**, there exists a Sun direction where **all points** are below the visibility limit.

## Simple picture (conceptual)
```
Sun altitude
    ^
    |           .   best point for this Sun direction
    |        .
    |     .
    |  .
    |.
    +--------------------> Sun direction sweep
        ^
        | worst-case max altitude (lowest of the best points)
```


## Witness (worst case on sampled grid)
- Declination: `-23.439°` (tilt of the Sun relative to Earth's equator for this direction)
- Hour angle: `278.500°` (Sun direction relative to local noon)
- min over grid of max dot: `-0.434385` (minimum across sampled directions of the max dot)

## Territory coverage (sampled points)
- Input points: `9` (add extreme boundary points for higher confidence)
- 00. **Kaliningrad** (lat `54.7104`, lon `20.4522`)
- 01. **Moscow** (lat `55.7558`, lon `37.6173`)
- 02. **Yekaterinburg** (lat `56.8389`, lon `60.6057`)
- 03. **Novosibirsk** (lat `55.0084`, lon `82.9357`)
- 04. **Irkutsk** (lat `52.2869`, lon `104.3050`)
- 05. **Vladivostok** (lat `43.1155`, lon `131.8855`)
- 06. **Petropavlovsk-Kamchatsky** (lat `53.0241`, lon `158.6436`)
- 07. **Anadyr (Chukotka)** (lat `64.7337`, lon `177.5089`) ← best at witness
- 08. **Sochi** (lat `43.5855`, lon `39.7231`)

## Notes
Anchor points from Kaliningrad to Chukotka, plus intermediate cities.

## Glossary
- **Visibility limit:** Altitude threshold used to define “visible” Sun.
- **Worst-case max altitude:** Highest Sun altitude achievable at the most challenging Sun direction.
- **Margin:** Worst-case max altitude minus the visibility limit.
- **Declination:** Sun’s angle north/south of Earth’s equatorial plane.
- **Hour angle:** Sun’s angular distance from local noon.

> Reminder: results depend on the adequacy of the territory point sampling. Use extreme boundary points (W/E/N/S) and split separated regions into components.