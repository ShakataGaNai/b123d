# M5Stack Unit C6L (U202)

## Identity and scope

Research date: 2026-10-16. Manufacturer: M5Stack. Product: Unit C6L, SKU U202,
868–923 MHz enclosed LoRa unit. The user's hardware revision is unknown; the
manufacturer's mechanical drawing has no visible revision/date identifier.
Electrical schematic B0.4.1 is linked on the product page but is not proof of the
specimen's mechanical revision. Consumer: `models/multiboard/unit_c6l/`.

Readiness: **approximate with listed assumptions**. Authoritative external
cross-section dimensions support a simple gravity pocket; no exact shell contour
or connected-cable fit is claimed. Antennas remain above the holder.

## Sources

| ID | Publisher / source | Revision / date | Evidence | Access / terms |
|---|---|---|---|---|
| S1 | M5Stack [Unit C6L documentation](https://docs.m5stack.com/en/unit/Unit_C6L) | Live page, revision/date unknown | SKU U202; 62 × 24 × 8 mm excluding antennas; 13.6 g; USB-C and Grove interfaces | 2026-10-16; redistribution terms unknown |
| S2 | M5Stack [Unit C6L model-size PDF](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1185/U202-MODEL-SIZE-unit-2sma.pdf), linked by S1 | `U202-MODEL-SIZE-unit-2sma`, revision/date unknown | Page 1 orthographic drawing, explicitly mm | 2026-10-16; redistribution terms unknown |
| S3 | M5Stack [drawing image](https://m5stack-doc.oss-cn-shenzhen.aliyuncs.com/1185/U202-MODEL-SIZE-unit-2sma_page_01.png) | Same drawing as S2 | Visually inspected dimensions and connector positions | 2026-10-16; redistribution terms unknown |

No manufacturer assets are committed: redistribution permission is unknown.
A temporary image was inspected; the model has no downloaded-file dependency.

## Dimensions and datums

Source and CAD units are mm. In the holder frame, X is device width, Y is
thickness (+Y toward Multiboard), and Z is vertical with antenna connectors up.
Device bottom is seated at holder Z=2.5; the holder print-bed datum is Z=0.
No scaling or CAD-source registration is required for this primitive envelope.

| Feature | Value | Class / evidence | Consequence |
|---|---:|---|---|
| Shell width | 24 | Authoritative, S2/S3 front view | Supersedes user's approximate 23 mm |
| Shell thickness | 8 | Authoritative, S2/S3 end view | Agrees with user's estimate |
| Shell height | 56 | Authoritative, S2/S3 front view | 44 mm of shell remains above a 12 mm pocket |
| Height including antenna connector stubs | 62 | Authoritative, S1 and S2/S3 | Not the shell-only height; excludes attached antennas |
| Front-outline bottom corner radius | 3 | Authoritative, S2/S3 | Simplified by a flat pocket floor; no exact conforming seat |
| End-view shell edge radius | 0.5 | Authoritative, S2/S3 | Full 24 × 8 rectangular clearance envelope is conservative |
| Two lower mounting holes | Diameter 5; 16 center spacing; 12 above bottom | Authoritative, S2/S3 | Not used for attachment; do not derive hidden bore depth |

Manufacturer tolerances are not specified. These are nominal drawing dimensions,
not specimen measurements. The rounded lower shell corners need not touch the
floor; its central bottom region provides gravity support.

## Keep-outs and limitations

Insert bottom-first along −Z, remove along +Z. No latch or anti-ejection feature.
The bottom HY2.0-4P Grove connector is covered by the closed floor: disconnect it
before insertion. The drawing shows side USB-C above the selected lower 12 mm,
but no USB opening coordinates or cable overmold dimensions are given; connected
USB cable clearance and button access are unverified. This is not a powered-cable
cradle. Upper screen and antenna connectors are outside the supported band.

## Design allowances, not product facts

- Slot: 24.8 × 8.8, with 0.4 clearance per side, uncalibrated for the printer.
- Insertion depth: 12, as requested; floor and walls: 2.5. Total height: 14.5.
- Slot XY corner radius: 0.5. Its rounded cutout still contains the entire nominal
  24 × 8 rectangular envelope; this is checked through the insertion path.
- Outer XY corner radius: 3, a 2.5 normal offset from the slot corners. These are
  rounded left/right outside corners, not semicircular ends cut into the device.
- Mount: registered Multiboard snap-insert peg, 13.5 across flats × 6.5 projection,
  bottom aligned at Z=0. See [measured connector evidence](../multiboard/measured-connectors.md)
  and the [module registry](../../../models/MODULES.md#multiboard-peg-and-rail-cutout).
  It requires a separate compatible snap, not the tile's large Multihole directly.
- Default printing setup: Prusa MK4S, PETG, and a 0.4 mm nozzle, confirmed by the
  user on 2026-10-16. Slicer profile is unspecified; 0.2 mm layers remain a
  recommendation, not a confirmed setting. The user subsequently confirmed this holder printed and validated good on 2026-10-16.
  Upright pocket orientation; inspect peg's lower diagonal overhangs in the slicer.
  Confirmed printing defaults alone do not justify changing the fit allowance.

## Verification contract

Check one valid solid, opening/depth/floor and constant wall offset, nominal-device
insertion clearance, and peg section/placement. Export STL/3MF and round-trip STEP;
inspect mesh previews. Physical drop-in fit, snap retention, cable access and print
quality remain untested. Tracked by [#32](https://github.com/ShakataGaNai/b123d/issues/32).
