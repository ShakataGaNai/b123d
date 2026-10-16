# LilyGO T-Deck Plus Multiboard cradle

**User-confirmed variant: factory-enclosed T-Deck Plus**, with its internal battery/GPS. Not the bare T-Deck or T-Deck Pro. LILYGO's finished-device graphic labels 72 × 115 × 20 mm; the official Plus STEP establishes the rounded lower shape and 20.4 mm whole-shell thickness. See [manufacturer measurements/provenance](../../research/objects/lilygo-tdeck-plus/README.md), saved before geometry changes, and [issue #40](https://github.com/ShakataGaNai/b123d/issues/40).

## Dimensions and use

Units mm. X width, Y thickness (keyboard/front −Y; rear/mount +Y), Z upright height. Print underside is Z=0; simplified device bottom/support datum Z=2.5. Lower the keyboard/USB end vertically from +Z and lift to remove. Gravity storage, not a typing dock, thermal enclosure or positively locked mount. Lower keyboard rows and side vents are partly shielded; remove for typing/service and verify safe contact/cooling.

| Feature | Dimension / evidence |
|---|---|
| Nominal lower device envelope | 72 wide × 20.4 thick × 115 high; lower STEP section is approximately 71.956 × 19 |
| Slot maximum section | 73.6 × 22.0, assumed 0.8 clearance per side |
| Insertion depth | 20 |
| Minimum walls / supporting floor ledges | 2.5 / 2.5 |
| Broad-face lower seat | R16.8 approximation of measured B-spline bottom, not an exact factory radius |
| Inner XY / outer XY corner radius | 2.2 / 3 |
| Exposed outer, mouth and underside USB edges | Shared R0.6; functional seat and pegs unchanged by cosmetic rounding |
| Bottom USB opening | Centered 24 wide × 22.0 through floor; design allowance |
| Holder bounds including pegs | 78.6 × 33.5 × 22.5 |
| Snap pegs | Two, 13.5 across flats × 6.5 exposed, X=±12.5 and Z=6.75; 0.8 root overlap |

Connect USB from below after mounting; the central opening preserves broad side support ledges and avoids resting on the plug. A centered cable corridor up to 20 mm wide is geometrically checked, **not** a measured universal USB plug fit. Verify actual port offset, overmold and downward bend space; leave slack. Do not route cable between holder and board. The upper antenna area stays above the pocket; rear tripod accessories, additional cases and modified antenna arrangements are not included.

The previous flat-bottom box is replaced by a **rounded lower seat in the broad width/height plane**, not merely larger XY corners. Official STEP sections widen from 44.23 mm at 2 mm above the bottom to 71.95 mm around 16 mm. The simple R16 nominal lower envelope (R16.8 cavity with clearance) stays outside the measured shell samples; it is deliberately not a tight negative mold. Measured station gaps are approximately 0.25–2.6 mm before settling. Side ledges beside the USB opening support the lower shell, while the curved seat rises toward both ends. Slight settling/rocking and real specimen tolerances require trial fit. The XY thickness envelope is independently conservative; the 73.14 mm upper-button assembly width never enters this shallow pocket.

The unchanged [registered Multiboard pegs](../MODULES.md#multiboard-peg-and-rail-cutout) are on 25 mm horizontal centers, bottom-aligned with the bed. They mate to **snap receivers**, not directly to tile multiholes. Both receivers must permit simultaneous straight insertion. No positive pull-out lock or load rating. Preserve the [connector attribution/noncommercial/share-alike limitations](../../research/objects/multiboard/measured-connectors.md).

## Build and verification

```sh
uv run python scripts/build.py models/lilygo_tdeck_multiboard_holder --step
```

`build()` returns fresh geometry without import-time construction/export or downloading manufacturer files. `check(shape)` checks one valid solid, envelope, continuous rounded-shell insertion sweep, independent manufacturer section witnesses, rising rounded seat/support material, flat ledges, USB/cable passage, analytical upper-wall section, R0.6 edge/mouth boundaries, and both peg sections/placements. The former square-prism insertion and unfilleted whole-volume formula no longer describe this geometry. CAD tolerances are not print allowances.

**unverified-fit; print_tested=false.** Current rounded-seat revision passed native/STEP design checks, one-body watertight STL and millimeter 3MF round trip on 2026-10-16. Four-view PNG inspected, including rising curved seat and USB opening. Report timestamp `2026-10-16T21:38:10.910676+00:00`, under `outputs/lilygo_tdeck_multiboard_holder/`. This supersedes the earlier square-bottom build; physical fit remains untested.

No slicing or physical fit/load test was performed. Print floor-down with calibrated FDM settings; inspect floor aperture, rounded lower seat and peg roots in the slicer. Trial-fit the actual Plus case and both snaps, checking seating, rocking, key pressure, USB access, cooling and removability. No transport retention or drop protection.

2026-10-16 revision: measured the official Plus shell after the user reported a much rounder bottom; replaced the flat pocket with a manufacturer-informed rounded lower seat, increased thickness allowance to cover the actual 20.4 mm CAD envelope, and applied the shared outside finish from [issue #43](https://github.com/ShakataGaNai/b123d/issues/43).
