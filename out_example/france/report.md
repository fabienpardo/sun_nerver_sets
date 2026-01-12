# Report: France (French Republic)

- **ID:** `france`
- **Verdict:** **PASS** ✅
- **Plain-language verdict:** At least one point in this territory has the Sun above the horizon for every achievable Sun direction.
- **Visibility limit (altitude):** `0.000°` (0.000° = geometric sunrise (Sun center above horizon).)
- **Worst-case max altitude:** `19.917°` (highest Sun altitude achievable at the worst Sun direction)
- **Margin:** `19.917°` (worst-case max altitude minus the visibility limit)

## Interpretation
- Margin ≥ 0° means the territory satisfies the “never sets” condition for the chosen visibility limit.

## Witness (worst case on sampled grid)
- Declination: `23.061°` (tilt of the Sun relative to Earth's equator for this direction)
- Hour angle: `111.500°` (Sun direction relative to local noon)
- min over grid of max dot: `0.340661` (minimum across sampled directions of the max dot)

## Points (anchors)
- Input points: `12` (add extreme boundary points for higher confidence)
- 00. **Paris** (lat `48.8566`, lon `2.3522`)
- 01. **Guadeloupe (Basse-Terre)** (lat `16.2650`, lon `-61.5510`)
- 02. **Martinique (Fort-de-France)** (lat `14.6415`, lon `-61.0242`)
- 03. **French Guiana (Cayenne)** (lat `4.9224`, lon `-52.3135`)
- 04. **Saint-Pierre-et-Miquelon** (lat `46.7800`, lon `-56.1700`)
- 05. **Réunion (Saint-Denis)** (lat `-20.8821`, lon `55.4507`)
- 06. **Mayotte (Mamoudzou)** (lat `-12.7806`, lon `45.2278`)
- 07. **Tahiti (Papeete)** (lat `-17.5516`, lon `-149.5585`)
- 08. **Wallis & Futuna (Mata-Utu)** (lat `-13.2825`, lon `-176.1736`)
- 09. **New Caledonia (Nouméa)** (lat `-22.2700`, lon `166.4400`) ← best at witness
- 10. **Kerguelen Islands** (lat `-49.3500`, lon `70.2100`)
- 11. **Clipperton Island** (lat `10.2833`, lon `-109.2167`)

## Notes
Anchor points across metropolitan France and overseas territories/collectivities.

## Glossary
- **Visibility limit:** Altitude threshold used to define “visible” Sun.
- **Worst-case max altitude:** Highest Sun altitude achievable at the most challenging Sun direction.
- **Margin:** Worst-case max altitude minus the visibility limit.
- **Declination:** Sun’s angle north/south of Earth’s equatorial plane.
- **Hour angle:** Sun’s angular distance from local noon.

> Reminder: results depend on the adequacy of the territory point sampling. Use extreme boundary points (W/E/N/S) and split separated regions into components.