# Unit C6L Multiboard pocket

Simple top-entry gravity holder for **M5Stack Unit C6L U202**. Rounded left/right
outside corners, flat closed floor, and the existing Multiboard snap peg. No
latch, rail or exact shell-contour reconstruction. Hardware revision unknown;
printed and validated good by the user on 2026-10-16. Current geometry is approved.

## Dimensions

All dimensions are mm.

| Feature | Dimension |
|---|---:|
| Nominal device width × thickness | 24 × 8 |
| Clear slot width × thickness | 24.8 × 8.8 |
| Insertion depth, rim to floor | 12 |
| Floor / normal wall thickness | 2.5 / 2.5 |
| Inner / outer XY corner radii | 0.5 / 3 |
| Pocket body width × thickness × height | 29.8 × 13.8 × 14.5 |
| Rear peg across flats / projection | 13.5 / 6.5 |
| Total envelope including peg | 29.8 × 20.3 × 14.5 |

[M5Stack's mechanical drawing](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1185/U202-MODEL-SIZE-unit-2sma.pdf)
establishes the 24 × 8 cross-section, 56 shell height and 62 height including
antenna connector stubs, excluding attached antennas. The user's approximate
23 mm width is superseded by 24 mm. Full evidence, revision limitations and
allowances are in the [research record](../../research/objects/m5stack-unit-c6l/README.md).

The 0.4 per-side clearance is an uncalibrated FDM allowance, not a verified
printer tolerance. A conservative square-cornered 24 × 8 device envelope clears
the rounded slot. The 2.5 wall is a constant normal offset through the outer
corner arcs. The shell's lower R3 corners are not reproduced in the seat; the
central bottom rests on the flat floor, leaving 44 mm of shell above the rim.

## Installation and printing

X is width; +Y points rearward toward Multiboard; +Z is up. Device bottom rests
at Z=2.5. Insert with antennas up; lift straight out to remove. The bottom Grove
connector is covered: disconnect its cable before seating. USB-C appears above
the supported band in the drawing, but cable overmold clearance/button access
are unverified. This is not a connected-cable cradle or an anti-ejection mount.

The rear feature imports `models.multiboard.peg.peg` unchanged: a 13.5 across-flats
octagon, projecting 6.5 from the rear wall, with its lowest flat at Z=0. It inserts
into a **separate compatible Multiboard snap**, not directly into a tile's large
Multihole. The snap revision and retention force are unspecified. See the
[module contract](../MODULES.md#multiboard-peg-and-rail-cutout) and
[connector provenance](../../research/objects/multiboard/measured-connectors.md).
The registered peg derives from the attributed Printables AirTag precedent;
its listing declares Attribution–Noncommercial–ShareAlike, exact version
unresolved. Retain that attribution and applicable terms when sharing derived
geometry.

Confirmed default printing setup: **Prusa MK4S, PETG, and a 0.4 mm nozzle**.
Print upright as exported, floor on XY and slot facing +Z. The recommended
0.2 mm layer height remains an assumption, not a confirmed or tested setting.
These defaults do not change the uncalibrated 0.4 mm per-side fit allowance. Inspect the
peg's lower 45-degree facets and bed contact in the slicer before deciding on
supports. No slicer settings are embedded in the 3MF.

## Build and verification

```sh
uv run python scripts/build.py models/unit_c6l_multiboard_holder --step
```

On 2026-10-16 this command passed native and saved/reimported STEP design checks:
one valid solid, correct overall envelope, 12 mm insertion depth and floor,
slot/wall boundaries, concentric rounded walls, unobstructed nominal-device
insertion path, analytical volume, and bottom-aligned octagonal peg dimensions.
The exported STL is one connected, watertight, consistently wound body. 3MF
millimeter-unit round-trip passed. PNG views and interactive HTML front/rear
views were inspected. The user subsequently confirmed a successful physical print
and good validation on 2026-10-16; cable-fit and load limits remain unspecified.

Artifacts under `outputs/unit_c6l_multiboard_holder/`:

- `unit_c6l_multiboard_holder.stl` — mesh; import as mm.
- `unit_c6l_multiboard_holder.3mf` — geometry-only, explicit mm units.
- `unit_c6l_multiboard_holder.step` — exact CAD exchange.
- `preview.png`, `preview.html` — exported-STL inspection views.
- `report.json` — timestamp and native, STEP, mesh and 3MF verification.

Geometry parameters are in `model.py`; metadata/research links in `model.toml`.
Omitting `--step` removes an older same-stem STEP after a successful build.
Tracked by [#32](https://github.com/ShakataGaNai/b123d/issues/32).
