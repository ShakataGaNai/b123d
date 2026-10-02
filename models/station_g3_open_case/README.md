# Station G3 full-height open case

Parametric, open-top enclosure reconstructed from beanfield's [Station G3 Case – Meshtastic / MeshCore enclosure](https://www.printables.com/model/1855194-station-g3-case-meshtastic-meshcore-enclosure), Printables **1855194**. **Physical fit is unverified.** This model describes the reference case's interfaces, not manufacturer-certified board geometry.

## Build and view

```sh
uv run --offline python scripts/build.py models/station_g3_open_case
```

This generates STL + geometry-only 3MF (millimeters), previews, and a report. Add `--step` to also export and round-trip check STEP; a successful build without it removes an older same-stem STEP. Generated output paths after a successful build:

- [Interactive preview](../../outputs/station_g3_open_case/preview.html)
- [Four-view PNG](../../outputs/station_g3_open_case/preview.png)
- [STEP (only with `--step`)](../../outputs/station_g3_open_case/station_g3_open_case.step)
- [STL](../../outputs/station_g3_open_case/station_g3_open_case.stl)
- [3MF](../../outputs/station_g3_open_case/station_g3_open_case.3mf)
- [Validation report](../../outputs/station_g3_open_case/report.json)

Generated files remain outside Git. Open the HTML directly in a WebGL-capable browser; import the STL in millimeters.

## Geometry

| Feature | Nominal geometry, mm |
|---|---|
| Outside envelope | 70.6 × 122.2 × 22.3 |
| Inner cavity | 65.8 × 117.4, open above Z=4.3 |
| Walls | 2.4, reduced to a 1.07 inner lip at connector recesses |
| Outside corner radius | 4.0 |
| Floor | Z=0…4.3; underside-component pocket ends at Z=3.0 |
| Seven mounting seats | Ø7, top Z=5.3 |
| Mounting bores | Ø2.5, blind from Z=5.3 down to Z=1.5 |
| Interior supports | Three flat Ø7 pads and two Ø7 pads with locator pins |
| Locator pins | Ø3.5 shaft, conical lead-in to Ø1.9, top Z=7.3 |

The shell uses the reference shell's native XYZ frame. Front is −Y; power is −X; Grove ports are +X; antenna is +Y. See the [research record](../../research/objects/bq-voyage-station-g3/README.md#full-height-open-case-reconstruction) for measured centers, source registration, section planes and uncertainties.

Preserved access:

- Two USB-C openings: motherboard power on −X and MCU communication on −Y, each 9.02 × 3.02 capsule profile.
- DC5521 barrel opening: Ø8.02 on −X.
- Both front MCU buttons, plus the reference's additional side MCU button and power-good test button.
- Four power-good LED windows.
- Both Grove connector openings: 12.02 × 8.02. These are the source's Grove accesses, not an assumption about native Qwiic socket dimensions.
- Antenna insertion slot: 6.42 wide from Z=15.09 through the top, with a wider shallow outside recess for the nut/base.

Shallow rectangular exterior pockets preserve cable-body access around the small through-openings. They stop at the 1.07 mm inner lip; enlarging the entire through-hole is unnecessary. The main parameters and feature tables live in [model.py](model.py).

## Deliberate changes from the reference

- Uniform 22.3 mm rim, raising the source's low front section by 4 mm; no lid or faceplate.
- Full-depth rounded rectangular footprint. The source's front USB/button wall projects beyond its lower base; this model extends the floor to that wall rather than moving the ports inward.
- Flat exterior bottom, without the source's underside grooves.
- No lid catches, decoration or side ventilation slits. The top remains open; thermal performance still needs checking.
- Square button cutouts enclose the source rounded profiles. Rectangular shallow pockets replace the source's curved/flared recesses and remove more exterior material.
- Conical locator tips replace the rounded tips while retaining shaft diameter and maximum height.
- Straight-sided 15.2 × 14.2 underside-component pocket preserves the full source mouth and removes more material than the original bottom blends.

## Verification and fit limits

The export workflow passed with **one valid solid**, native and STEP-round-trip design checks, and a **watertight, consistently wound, single-body STL**. Bounds are 70.6 × 122.2 × 22.3 mm. Checks cover blind-bore floors/diameters, mounting seats, support heights, the component pocket, clear port/recess volumes, the open antenna path and retained inner lips. The PNG and orbitable HTML were inspected from both sides, including power and antenna access.

These are historical verification results, not evidence that a 3MF has been regenerated. Consult the latest report for current exports and checks.

No board, printed fit, cable insertion, button travel, loading or thermal test has been performed. Confirm the exact motherboard/MCU/RF revisions and the reference author's **7 mm and 12 mm M2.5 standoffs with 4 mm studs** against your assembly. Ø2.5 modeled bores are not a guaranteed printed thread or clearance fit. Keep the MCU communication USB-C's electrical restrictions in the [official wiki](https://wiki.bqvoy.com/en/devkits/station-g3) separate from mechanical access.

Print orientation is the flat bottom on XY, Z up. Review bridges over the port openings and any required supports in the slicer. Use a mounting/port coupon before a full print; calibrate hole and connector clearances for the printer/material. Open top and omitted side vents do not establish thermal suitability or weather resistance.

## Attribution and reuse

Source geometry: **beanfield**, Printables **1855194**, `SG3-01-Case.stl` (file 7750403), with `SG3-04-Backplate.stl` (7750399) as a mounting-interface cross-check. The source listing declares **Creative Commons Attribution–ShareAlike**. Preserve attribution and comply with the source's applicable ShareAlike terms when sharing this reconstruction or its exports; STL-to-parametric reconstruction does not remove those obligations. The inspected API did not establish a license version, so none is invented here. No geometry from the separately licensed Printables 1816444 model was used.

Changes are listed above. Original download URLs, SHA-256 identities and source evidence are retained in the research record. Work item: [#5](https://github.com/ShakataGaNai/b123d/issues/5).
