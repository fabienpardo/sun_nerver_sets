# Report: United Kingdom (excluding BIOT/Diego Garcia)

- **ID:** `uk_no_biot`
- **Verdict:** **FAIL** ❌
- **Plain-language verdict:** There exists at least one achievable Sun direction where all points are below the visibility limit.
- **Visibility limit (altitude):** `0.000°` (0.000° = geometric sunrise (Sun center above horizon).)
- **Worst-case max altitude:** `-20.607°` (highest Sun altitude achievable at the worst Sun direction)
- **Margin:** `-20.607°` (worst-case max altitude minus the visibility limit)

## Interpretation
- Margin ≥ 0° means the territory satisfies the “never sets” condition for the chosen visibility limit.

## Witness (worst case on sampled grid)
- Declination: `-9.439°` (tilt of the Sun relative to Earth's equator for this direction)
- Hour angle: `111.500°` (Sun direction relative to local noon)
- min over grid of max dot: `-0.351955` (minimum across sampled directions of the max dot)

## Points (anchors)
- Input points: `13` (add extreme boundary points for higher confidence)
- 00. **London** (lat `51.5074`, lon `-0.1278`)
- 01. **Aberdeen** (lat `57.1497`, lon `-2.0943`) ← best at witness
- 02. **Gibraltar** (lat `36.1408`, lon `-5.3536`)
- 03. **Bermuda** (lat `32.2960`, lon `-64.7820`)
- 04. **Anguilla** (lat `18.2208`, lon `-63.0686`)
- 05. **Cayman Islands** (lat `19.3022`, lon `-81.3857`)
- 06. **Falkland Islands (Stanley)** (lat `-51.7963`, lon `-59.5236`)
- 07. **Saint Helena (Jamestown)** (lat `-15.9667`, lon `-5.7167`)
- 08. **Pitcairn Islands** (lat `-25.0667`, lon `-130.1000`)
- 09. **Turks & Caicos** (lat `21.3419`, lon `-71.7979`)
- 10. **Montserrat** (lat `16.7425`, lon `-62.1874`)
- 11. **British Virgin Islands (Road Town)** (lat `18.4207`, lon `-64.6390`)
- 12. **South Georgia (King Edward Point)** (lat `-54.2806`, lon `-36.5092`)

## Notes
UK + selected Overseas Territories, excluding BIOT.

## Glossary
- **Visibility limit:** Altitude threshold used to define “visible” Sun.
- **Worst-case max altitude:** Highest Sun altitude achievable at the most challenging Sun direction.
- **Margin:** Worst-case max altitude minus the visibility limit.
- **Declination:** Sun’s angle north/south of Earth’s equatorial plane.
- **Hour angle:** Sun’s angular distance from local noon.

> Reminder: results depend on the adequacy of the territory point sampling. Use extreme boundary points (W/E/N/S) and split separated regions into components.