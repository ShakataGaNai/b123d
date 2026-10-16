# Seeed SenseCAP Card Tracker T1000-E

Research date: 2026-10-16. Consumed by [the Multiboard holder](../../../models/seeed_t1000e_multiboard_holder/README.md), tracked in [#38](https://github.com/ShakataGaNai/b123d/issues/38). Record saved before geometry.

## Identity and sources

Exact product: Seeed Studio **SenseCAP Card Tracker T1000-E for Meshtastic**, finished sealed enclosure, without cable or lanyard. This is not the LoRaWAN T1000-A/B or the mechanically unverified T1000-E Plus. PCB/enclosure revision and drawing publication date are unknown. Readiness: **approximate with listed assumptions**; manufacturer's nominal finished-device envelope is established, production tolerances and physical fit are not.

| ID | Primary source and locator | Revision/date | Accessed | Rights |
|---|---|---|---|---|
| S1 | [Seeed T1000-E introduction](https://wiki.seeedstudio.com/t1000_e_intro/), Specification / General / Dimensions, Hardware overview | Live unversioned manufacturer wiki; publication date unknown | 2026-10-16 | Asset redistribution permission not established |
| S2 | [Seeed hardware overview illustration](https://files.seeedstudio.com/wiki/SenseCAP/Meshtastic/4-pogo.png), linked by S1 | Unversioned; publication date unknown | 2026-10-16 | Unknown; link only |
| S3 | [Multiboard connector record](../multiboard/measured-connectors.md) and [grid evidence](../multiboard/board-geometry.md) | Existing repository research | 2026-10-16 | AirTag precedent Attribution–Noncommercial–ShareAlike, exact version unresolved |

No manufacturer assets copied into the repository: source links and original extraction notes suffice and redistribution permission is unknown. Dimensions below are read from the manufacturer's specification, not inferred from image pixels. No specimen was measured.

## Envelope, axes and access

Source units and model units are mm. Model X is the 55 mm card width, Y its 6.5 mm thickness (+Y toward the board), and Z the 85 mm height, lanyard end up. The holder's XY bottom is Z=0; the seated device's bottom is Z=2.5. Front/back orientation may be reversed to put the magnetic contacts toward the user.

| Feature | Value | Class / source | Uncertainty or consequence |
|---|---:|---|---|
| Finished device height × width × thickness | 85 × 55 × 6.5 mm | Authoritative, S1 Specification | No tolerance or revision stated; no accessory envelope |
| Charging/data contacts | Four pogo contacts; magnetic USB cable | Authoritative, S1 Features and Battery; S2 | Contact positions and cable overmold/bend space not dimensioned |
| Controls/sensors | Button, LED/light sensor, temperature sensor, buzzer | Authoritative, S1/S2 | Locations qualitative only; not mechanically modeled |
| Lanyard slot | At upper end | Observed in S2 | No hole size/centers; not used for mounting |
| Case radii / bottom contour | Unknown | No dimensioned contour recovered | Use conservative square envelope for clearance; flat seat is approximate |

The lower 20 mm is surrounded by the holder; the bottom face is covered. With the illustrated lanyard end uppermost, S2 shows the charging contacts and button outside the lower band. This is a qualitative access decision, not measured cable clearance. Turn contacts outward for charging rather than trapping the plug between card and board. Opposite-face controls can then face the board; hand access is unverified. Remove the tracker if a plug, control or sensor is obstructed. No connector notch is invented from an undimensioned picture; cable-attached insertion is not claimed. No screws, mounting holes or fasteners are needed.

## Design decisions, separate from hardware facts

- User requirement: **20 mm insertion depth**, vertical rim-to-floor distance; not a 20 mm front/back gap.
- Trial FDM fit allowance: **0.4 mm per side**, giving a **55.8 × 7.3 mm** clear opening. This is not a manufacturer tolerance or a calibrated printer correction.
- Assumed structural dimensions: 2.5 mm floor and normal walls, 0.5 mm inner XY corner radius and 3 mm outer radius. A square-cornered nominal device must clear the opening; the small rounded pocket is not an exact case reconstruction.
- Body envelope: 60.8 × 12.3 × 22.5 mm. With pegs: 60.8 × 18.8 × 22.5 mm. Device projects 65 mm above rim when seated.
- Two registered **13.5 mm across-flats × 6.5 mm projection** pegs at X=±12.5, Z=6.75, rearward +Y. Their **25 mm** pitch matches one same-family board-grid interval. Two pegs fit fully on the flat rear wall; 50 mm pitch does not. Separate compatible snaps are required; direct tile engagement and snap retention are not established.
- Print floor-down on XY, opening +Z. PETG / 0.4 mm nozzle follows the existing holder's project setup; layer height and final slicing require evaluation. No latch or ejection protection.
- [#43](https://github.com/ShakataGaNai/b123d/issues/43), 2026-10-16: retain slot, 20 mm seat, R3 outside corners and R0.6 exposed edges. `T1000E` is debossed 0.2 mm into the inside floor at Z=2.5, leaving 2.3 mm backing. Text is nominal 4 mm DejaVuSans, centered by glyph bounds. Flip 180° about Y from the former underside label: +X text direction, tops toward the board (+Y), readable from the front. Underside restored flat. Peg mating geometry and 0.8 mm hidden overlap unchanged. These are design requirements, not measured device features; geometry remains unprinted.

## Verification plan and limits

`check(shape)` verifies insertion, seat/floor, walls, both pegs and the complete inner-floor label void with exact 0.2 mm depth and intact backing. Boolean comparison proves only the former underside marking was filled and the new inner-floor marking removed. See the model README for current export/visual verification. Numerical CAD tolerances are not manufacturing tolerances. Physical device/snap trials remain necessary for fit, retention, cable access and printability; no load, RF-performance or exact-fit claim.
