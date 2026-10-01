# Recovering features from sections

## Planes, layers and envelopes

Start with native XYZ bounds and orthographic views. Bounds identify extremes, not continuous surfaces: a local connector projection can define minimum Y even though most of the floor ends several units inward. Inspect the actual planar footprint and cross-sections before placing a wall on an AABB edge.

Choose sections **inside** material intervals, away from coplanar faces and triangle vertices. For a Z-oriented plate, use XY sections below its floor, inside the floor, just above it, inside bosses, and above the bosses. Repeat in XZ/YZ for recess bottoms, steps and connector access. Use several nearby offsets around a suspected transition; report the bracketed height interval, not a falsely exact boundary from one slice. For an exact plane height, corroborate with aligned mesh-face coordinates/normals or analytic CAD. A no-intersection result is evidence at that plane only.

```sh
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/station-g3-reference/SG3-04-Backplate.stl --axis z --offset 0.5
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/station-g3-reference/SG3-04-Backplate.stl --axis z --offset 1.5
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/station-g3-reference/SG3-04-Backplate.stl --axis y --offset -29.5
```

Track features by coordinates, dimensions and overlap, not contour index: topology/order can change between slices. Multiple contours may be disconnected solids, voids, lettering or nested bosses. Cross-sections on open/non-manifold meshes may be incomplete or branched; an individual closed loop does not make the whole mesh a valid solid. Section tolerances can join nearby endpoints; corroborate fragile results rather than treating closure as exact topology.

## Circle candidates, holes and bosses

The helper reads `section.entities` vertex indices, avoiding `section.discrete` and polygon routines that may require absent optional dependencies. It centers/scales coordinates before fitting, then refines a circle geometrically using uniform perimeter samples. It retains all contour segments; no robust-statistics outlier trimming is allowed to conceal a notch. Whole-segment maximum radial residual guards against fitting the four corners of a rectangle perfectly. Full angular coverage/winding guards against treating partial arcs as circles. Ill-conditioned fits yield reasons instead of giant radii or NaNs.

- **Spans** are coordinate-wise max minus min; two equal spans do not establish a circle. A fitted **diameter** is twice the inferred radius; center coordinates are not edge offsets.
- Mesh polygons and triangulation-created points lie on chords. Their fitted circle can be slightly smaller than the generating CAD circle. Retain residuals/facet uncertainty; do not round the fitted diameter into an asserted nominal thread size.
- An accepted circular outer contour can be a post/boss. A nested inner contour may be a bore, but establish material/void with adjacent sections, side views and solid context before naming it.
- Prove a **through-hole** across the relevant material thickness, including both ends. A closed circular loop above a floor can be a blind recess. Bracket its bottom and check a perpendicular section before choosing cutter depth.
- Repeated radii at different heights can identify a cylindrical bore; changing radii can indicate draft or a countersink. A stepped radius can indicate a counterbore. Neither establishes thread specification.
- Clearance envelope, fastener nominal size, measured opening and desired print fit are separate quantities. Record radial versus diametral allowances explicitly.

## Registering parts and mapping features

Declare a right-handed source frame and view direction before renaming axes. Keep measurement coordinates in that frame; document an explicit mapping `p_model = scale * R @ p_source + translation`. Record scale units, rotation matrix/order, translation units, datum and whether a reflection was necessary. Rigid assembly placement is not equivalent to independently centering each file.

Use at least three well-spaced, non-collinear corresponding features to constrain planar registration and check residuals on remaining features. Symmetric patterns can leave ambiguous rotations/reflections; use an asymmetric feature or documented orientation. Coplanar hole centers alone cannot determine an assembled Z offset: use mating planes, stops or known stack heights. Do not infer a shared origin from equal overall dimensions. Report unmatched features instead of optimizing a misleading registration against unrelated geometry.

The [Station G3 record](../../../../research/objects/bq-voyage-station-g3/README.md) is a worked evidence source, not universal dimensions. Its reference shell and backplate share a seven-opening XY pattern with shell Y = backplate Y + 1.3. A functional Z relation must be established separately from corresponding planes/features; XY agreement by itself does not prove it. Case openings still do not become manufacturer PCB holes through registration.

Assign ports using manufacturer drawings, revision-specific photographs, labels and assembly orientation. Photographs can establish identity and ordering without supplying metric coordinates; perspective, lens distortion and unknown depth defeat casual pixel scaling. Confirm plug insertion/removal, cable bends and tool access separately from the opening's perimeter.

## Uncertainty and provenance

Use the existing research record for source citations, license/attribution, hashes, transformations and dimension evidence classes. Mesh-derived dimensions are **derived**, not physical caliper measurements. An original-download hash identifies bytes, not truth, license permission or hardware revision. Prefer applicable analytic STEP/drawings when available; retain conflicting evidence instead of averaging it silently.

Record bounds on uncertainty from faceting, source rounding, section-plane placement, registration residual, unsupported scale assumptions and actual specimen measurements. Keep those separate from process compensation and intentional clearance. A low fit residual establishes agreement with the polygon, not original CAD accuracy or manufactured fit. If remaining uncertainty can change the required function, mark that interface blocked or explicitly approximate rather than presenting an exact reconstruction.
