# MeshTracker X1 Multiboard pocket

Top-entry holder for the **Seeed SenseCAP MeshTracker X1**, SKU **100093876**. The 25 mm-tall rectangular body has a **measured angled-bottom pocket**, rounded top/sides, and the registered Multiboard snap peg with its lowest flat flush with the holder bottom. No rail, latch or exact enclosure-contour cutter is used.

## Dimensions

All dimensions are **mm**.

| Feature | Dimension |
|---|---:|
| Pocket body, width × depth × height | 62.8 × 13.8 × 25 |
| Top slot, width × thickness | 57.8 × 8.8 |
| Central slot depth from top to floor | 22.5 |
| Straight walls / floor | 2.5 / 2.5 |
| Outside vertical-corner fillet radius | 0.8 |
| Outside top-rim fillet radius | 0.6 |
| Slot-entrance fillet radius | 0.5 |
| Rear peg across flats / projection | 13.5 / 6.5 |
| Peg center above bottom / lowest flat | 6.75 / 0 |
| Total envelope, including peg | 62.8 × 20.3 × 25 |
| Pocket corner slope, horizontal run / vertical rise | 5 / 10 |
| Angled-to-straight pocket transition above bottom | 12.4056 |

The bottom remains flat. Fillets thin the rim locally; 2.5 mm describes the straight walls, not a certified minimum normal wall thickness. The peg is a straight octagonal prism with its original profile preserved, not a direct connector for the board's larger Multihole.

## Measurement basis and fit

Following the requested **measure-first** approach, the [X1 research record](../../research/objects/seeed-meshtracker-x1/README.md) measures the shell STL instead of reconstructing its exact contours. Its lower 22.5 mm spans approximately **57 × 8 mm**. Repeated lower sections also establish the angled sides: a **5 mm horizontal run over 10 mm vertical rise**, approximately **26.565° from vertical**, reaching a nominal 47 mm-wide flat base. A square-bottom cavity would leave those corners unsupported; the revised cutout retains matching sloped support surfaces.

The top slot remains 57.8 × 8.8 mm. Its lower profile follows the measured slopes, offset outward by **0.4 mm normal to the ramps**; the straight front/back and upper side allowances are 0.4 mm per side. The flat floor is at Z=2.5, with pocket half-width 23.9472 mm there; ramps meet the full-width opening at Z≈12.4056. Straight lines envelope the source's rounded slope endpoints rather than exactly reconstructing them. Checks against all measured lower-band vertices and entry-plane triangle intersections give approximately **0.4000 mm normal ramp clearance** and **0.3997 mm minimum front/back clearance**. This is an uncalibrated design allowance, not a physical fit claim: the reference mesh is nonwatertight and was not used as a volume.

The rear mount imports **`from models.multiboard.peg import peg`**, following [the module registry](../MODULES.md#multiboard-peg-and-rail-cutout); there is no duplicate peg construction in this model. The registered helper is unchanged. It supplies the documented 13.5 mm across-flats / 6.5 mm projecting profile, placed with its root on the rear wall and center at Z=6.75, so its lowest flat is **Z=0**. [The existing-holder evidence](../../research/objects/multiboard/existing-holder-examples.md) records the author's confirmation that these pegs insert into snaps. Snap revision, retention force and printer compensation remain physically unverified.

Installed frame: X is width, +Y is the rear/board side, and +Z is up. The reference device is placed bottom-first using `(X, Y, Z) → (X, −Y + 2.5, −Z + 47.500031)` mm from its native STL frame. It rests at the 2.5 mm floor and extends above the pocket. The lower USB-C end is covered: **remove the tracker for charging**. This is an open-top gravity pocket, not an anti-ejection latch or protective case.

## Build and print

```sh
uv run python scripts/build.py models/meshtracker_x1_multiboard_holder
```

This generates STL + geometry-only 3MF with millimeter units, previews, and a report. Add `--step` for CAD exchange and STEP round-trip checks. A successful default build removes an older same-stem STEP.

Print upright as exported, with the holder floor and peg's lowest flat on XY and the slot facing +Z. The peg now rises from the bed rather than starting above it; inspect its 45° lower facets in the slicer before deciding on supports, and keep supports out of the pocket. PETG and 0.2 mm layers are reasonable starting assumptions, not tested process settings. Calibrate the peg/slot against the actual snap and tracker before relying on retention. No slicer or physical print verification has been performed.

`model.py` owns geometry parameters; `model.toml` records research and unverified-fit status. `build()` has no downloaded-file dependency. Changing pocket dimensions derives the body dimensions automatically; changing an edge radius or peg placement must still satisfy the geometric checks.

## Verification and artifacts

The build CLI passed on native geometry and the saved/reimported STEP: one valid solid, correct outer dimensions, open top-entry region, flat central floor, **supporting angled pocket boundaries at three heights**, and octagonal peg area/across-flats/diagonal flats with its lowest flat at **Z=0**. The exported STL is watertight, consistently oriented and one connected body. PNG and interactive HTML views were inspected, including the rear peg. A section overlay compares the actual exported holder mesh with the registered X1 mesh; seated and lifted insertion-envelope checks passed at 0, 2, 5, 10 and 22.5 mm lift.

These are historical verification results, not evidence that a 3MF has been regenerated. Consult the latest report for current exports and checks.

The outside radii are deliberately unequal. R0.8 sides combined with an R0.8 top produced degenerate corner-pole STL edges despite valid BREP; R0.8 sides with an R0.6 top avoids that junction without mesh repair or disabling validation.

Build output paths under `outputs/meshtracker_x1_multiboard_holder/`:

- `meshtracker_x1_multiboard_holder.step` — optional CAD exchange geometry, only with `--step`.
- `meshtracker_x1_multiboard_holder.stl` — printable mesh; import as millimeters.
- `meshtracker_x1_multiboard_holder.3mf` — geometry-only mesh with millimeter units, without slicer settings or material assignments.
- `preview.png`, `preview.html` — exported-mesh visualizations.
- `report.json` — build timestamp, native/mesh results and conditional STEP results.

Separately generated evidence (not regenerated by the build command):
- `fit-estimate.json` — angled-profile and insertion-envelope clearance estimates.
- `fit-section.png` — actual holder/device mesh section showing the matching lower slopes.

Measurements remain at `outputs/research/meshtracker-x1/{holder-measurements,angled-base-sections,angled-base-estimate}.json`. Original hardware revision, print shrinkage, actual insertion/removal, snap retention/load and physical fit remain untested. Initial holder: [#14](https://github.com/ShakataGaNai/b123d/issues/14); angled-pocket/module/bottom-alignment correction: [#18](https://github.com/ShakataGaNai/b123d/issues/18). Measure-first guidance: [#16](https://github.com/ShakataGaNai/b123d/issues/16).
