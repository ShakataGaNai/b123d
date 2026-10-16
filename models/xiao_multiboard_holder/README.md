# XIAO two-slot Multiboard cradle

Compact, open-center holder for a **Seeed XIAO with two downward-facing seven-pin male headers**. Primary target: **XIAO ESP32S3 + Wio-SX1262 Meshtastic kit, SKU 102010611**. The user confirmed the prior 8 mm antenna-slot version printed and validated good on 2026-10-16. The current deeper-slot revision is not yet physically printed; hardware revision/header supplier remains unspecified.

Insert the pins downward into the two continuous slots until the **header plastic**, not the pin tips, rests on the flat rail tops. USB faces the open front. There are no individual pin holes, screws, electrical contacts or upper enclosure walls. The board is gravity-supported and removable; this is **not a locking clip**. Do not pull on cables or invert it expecting retention.

The rear spine holds a flat LoRa antenna upright in an **8.4 × 1.4 mm slot, 12 mm deep**, leaving a **1.5 mm closed floor**. This is the maximum depth under the chosen minimum-floor constraint, matching the thin prong walls; a through-slot would lose bottom support. Width, position and every other feature are unchanged. The user's approximate **8 × 1 mm** antenna size retains **0.2 mm clearance per side**. It is a loose slot, not a clamp; cable attachment relief is intentionally omitted.

Both prongs have **1 mm-radius inner vertical corners at the front tips and rear joins**, matching the outside corner radius. These rounds extend through the full 13.5 mm height; the flat header seats and all three slots retain their dimensions.

## Dimensions and datums

All dimensions in **mm**. XY is the print bed; +Z is up; +Y faces the Multiboard, −Y is the USB/open-front side. The header array is centered at X=Y=0. Header-plastic undersides seat at Z=13.5.

| Feature | Dimension |
| --- | --- |
| Body, width × depth × height | 19.64 × 29.4 × 13.5 |
| Total envelope including peg | 19.64 × 35.9 × 13.5 |
| Two pin slots, width × length × depth | 1.4 × 17 × 8 each |
| Slot row center spacing | 15.24 |
| Outer / inner wall beside each pin slot | 1.5 / 1.5 |
| Whole arm width between straight walls | 4.4 |
| Pin pitch / pins per row | 2.54 / 7 |
| Material below header-pin slots | 5.5 |
| Open center width between straight walls | 10.84 |
| Rear spine depth / front and rear webs | 5.4 / 2 each |
| Antenna slot, width × thickness × depth | 8.4 × 1.4 × 12 |
| Material below antenna slot | 1.5 |
| Rearward extension from original cradle | 3.4 |
| Outside vertical-corner radius | 1 |
| Inner front-tip / rear-join vertical radii | 1 / 1 |
| Rear octagonal peg across flats / projection | 13.5 / 6.5 |
| Peg bottom above bed | 0 |

The [hardware record](../../research/objects/seeed-xiao-esp32s3-wio-sx1262/README.md) cites the manufacturer footprint and distinguishes nominal facts from fit allowances. The slots assume ordinary **0.64 mm square pins**, **6 mm exposed length**, and **2.54 mm-wide × 2.5 mm-high header plastic**. They give 0.38 mm nominal clearance per pin side, 0.56 mm clearance at each array end, 2 mm clearance beneath 6 mm pins, and 0.57 mm of support beneath each side of the plastic. Pins up to 7.5 mm long retain 0.5 mm bottom clearance. These are uncalibrated design allowances, not measured printing accuracy.

The center is open through the bottom and front; its rear edge at Y=11 is 0.5 mm behind the nominal 21 mm PCB's rear edge. Header slots and the front edge at Y=−13 remain unchanged. The back face stays at Y=16.4, with the antenna slot centered at X=0, Y=13.7 and its floor now at Z=1.5; the peg is unchanged. There are no holder features above the support plane, leaving the Wio daughterboard, buttons and antenna connections above the holder. Other classic 2×7 XIAO boards are intended to fit, but alternate headers, solder blobs, underside heatsinks, GNSS, batteries and accessories require their own checks. The Wi-Fi antenna and battery are supported separately; antenna length and RF performance remain unverified.

## Multiboard attachment

The model imports `models.multiboard.peg.peg` without modifying the shared helper. It is the same nominal 13.5 mm across-flats × 6.5 mm projection used by the approved prior XIAO geometry. It inserts into a **Multiboard snap**, not directly into a tile Multihole. Snap revision and quantified retention/strength remain unspecified.

Provenance: [ShakataGaNai's AirTag holder](https://www.printables.com/model/1407536-airtag-holder-for-multiboard), documented in the [connector research](../../research/objects/multiboard/measured-connectors.md). Its listing declares Attribution–Noncommercial–ShareAlike with the exact version unresolved. Retain that attribution and applicable terms when sharing source-derived geometry.

## Build and printing

```sh
uv run python scripts/build.py models/xiao_multiboard_holder --step
```

`model.py` owns the geometry and `check(shape)`; `model.toml` owns catalog metadata. Imports do not build or export. The standard build works without downloaded hardware files. Omit `--step` for STL/3MF only; the exporter then removes an older same-stem STEP.

Print as exported, flat rail bottoms and peg bottom on XY, slots facing up. Nonconductive PETG with a 0.4 mm nozzle and 0.2 mm layers is an initial recommendation, **not a tested process**. Inspect the slicer for the peg's 45° lower faces and keep support out of the narrow blind slots. Check fit without forcing or bending pins; no printer compensation is hidden in the peg. No thermal, strength or RF performance certification is claimed.

## Verification and artifacts

On 2026-10-16, `scripts/build.py ... --step` passed using Python 3.14.8 / build123d 0.13.0:

- One valid solid on native geometry and saved/reimported STEP.
- Dimension-specific checks: full-width/depth continuous pin slots; closed floors and side/end walls; complete pin-array insertion sweeps; supporting header ledges; open center/front with rounded rear joins; all four inner quarter-circle boundaries at three angles and three heights; nominal PCB clearance; antenna slot entry, dimensions, floor, walls and 8 × 1 mm insertion sweep; front/rear spine webs; peg section area, across-flats dimensions and bed alignment; independent analytical volume.
- Full-length 1.5 mm inner and outer slot walls, clear center channel and clear space immediately outside both arms; complete header support ledges retained.
- Saved STL: watertight, consistently oriented, one connected body, 1,132 triangles.
- Saved millimeter 3MF: round trip passed. Geometry only, without slicer settings/material assignments.
- PNG isometric/top/bottom/front views and interactive HTML inspected, including both rounded front tips, rear joins and the transverse antenna slot.

Artifacts under `outputs/xiao_multiboard_holder/`:

- `xiao_multiboard_holder.stl` — mesh; import as millimeters.
- `xiao_multiboard_holder.3mf` — millimeter geometry package.
- `xiao_multiboard_holder.step` — exact CAD exchange.
- `preview.png`, `preview.html`, `report.json` — exported-mesh views and fresh build evidence.

Prior geometry was printed and validated good by the user on 2026-10-16; the deeper-slot revision still requires a physical print. Pin/header variation and cable-load limits remain unspecified. Approval: [#35](https://github.com/ShakataGaNai/b123d/issues/35); slot revision: [#37](https://github.com/ShakataGaNai/b123d/issues/37).

Revision 2026-10-16: extended only the rear by 3.4 mm and added the user-sized antenna slot; kept the header slots, open center and peg profile unchanged. Rebuilt STL/3MF/STEP and regenerated the catalog.

Corner revision 2026-10-16: added R1 full-height fillets to all four inner prong corners. The rear corners now curve into the 11.4 mm-wide channel over its last 1 mm; the front tips round outward into the opening. Equal front material removal and rear addition cancel in volume. Pin/antenna dimensions, header seats, outer envelope and peg remain unchanged. Native/STEP checks and fresh exports passed.

Thin-arm revision 2026-10-16: reduced the outer pin-slot walls from 2.68 to 1.5 mm, removing 1.18 mm from each side of the body and rear spine. Overall width is now 19.64 mm; inner walls remain 1.22 mm and whole arms are 4.12 mm wide. Header slots, seats, inner opening, antenna slot and webs, corner radii and peg remain unchanged. Native/STEP checks and STL/3MF exports passed; PNG/HTML views inspected. Report timestamp `2026-10-16T18:53:28.797904+00:00`. Strength and physical fit remain untested.

Matching-wall revision 2026-10-16: thickened each inner wall from 1.22 to 1.5 mm to match the outer wall. The derived center opening is 10.84 mm and each whole arm is 4.4 mm wide. Outside dimensions, slots, peg and R1 corner radii remain unchanged. Full-length inner/outer wall checks passed on native and reimported STEP geometry; STL/3MF exports and PNG/HTML inspections passed. Report timestamp `2026-10-16T18:55:45.205165+00:00`. Physical fit and strength remain untested.

Deep-slot revision 2026-10-16: increased only antenna depth from 8 to 12 mm,
retaining a 1.5 mm closed floor. Boolean comparison against the pre-edit BREP
showed **0 mm³ added** and exactly the intended **8.4 × 1.4 × 4 mm prism
(47.04 mm³) removed**, with no differences elsewhere. Native/STEP checks,
watertight one-body STL and millimeter 3MF round trip passed; PNG/HTML inspected.
Report timestamp `2026-10-16T21:17:04.051664+00:00`. Prior print approval is
retained as history; this revision needs a new physical print.

Completion decision 2026-10-16: the user considers XIAO done. Current geometry
is approved and excluded from subsequent dual-peg, label and rounding changes.
The current design approval does not invent a new physical print report;
the confirmed physical print remains the prior 8 mm-slot version.
