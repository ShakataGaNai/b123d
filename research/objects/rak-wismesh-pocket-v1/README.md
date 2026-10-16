# RAKwireless WisMesh Pocket: original V1

Research date: 2026-10-16. Work: [#42](https://github.com/ShakataGaNai/b123d/issues/42). Consumer: [WisMesh Pocket V1 Multiboard cradle](../../../models/wismesh_pocket_multiboard_holder/README.md).

## Identity and evidence tier

The user explicitly confirmed the **original WisMesh Pocket (V1)**, not V2 or V3. Target: original factory 3D-printed enclosure with internal battery, OLED display, external SMA antenna and low side power switch. RAK's original overview describes a 3600 mAh battery; the discontinued dealer listing describes 3200 mAh. Battery capacity is not used to infer case size. Exact PCB/enclosure revisions and production tolerances are unknown.

Readiness: **approximate with listed assumptions**. Primary manufacturer sources establish the original product and interfaces, but reviewed primary sources do **not** give the V1 finished envelope. The **94 × 52 × 30 mm** enclosure size is supported by an explicitly discontinued **V1 reseller listing**, not by a manufacturer drawing, measurement or presumed equivalence to V2. This secondary-evidence limitation remains visible in model documentation.

## Sources and retrieval limits

All accessed 2026-10-16. Publication dates, drawing revisions and dimensional tolerances are unknown. Manufacturer documentation carries an all-rights-reserved notice; reseller image redistribution permission is unknown. No source images/PDF/CAD bytes are committed; no asset checksum applies.

| ID | Publisher and source | Evidence / classification |
|---|---|---|
| V1 | RAKwireless, [original WisMesh Pocket overview](https://docs.rakwireless.com/product-categories/meshtastic/wismesh-pocket/overview/) | Primary identity; 3600 mAh battery and external antenna. The current download link points to V2 PDF, which is not V1 dimension evidence. |
| V2 | RAKwireless, [original Pocket quick start](https://docs.rakwireless.com/product-categories/meshtastic/wismesh-pocket/quickstart/) and [legacy repository source](https://github.com/RAKWireless/rakwireless-docs/blob/master/docs/Product-Categories/Meshtastic/WisMesh-Pocket/Quickstart/README.md) | Primary original interfaces: USB-C charging, power switch, external SMA and internal BLE/GNSS antennas. No finished-envelope values. |
| V3 | RAKwireless, [original disassembly illustration](https://res.rakwireless.com/ext/images.docs.rakwireless.com/meshtastic/install-01.png?fm=webp) | Primary qualitative locations: bottom USB, low side switch, upper user button, antenna/lanyard opposite USB. No numerical port template. |
| V4 | PileupDX, [discontinued original RAK WisMesh Pocket](https://pileupdx.com/product/rak-wismesh-pocket/) | **Secondary reseller evidence:** page explicitly says discontinued/replaced by Pocket V2 and lists enclosure **94mm × 52mm × 30mm**, antenna 51 mm long × 8 mm diameter, 3D-printed case. Original product identity is explicit; page metadata last modified 2026-01-20, not a mechanical revision. |
| V5 | RAKwireless, [current store](https://store.rakwireless.com/products/wismesh-pocket) and [V3 overview](https://docs.rakwireless.com/product-categories/meshtastic/wismesh-pocket-v3/overview) | Variant exclusion only: store now identifies V2; V3 explicitly changes to an injection-molded enclosure. Neither supplies V1 fit proof. |

Additional searches covered the original GitHub documentation, manufacturer portable-enclosure CAD catalog (currently V2/alternative cases), S3 Meshtastic and ebook listings including archive guides, and Wayback availability for the original store URL at 2024-08-01 (no available snapshot returned). No primary V1 finished-envelope drawing or usable V1 CAD was established. Do not promote V4's numbers to manufacturer evidence.

## Dimensions and coordinate contract

Source/model units mm. X is enclosure width; Y thickness with display/front −Y and board-facing rear +Y; Z is height. USB end down; antenna/lanyard end up. Device bottom sits at model Z=2.5, centered on X=Y=0. Holder underside Z=0. V4's dimensions are interpreted height × width × thickness using V3's orientation; the separately listed antenna is not part of the cradle envelope.

| Feature | Value | Class / source | Uncertainty |
|---|---:|---|---|
| Enclosure height | 94 mm | Reported secondary specification, V4 | Manufacturer tolerance and lanyard inclusion unknown |
| Enclosure width | 52 mm | Reported secondary specification, V4 | Not measured; switch projection inclusion unspecified |
| Enclosure thickness | 30 mm | Reported secondary specification, V4 | Screw-head inclusion/tolerance unspecified |
| USB | Bottom, near center | Qualitative primary illustration V3; USB-C per V2 | Port center and cable overmold undimensioned |
| Power switch | Low side wall | Qualitative primary illustration V3 | Depth position and projection undimensioned |

No hardware mounting holes are used; the cradle does not fasten to shell screws. Hole sizes/centers and screw service envelopes are therefore intentionally not invented. Remove device for enclosure servicing.

## Allowances and design

- Slot **53.6 × 31.6 mm** from the V1 reseller-supported 52 × 30 cross-section plus **0.8 mm clearance per face**, explicitly uncalibrated. The dimensions happen to match the earlier V2 candidate, but their evidence is now V1-specific V4; no V2 equivalence is assumed.
- 20 mm shallow insertion, 2.5 mm floor ledges/walls, inner XY radius 0.5 mm and outer radius 3 mm. Holder including pegs: **58.6 × 43.1 × 22.5 mm**. Conservative square-envelope insertion, no exact shell contour claim.
- Centered **24 × 31.6 mm through-floor USB opening**; two floor ledges support the case. A centered 20 mm-wide cable corridor is checked. Opening size/center and cable corridor are design allowances, not measured connector geometry. Route cable downward with slack; trial-fit actual port/overmold and bend space.
- Open-top side reliefs on both sides, **23.6 mm in Y** (Y=±11.8), from seat to rim; 4 mm of retained side strip at front/rear before rounded corners. These avoid a guessed low-switch-height cutout; verify physical finger access. Front/rear walls and retained corner strips guide insertion.
- Two registered 13.5 mm AF × 6.5 mm snap pegs, X=±12.5 and Z=6.75, 25 mm horizontal spacing, 0.8 mm buried overlap bridging the underside round. [Multiboard source/grid record](../multiboard/README.md); [peg attribution/license scope](../multiboard/measured-connectors.md).
- Shared R3 outside plan and free upper-end profile corners, then R0.6 exposed edge rounds. Distinct profile/edge radii avoid coincident spherical-pole triangulation failures. Functional side openings and nominal insertion envelope remain unchanged.
- Gravity-only storage, no latch/strap/load rating. Antenna/lanyard and upper display/button remain above the 20 mm rim. No accessory case/battery or modified downward antenna support.

## Verification and limitations

`check(shape)` covers one valid solid, envelope, nominal-device insertion, retained floor cores, USB/cable passage, side relief/retained strips, walls, edge boundaries and peg sections/centers. Current rounded revision passed native/STEP checks, watertight one-body STL and millimeter 3MF round trip on 2026-10-16; PNG/HTML inspected. See the model README for the report timestamp. No slicing, specimen measurement, physical fit or load test was performed.

Confirm **actual V1 width/thickness** before printing, then trial-fit the device and both snap receivers without force. Cable/switch access, screw heads, rocking, simultaneous snap insertion and pull-out/load behavior remain untested. Print floor-down in XY/+Z up; inspect the floor hole, side openings and peg roots in the slicer. No universal Pocket compatibility or support-free printing claim follows from valid CAD.

2026-10-16: user-confirmed V1 record saved before retargeting model metadata/source; replaces preliminary V2 research. Dimensional evidence is V1-specific but secondary.
