# Cardputer Mesh Multiboard pocket

A landscape, bottom-first storage pocket for the user’s Cardputer Mesh specimen, sized to include its buttons, with rear spacing for Cap LoRa-1262 and two antenna rests. Work item: [#30](https://github.com/ShakataGaNai/b123d/issues/30). Physical fit is unverified.

All dimensions are **mm**:

| Feature | Dimension |
| --- | ---: |
| Straight pocket opening | 84.8 × 17 |
| Pocket depth / floor | 10 / 3.5 |
| Walls / entrance radius | 2.5 / 0.5 |
| Slot rear boundary to peg-root shoulder | 20 |
| Rear arms | 20 wide × 13.5 high |
| Two snap pegs | 13.5 across flats × 6.5 projection |
| Peg center spacing | 50 |
| Antenna rests | Ø10, 5 deep, axis along X |
| Web below antenna rests | 8.5 |
| Rear arm / inside root radius | 2 |
| Complete exported envelope | 89.8 × 46 × 13.5 |

## Fit and orientation

See the [hardware evidence and assumptions](../../research/objects/m5stack-cardputer-mesh/README.md). The user reports approximately **15 mm body thickness excluding buttons** and **16 mm cap rear protrusion**, and specifies **17 mm total slot thickness including buttons and clearance**. No extra thickness allowance is added. Width allowance is 0.4 mm per side; fit allowances are uncalibrated. Hardware revision and measurement method are unspecified, so compatibility with every standard/Adv variant is not established.

Installed frame: X spans the keyboard, +Y faces the Multiboard, and +Z is up. The device bottom rests at Z=3.5. The pocket rim is Z=13.5; keyboard faces −Y. The rim overlaps the lowest keyboard area. Lift the device out for unrestricted controls/ports. This is a gravity pocket without an anti-ejection latch.

The rear slot boundary is Y=8.5; the arm ends/peg roots are Y=28.5 at X=±25, Z=6.75. The 20 mm spacing excludes the 6.5 mm peg projection, giving **4 mm nominal upright clearance** for the reported 16 mm cap overhang. Clearance throughout rocking is not guaranteed. Peg shoulders must seat at or forward of the backplane.

Both antenna saddles are centered at Y=19.75, halfway along the exposed 17.5 mm arm length between the holder’s rear exterior and peg roots. Their circular axes run along X, allowing a 10 mm diameter antenna to lie across both arms with half its diameter recessed. The exact Ø10 grooves have no extra fit allowance and leave 8.5 mm material beneath them. Actual antenna length, connector and cable routing remain unverified. Four rear vertical arm corners and the two concave inside roots have 2 mm radii; the snap profiles remain unchanged.

The peg geometry imports `models.multiboard.peg.peg` unchanged. These pegs enter **Multiboard snaps**, not bare tile Multiholes. Fit both receivers on the documented 25 mm grid, two grid intervals apart. Receiver revision and simultaneous insertion remain physically untested. Retain the source-derived peg attribution and applicable Attribution–Noncommercial–ShareAlike terms described in [connector research](../../research/objects/multiboard/measured-connectors.md) and the [module registry](../MODULES.md#multiboard-peg-and-rail-cutout).

## Build and verification

```sh
uv run python scripts/build.py models/cardputer_mesh_multiboard_holder
```

Outputs are in `outputs/cardputer_mesh_multiboard_holder/`: `cardputer_mesh_multiboard_holder.stl`, `cardputer_mesh_multiboard_holder.3mf`, `preview.png`, `preview.html`, and `report.json`. STL is millimeters; 3MF has explicit millimeter units and geometry only. No STEP export was requested.

The 2026-10-16 build passed native validity and one-solid checks, the design-specific cavity/insertion, floor/wall cores, arm web continuity, circular saddle profiles, rounded corner probes, peg-section/location and nominal upright rear-clearance checks, watertight STL with consistent winding, and 3MF round-trip verification. Native volume is 22050.818 mm³; mesh has 2196 triangles. The four-view PNG was visually inspected. The HTML was generated and opened in the default browser at the user's request; agent visual inspection of HTML was unavailable because no browser connection was available.

Print in the exported orientation, floor/arms and lowest peg flats on XY, slot upward. PETG with 0.2 mm layers is an untested starting assumption. Inspect the peg's 45° underside facets and perimeter structure in the slicer. No slicer, physical fit, strength or retention test has been performed; CAD checks do not establish print readiness.
