# Circuit-board Multiboard display shelf

Generic open-sided shelf for displaying small, unpowered circuit boards. User-specified **40 mm width, 30 mm depth and 10 mm front lip**; no device-specific outline or screw pattern. Tracked in [#36](https://github.com/ShakataGaNai/b123d/issues/36).

## Geometry contract

All dimensions are mm. XY is the bed; +Y faces Multiboard, +Z is up.

| Feature | Dimension |
| --- | --- |
| Usable deck, width × depth | 40 × 30 |
| Deck, lip and rear-wall thickness | 3 |
| Lip above deck | 10 |
| Back wall total height | 13.5 |
| Shelf body, width × depth × height | 40 × 36 × 13.5 |
| Total envelope including pegs | 40 × 42.5 × 13.5 |
| Peg across flats × projection | 13.5 × 6.5 |
| Peg center spacing | 25 |
| Outside plan corners / exposed edge rounds | R3 / R0.6 |

The clear deck runs Y=0…30 at Z=3. Front lip occupies Y=−3…0;
back wall occupies Y=30…33. Sides remain open. Two pegs resist sideways
rotation and are bottom-aligned with the bed. The 3 mm deck/walls are a
conservative light-PCB starting choice, **not a tested load rating or proof of
minimum stable thickness**. No gussets, board clamp, electrical insulation
certification or powered-board cooling provision is included. Tall boards may
tip; do not mount heavy equipment or rely on this as fall protection.

The [shared finish standard](../MODULES.md#multiboard-holder-finishing) rounds
outside plan corners and all exposed lip/deck perimeter edges. Concave
deck-to-wall support joints and snap mating profiles stay unchanged.
The hidden peg overlap is 0.8 mm to bridge the rounded rear underside.

Attachment imports `models.multiboard.peg.peg` unchanged: fit two compatible
**Multiboard snaps**, one 25 mm grid interval apart, not bare tile Multiholes.
See [module contract](../MODULES.md#multiboard-peg-and-rail-cutout) and
[connector evidence](../../research/objects/multiboard/measured-connectors.md).
Peg provenance is ShakataGaNai's Printables AirTag holder; retain its declared
Attribution–Noncommercial–ShareAlike terms (exact version unresolved) when
sharing derived geometry.

## Build and printing

```sh
uv run python scripts/build.py models/circuit_board_multiboard_shelf --step
```

Print upright as exported, deck bottom on XY. Nonconductive PETG, 0.4 mm nozzle
and 0.2 mm layers are starting assumptions. Inspect peg undersides and deck
perimeters in the slicer. Physical fit, creep, load capacity and print quality
remain unverified; 3MF contains geometry only, not printer settings.

`check()` measures the usable open deck, retained deck/lip/back-wall cores,
front lip height, both octagonal peg sections/locations and actual R3/R0.6 boundaries.
Artifacts are under `outputs/circuit_board_multiboard_shelf/`: same-named STL,
3MF and optional STEP plus `preview.png`, `preview.html` and `report.json`.
STL must be imported as mm; 3MF declares mm.

Rounded-revision verification on 2026-10-16: native/STEP design checks passed,
STL is one watertight, consistently oriented body and millimeter 3MF round trip
passed. Four-view PNG inspected; report timestamp
`2026-10-16T21:37:27.521552+00:00`. Physical load capacity remains untested.
