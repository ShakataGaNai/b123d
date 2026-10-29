# Station G2 Multiboard pocket

Rounded top-entry gravity pocket for **BQ Voyage Station G2's original stacked-PCB enclosure**, not G3 or an aftermarket case. The user reports the previous boxy split-front cradle does not work and corrects the **body thickness to 12 mm, excluding screws**. This replacement follows that evidence. [Research and uncertainties](../../../research/objects/bq-voyage-station-g2/README.md); [issue #41](https://github.com/ShakataGaNai/b123d/issues/41), shared finish [#43](https://github.com/ShakataGaNai/b123d/issues/43).

## Dimensions and insertion

All dimensions are mm. X is width, +Y is rearward toward Multiboard, +Z is toward the antenna. Floor underside is Z=0; nominal body is centered at X=Y=0 with bottom Z=2.5.

| Feature | Dimension |
| --- | --- |
| Device body | 110 high × 58 wide × **12 thick**, excluding screws |
| Rear screws | Approximately 5 projection, user-reported |
| Full-body-width rear relief | **6.5 = 5 projection + 1.5 allowance**, Y=6…12.5 |
| Side/front allowances | 0.6 per side / 0.6 front |
| Clear slot | **59.2 × 19.1**, R0.5 inner plan corners |
| Floor / walls | **2.5 / 2.5**, closed floor and continuous walls |
| Insertion depth | **20** above the floor, open top |
| Outside finish | R3 plan corners; R0.6 top, bottom and slot-mouth edges |
| Pegs | Two, 13.5 across flats × 6.5 projection, 25 center spacing |
| Holder envelope with pegs | **64.2 × 30.6 × 22.5** |

The R0.5 pocket corners are smaller than the 0.6 side allowance: they preserve both the square body envelope and the full **58 mm-wide** screw insertion band, including its 1.5 mm rear allowance. No screw locations or diameters are guessed. The web page's ambiguous 22 mm thickness is retained in research as superseded source evidence, not used as body thickness.

Mount antenna-up, screen outward. Lower the unplugged device vertically into the slot; lift straight up to remove. The continuous floor supports the entire nominal body footprint. There are no old open-front claws, lowered lips, or split shelves. The seating-floor edge remains sharp to preserve its functional datum.

The floor is deliberately closed: USB center/plug dimensions have not been measured, so no speculative opening is provided. **Remove the device for bottom USB access.** Connectors in the lowest 20 mm may be covered. Upper device and antenna stay exposed. Rear screws are assumed to remain within the 58 × 110 mm silhouette. Gravity retention only: indoors and upright, not inverted or in vehicles.

## Attachment and printing

Uses the unchanged [`models.multiboard.peg.peg`](../../MODULES.md#multiboard-peg-and-rail-cutout) interface on 25 mm horizontal centers. These insert into compatible **Multiboard snaps**, not directly into tile Multiholes. Pegs are bottom-aligned at Z=0. Their 0.8 mm root overlap bridges the rounded underside and stays inside the rear wall, outside the screw corridor. The reused interface's [source attribution and unresolved CC BY-NC-SA version](../../../research/objects/multiboard/measured-connectors.md) apply when sharing source-derived geometry.

Print floor-down on XY. Inspect horizontal peg overhangs, support strategy and lower-edge fit in the slicer. Material and thermal suitability require evaluation for the real unit's duty cycle; do not support it by antenna leverage. Status remains **unverified-fit**, `print_tested = false`; no physical fit, load, thermal or vibration qualification is claimed.

## Checks and build

`build()` is import-side-effect-free. `check(shape)` checks one valid solid, bounds, the 12 mm body's complete insertion sweep, the full-width screw sweep including allowance, rounded slot, complete body-bearing floor and seat height, continuous front/side/rear walls, R3/R0.5 plan radii, R0.6 outer/mouth edge radii, and both octagonal peg sections and locations. Wall probes avoid cosmetic rounds rather than requiring square corners at rounded surfaces.

Build command:

```sh
uv run python scripts/build.py models/multiboard/station_g2 --step
```

The corrected rounded-slot revision passed native/STEP checks, one-body watertight STL and millimeter 3MF round trip on 2026-10-16. Four-view PNG inspected: narrow continuous slot, closed floor and two peg roots. Report timestamp `2026-10-16T21:33:29.811800+00:00`, under `outputs/multiboard/station_g2/`. Physical fit remains unverified; numerical tolerances are not print compensation.

### Superseded validation history

On 2026-10-16 the **old 22 mm-body, split-front cradle** passed geometric/export checks (historical report `2026-10-16T21:17:11.957115+00:00`). The user subsequently reported it does not work. Those results do not establish physical compatibility and no physical print success was recorded. The current 12 mm-body revision is verified separately above.
