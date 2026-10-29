# WisMesh Pocket V1 Multiboard cradle

**User-confirmed variant: original RAKwireless WisMesh Pocket (V1)**, factory 3D-printed enclosure with internal battery, OLED and external SMA antenna. Not a V2/V3 compatibility claim. The **94 × 52 × 30 mm enclosure dimensions come from the explicitly discontinued V1 PileupDX reseller listing**, not a manufacturer drawing or specimen measurement. Original RAK documentation establishes identity and interface locations but gives no finished envelope. This is an approximate trial-fit cradle based on secondary dimensional evidence; see the [hardware record](../../../research/objects/rak-wismesh-pocket-v1/README.md) and [issue #42](https://github.com/ShakataGaNai/b123d/issues/42).

## Dimensions and use

Units mm. X width, Y thickness (display/front −Y, wall/rear +Y), Z upright height. Device USB end sits on Z=2.5, antenna/lanyard up. Insert down from +Z and lift to remove; gravity only, no latch/strap. Upper display/button/antenna remain above the shallow rim.

| Feature | Dimension / evidence |
|---|---|
| V1 enclosure | 52 wide × 30 thick × 94 high; V1 reseller specification, tolerance unknown |
| Slot | 53.6 × 31.6; assumed 0.8 clearance per face |
| Insertion depth | 20 |
| Floor ledges / walls | 2.5 / 2.5 |
| Inner / outer XY corner radius | 0.5 / 3 |
| Bottom USB opening | Centered 24 wide × 31.6 through floor |
| Side access openings | Both sides, Y=±11.8, floor-seat to rim |
| Retained side strips | 4 mm at front/rear before rounded corners |
| Holder bounds including pegs | 58.6 × 43.1 × 22.5 |
| Snap pegs | Two, 13.5 across flats × 6.5 exposed; X=±12.5, Z=6.75 |

The bottom hole permits USB connection from below while the case rests on side ledges. The checked centered cable corridor is 20 mm wide; hole/corridor sizes are **design allowances, not measured port templates**. Verify the actual plug overmold, centering and downward bend space. Side openings avoid a guessed low-power-switch height/projection and retain guiding corner strips; trial-fit finger access and shell screw-head clearance. Remove from holder for enclosure servicing.

Two unchanged [registered Multiboard pegs](../../MODULES.md#multiboard-peg-and-rail-cutout) sit on 25 mm centers and are bottom-aligned with the bed. Use matching **snaps**, not direct tile multiholes. Confirm simultaneous straight installation of both snaps. No positive pull-out lock or load rating. Retain [connector provenance/license limitations](../../../research/objects/multiboard/measured-connectors.md) when sharing derived geometry.

Shared finish: R3 outside plan corners and free upper-end profiles, with R0.6
exposed rim, side-access and underside aperture edges. R3 end profiles precede
R0.6 edge rounds, avoiding equal-radius spherical-pole export degeneracies.
The hidden peg overlap is 0.8 mm; mating profiles and projection remain unchanged.

## Build and verification

```sh
uv run python scripts/build.py models/multiboard/wismesh_pocket --step
```

`build()` returns fresh geometry without import-time work. `check(shape)` covers one valid solid, envelope, nominal-device insertion, complete retained floor cores, USB/cable corridor, side openings/retained strips, straight/rounded walls, actual R0.6 rim boundaries and both peg sections/placements. CAD tolerance is not print compensation.

**unverified-fit; print_tested=false.** Rounded revision passed native/STEP checks, one-body watertight STL and millimeter 3MF round trip on 2026-10-16. Four-view PNG inspected; report timestamp `2026-10-16T21:37:46.475580+00:00`. Artifacts are under `outputs/multiboard/wismesh_pocket/`. Confirm actual V1 width/thickness before printing. No slicing, physical fit or load tests were performed; cable/switch/screw access and retention require a real-device trial.
