# Topology, selection, and sketch validity

## What each level guarantees

`Vertex → Edge → Wire → Face → Shell → Solid` describes increasing dimensional structure, not automatic validity. A wire may be open. A shell is a connected set of faces and may be open; it is not necessarily a watertight volume. A `Compound` groups shapes and does not fuse them. A `Part` can contain several solids.

`shape.edges()`, `.faces()`, `.solids()`, and related selectors return `ShapeList` collections. Extracted topology has parent context used by operations such as `fillet`. Select from the current shape that will be modified rather than constructing a geometrically similar but unrelated edge.

## Select by design intent

Prefer this hierarchy:

1. A semantic datum and geometric predicate: top planar face at a known Z, bore wall of a known radius, vertical edges outside a mounting region.
2. Direction/type filters, followed by position, length/radius, or area refinement.
3. Immediate operation history (`Select.LAST` / `Select.NEW`) when that feature is exactly what the previous operation created.
4. A numeric list index only after proving the selection has a meaningful ordering and expected size.

Useful operations:

| Expression | Interpretation |
| --- | --- |
| `part.edges().filter_by(Axis.Z)` | Linear edges parallel to Z, not edges lying in XY |
| `part.faces().filter_by(Axis.Z)` | Planar faces whose normals are parallel to Z; both orientations |
| `part.edges().filter_by(GeomType.CIRCLE)` | Circular edges, not every curved edge |
| `part.faces().filter_by(GeomType.CYLINDER)` | Cylindrical faces |
| `part.faces().sort_by(Axis.Z)` | Sort by geometric center projected along Z |
| `part.faces().group_by(Axis.Z)[-1]` | Highest center-position group; potentially several faces |
| `part.edges().filter_by_position(Axis.Z, z0, z1)` | Filter using center position along the axis |
| `part.faces().filter_by(lambda f: ...)` | Custom predicate using known type/measurements |

A face with the highest center is not automatically an entire top surface. Steps, chamfers, pockets, and rounded faces can change that result. Filter planar faces first and compare their normal and position with a tolerance. `filter_by_position` does not mean every point of an object lies in the interval; use its bounding box when containment is required.

For example, a **fragment** inside a model with known `part`, `height`, and `tol`:

```python
# Fragment: part is the current solid/part; height and tol are model values.
from build123d import GeomType

candidates = [
    face for face in part.faces().filter_by(GeomType.PLANE)
    if face.normal_at().Z > 0.999
    and abs(face.center().Z - height) < tol
]
assert len(candidates) == 1, "Expected one planar top face"
top = candidates[0]
```

### Preserve meaning, not old edge objects

Booleans, cleanup, fillets, and offsets can split, merge, or replace faces and edges. A saved edge can become stale after modifying its parent. Re-select after each topology-changing operation. A parameter edit changing a selector's cardinality should produce a useful assertion instead of silently rounding a different edge.

`Select.LAST` includes features brought in or produced by the last operation. `Select.NEW` is narrower: topology that was in neither input. Neither is a durable feature-name mechanism. Cleaning same-domain faces can also affect history and counts.

For circular holes, filter circular edge geometry before reading `edge.radius`; use `edge.arc_center` for the circle center rather than assuming the generic edge center has the same meaning for arcs. A through-hole often contributes two rim edges but one cylindrical face. Counting every circular edge as one hole doubles the apparent hole count.

## Building valid sketch faces

A solid-producing extrusion starts with planar filled faces. `BuildLine` supplies perimeter edges; `make_face()` turns a single closed perimeter into a face in `BuildSketch`.

- Use coincident endpoints generated from shared parameter expressions, not separately rounded coordinates.
- Close the last segment to the first. A visual gap smaller than the viewport pixel size is still a geometric gap.
- All points of a planar face must lie in one plane. A 3D path belongs in a sweep, not a planar face constructor.
- Avoid duplicate edges, backtracking segments, self-crossing loops, and zero-length spans.
- Use a single perimeter per `make_face()` call. Its contract is one closed wire; it is not an arbitrary-loop classifier.
- For holes, use sketch subtraction (`Circle(..., mode=Mode.SUBTRACT)`) or the direct `Face(outer_wire, inner_wires)` constructor with valid nonintersecting inner loops. Disjoint outer loops should become separate faces, not be passed as one perimeter.
- Prefer `RectangleRounded` or 2D vertex fillets for a profile that will be uniformly extruded; this expresses a plan-view corner radius without a fragile 3D edge selection.

For direct wire construction, examine `Wire.combine(edges)`: confirm it yields exactly the intended number of connected wires. Check `wire.is_closed` and face validity before extrusion. A closed wire can still self-intersect, so closure alone is insufficient.

## Distinguish topology and manufacturing requirements

A valid solid with a 0.01 mm wall can be unsuitable for printing. Two valid solids may collide. A compound of valid solids may have an unintended disconnected island. Validate connectivity, wall dimensions, and mating behavior separately; see [verification](verification.md).

## Sources

- [Tagged topology selection guide](../../../../vendor/build123d-0.13.0/docs/topology_selection.rst)
- [ShapeList filter and sort implementation](../../../../vendor/build123d-0.13.0/src/build123d/topology/shape_core.py)
- [Wire and edge APIs](../../../../vendor/build123d-0.13.0/src/build123d/topology/one_d.py)
- [Face construction](../../../../vendor/build123d-0.13.0/src/build123d/topology/two_d.py)
- [make_face contract and implementation](../../../../vendor/build123d-0.13.0/src/build123d/operations_sketch.py)
