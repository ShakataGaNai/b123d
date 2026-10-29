# WisMesh Tag Multiboard pocket

Simple rounded, top-entry gravity holder for the **RAKwireless WisMesh Tag**
finished device, in portrait orientation. Not WisMesh Pocket, Pod or a bare PCB.
No latch, rail or exact shell contour. **Physical fit and print quality unverified.**

## Dimensions

All dimensions in mm; manufacturer's envelope and design allowances are distinct.

| Feature | Dimension |
|---|---:|
| Manufacturer finished device, height × width × thickness | 92 × 59 × 7.5 |
| Clear pocket width × front/back gap | 59.8 × 8.3 |
| Insertion depth, vertical rim to floor | **20** |
| Floor / normal wall away from rounds | 2.5 / 2.5 |
| Inner / outer XY corner radius | 0.5 / 3 |
| Body width × thickness × height | 64.8 × 13.3 × 22.5 |
| Total envelope including pegs | 64.8 × 19.8 × 22.5 |
| Two peg centers, X / Z | ±12.5 / 6.75 |
| Peg center spacing | 25 |
| Each peg across flats / rear projection | 13.5 / 6.5 |
| Outside top/bottom and inner-mouth edge radius | 0.6 |
| Inside-floor text / deboss depth | Wis Tag / 0.2 |

The [manufacturer guide's enclosure drawing](https://docs.rakwireless.com/product-categories/meshtastic/wismesh-tag/quickstart/#dimensions)
and current store dimension image both state 92 × 59 × 7.5. The
[dedicated research record](../../../research/objects/rak-wismesh-tag/README.md)
records source images, revision limits and unknowns. **0.4 mm per-side** clearance
is an uncalibrated FDM choice, not a manufacturer tolerance. Rubber-shell friction
and production variation need a physical trial. The square nominal device envelope
must clear the opening; the flat floor does not reproduce undocumented case corners.

[#43](https://github.com/ShakataGaNai/b123d/issues/43) standardizes R3 outside corners and R0.6 exposed top/bottom/mouth edges. **Wis Tag** is centered by actual glyph bounds, nominal 4 mm DejaVuSans from matplotlib's bundled font. The inside-floor deboss spans Z=2.3…2.5, leaving 2.3 mm backing. Flipped 180° about Y from the former underside label, it reads from the front when mounted: text runs +X, letter tops toward the board (+Y). The underside is restored flat. Peg mating profiles and 0.8 mm hidden root overlap are unchanged.

## Installation and printing

X is width, +Y toward Multiboard, +Z up. Seat bottom at Z=2.5 with lanyard end up;
72 mm of device remains above the rim. **20 mm means insertion depth**, not the
front/back gap. Lift vertically to remove.

The bottom and lower 20 mm of case are covered. Put the charging-contact face
outward. Manufacturer illustrations place the contacts, front button and LEDs
above the covered lower band. Its prose calls the connector “on the top,” while
its illustrations show an upper broad-face contact pad, not an edge-mounted USB
socket. No undocumented connector notch is invented. Exact cable overmold/bend
clearance and connected-cable insertion remain unverified. The back reset button
faces the board and may require lifting the device out to operate. Remove the
device for any obstructed operation.

Two imports of `models.multiboard.peg.peg` retain the registered interface. Their
25 mm spacing fits the flat rear wall and one same-family grid interval; 50 mm
would not fit. Both lowest flats are Z=0. Each needs a **separate compatible
Multiboard snap**, not direct insertion into a tile Multihole. Snap variant and
retention force are unknown. See the [module contract](../../MODULES.md#multiboard-peg-and-rail-cutout)
and [connector provenance](../../../research/objects/multiboard/measured-connectors.md).
The peg follows the Printables AirTag precedent, whose listing declares
Attribution–Noncommercial–ShareAlike (exact version unresolved); retain attribution
and applicable terms when sharing derived geometry.

Print floor-down as modeled with opening up. Project baseline is Prusa MK4S,
PETG and a 0.4 mm nozzle; 0.2 mm layers are a starting assumption. Inspect peg
facets and bed contact in the slicer before deciding on supports. No print,
load/retention, rubber-friction or cable-access test has run. This is not an
anti-ejection mount. 3MF export has geometry only, without slicer settings.

## Build and checks

```sh
uv run python scripts/build.py models/multiboard/wismesh_tag --step
```

`build()` returns fresh geometry without import-time work. `check(shape)` checks
one valid solid, total bounds, full nominal-device insertion sweep, floor thickness
and 20 mm seat, straight/concentric curved walls, analytical wall-section area, both
peg sections and the complete label void with exact depth and intact floor backing.
These are design checks, not physical fit evidence.

Inside-floor revision passed native/STEP checks, one-body watertight STL and
millimeter 3MF round trip on 2026-10-16; report `2026-10-16T21:44:54.831603+00:00`.
PNG/HTML and contrast-enhanced exported-STL `inside-floor-inspection.png` inspected:
upright `Wis Tag` viewed from the front, board at top; exact Z=2.3…2.5 mm cut.
Boolean comparison proves only the old label was filled and the inner label cut,
2.707712 mm³ each. Artifacts: `outputs/multiboard/wismesh_tag/`.
Physical device/snap trials remain required. Original [#39](https://github.com/ShakataGaNai/b123d/issues/39);
rounding/label [#43](https://github.com/ShakataGaNai/b123d/issues/43).
