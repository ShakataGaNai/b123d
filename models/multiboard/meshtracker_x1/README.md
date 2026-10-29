# MeshTracker X1 Multiboard pocket

Top-entry holder for the **Seeed SenseCAP MeshTracker X1**, SKU **100093876**. The 25 mm-tall body preserves the measured angled-bottom pocket, with two registered Multiboard snap pegs at X=±12.5 mm, standard R3/R0.6 finishing and an **X1** label inside the slot floor. No rail, latch or exact enclosure-contour cutter is used.

**Revised geometry is unprinted** ([#43](https://github.com/ShakataGaNai/b123d/issues/43)). The preceding single-peg geometry was printed, tested and approved by the user on 2026-10-16 ([#29](https://github.com/ShakataGaNai/b123d/issues/29)). That historical approval does not cover this revision; printer/material settings and quantified retention were not supplied.

## Dimensions

All dimensions are **mm**.

| Feature | Dimension |
|---|---:|
| Pocket body, width × depth × height | 62.8 × 13.8 × 25 |
| Top slot, width × thickness | 57.8 × 8.8 |
| Central slot depth from top to floor | 22.5 |
| Straight walls / floor | 2.5 / 2.5 |
| Outside vertical-corner radius | 3 |
| Outside top/bottom and slot-entrance edge radius | 0.6 |
| Two rear pegs, across flats / projection | 13.5 / 6.5 |
| Peg centers X / spacing | ±12.5 / 25 |
| Peg center above bottom / lowest flat | 6.75 / 0 |
| Total envelope, including pegs | 62.8 × 20.3 × 25 |
| Pocket corner slope, horizontal run / vertical rise | 5 / 10 |
| Angled-to-straight pocket transition above bottom | 12.4056 |

The inside-floor label **X1** is debossed exactly 0.2 mm below the Z=2.5 seat, leaving 2.3 mm backing. Nominal 4 mm DejaVuSans text uses matplotlib's explicit bundled font and actual glyph-bound centering. A 180° flip about Y from the former underside marking makes it readable from the front when mounted: letters run +X, with tops toward the board (+Y). The shared check proves the complete glyph void, backing and restored flat underside. Rounds thin the rim locally; 2.5 mm describes straight walls away from rounds. Peg mating profiles and 0.8 mm hidden root overlap are unchanged.

## Measurement basis and fit

Following the requested **measure-first** approach, the [X1 research record](../../../research/objects/seeed-meshtracker-x1/README.md) measures the shell STL instead of reconstructing its exact contours. Its lower 22.5 mm spans approximately **57 × 8 mm**. Repeated lower sections also establish the angled sides: a **5 mm horizontal run over 10 mm vertical rise**, approximately **26.565° from vertical**, reaching a nominal 47 mm-wide flat base. A square-bottom cavity would leave those corners unsupported; the revised cutout retains matching sloped support surfaces.

The top slot remains 57.8 × 8.8 mm. Its lower profile follows the measured slopes, offset outward by **0.4 mm normal to the ramps**; the straight front/back and upper side allowances are 0.4 mm per side. The flat floor is at Z=2.5, with pocket half-width 23.9472 mm there; ramps meet the full-width opening at Z≈12.4056. Straight lines envelope the source's rounded slope endpoints rather than exactly reconstructing them. Checks against all measured lower-band vertices and entry-plane triangle intersections give approximately **0.4000 mm normal ramp clearance** and **0.3997 mm minimum front/back clearance**. This is an uncalibrated design allowance, not a physical fit claim: the reference mesh is nonwatertight and was not used as a volume.

The rear mount imports **`models.multiboard.peg.peg`** twice, following [the module registry](../../MODULES.md#multiboard-peg-and-rail-cutout). Each unchanged 13.5 mm across-flats / 6.5 mm projecting profile is centered at Z=6.75, lowest flat Z=0. Two compatible snaps on 25 mm centers are required; these are not direct tile-Multihole connectors. The [existing-holder evidence](../../../research/objects/multiboard/existing-holder-examples.md) records the original interface provenance. Snap revision and quantified retention remain unspecified.

Installed frame: X is width, +Y is the rear/board side, and +Z is up. The reference device is placed bottom-first using `(X, Y, Z) → (X, −Y + 2.5, −Z + 47.500031)` mm from its native STL frame. It rests at the 2.5 mm floor and extends above the pocket. The lower USB-C end is covered: **remove the tracker for charging**. This is an open-top gravity pocket, not an anti-ejection latch or protective case.

## Build and print

```sh
uv run python scripts/build.py models/multiboard/meshtracker_x1
```

This generates STL + geometry-only 3MF with millimeter units, previews, and a report. Add `--step` for CAD exchange and STEP round-trip checks. A successful default build removes an older same-stem STEP.

Print upright as exported, floor and peg lowest flats on XY, slot facing +Z. Inspect the 45° peg facets and shallow interior-floor lettering in the slicer. PETG and 0.2 mm layers are starting recommendations, not confirmed settings for this revision. Keep supports out of the pocket.

`model.py` owns geometry parameters; `model.toml` marks this revision unprinted. `build()` has no downloaded-file dependency. Changes require renewed geometric checks and physical approval.

## Verification and artifacts

Historical single-peg builds passed native/STEP checks, mesh export and measured-device insertion/section checks. Those exports are not evidence for the #43 revision. Current checks retain the insertion, angled support and floor proofs, check both peg sections and diagonal flats, and geometrically verify exact glyph removal, 0.2 mm depth and no floor breakthrough.

The shared finish uses R3 plan corners and R0.6 top/bottom and mouth edges. Inspect inside-floor text and both roots before printing; the earlier R0.8-side finish and underside marking are superseded.

Inside-floor revision passed native/STEP checks, one-body watertight STL and
millimeter 3MF round trip on 2026-10-16 (report `2026-10-16T21:44:41.866584+00:00`).
PNG/HTML inspected. `inside-floor-inspection.png` shows the exported-STL lettering
with contrast enhanced, board side at top. Text is shallow in ordinary shading.
Boolean comparison against the preceding STEP proves only the old label was filled
and the new inner label cut: 0.835908 mm³ each, with no other geometry changed.

Build output paths under `outputs/multiboard/meshtracker_x1/`:

- `meshtracker_x1.step` — optional CAD exchange geometry, only with `--step`.
- `meshtracker_x1.stl` — printable mesh; import as millimeters.
- `meshtracker_x1.3mf` — geometry-only mesh with millimeter units, without slicer settings or material assignments.
- `preview.png`, `preview.html` — exported-mesh visualizations.
- `report.json` — build timestamp, native/mesh results and conditional STEP results.

Separately generated evidence (not regenerated by the build command):
- `fit-estimate.json` — angled-profile and insertion-envelope clearance estimates.
- `fit-section.png` — actual holder/device mesh section showing the matching lower slopes.

Measurements remain at `outputs/research/meshtracker-x1/{holder-measurements,angled-base-sections,angled-base-estimate}.json`. Prior physical approval applies only to the preceding single-peg holder; original hardware revision, print settings and quantified retention remain unspecified. Initial holder: [#14](https://github.com/ShakataGaNai/b123d/issues/14); angled-pocket correction: [#18](https://github.com/ShakataGaNai/b123d/issues/18); measure-first guidance: [#16](https://github.com/ShakataGaNai/b123d/issues/16); current finish, label and dual pegs: [#43](https://github.com/ShakataGaNai/b123d/issues/43).
