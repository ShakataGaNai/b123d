# Coordinate frames and placements

**Checked facts:** build123d 0.13.0. Use explicit datums for mating geometry; inferred face frames are convenient but can change when topology changes.

## Local axes are the operation's axes

A `Plane` is an origin plus a right-handed basis. `x_dir` establishes local X; `z_dir` is the normal; local Y follows from the basis. A sketch's `(x, y)` coordinates are local, not necessarily global X/Y.

| Plane | Local X in world | Local Y in world | Normal / local Z |
| --- | --- | --- | --- |
| `Plane.XY` | +X | +Y | +Z |
| `Plane.XZ` | +X | +Z | **−Y** |
| `Plane.YZ` | +Y | +Z | +X |

`Plane.XZ` is a frequent sign trap: positive extrusion goes toward world −Y. `Plane.XY.offset(h)` moves the plane by `h` along its normal. Offsetting XZ moves along −Y, not +Z.

Define an angled datum with `Plane(origin=(...), x_dir=(...), z_dir=(...))`. Choose nonparallel direction vectors. When clocking matters, specify `x_dir`; knowing only the surface normal leaves a rotational degree of freedom.

`Plane(face)` establishes a plane from a planar face. Inspect `face.normal_at()` and the resulting plane axes before placing a directional feature. The inferred origin and X direction are not a promise to preserve your design datum after revisions. For a plate top whose height is a known parameter, `Plane.XY.offset(thickness)` is usually more stable than selecting a face by list index.

## Alignment is local and precedes placement

- `Align.MIN`: local lower bound sits at zero.
- `Align.CENTER`: local extent is centered on zero.
- `Align.MAX`: local upper bound sits at zero.
- `Align.NONE`: preserve the primitive's native coordinates.

Use `align=(Align.CENTER, Align.CENTER, Align.MIN)` for a centered XY part resting at Z=0. A cylinder with `Align.MAX` in Z extends downward from its origin. These alignments apply in the primitive's construction frame before rotation/placement; they do not align the final rotated shape to world axes.

Most boxes/cylinders are centered by default, so `Box(20, 10, 4)` spans Z=−2…+2. Extruding a positive-normal XY sketch with `amount=4` instead spans Z=0…4. Account for this difference when mixing feature types.

## Composition order

Read `Pos(10, 0, 0) * Rot(Z=90) * shape` right to left: rotate the shape around the origin, then translate it along world X. Swap `Pos` and `Rot` and the translation direction rotates too. Transform multiplication is not commutative.

`plane * Pos(x, y, z) * shape` interprets the translation in the plane's local frame. `Pos(...) * plane * shape` translates the already oriented result in the outer/world frame. The same distinction matters in nested assembly placements.

`Location((x, y, z), (rx, ry, rz))` combines translation and Euler rotation; angles are degrees. Avoid accumulating rotations by adding Euler tuples: composition is a transform operation, not componentwise angle arithmetic. Use explicit `Rot` factors or `shape.rotate(Axis(origin, direction), angle)` when a pivot axis is the design intent.

| Operation | Changes original? | Interpretation |
| --- | --- | --- |
| `shape.move(location)` | Yes | Relative transform |
| `shape.moved(location)` | No | Relative transform on a copy |
| `shape.locate(location)` | Yes | Replace location |
| `shape.located(location)` | No | Replace location on a copy |

Absolute placement can erase an earlier transform. Use separate prototype and placed-instance variables when reusing a component.

## Builder placement in 0.13.0

All builders construct in local XY coordinates. `BuildSketch(Plane.XZ)` builds `sketch_local` on XY, then publishes `.sketch` on XZ. Similarly, `BuildPart(placement)` publishes `.part` after transforming `.part_local`. Selectors inside the builder refer to the local construction result. This distinction is particularly important when code compares coordinates or uses `Axis.Z` inside a rotated builder.

`Locations` inside a builder positions objects before they register. Nested locations compose relative to each other. A location around an entire builder applies to its completed output. Multiple placements replicate that output: do not manually reapply the same transform to `.part` or `.sketch`.

## Normals and direction checks

- A positive extrusion follows a profile's normal unless `dir=(...)` overrides it; a negative amount reverses direction.
- Algebra `Polygon` uses winding: counterclockwise in XY yields +Z, clockwise −Z. Builder sketches normalize their local face orientation upward.
- On a planar face, `normal_at()` is constant. On a curved face, a single sampled normal is not a global face direction.
- Axis filters generally accept parallel and antiparallel directions. To require upward orientation, also check `face.normal_at().Z > 0` on a planar face.
- After placing a part on the print bed, check the actual `bounding_box().min.Z`, not merely the object's location: a shape can have a zero location while geometry lies below zero.

## Sources

- [Tagged builder local construction/output placement rules](../../../../vendor/build123d-0.13.0/docs/key_concepts_builder.rst)
- [Tagged algebra placement arithmetic](../../../../vendor/build123d-0.13.0/docs/key_concepts_algebra.rst)
- [Moving objects](../../../../vendor/build123d-0.13.0/docs/moving_objects.rst)
- [Plane, Location, and rotation implementation](../../../../vendor/build123d-0.13.0/src/build123d/geometry.py)
- [Polygon orientation and primitive alignment](../../../../vendor/build123d-0.13.0/src/build123d/objects_sketch.py)
