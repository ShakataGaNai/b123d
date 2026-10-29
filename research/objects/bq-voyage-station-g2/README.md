# BQ Voyage Station G2 — Multiboard cradle research

Recorded 2026-10-16, before holder geometry. Consumer: [`multiboard/station_g2`](../../../models/multiboard/station_g2/README.md). Work: [#41](https://github.com/ShakataGaNai/b123d/issues/41).

## Hardware and primary sources

This record concerns **Station G2's original stacked-PCB enclosure**, not Station G3, Nano G2, or an aftermarket printed enclosure. The official comparison table identifies current G2 hardware as **01 Jun 2024**, initial release 18 Jan 2024; the user's exact board date is unknown.

- BQ Voyage, [Station G2 wiki](https://wiki.bqvoy.com/en/meshtastic/station-g2), accessed 2026-10-16, page updated 2026-10-11. Relevant sections: Characteristics → Dimension, Hardware → Mechanical Design, PCB. Dimension tab specifies **11 cm × 5.8 cm × 2.2 cm**, black, approximately 87.5 g without antenna. No mechanical tolerances or exclusion of screw heads are stated.
- BQ Voyage, [mechanical assembly photograph](https://wiki.bqvoy.com/meshtastic/station_g2/station_g2_mechanical_design.jpg), linked from Mechanical Design; revision/date unknown, accessed 2026-10-16. Shows stacked front panel, aluminum heat-spreader, main PCB and rear panel, nylon screws/nuts, and USB on one short edge with SMA on the opposite edge. Used for orientation only, **not scaled for dimensions**.
- BQ Voyage, [overview photograph](https://wiki.bqvoy.com/meshtastic/station_g2/station_g2_overview.jpg), revision/date unknown, accessed 2026-10-16. Confirms antenna-up, USB-down orientation with screen facing forward.
- User correction on 2026-10-16: **body thickness is 12 mm WITHOUT screws**, and big rear screws project approximately **5 mm**. The previous boxy split-front cradle does not work. These observations govern the revised model; the 12 mm body supersedes the web page's ambiguous 22 mm thickness for this specimen. Width 58 mm and height 110 mm remain manufacturer nominal.

Wiki HTML identifies content license as CC BY-NC-SA, exact version unknown. No third-party source assets are redistributed here; links and original extraction notes only. No asset checksum is applicable. The first text-reader response omitted tab content; the raw page's Dimension table supplied the numeric evidence.

## Dimension and interface table

Units normalized from cm to mm by ×10. Holder axes: X = short-edge width; Y = front-to-rear, positive toward Multiboard; Z = antenna-up insertion direction. Nominal device centered at X=Y=0, bottom at holder floor Z=2.5.

| Feature | Value / location | Evidence class and limitation |
| --- | --- | --- |
| Long dimension | 110 mm, modeled along Z | Manufacturer nominal; no tolerance |
| Short dimension | 58 mm, modeled along X | Manufacturer nominal; no tolerance |
| Front-to-rear body thickness | **12 mm**, modeled Y=−6…+6, excluding screws | User-corrected specimen dimension; supersedes web 22 mm for this holder |
| Rear screw projection | approximately 5 mm beyond rear body datum | User-reported; uncertainty not quantified |
| Rear screw diameter / centers | Unknown | Not required: full-width continuous clearance, no screw holes |
| Assembly fasteners | 4× M3×15 screws, 2× M3×10 screws, 4× M3 nuts, 6× M3×6 female-female studs | Official mechanical BOM; not a hole-pattern specification |
| Bottom USB-C | On lower short edge | Official photographs; exact center, plug dimensions and projection unknown |
| Antenna SMA | Opposite short edge, above holder | Official photographs; attached antenna envelope unknown |
| Side accessory connectors | Grove GPS/I2C, QWIIC, IO extension, external power | Official PCB list; mating cable envelopes and coordinates unknown |

## Modeling decisions and allowances

- Use **58 × 12 mm** rectangular body cross-section and 110 mm height. Keep the conflicting published 22 mm thickness in the source record, not in the functional envelope.
- Lateral gap **0.6 mm each side**; front gap **0.6 mm**. Rear uninterrupted relief **6.5 mm = 5 mm nominal screw projection + 1.5 mm explicit fit allowance**, from Y=6 to 12.5. Opening is **59.2 × 19.1 mm**, with **R0.5 inner plan corners**; the radius is less than the side gap, so the full 58 mm-wide rear screw band reaches the rear inner datum without corner interference. These allowances are not manufacturer tolerances.
- Replace the failed boxy, split-floor, lowered-front design with a simple rounded top-entry slot: **2.5 mm closed floor and walls**, **20 mm insertion** above floor, continuous front/side/rear walls. Outside plan corners are **R3**; outer top/bottom and exposed slot mouth are **R0.6**, using the shared Multiboard finish helper. The seating-floor edge is not rounded.
- No USB opening is guessed. Exact USB position and plug envelope are unmeasured, so the floor stays closed and the device must be removed for bottom USB access. This intentionally replaces the former unsupported 30 mm front/floor opening and its two claws.
- Rear wall and peg roots stay beyond Y=12.5. Two standard pegs on **25 mm X centers**, each **13.5 mm across flats × 6.5 mm exposed projection**, bottom-aligned at Z=0. Root overlap **0.8 mm** bridges the R0.6 underside round without entering the pocket. Use matching Multiboard **snaps**, not direct tile Multiholes. See [peg evidence](../multiboard/measured-connectors.md) and its source-license limitations.
- Upper device and antenna remain open. Connectors within the lowest 20 mm may be covered; this is a gravity holder, not an accessory-access enclosure. Rear clearance is screw space, not a custom wire raceway.

## Verification scope and remaining uncertainty

The revised `check()` covers actual 12 mm body insertion, full 58 mm-wide screw corridor including allowance, rounded opening, complete floor, continuous walls, R3/R0.5 plan corners, R0.6 edges and both pegs. Current revision passed native/STEP, watertight one-body STL and millimeter 3MF checks on 2026-10-16; four-view PNG inspected. See the model README and generated report for evidence.

Historical only: on 2026-10-16 the **superseded 22 mm, split-front cradle** passed native/STEP checks and one-body watertight STL/3MF checks, with PNG/HTML inspection. The user subsequently reported that cradle does not work; those checks are not evidence for this replacement. No physical print success is recorded.

Physical fit and thermal suitability remain unverified. Exact resting edges, screw-head lateral extent, manufacturing tolerance and cable/side-connector envelopes remain unmeasured. Screws are assumed to stay within the 58 × 110 mm front/rear silhouette; no screw-center assumption is made. Trial fit the corrected slot before use. Gravity retention only: not a locking, vehicle, vibration, or inverted mount. CAD clearance checks are not load or thermal qualification.
