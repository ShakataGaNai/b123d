# RAKwireless WisMesh Tag

Research date: 2026-10-16. Consumed by [the Multiboard holder](../../../models/wismesh_tag_multiboard_holder/README.md), tracked in [#39](https://github.com/ShakataGaNai/b123d/issues/39). Record saved before geometry.

## Identity and sources

Exact product: **RAKwireless WisMesh Tag**, finished sealed enclosure with rubber-style protection and internal 1000 mAh battery; no cable, strap or aftermarket case. Store page currently identifies SKU B05046 and black/limited blue finishes with the same hardware. This is not WisMesh Pocket, Pod, or a bare RAK4631. Hardware/enclosure revision and drawing publication dates are unknown. Readiness: **approximate with listed assumptions**; manufacturer's finished-device dimension drawing establishes nominal envelope, not production tolerance or print fit.

| ID | Primary source and locator | Revision/date | Accessed | Rights |
|---|---|---|---|---|
| R1 | [RAK WisMesh Tag quick start](https://docs.rakwireless.com/product-categories/meshtastic/wismesh-tag/quickstart/), Hardware Description, Recharging Port, Dimensions | Live unversioned manufacturer guide; publication date unknown | 2026-10-16 | Site says all rights reserved |
| R2 | [Enclosure dimension illustration](https://res.rakwireless.com/ext/images.docs.rakwireless.com/meshtastic/wismesh-tag-enclosure.png?fm=webp), linked by R1 | Unversioned | 2026-10-16 | Redistribution permission unknown; link only |
| R3 | [Manufacturer store listing](https://store.rakwireless.com/products/wismesh-tag-meshtastic-gps-lora-tracker-ip66) and its [dimensions-v2 image](https://store.rakwireless.com/cdn/shop/files/wismesh-tag-dimensions-v2_1024x1024.webp?v=1776420109) | Image filename v2; enclosure revision not identified | 2026-10-16 | Redistribution permission unknown; link only |
| R4 | [Recharging contact illustration](https://res.rakwireless.com/ext/images.docs.rakwireless.com/meshtastic/wismesh-tag-port.png?fm=webp), linked by R1 | Unversioned | 2026-10-16 | Redistribution permission unknown |
| R5 | [Multiboard connector record](../multiboard/measured-connectors.md) and [grid evidence](../multiboard/board-geometry.md) | Existing repository research | 2026-10-16 | AirTag precedent Attribution–Noncommercial–ShareAlike, exact version unresolved |

R2 and R3 images were inspected directly: both explicitly label **59 mm width, 92 mm height, 7.5 mm thickness**. These are finished-enclosure dimensions, not PCB measurements or pixel-scale estimates. No manufacturer assets copied into the repository because redistribution permission is unknown; the linked originals and original extraction notes are retained. No specimen measurements were taken.

## Envelope, axes and access

Source/model units: mm. Model X is card width (59), Y thickness (7.5; +Y rearward toward Multiboard), Z height (92), lanyard end up. Holder bed is Z=0; seated device bottom is Z=2.5. Point the charging-contact face toward the user (−Y).

| Feature | Value | Evidence class / source | Uncertainty or consequence |
|---|---:|---|---|
| Finished device height × width × thickness | 92 × 59 × 7.5 mm | Authoritative, R2 Dimensions and R3 dimensions-v2 | No tolerance/revision given; cable and strap excluded |
| Charging/USB connector | Four magnetic-cable contacts | Authoritative, R1 Recharging Port and R4 | Contact coordinates/plug overmold/bend envelope not dimensioned |
| User and reset controls | Upper front and upper back buttons | Authoritative, R1 Button sections | Button protrusion detail not dimensioned independently |
| Lanyard slot | At top of enclosure | Observed R2/R3 | Not used as mounting interface; dimensions/centers unknown |
| Case corners/chamfers | Undimensioned | R2/R3 | Envelope-only clearance, not contour matching |

R1 calls the connector “on the top”; R2/R4 show the four contacts on an upper broad face rather than on the narrow top edge. Use the illustrations to identify the contact face, not an invented edge-port cutout. Keeping the lanyard end up and contacts outward leaves the shown charging interface, front button and LEDs above the 20 mm supported band. This is qualitative placement evidence, not a cable clearance measurement. The rear reset button faces the board and may require lifting the device out for access. Bottom face and lower 20 mm of both broad faces/edges are covered. Remove the device to service any obstructed feature; connected-cable insertion and cable bend clearance are unverified. No screws or mounting-hole pattern is used.

## Design decisions, separate from hardware facts

- User requirement: **20 mm insertion depth** from rim down to seat, not a 20 mm front/back gap.
- Uncalibrated FDM clearance: **0.4 mm per side**; clear pocket **59.8 × 8.3 mm**. Rubber surface friction and production variation still need a real-device trial.
- Assumed structural geometry: floor and normal walls 2.5 mm; inner/outer XY radii 0.5/3 mm. Use a conservative square nominal envelope for clearance rather than reconstructing undocumented case contours.
- Pocket body envelope: 64.8 × 13.3 × 22.5 mm; total with pegs 64.8 × 19.8 × 22.5 mm. Seated nominal device extends 72 mm above rim.
- Two registered 13.5 mm across-flats × 6.5 mm projection pegs at X=±12.5, Z=6.75, rearward +Y. **25 mm** center spacing follows one same-family board interval and fits the flat rear wall; 50 mm does not. A separate compatible snap is required for each peg. No direct tile fit or retention force is claimed.
- Print floor-down on XY, opening +Z. PETG / 0.4 mm nozzle follows project holder setup, not a physical test. No latch or anti-ejection feature.
- [#43](https://github.com/ShakataGaNai/b123d/issues/43), 2026-10-16: retain slot, 20 mm seat, R3 outside corners and R0.6 exposed edges. `Wis Tag` is debossed 0.2 mm into the inside floor at Z=2.5, leaving 2.3 mm backing. Text is nominal 4 mm DejaVuSans, centered by glyph bounds. Flip 180° about Y from the former underside label: +X text direction, tops toward the board (+Y), readable from the front. Underside restored flat. Peg mating geometry and 0.8 mm hidden overlap unchanged. These are design requirements, not measured device features; geometry remains unprinted.

## Verification plan and limits

`check(shape)` verifies insertion, seat/floor, walls, both pegs and the complete inner-floor label void with exact 0.2 mm depth and intact backing. Boolean comparison proves only the former underside marking was filled and the new inner-floor marking removed. See the model README for current export/visual verification. Numerical CAD tolerances are not manufacturing tolerances. Physical fit, rubber-shell friction, retention, printer behavior, cable access and board-side reset-button access remain unverified; no load rating or RF claim.
