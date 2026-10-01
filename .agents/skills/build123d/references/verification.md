# CAD verification and troubleshooting

## Three independent proofs

1. **Kernel correctness:** the result is non-null, valid, and contains the expected solids.
2. **Design correctness:** critical dimensions, locations, connectivity, wall thickness, and mating behavior match the requirements.
3. **Delivery correctness:** exports exist, can be inspected, carry the intended scale, and are suitable for the next manufacturing/tooling step.

None implies the other two. A valid wrong-sized box is wrong. A convincing preview can hide an open shell or internal disconnected island. A valid STEP does not establish that an STL was tessellated finely enough.

## Validation order

### Before construction

Validate parameter relationships: positive thicknesses/radii, cavity smaller than outer body, corner radii fitting their rectangles, enough edge distance around holes, and meaningful engagement depth. Report impossible input combinations rather than allowing the CAD kernel to fail much later.

For real objects, record dimensions with their source, revision, and confidence in the reusable research folder linked by model metadata. Distinguish a measured value from a drawing dimension, a visual estimate, and an engineering allowance. Missing mounting dimensions should not become silently invented exact values.

### After primary features

Use 0.13.0 property syntax:

```python
# Fragment: shape is a completed Solid/Part/Compound.
assert not shape.is_null
assert shape.is_valid
solids = shape.solids()
assert len(solids) == 1
assert all(solid.volume > 0 for solid in solids)
box = shape.bounding_box()
```

`is_valid` returns true for a null underlying shape in this release, so the first check matters. `is_manifold` is an additional edge/face incidence diagnostic, not a universal replacement for the kernel validity check. Periodic/seam geometry can complicate incidence interpretation; investigate disagreements rather than relabeling a clearly valid solid from one boolean alone.

Check `box.min`, `box.max`, and `box.size` with tolerances, not exact floating equality. Verify expected origin/datum as well as size: a correctly sized part shifted below the bed is still misplaced.

Use analytical volume for simple shapes; include all intended holes/cavities. For more complex geometry, compare material removed/added to a justified range and assert critical measurements directly. Total volume is insensitive to translations and can match even if a hole is in the wrong place, so it complements rather than replaces position checks.

Check dimensions that matter to the consumer:

- Hole center coordinates, diameter, axis direction, and through/blind extent.
- Floor thickness from known cavity datum, and minimum walls near recesses/corners.
- Boss-to-wall connectivity and remaining material below counterbores.
- Mating gaps, insertion depth, and independent-part interference.
- Expected number of solids after cuts that might split the body.

### Give tolerances units and a purpose

Keep four quantities separate: a design allowance changes nominal geometry; a numerical acceptance tolerance permits measurement/round-trip error; a mesh deflection controls tessellation; a manufacturing tolerance describes acceptable variation in the made part. Kernel tolerances are internal geometric precision, not a calibration of any of these.

- Position/radius checks use **mm**, area checks **mm²**, and overlap/volume checks **mm³**. Choose each threshold for the feature scale; a length tolerance reused as a volume threshold has no dimensional justification.
- `math.isclose`'s `abs_tol` has the units of the compared values; `rel_tol` is dimensionless. Set `rel_tol=0` when only an absolute limit is intended, especially at large coordinates.
- A unit-normal test such as `normal.Z > 0.999` is dimensionless. Axis-direction filtering with `filter_by(Axis.Z, tolerance=...)` uses **degrees** in 0.13.0 (`Axis.is_parallel` converts to OCCT radians); it is not a positional mm tolerance.
- The CLI's linear mesh deflection is a requested **mm** meshing parameter, not a measured maximum mesh error. Its angular deflection is **radians**, unlike ordinary construction angles.

### After edge treatments

Recheck validity, solid count, critical envelope, and local material. Fillets can consume thin sections; chamfers can reduce seating area or shorten engagement. Topology counts may legitimately change, so assert semantic requirements rather than a global magic face count.

### At export

Run the repository CLI on the model directory. Its default is one solid; intentional assemblies need `--expected-solids N`. Inspect `report.json`, STEP, STL, PNG, and offline HTML in `outputs/<relative model path>/`. Open the HTML or image rather than assuming the renderer's success means the model looks right.

The repository uses an **absolute** linear mesh deflection of 0.05 mm and angular deflection of 0.1 rad by default, configurable through `--linear-deflection` and `--angular-deflection`. Upstream 0.13.0 `export_stl` and `Shape.mesh` pass OCCT's relative-deflection flag; their numeric tolerance should not be described as a guaranteed absolute millimeter error. The repository exporter instead cleans cached triangulation and calls the OCCT mesher with relative deflection disabled before binary STL writing.

Mesh deflection is not a fit allowance, wall thickness, or manufacturing accuracy. Tighten mesh settings where a small feature or roundness requirement needs them, while retaining the STEP BREP as the exact CAD exchange deliverable. STL carries no unit declaration: explicitly import it as millimeters in the slicer and confirm overall dimensions.

The generated preview views are **iso/top/bottom/front**, all orthographic. Use top/bottom/front for alignment and iso for feature recognition; create sections or additional interior views separately for hidden geometry. Preview tessellation and transparency can create artifacts; when a seam looks suspicious, inspect the actual topology and exported mesh rather than inferring failure from shading alone.

## Failure localization

Find the first operation where a known-good intermediate becomes wrong. Inspect its input shapes, coordinate frames, selected topology, and output. Reduce only the diagnostic reproduction; preserve the requested design in the final result.

| Symptom | Likely causes to inspect | Focused next action |
| --- | --- | --- |
| Feature appears at origin instead of translated position | Constructor registered before `.moved()`; mixed algebra inside builder | Replace with placement context before construction or isolate algebra outside builder |
| Extrusion goes the wrong way | Plane normal, winding, XZ normal −Y, or negative amount | Print/check the profile normal and input plane basis |
| Empty pending-face error | Previous operation consumed faces; sketch not published; private builder | Keep sketch/consume pair adjacent or supply explicit face/sketch |
| `bool` object not callable | Property used as old method syntax | Use `shape.is_valid`, `is_null`, or `is_manifold` without parentheses |
| Wire renders but face fails | Open endpoints, nonplanarity, self-crossing, duplicate spans | Inspect wire count, closure, endpoints, and plane before making a face |
| Boolean leaves shape unchanged | Tool misses target; wrong datum/sign; incorrect `mode` | Inspect cutter separately, compare bounding boxes and before/after volume |
| Union produces multiple solids | Separated volumes, tangent-only contact, intended overlap absent | Check spatial relation and design a real material connection |
| Fillet/chamfer fails | Stale selection, too-large radius, sliver edge, conflicting blends | Re-select on current shape; isolate edge groups and nearby geometry |
| Offset fails or erases holes | Thickness exceeds local radius/gap; inner loops collapse | Inspect local sections and compare explicit cavity construction |
| Loft twists or bulges | Section/seam order mismatch, abrupt changes, smooth interpolation | Use aligned sections; compare ruled result and add justified stations |
| Sweep self-intersects | Wrong start plane, small bend radius, path self-proximity | Check initial tangent, section extent, and bend/section ratio |
| Export is tiny/huge in slicer | STL imported in wrong units, inch/mm conversion applied twice | Compare known envelope and set mm import explicitly |
| Valid BREP but open/nonmanifold STL | Corner-only contacts, a highly perforated planar face, or tessellation defects | Inspect exported edge incidence and coordinates; correct real material connectivity or preserve useful face partitions, then re-export and check the mesh |
| Wrong interior but convincing preview | Occlusion or unexamined section | Inspect cavity sections, floor datum, and actual cut volume |

## Repair is not design correction

`clean()` unifies/removes redundant topology; it does not fill an intended gap or correct a misplaced hole. `fix()` invokes kernel repair and may alter representation; inspect the result and revalidate dimensions. Neither should hide the first failing operation. Avoid broad exception handling that exports an earlier incomplete shape when the requested final feature fails.

The [Wi-Fi QR sample](../../../../models/wifi_qr/README.md) is a tested local example of why this distinction matters: corner-only raised-module contacts produced four-facet mesh edges, and a large perforated base face produced open triangles. Small explicit run separations plus coplanar row partitions preserved one solid and passed the saved-STL regression. Those are model-specific topology decisions, not permission to suppress watertightness checks or blindly skip cleanup everywhere.

A robust completion report states which commands and outputs were actually inspected, key resulting dimensions/solid count, and any remaining manufacturing uncertainty. Keep guesses marked as assumptions rather than calling a model “print-ready” solely because export succeeded.

## Sources

- [Shape validity, nullness, manifold diagnostic, and bounding boxes](../../../../vendor/build123d-0.13.0/src/build123d/topology/shape_core.py)
- [Export implementation and relative mesh flag](../../../../vendor/build123d-0.13.0/src/build123d/exporters3d.py)
- [Builder semantics](../../../../vendor/build123d-0.13.0/docs/key_concepts_builder.rst)
- [Part operations](../../../../vendor/build123d-0.13.0/src/build123d/operations_part.py)
- [Generic edge and offset operations](../../../../vendor/build123d-0.13.0/src/build123d/operations_generic.py)
- [Axis angular tolerance conversion](../../../../vendor/build123d-0.13.0/src/build123d/geometry.py)
