# Report: United States (incl. selected territories)

- **ID:** `usa`
- **Verdict:** **FAIL** ❌
- **Plain-language verdict:** ❌ There exists at least one achievable Sun direction where all points are below the visibility limit.

## At a glance
- **Visibility limit (what counts as “Sun visible”):** `0.000°` (0.000° = geometric sunrise (Sun center above horizon).)
- **Worst-case max altitude:** `-19.530°` (highest Sun altitude achievable at the *hardest* Sun direction)
- **Margin:** `-19.530°` (worst-case max altitude − visibility limit)

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
- Hour angle: `39.000°` (Sun direction relative to local noon)
- min over grid of max dot: `-0.334295` (minimum across sampled directions of the max dot)

## Territory coverage (sampled points)
- Input points: `13` (add extreme boundary points for higher confidence)
- 00. **Washington, DC** (lat `38.9072`, lon `-77.0369`)
- 01. **Los Angeles** (lat `34.0522`, lon `-118.2437`)
- 02. **Seattle** (lat `47.6062`, lon `-122.3321`)
- 03. **Anchorage** (lat `61.2181`, lon `-149.9003`)
- 04. **Unalaska (Aleutians)** (lat `53.8846`, lon `-166.5320`)
- 05. **Honolulu** (lat `21.3069`, lon `-157.8583`)
- 06. **San Juan (Puerto Rico)** (lat `18.4655`, lon `-66.1057`)
- 07. **Charlotte Amalie (USVI)** (lat `18.3358`, lon `-64.8963`) ← best at witness
- 08. **Pago Pago (American Samoa)** (lat `-14.2756`, lon `-170.7020`)
- 09. **Hagåtña (Guam)** (lat `13.4443`, lon `144.7937`)
- 10. **Wake Island** (lat `19.2814`, lon `166.6470`)
- 11. **Baker Island** (lat `0.2192`, lon `-176.4769`)
- 12. **Howland Island** (lat `0.8076`, lon `-176.6175`)

## Notes
Anchor points across mainland + major territories (illustrative).

## Glossary
- **Visibility limit:** Altitude threshold used to define “visible” Sun.
- **Worst-case max altitude:** Highest Sun altitude achievable at the most challenging Sun direction.
- **Margin:** Worst-case max altitude minus the visibility limit.
- **Declination:** Sun’s angle north/south of Earth’s equatorial plane.
- **Hour angle:** Sun’s angular distance from local noon.

> Reminder: results depend on the adequacy of the territory point sampling. Use extreme boundary points (W/E/N/S) and split separated regions into components.