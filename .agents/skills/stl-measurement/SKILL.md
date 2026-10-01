---
name: stl-measurement
description: Recover dimensions, datums, mounting patterns and feature depths from existing STL meshes; register separately exported parts and hand off evidence to parametric CAD reconstruction.
---

# STL measurement and reconstruction

Use for mesh-derived object measurements, including enclosure references that only indirectly constrain the enclosed hardware. Source CAD need not be absent: look for revision-matched drawings, native CAD or analytic STEP first and use mesh sections for comparison where useful.

## Workflow

1. **Identify the evidence.** Read the repository [research contract](../../../research/README.md) and reuse its [object template](../../../research/templates/object.md), not a second measurement schema. Record exact object/revision, original listing and download URLs, publisher, file identity, license and attribution. Preserve original bytes; inspect downloaded data without executing supplied code. A community case is evidence about that case, not an authoritative PCB model.
2. **Inspect the file.** Run the helper below. Record its SHA-256, native bounds, validity warnings and tool versions. Resolve units from independent evidence; STL has no unit declaration. A named 1 mm spacer matching one coordinate unit supports scale but is not physical calibration. Stop on empty/non-finite input; keep open-mesh limitations visible rather than repairing them silently.
3. **Recover functional features.** Read [section analysis](references/analysis.md) before inferring holes, bosses, depths, continuous walls or registration. Section each relevant axis at multiple interior offsets; preserve native coordinates. Record circle residuals and distinguish axis spans from fitted diameters. Match candidate features to drawings/photos and assembly context before assigning their function. Completion means every required interface has evidence or an explicit unresolved blocker, not merely a matching bounding box.
4. **Register and record.** Write source-to-object and object-to-model transforms, units, feature tables, uncertainty and through/blind evidence into the object research record. Separately exported parts can have different origins. Separate derived mesh geometry, physical measurements, assumptions and chosen fit allowances.
5. **Reconstruct and check.** Follow the [parametric handoff](references/handoff.md), then the [build123d skill](../build123d/SKILL.md). Build meaningful sketches/solids/cuts rather than one BREP face per triangle. Preserve functional interfaces before simplifying cosmetics. Link research in metadata and verify feature-specific geometry on native and STEP-round-trip solids; visual and physical-fit evidence remain separate.

## Runnable helper

Run from the repository root using the existing locked NumPy/trimesh environment; no additional packages:

```sh
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py inspect tmp/station-g3-reference/SG3-04-Backplate.stl
uv run --locked python .agents/skills/stl-measurement/scripts/measure.py section tmp/station-g3-reference/SG3-04-Backplate.stl --axis z --offset 1.5
```

These example inputs are ignored local downloads, not bundled assets. Substitute a permitted STL path on another checkout. `--axis x|y|z` names the plane normal; `--offset` is its coordinate in unchanged native units. The remaining axes are `plane_axes_uv` (`yz`, `xz`, `xy`). A negative offset is valid. Consult `--help` for pagination (`--start`, `--max-loops`); results default to at most 40 contours, with total and omitted counts.

Output is readable JSON, never a mesh dump. Inspection reports exact-coordinate vertex indexing without tolerance welding, repair, scale changes or reorientation. It checks finite coordinates, zero-area triangles, watertightness and winding; it does not establish absence of self-intersections or physical validity. Open meshes remain measurable with warnings. Section contour assembly uses trimesh's intersection/path tolerances; near-coplanar, tiny or nearly touching features require independent inspection.

Circle acceptance is deliberately conservative: full closed perimeter, well-conditioned fit, one monotonic winding, vertex angular gaps at most 45°, and maximum radial deviation at most 0.5% of fitted radius. Fitting uses uniformly spaced perimeter samples, with residual maxima checked on every segment and vertex. Coarse polygons can be rejected despite originating from circles. Accepted entries are **near-circular contours**, not identified holes; rejected entries omit center and diameter. Reported fit precision is not manufacturing tolerance. No outlier removal disguises flats or notches.

Invalid/empty/non-finite input exits 2 with an error; a valid plane missing the mesh succeeds with `no intersection`. Non-watertightness is not a parse error. For runnable synthetic examples, stock-backplate expectations and error cases, see [CLI smoke scenarios](references/cli-smoke.md).
