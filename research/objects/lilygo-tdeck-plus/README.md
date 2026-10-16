# LILYGO T-Deck Plus: factory-enclosed device

Research date: 2026-10-16. Work: [#40](https://github.com/ShakataGaNai/b123d/issues/40). Consumer: [T-Deck Plus Multiboard cradle](../../../models/lilygo_tdeck_multiboard_holder/README.md).

## Identity and readiness

The user explicitly confirmed **T-Deck Plus**, superseding the initial original-bare-T-Deck interpretation. Target: factory-enclosed T-Deck Plus with built-in 2000 mAh battery/GPS, standard keyboard/display, no added rear bracket or case. Bare T-Deck and T-Deck Pro are excluded. Radio/GPS choices do not establish additional mechanical revisions; exact tooling revision is unknown. Readiness: **approximate with listed assumptions**. The nominal finished-device envelope is manufacturer evidence; physical fit is unverified.

## Primary evidence

Accessed 2026-10-16. Image publication date and drawing revision are unknown (CDN query strings are not declared drawing revisions). Manufacturer tolerances and asset redistribution permission are unknown. Images are cited rather than committed. The original Plus STEP was downloaded to ignored `tmp/` for measurement only; provenance follows.

| ID | Publisher and source | Evidence |
|---|---|---|
| P1 | LILYGO, [T-Deck Plus Canada listing](https://lilygo.cc/en-us/products/t-deck-plus-ca) | Factory-enclosed Plus identity; links P2/P3; built-in 2000 mAh battery and GPS. Regional sales listing, not a separate claimed shell design. |
| P2 | LILYGO, [T-Deck-Plus-lilygo_4 dimension graphic](https://cdn.shopify.com/s/files/1/0617/7190/7253/files/T-Deck-Plus-lilygo_4.jpg?v=1723255752) | Finished-device photograph explicitly labeled **W:72mm, L:115mm, H:20mm**. Dimensions transcribed from labels, not measured from pixels. |
| P3 | LILYGO, [T-Deck-Plus-lilygo_5 orthographic product views](https://cdn.shopify.com/s/files/1/0617/7190/7253/files/T-Deck-Plus-lilygo_5.jpg?v=1723255797) | Bottom central USB-C, lower side vents, upper side controls, rear tripod insert and top antenna knockouts. Qualitative feature locations only. |
| P4 | LILYGO, [current Plus listing](https://lilygo.cc/products/t-deck-plus-1) | Plus identity and GPS/radio/accessory choices; no claim of compatibility with bare board. |
| P5 | LILYGO, [manufacturer shell directory](https://github.com/Xinyuan-LilyGO/T-Deck/tree/master/shell) | Separately names T-Deck-Plus-Shell.stp and T-Deck-Shell.stp. The Plus STEP is measured below; do not substitute the bare-board shell. |

## Manufacturer CAD revision and lower profile

The Plus file was added by [commit c43766f13c61b786777405e17fd9e6d6c8bed86c](https://github.com/Xinyuan-LilyGO/T-Deck/commit/c43766f13c61b786777405e17fd9e6d6c8bed86c), 2024-10-28. [Pinned original download](https://raw.githubusercontent.com/Xinyuan-LilyGO/T-Deck/c43766f13c61b786777405e17fd9e6d6c8bed86c/shell/T-Deck-Plus-Shell.stp): 3,006,752 bytes; SHA-256 `2aa19eb37525fdb9852c0f0ede206a379145ce3d2a811609da3118b53c2eff18`; Git blob `04c0b083c4c465f3228fdc73720d07574b6d9754`. Local original: `tmp/lilygo-tdeck-plus/T-Deck-Plus-Shell-c43766f.stp`. The repository license endpoint returned 404 and the shell README supplies pictures, not CAD license terms. Redistribution permission is **unknown**: do not commit or redistribute the source STEP. These numerical measurements and our simplified holder are not a copy of the shell geometry. No downloaded code was executed.

Read with build123d's STEP importer, four solids. Source axes: X width, Y device height, Z thickness; broad front face is source Z=+7. Register to holder coordinates using `x = X − 136.7287661069`, `y = −Z − 3.2`, `z = Y − 64.1354122922 + FLOOR`. This is a right-handed rotation/translation, not a scale. The bottom datum is the shell's extreme Y, not its USB opening or a flat bottom that does not exist.

| CAD measurement | Result (mm) | Interpretation |
|---|---:|---|
| Whole assembly bounding size | 73.1401 × 114.9849 × 20.4000 | Includes upper side pieces; not the lower insertion cross section |
| Main shell lower width | 71.9554 | Lower straight sides, approximately the advertised 72 |
| Lower section thickness, heights 6–25 | 19.0000, source Z −12…+7 | Rear upper features cause the larger whole-device thickness |
| Lower broad-face straight-side transition | Height approximately 16.26 | The conspicuous bottom rounding is in **width/height**, not just XY thickness corners |

Plane sections of the original main shell give these lower silhouette stations. Coordinates are mm from the registration above. They include the thickness direction; negative and positive X differ slightly.

| Height above extreme bottom | Minimum X | Maximum X |
|---:|---:|---:|
| 1 | −14.9270 | 19.0438 |
| 2 | −20.7960 | 23.4333 |
| 4 | −27.2586 | 28.4543 |
| 6 | −30.9267 | 31.4154 |
| 8 | −33.1939 | 33.3309 |
| 10 | −34.6001 | 34.5890 |
| 12 | −35.4276 | 35.3826 |
| 16 | −35.9762 | 35.9758 |
| 20 | −35.9777 | 35.9777 |

Bottom outer faces are B-splines, **not an exact single circular radius**. The model uses a deliberately simple 72 mm-wide broad-face envelope with R16 lower corners, offset horizontally by the 0.8 mm fit allowance (cavity width 73.6, lower corner R16.8). At X=±12.6, measured bottom heights are 0.7487 / 0.2454; at ±17 they are 1.2881 / 0.6858. At X=24/28/30/32/34/35 the positive-side heights are 2.1703/3.7629/4.9297/6.5267/8.9565/10.9108. The simplified seat leaves approximately 0.25–2.6 mm broad-face clearance at these measured stations before settling; it follows the large rounded lower corners rather than claiming a tight negative mold. The USB gap means first support is on the adjacent side ledges, not at the extreme central bottom; slight settling/rocking must be trial-fitted.

Additional research-only surface sampling at 0.03 mm chordal / 0.1 rad angular deflection yielded 13,322 lower-shell vertices (height <22): all lay above the nominal R16 bottom; minimum sampled vertical margin 0.00087 mm. A nominal 72 × 20.4, R3 XY envelope was exceeded by 0.3594 mm; reducing the **approximate envelope** radius to R1.4 contained the samples within 0.000001 mm. The cavity uses R2.2, an outward 0.8 mm offset of that envelope. This is sampled evidence, not a certified continuous error bound. One rear chamfer plane failed triangulation; its bounds (height ≥19.1009, source Z −10.7899…−6.3428, X≤172.7065) are safely inside the simplified allowance envelope. An exact section at X=−32 returned empty; neighboring sections and independent surface samples were used instead, not a fabricated dimension.

The lower seating envelope is the intersection of a rounded XY section and rounded-bottom XZ profile; its constant maximum section continues upward. This is a continuous straight insertion sweep of the lower shell, not a square-prism test or a sweep of the upper buttons through a pocket they never enter. The rounded-bottom analytical envelope and recorded manufacturer section witnesses are checked separately. No runtime download or imported manufacturer CAD is required by the holder.

## Dimensions and frame

Source and model units mm. Holder X is width, Y thickness (front/keyboard −Y, rear/mount +Y), Z upright height. Simplified nominal bottom is model Z=2.5; X=Y=0 is the lower envelope center. Holder underside is Z=0, peg axes +Y. See the explicit STEP transform above. No hole mounting or tripod attachment is used: hole-center pattern, thread engagement and tooling clearances are not required.

| Feature | Value | Evidence class | Uncertainty |
|---|---:|---|---|
| Finished device width | 72 mm | Authoritative, P2 W | Tolerance not specified |
| Finished device thickness | 20 mm | Authoritative, P2 H | Local keyboard/back features not separately dimensioned |
| Finished device height | 115 mm | Authoritative, P2 L | No external antenna included |
| USB-C | Bottom, approximately centered | Qualitative authoritative, P3 | Port center and cable overmold size undimensioned |
| Side controls | Above lower end | Qualitative authoritative, P3 | Exact button heights not measured |
| Lower side vents | Present | Qualitative authoritative, P3 | No thermal performance specification for partial shielding |

## Design allowances and decisions

- Slot **73.6 × 22.0 mm**, derived from lower nominal width 72 and whole-shell thickness 20.4 plus 0.8 mm clearance **per face**, an uncalibrated design allowance, not manufacturer tolerance. Nominal XY R1.4 is a simple envelope approximation; cavity R2.2 is its outward offset. This clears the measured lower section and accommodates its front/rear shape without copying every chamfer.
- 20 mm shallow insertion; minimum walls/floor ledges 2.5 mm. Lower broad-face seat R16.8 (functional, manufacturer-informed approximation), external plan corners R3, exposed external/mouth edges R0.6 shared with the other Multiboard holders. Holder bounds including pegs **78.6 × 33.5 × 22.5 mm**.
- Bottom USB opening **24 × 22.0 mm**, through the floor, centered. This deliberately broad design allowance avoids a guessed port template and preserves side seating ledges. A centered 20 mm-wide cable corridor is checked; actual plug offset, overmold and downward bend space require trial fit. Connect from below while wall-mounted; do not route cable behind the holder.
- Lower keyboard rows and lower side vents are partly shielded by the rim. This is a gravity **storage cradle**, not a typing dock, thermal enclosure or guaranteed charging station. Remove for typing/service; verify the case rests without pressing keys or blocking necessary cooling.
- Two unchanged registered Multiboard pegs: 13.5 mm AF, 6.5 mm exposed projection, 25 mm centers at X=±12.5, Z=6.75, 0.8 mm buried root overlap to bridge the rounded underside. [Grid/source record](../multiboard/README.md) and [connector attribution/license scope](../multiboard/measured-connectors.md).
- The factory top antenna/knockout area remains above the cradle. External antenna modifications, rear tripod accessories and larger cases are not within the envelope claim.

## Verification and limits

The revised `check(shape)` covers the rounded insertion envelope, independent manufacturer witnesses, curved support/ledge material, USB passage, walls, finish and pegs. Current rounded revision passed native/STEP checks, one-body watertight STL and millimeter 3MF round trip on 2026-10-16; four-view PNG inspected. See the model README and fresh report. Slicing, hardware fit and loads remain untested; verify real-case seating, key pressure, cable clearance, cooling and retention. No load rating or transport lock.

Print floor-down in XY with +Z up using a calibrated FDM process; inspect the slice rather than asserting support-free printing from CAD validity.

2026-10-16: user-confirmed Plus record saved before revising the holder geometry; replaces the preliminary bare-device research record.

2026-10-16, rounded-seat revision: user reported the bottom is much rounder. Downloaded, checksummed and measured the original Plus STEP; recorded this evidence **before** replacing the square-bottom pocket. Retained prior verification history without applying it to the new geometry.
