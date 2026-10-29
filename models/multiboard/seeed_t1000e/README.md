# Seeed T1000-E Multiboard pocket

Simple rounded, top-entry gravity holder for the **Seeed SenseCAP Card Tracker
T1000-E**, in portrait orientation. Not T1000-A/B or T1000-E Plus. No latch, rail,
or reconstructed shell contour. **Physical fit and print quality unverified.**

## Dimensions

All dimensions in mm; manufacturer's envelope and design allowances are distinct.

| Feature | Dimension |
|---|---:|
| Manufacturer finished device, height × width × thickness | 85 × 55 × 6.5 |
| Clear pocket width × front/back gap | 55.8 × 7.3 |
| Insertion depth, vertical rim to floor | **20** |
| Floor / normal wall away from rounds | 2.5 / 2.5 |
| Inner / outer XY corner radius | 0.5 / 3 |
| Body width × thickness × height | 60.8 × 12.3 × 22.5 |
| Total envelope including pegs | 60.8 × 18.8 × 22.5 |
| Two peg centers, X / Z | ±12.5 / 6.75 |
| Peg center spacing | 25 |
| Each peg across flats / rear projection | 13.5 / 6.5 |
| Outside top/bottom and inner-mouth edge radius | 0.6 |
| Inside-floor text / deboss depth | T1000E / 0.2 |

The [manufacturer specification](https://wiki.seeedstudio.com/t1000_e_intro/)
provides the finished-device dimensions. The [dedicated research record](../../../research/objects/seeed-t1000e/README.md)
records revision limits, provenance, access evidence and allowances. The **0.4 mm
per-side** clearance is an uncalibrated FDM choice, not a factory tolerance.
The nominal square-cornered envelope must clear the rounded opening; the floor
supports the lower edge without reproducing its unknown radius.

[#43](https://github.com/ShakataGaNai/b123d/issues/43) standardizes R3 outside corners and R0.6 exposed top/bottom/mouth edges. **T1000E** is centered by actual glyph bounds, nominal 4 mm DejaVuSans from matplotlib's bundled font. The inside-floor deboss spans Z=2.3…2.5, leaving 2.3 mm backing. Flipped 180° about Y from the former underside label, it reads from the front when mounted: text runs +X, letter tops toward the board (+Y). The underside is restored flat. Peg mating profiles and 0.8 mm hidden root overlap are unchanged.

## Installation and printing

X is width, +Y toward Multiboard, +Z up. Seat the bottom at Z=2.5 with the lanyard
end uppermost; 65 mm of device extends above the rim. The **20 mm** dimension is
insertion depth, not the front/back gap. Lift straight up to remove.

The bottom and lower 20 mm of case are covered. The manufacturer's overview
places charging contacts and button above this lower band, but supplies no
connector or cable-overmold dimensions. Face the magnetic contacts outward for
charging; opposite-face controls can then face the board. Cable clearance,
board-side button access, sensor exposure and connected-cable insertion are not
verified. Remove the tracker for any obstructed operation. No speculative port
notch is cut.

Two imports of `models.multiboard.peg.peg` retain the registered snap interface.
Their 25 mm spacing fits the flat rear wall and one same-family grid interval;
50 mm spacing would not fit. Both lowest flats are at Z=0. Each needs a **separate
compatible Multiboard snap**, not a direct tile Multihole. Snap revision and
retention force remain unknown. See the [module contract](../../MODULES.md#multiboard-peg-and-rail-cutout)
and [connector provenance](../../../research/objects/multiboard/measured-connectors.md).
The peg follows the Printables AirTag precedent, whose listing declares
Attribution–Noncommercial–ShareAlike (exact version unresolved); retain that
attribution and applicable terms when sharing derived geometry.

Print floor-down as modeled, opening upward. Project baseline is Prusa MK4S,
PETG and 0.4 mm nozzle; 0.2 mm layers are a starting assumption. Inspect the peg
facets and bed contact in the slicer before deciding on supports. No print,
load/retention or cable-access test has been performed; this is not an anti-ejection
mount. 3MF export is geometry only, without slicer settings.

## Build and checks

```sh
uv run python scripts/build.py models/multiboard/seeed_t1000e --step
```

`build()` returns fresh geometry without import-time work. `check(shape)` checks
one valid solid, total bounds, the full nominal-device insertion sweep, floor
thickness and 20 mm seat, straight and concentric curved walls, analytical wall-section area,
both peg sections and the complete label void with exact depth and intact floor backing.
These are design checks, not evidence of physical fit.

Inside-floor revision passed native/STEP checks, one-body watertight STL and
millimeter 3MF round trip on 2026-10-16; report `2026-10-16T21:44:47.986209+00:00`.
PNG/HTML and contrast-enhanced exported-STL `inside-floor-inspection.png` inspected:
upright `T1000E` viewed from the front, board at top; exact Z=2.3…2.5 mm cut.
Boolean comparison proves only the old label was filled and the inner label cut,
2.804993 mm³ each. Artifacts: `outputs/multiboard/seeed_t1000e/`.
Physical device/snap trials remain required. Original [#38](https://github.com/ShakataGaNai/b123d/issues/38);
rounding/label [#43](https://github.com/ShakataGaNai/b123d/issues/43).
