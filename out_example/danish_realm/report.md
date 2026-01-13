# Report: Danish Realm (Denmark + Faroe Islands + Greenland)

- **ID:** `danish_realm`
- **Verdict:** **FAIL** ❌
- **Plain-language verdict:** ❌ There exists at least one achievable Sun direction where all points are below the visibility limit.

## At a glance
- **Visibility limit (what counts as “Sun visible”):** `0.000°` (0.000° = geometric sunrise (Sun center above horizon).)
- **Worst-case max altitude:** `-35.099°` (highest Sun altitude achievable at the *hardest* Sun direction)
- **Margin:** `-35.099°` (worst-case max altitude − visibility limit)

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
- Hour angle: `131.100°` (Sun direction relative to local noon)
- min over grid of max dot: `-0.574994` (minimum across sampled directions of the max dot)

## Territory coverage (sampled points)
- Input points: `8` (add extreme boundary points for higher confidence)
- 00. **Copenhagen** (lat `55.6761`, lon `12.5683`)
- 01. **Aarhus** (lat `56.1629`, lon `10.2039`)
- 02. **Tórshavn (Faroe Islands)** (lat `62.0079`, lon `-6.7900`)
- 03. **Nuuk (Greenland)** (lat `64.1814`, lon `-51.6941`)
- 04. **Tasiilaq (Greenland east)** (lat `65.6142`, lon `-37.6368`)
- 05. **Qaanaaq (Greenland north)** (lat `77.4670`, lon `-69.2280`) ← best at witness
- 06. **Qaqortoq (Greenland south)** (lat `60.7195`, lon `-46.0453`)
- 07. **Ilulissat (Greenland)** (lat `69.2167`, lon `-51.1000`)

## Notes
Anchor points across Denmark, Faroes, and Greenland.

## Glossary
- **Visibility limit:** Altitude threshold used to define “visible” Sun.
- **Worst-case max altitude:** Highest Sun altitude achievable at the most challenging Sun direction.
- **Margin:** Worst-case max altitude minus the visibility limit.
- **Declination:** Sun’s angle north/south of Earth’s equatorial plane.
- **Hour angle:** Sun’s angular distance from local noon.

> Reminder: results depend on the adequacy of the territory point sampling. Use extreme boundary points (W/E/N/S) and split separated regions into components.