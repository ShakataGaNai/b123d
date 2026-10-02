# Object geometry record: Seeed SenseCAP MeshTracker X1

## Identity and purpose

- Manufacturer: Seeed Studio. Exact product: **SenseCAP MeshTracker X1 for Meshtastic**, SKU **100093876** [S1, S3]. Not the T1000-E or Wio Tracker L1.
- Research date: 2026-10-01. Work item: [b123d #12](https://github.com/ShakataGaNai/b123d/issues/12).
- Intended interface: an external holder around the supplied enclosure. The [25 mm Multiboard pocket](../../../models/meshtracker_x1_multiboard_holder/README.md) uses this record; physical fit remains unverified. USB cable and supplied leather keychain are not included in the CAD envelope verification.
- Production hardware revision: **unknown**. CAD filename/export date identifies downloaded geometry, not the revision of a purchased specimen.
- Readiness: **ready as a nominal CAD reference for holder design**, not verified physical fit. Official shell STEP exists; the 8 mm specification versus approximately 9 mm CAD thickness remains unresolved.

## Sources

All sources accessed 2026-10-01.

| ID | Publisher / source | URL | Revision / relevant evidence | Terms |
|---|---|---|---|---|
| S1 | Seeed, exact-SKU product page | [Product page](https://www.seeedstudio.com/sensecap-meshtracker-x1-meshtastic-gps-tracker-p-6935.html) | Rendered resource link **Shell 3D File** points directly to S2. Text-only page extraction omitted the resource content. | No asset-specific CAD license identified. |
| S2 | Seeed, official shell STEP | [X1_Shell_20260914.stp](https://files.seeedstudio.com/wiki/SenseCAP/Meshtastic/X1_Shell_20260914.stp) | STEP header: `000_RAPTOR_BADGE_GEN_2_V1_ASM`, export `2026-09-14T13:55:50`, Creo Parametric. Source length units explicitly millimeters. Three imported solids. | Redistribution permission unknown; original stays in ignored outputs. |
| S3 | Seeed, industrial product datasheet | [100093876.pdf](https://files.seeedstudio.com/Bazaar/product_pdf/100093876.pdf) | SKU 100093876; updated 2026-09-21 10:07:42. Specification p. 5: 90 × 57 × 8 mm; resource list p. 8 names **Shell 3D File**. | No CAD-specific grant identified in extracted document. |
| S4 | Seeed, X1 introduction | [Wiki](https://wiki.seeedstudio.com/meshtracker_x1_intro/) | Nominal dimensions 90 × 57 × 8 mm. Resource section lists battery ZIP and consumption XLSX, not the shell STEP at access time. | [Wiki license policy](https://wiki.seeedstudio.com/License/) covers documents/images and software separately; do not assume it licenses S2 CAD. |
| S5 | Seeed, hardware illustration | [HardwareDiagramBu.png](https://files.seeedstudio.com/wiki/SenseCAP/MeshTrackerX1/HardwareDiagramBu.png) | Exploded/perspective enclosure, button, LED, antennas, buzzer and USB-C illustration. No dimension annotations or scale. | See wiki image policy; not copied into repository. |
| S6 | MakerNova, exact-X1 holster listing | [SenseCAP MeshTracker X1 Holster](https://makernova.io/products/sensecap-meshtracker-x1-holster-for-meshtastic) | Physical ASA holsters, MOLLE and Baofeng-clip versions; seller claims custom/rattle-free fit and shows device photos. Embedded display models available as GLB/USDZ, not a verified device-solid STEP. | No geometry reuse license verified. Do not copy the holster design merely because display assets are public. |

### Local assets and provenance

- Original STEP: `outputs/research/meshtracker-x1/X1_Shell_20260914.stp` (ignored, not committed).
- Original size: **4,719,561 bytes**.
- SHA-256: `07a332bcf9ec175f47269356e7b3aeee78950901455b90e16721ef60d21cf63f`.
- Inspection results: `outputs/research/meshtracker-x1/inspection.json`.
- Visualization derivative: `outputs/research/meshtracker-x1/shell.stl`; tessellation is not the exact CAD source. Preserve STEP for dimensional work.
- Interactive visualization: `outputs/research/meshtracker-x1/preview.html`, generated from the imported STEP's tessellated shell and inspected in Chromium.
- Downloaded data was imported as CAD; no manufacturer/community scripts were executed. No source CAD, PDF or images were added to tracked assets because CAD redistribution terms were not established and copied documentation was unnecessary.

## Units, datums and geometry

Source units: **mm**, explicitly declared as `SI_UNIT(.MILLI.,.METRE.)`. No scale conversion was applied. Coordinates below are the imported STEP frame; they are not a manufacturing/print-bed frame. X spans width, Y spans thickness, Z spans length. Original origin is retained; the object is not centered in Y or resting on Z=0. Front/back sign and a holder frame must be selected by inspecting the geometry rather than inferred from axis names.

| Feature | Value (mm) | Evidence class | Uncertainty / consequence |
|---|---|---|---|
| Published length × width × thickness | 90 × 57 × 8 | Authoritative nominal, S3/S4 | No production tolerance stated; thickness conflicts with S2. |
| Imported whole-CAD X × Y × Z bounds | 57.000108 × 9.000404 × 90.000700 | Derived from S2 BREP bounding box | Numerical CAD bounds, not specimen measurements or production tolerances. |
| Imported minimum X/Y/Z | −28.500020 / −1.500404 / −45.000001 | Derived from S2 | Retain source registration when importing individual components. |
| Imported maximum X/Y/Z | 28.500088 / 7.500000 / 45.000699 | Derived from S2 | Rounded envelope is approximately 57 × 9 × 90 mm. |
| Solid 0 X/Y/Z extent | 57.000108 / 9.000114 / 90.000700 | Derived from S2 | Main solid already spans approximately 9 mm thickness; do not attribute the entire 1 mm discrepancy to the separate small solid. |
| Solid 1 X/Y/Z extent | 15 / 1.750001 / 15 | Derived from S2 | Imported component identity not established by its unlabeled build123d solid. |
| Solid 2 X/Y/Z extent | 54.800000 / 5.250407 / 87.800000 | Derived from S2 | Do not use this smaller component alone as the whole-device envelope. |

No physical measurements were taken. Corner radii, shell contours, apertures and local features can be interrogated directly from S2 when designing a specific holder; they have not all been separately dimensioned here. Button actuation travel, plug-body/cable clearance, production variation and insertion/removal motion are not established by the overall bounds. No mounting-hole center table is claimed.

### Lower-body STL estimates for the rectangular holder

Follow-up requested in [#14](https://github.com/ShakataGaNai/b123d/issues/14): measure the STL like a physical specimen and use rounded rectangular cutout estimates, without exact contour reconstruction.

- Reference derivative: `outputs/research/meshtracker-x1/shell.stl`; SHA-256 `949265fb042619c5cd03ff33d95e47b8e7b6b569e4edd0a18246bc9f79832a7c`. This is the S2 visualization export, not a downloaded manufacturer STL. Millimeters are inherited from the source STEP/export; STL does not declare units.
- Measurement helper found 52,815 triangles, finite coordinates, consistent winding, **23 zero-area triangles and nonwatertightness**. Use as a rough dimension reference, not as a solid for volumetric fit claims. No repair, rescaling or recentering was used in measurement.
- Native sections at Z=24 and 32 span approximately **57 × 7.85–7.94 mm** on the main outer contour; Z=40 narrows to approximately **52 × 8 mm** near the end corners. These are cross-section bounds, not circular diameters.
- Combining all vertices in the lower 22.5 mm band with the entry-plane triangle intersections gives X/Y/Z spans **56.999987 × 8.000682 × 22.5 mm**. Source band Z=22.500031..45.000031; its Y bounds are −1.500348..6.500333. Multiple shell contours were considered together, not just one component.
- Adopt **57 × 8 mm** as the rough inserted-body estimate. This does not shrink or reinterpret the whole 9 mm-thick reference: the thicker region remains outside the 25 mm holder.
- Holder design allowance: **0.4 mm per side**, yielding a **57.8 × 8.8 mm** top slot, with 2.5 mm floor and straight walls. The lower cutout now follows the measured angled corners below rather than remaining rectangular to the floor. The allowance is an uncalibrated design choice, not physical fit evidence.
- Registration for upright bottom-first placement: source `(X, Y, Z)` becomes holder `(X, −Y + 2.5, −Z + 47.500031)` mm (180° X rotation, then translation). The lower source +Z end sits on the holder's 2.5 mm floor; source front +Y faces holder front −Y.
- Raw estimate results: `outputs/research/meshtracker-x1/holder-measurements.json`. Mesh faceting, unidentified production revision and physical print variation remain uncertainties.

### Angled-base measurement correction

[#18](https://github.com/ShakataGaNai/b123d/issues/18) corrects the initial holder's square-bottom cutout. Native Z sections were measured at 23, 28, 32, 34–44, 44.5 and 44.8 mm; all contours contributed to each section's bounds. Results are in `outputs/research/meshtracker-x1/angled-base-sections.json`.

| Native source Z (mm) | Height above the lower end, rounded (mm) | Outer half-width, rounded (mm) |
|---|---:|---:|
| 32 | 13 | 28.5 |
| 37 | 8 | 27.5 |
| 38 | 7 | 27 |
| 39 | 6 | 26.5 |
| 40 | 5 | 26 |
| 41 | 4 | 25.5 |
| 43 | 2 | 24.26 |
| 44 | 1 | 23.09 |
| 44.8 | 0.2 | 21.32 |

The straight angled segment at native Z=37..41 gives **half-width = 23.5 + 0.5 × height above the lower end**, approximately **26.565° from vertical**. Rounded construction dimensions: **5 mm horizontal run over 10 mm vertical rise**, joining the full 57 mm-wide body to a nominal **47 mm-wide flat base**. The source rounds both ends of this segment; the straight-line estimate encloses those rounds instead of exactly reproducing them.

For the holder cutout, offset the angled lines outward by **0.4 mm normal to each slope**. This adds `0.4 × sqrt(1 + 0.5²) = 0.447214 mm` to the half-width intercept. With the cutout's central floor at Z=2.5, the angled pocket runs from half-width **23.947214 mm** at that floor to half-width **28.9 mm** at Z≈**12.405573 mm**; above that, the sides are vertical. Keep the full 8.8 mm front/back opening through this simple profile. Device placement and the 25 mm outside body remain unchanged.

This is **mesh-derived simple geometry with an assumed clearance**, not a physical measurement or exact shell subtraction. Check the measured lower-band vertices and triangle/entry-plane intersections against the sloped profile and visualize a section; generic bounds alone cannot establish the angled fit. Fit-estimate parameters and residuals are recorded in `outputs/research/meshtracker-x1/angled-base-estimate.json`.

## Community search outcome

Bounded searches covered exact-name variants on Printables, MakerWorld, Thingiverse, Thangs, Cults and GitHub, plus manufacturer/community discussion leads. No exact-X1 reusable STEP/STL listing was verified there. This is not proof that none exists: indexing and access restrictions limit the search.

The useful positive is S6, a **physical holster product**, not a digital STL listing. Its embedded Baofeng and MOLLE display geometry was accessible as GLB/USDZ in the research pass. Those assets are holster meshes, not established device CAD, carry no verified reuse license, and are unnecessary now that S2 is available. A Reddit designer discussion and Etsy listing could not be verified through their blocked primary pages; their authorship/file/license claims are not adopted.

T1000-E holders are not X1-fit evidence. The official X1 shell STEP is preferable to scaling a different tracker model or measuring photographs.

## Modeling decision and remaining limits

Use **S2 official STEP** as the nominal geometric reference, retaining all relevant shell components in their original registration. This avoids manually reconstructing the full enclosure from calipers. A holder can be designed against its exact BREP rather than an 8 mm-thick guessed box.

- Treat approximately **9 mm** as the full-device CAD envelope; use the measured **8 mm lower band** only for the explicitly scoped 25 mm pocket above. Do not claim either value matches every shipping unit.
- Keep holder fit clearance, print compensation and retention geometry separate from nominal device geometry; the holder selects 0.4 mm per-side slot allowance, not a manufacturing tolerance.
- Confirm purchased-unit revision/applicability and perform a physical fit check before claiming snap-fit reliability. A small clearance coupon can test the interface without manually measuring every contour.
- Preserve USB-C plug access, button access, buzzer openings and insertion/removal space as holder-specific checks. The shell does not include a verified cable/plug envelope.
- Original shell CAD is not automatically a printable solid device dummy or a licensed redistributable design. A manufacturing clearance envelope is a later design operation, not something proven by import validity.

## Verification

Observed under **Python 3.14.7 / build123d 0.13.0** using `uv run python`:

1. Rendered the actual manufacturer product page in Chromium and extracted its **Shell 3D File** link; independently corroborated its presence in S3.
2. Downloaded S2 successfully and computed the checksum above.
3. Imported S2 with `build123d.import_step`: non-null, valid compound; **3 solids**, each valid. Recorded bounds and component volumes in `inspection.json`.
4. Exported a visualization STL and inspected its interactive Plotly preview in Chromium; observed the shell outline and circular button feature. The standard CPU PNG renderer timed out at 120 seconds and again at 180 seconds with a coarser STL; an interactive HTML visualization was used instead. The retained mesh has 52,815 triangles. Renderer investigation is tracked separately in [#13](https://github.com/ShakataGaNai/b123d/issues/13). This is not a physical fit, tolerance, wall-thickness or printability check.

Renderer follow-up ([#13](https://github.com/ShakataGaNai/b123d/issues/13)): profiling identified repeated whole-face-buffer hashing when the triangle loop accessed Trimesh's `face_normals` property. Reading normals once per view removed that overhead without changing the raster algorithm or mesh. The actual preview CLI completed this same **52,815-triangle shell in 3.80 seconds**, including imports, four-view PNG and offline HTML; the PNG was inspected. All four shell views matched the previous raster algorithm pixel-for-pixel on detached arrays, as did all four configured-color Wi-Fi plaque views. The **31-test suite passed**, including depth-occlusion and geometry-mutation checks. This runtime is an observation on the local environment, not a cross-machine guarantee.

The initial #12 source-research pass did not build a holder or measure a production specimen. The holder was subsequently built under #14 and corrected under #18 using the measured lower slopes above; physical fit remains untested.

## Change record

| Date | Change | Consuming models |
|---|---|---|
| 2026-10-01 | Found and imported official September 14 shell STEP; recorded nominal-versus-CAD thickness conflict and community holster reference. | None yet. |
| 2026-10-01 | Measured lower-body STL band and selected rounded 57 × 8 mm estimate for a 25 mm-tall rectangular pocket; no exact contour reconstruction. | `models/meshtracker_x1_multiboard_holder/` |
| 2026-10-01 | Measured the 5 mm run / 10 mm rise lower corner slopes and replaced the square-bottom pocket with an angled profile; peg uses the registered module and is bottom-aligned. | `models/meshtracker_x1_multiboard_holder/` |
| 2026-10-02 | Fixed the CPU preview bottleneck by reading face normals once per view; verified the unchanged reference mesh renders in 3.80 seconds. | Preview tool only; CAD and physical-fit status unchanged. |
