# API and construction semantics

**Scope:** checked build123d 0.13.0 API facts. Dimensions are millimeters in this repository; ordinary modeling angles are degrees. Mesh angular tolerance is a separate, radian-valued export setting.

## Choose one state model per construction block

**Algebra** stores explicit values: `a + b` fuses, `a - b` cuts, `a & b` intersects, and `Pos(...) * a` returns a placed shape. Use it when reusable components and explicit intermediate results help. Outside a builder, `mode=Mode.SUBTRACT` does not identify anything to cut; write the subtraction expression.

**Builder** accumulates state. `BuildLine` creates curves, `BuildSketch` creates planar faces, and `BuildPart` creates solids. Their completed results are `.line`, `.sketch`, and `.part`; the builder itself is not a shape. Inside a builder, constructors and operations update the active context automatically.

| Builder mode | Effect on the running result |
| --- | --- |
| `Mode.ADD` | Union/addition; separate solids can remain separate |
| `Mode.SUBTRACT` | Remove tool geometry |
| `Mode.INTERSECT` | Keep common geometry |
| `Mode.REPLACE` | Replace the running result |
| `Mode.PRIVATE` | Construct without contributing to the enclosing result |

Use isolated builder contexts for reusable components, then combine their completed shapes outside the contexts. To bring a prebuilt shape into a builder use `insert(shape, mode=...)`. `add()` is a deprecated spelling in 0.13.0. Keep algebra constructors outside live builders: an expression such as `Pos(...) * Box(...)` can register the original `Box` before placement and therefore does not express the intended builder operation.

### State traps

- `Cylinder(...).moved(...)` inside `BuildPart` moves the returned temporary, not the cylinder already added to the part. Use `with Locations(...): Cylinder(...)`.
- A nested `BuildSketch` publishes faces to its enclosing part when it exits; `extrude()` consumes pending faces. A second implicit `extrude()` has no faces unless more were supplied. Keep sketch/consume steps adjacent.
- `BuildLine` produces edges, not filled regions. In a sketch, call `make_face()` after closing a perimeter. An open wire cannot be extruded into a solid just because it renders as an outline.
- `Mode.PRIVATE` is appropriate for construction geometry, not for silently discarding required features. When using private nested builders, explicitly transfer the finished geometry when needed.
- `Select.LAST` and `Select.NEW` describe the latest operation, not named permanent features. Capture the intended selection immediately or reconstruct a geometric predicate later.
- Builder labels/settings that affect publication belong inside the context. After exit, change `builder.part.label`, not `builder.label`.
- `BuildPart` can contain several disjoint solids. Its class name does not establish connectivity.

## Common constructors: dimension meanings

Signatures below list the meaningful shape arguments, not every optional parameter. Use keyword arguments for optional dimensions, angles, alignment, and modes.

| Constructor | Meaning and common mistake |
| --- | --- |
| `Box(length, width, height)` | Local X, Y, Z dimensions; centered on all axes by default |
| `Cylinder(radius, height, arc_size=360)` | Radius, axial height, angular sector in degrees; not diameter |
| `Cone(bottom_radius, top_radius, height, arc_size=360)` | Radii at local bottom/top; top radius may be zero |
| `Sphere(radius)` | Radius; partial sphere angles have separate parameters |
| `Torus(major_radius, minor_radius)` | Major radius to tube centerline; minor radius is tube radius |
| `Rectangle(width, height)` | Local sketch X/Y dimensions; centered by default |
| `RectangleRounded(width, height, radius)` | Corner radius; both dimensions must be strictly greater than `2 * radius` |
| `Circle(radius, arc_size=360)` | Filled disk/sector, not a wire-only circle |
| `Ellipse(x_radius, y_radius)` | Semiaxes, not full width/height |
| `RegularPolygon(radius, side_count, major_radius=True)` | True: circumradius to vertices; False: apothem to sides |
| `Polygon(*points, align=(Align.NONE, Align.NONE))` | Coordinates retained by default; order determines algebra-mode face normal |
| `Hole(radius, depth=None)` | Subtractive by default; see version-specific depth warning below |
| `CounterBoreHole(radius, counter_bore_radius, counter_bore_depth, depth=None)` | All circular dimensions are radii; explicit bore depth is measured below the entry plane, independently of recess depth |
| `CounterSinkHole(radius, counter_sink_radius, depth=None, counter_sink_angle=82)` | Included cone angle; 82° is the API default, not the correct choice for every screw |

For a hexagonal nut pocket specified by across-flats dimension `af`, use `RegularPolygon(af / 2, 6, major_radius=False)`. Orient flats explicitly if a wall or tool-access requirement depends on them.

### Hole depth is not cylinder height

In the 0.13.0 `Hole` implementation, an explicit `depth=d` produces a `2*d` cylinder centered at the supplied origin. This cuts to depth `d` below an entry plane but also extends `d` above it, potentially cutting other material. `depth=None` uses the active part size and distance to the hole origin to construct a conservative through-cutter and requires a nonempty builder part. Counterbore and countersink implementations use downward bores and also extend their entry relief above the entry plane. Their recess/cone is not clipped to `depth`: a deeper recess or cone can cut beyond the straight bore. For a controlled blind cavity use a cylinder aligned `Align.MAX` in Z at the entry height, or a negative extrusion from a known entry sketch.

## Properties versus methods

| Property: no parentheses | Method: call it |
| --- | --- |
| `shape.is_valid`, `shape.is_null`, `shape.is_manifold` | `shape.solids()`, `shape.faces()`, `shape.edges()` |
| `shape.volume`, `shape.area`, `edge.length` | `shape.bounding_box()`, `shape.center()` |
| `shape.location`, `shape.global_location` | `shape.moved(location)`, `shape.located(location)` |
| `shape.geom_type`, `edge.radius` when circular | `face.normal_at()`, `face.outer_wire()`, `face.inner_wires()` |
| `bbox.min`, `bbox.max`, `bbox.size` | `shape.distance_to(other)` |

Check a geometry type before asking for type-specific measurements such as circular edge radius. Do not port historical snippets by blindly adding/removing parentheses everywhere.

## Sources

- [0.13.0 builder semantics and placement publication](../../../../vendor/build123d-0.13.0/docs/key_concepts_builder.rst)
- [0.13.0 algebra semantics](../../../../vendor/build123d-0.13.0/docs/key_concepts_algebra.rst)
- [Part object signatures and hole implementation](../../../../vendor/build123d-0.13.0/src/build123d/objects_part.py)
- [Sketch object signatures](../../../../vendor/build123d-0.13.0/src/build123d/objects_sketch.py)
- [Insert and generic operations](../../../../vendor/build123d-0.13.0/src/build123d/operations_generic.py)
- [Shape properties](../../../../vendor/build123d-0.13.0/src/build123d/topology/shape_core.py)
