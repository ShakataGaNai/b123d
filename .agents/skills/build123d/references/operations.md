# Feature operations

**API facts:** build123d 0.13.0. **Design guidance:** choose feature order, radii, and tolerances to preserve the specified geometry; there is no universally successful kernel tolerance or fillet ratio.

## Boolean construction

Algebra `+`, `-`, and `&` mean union, difference, and intersection. Builder modes express the same operations against the current result. A union of separated volumes remains multipart; tangency at one point or one edge does not create a useful connected mechanical joint.

For an intended through-cut, make the cutter extend beyond both surfaces by a small named modeling margin. This avoids a cutter accidentally ending short because of a datum or rounding error. A modeling margin is not a manufacturing clearance: keep separate parameters. Exactly shared planar faces can fuse successfully; positive overlap is useful when implementing an intended joined feature, but must not silently alter functional dimensions.

After a significant boolean, check non-nullness, validity, solid count, and volume direction. A subtraction should remove a predictable amount; unchanged volume suggests a missed target or a wrong frame. A lost solid may mean a cutter was oversized. Keep tool geometry available as a separately named value when diagnosis would otherwise require reconstructing it.

## Extrude: prismatic geometry

Core signature:

`extrude(to_extrude=None, amount=None, dir=None, until=None, target=None, both=False, taper=0, clean=True, mode=Mode.ADD)`

- Explicit input is a face/sketch; implicit input consumes the builder's pending faces.
- Positive/negative amount follows/opposes the profile normal unless `dir` overrides it.
- `both=True` repeats the full amount each side: `amount=5` means total thickness 10.
- `taper` is an angle in degrees. Acute details and inner loops can make drafted extrusions fail or change wall thickness.
- `until=Until.NEXT` or `Until.LAST` provides geometric termination. Supply an explicit `target` in algebra mode; builder mode can use the current part. Use this only when target topology has a clear intended next/last boundary.
- A filled face creates a solid; a mere edge is not an equivalent solid profile.

For a cut from the top of an XY-based plate, sketch at `Plane.XY.offset(thickness)` and use a negative amount. For repeated through-holes, one sketch containing all disks followed by one subtractive extrusion is easy to reason about.

## Revolve: turned parts

`revolve(profiles=None, axis=Axis.Z, revolution_arc=360, clean=True, mode=Mode.ADD)`

Create the material cross-section in a plane containing the axis. For world-Z rotation use `Plane.XZ`; sketch X is radius and sketch Y is world Z. Keep an annular profile wholly on the positive-radius side. A profile straddling the axis can sweep overlapping material and fail or produce unintended results. An edge on the axis is valid for many fully solid profiles, but a zero-thickness tip or a point-only connection needs scrutiny.

Use a single stepped polygon for a bushing or turned collar instead of a stack of nearly coincident cylinders. An internal bore is represented by the profile's inner radial boundary. The [turned-bushing recipe](recipes.md#turned-bushing-revolve) shows this arrangement.

## Loft: changing cross-sections

`loft(sections=None, ruled=False, clean=True, mode=Mode.ADD)`

Give sections in progression order. They need not be equally spaced. `ruled=True` uses ruled transitions between sections; the default makes a smooth transition, which can bulge between constrained sections. Check the resulting envelope, not only the input profiles.

For predictable behavior:

1. Use parallel planes initially and keep profile winding consistent.
2. Keep corresponding corners/seams aligned; rotated seams can twist a loft.
3. Avoid abrupt area changes over tiny distances.
4. Check each section is a valid face before lofting.
5. Use a vertex only at the first/last section, not in the middle.

In 0.13.0, loft faces may contain inner wires, but each section must have the same number of holes. The implementation matches holes geometrically by centers. Closely spaced, crossing, or heavily displaced hole trajectories can be paired incorrectly. For critical internal channels, construct outer and inner lofts separately and subtract, then inspect sections and minimum wall thickness. Neither strategy guarantees constant normal wall thickness.

## Sweep: following a path

`sweep(sections=None, path=None, multisection=False, is_frenet=False, transition=Transition.TRANSFORMED, normal=None, binormal=None, clean=True, mode=Mode.ADD)`

Put the section at the start of the path and normal to its initial tangent. A robust algebra pattern is `Plane(origin=path @ 0, z_dir=path % 0) * Circle(radius)`; `@` samples position and `%` samples tangent with normalized parameter 0…1. Specify an X direction too for noncircular profiles whose clocking matters.

- A filled section swept along a connected path produces a solid. Sweeping edges instead produces surfaces.
- `is_frenet` changes section-frame behavior along a curved path; it is not a universal fix for twisting. Curvature changes and inflection points need inspection.
- `normal` and `binormal` constrain frame behavior. Choose the constraint that matches the design rather than stacking flags until the operation succeeds.
- `transition` governs corners (`TRANSFORMED`, `ROUND`, `RIGHT`). A sharp path corner can create overlaps; fillet the path or use an explicit elbow profile when bend geometry matters.
- The section must fit within bend radii and avoid colliding with other path spans. A self-intersecting sweep can be invalid even when path and section are individually valid.
- `multisection=True` changes section shape along one path. Prefer an ordinary loft when a path constraint is not needed.

## Fillet and chamfer

`fillet(objects, radius)` takes 3D edges or 2D vertices. `chamfer(objects, length, length2=None, angle=None, reference=None)` supports symmetric and asymmetric chamfers. For asymmetric chamfers, establish which adjacent face/edge receives the first distance with `reference`; a changed orientation can otherwise reverse the intended treatment.

Select from the current shape, assert cardinality, then apply. In algebra mode assign the return value. In a builder the operation modifies the running result. Adjacent thin walls and small edges bound feasible radii; kernel failure is not proof that the entire part is malformed.

Recommended order is a design decision, not a hard law:

- Establish primary volumes, major openings, and functional reference surfaces.
- Apply structural radii early enough that dependent features intentionally reference the rounded body.
- Apply small cosmetic fillets/chamfers late, when they cannot destabilize earlier selectors.

When a fillet fails, isolate the selected edge set and try one intentional subset at a time to identify the conflict. Inspect nearby sliver edges and competing blends. Do not silently omit the requested fillet or repeatedly shrink its radius without reporting the design change.

## Offset and shelling

`offset(objects=None, amount=0, openings=None, kind=Kind.ARC, side=Side.BOTH, closed=True, min_edge_length=None, mode=Mode.REPLACE)`

The input dimension determines the result: offset curves, expand/contract faces, or offset solids. Positive amount is outward, negative inward. `openings` identifies solid faces to remove while creating a shell, e.g. the top of a container. The builder default is **REPLACE**, unlike most additive feature operations.

For an open box, select the current top face and use `offset(amount=-wall, openings=top)` to preserve the outside envelope with an inward wall. Offset can fail around narrow gaps or radii smaller than the requested thickness. It can also eliminate small holes: always recheck topology and minimum sections afterward. `min_edge_length` removes degenerate offset edges; it is not permission to erase specified small features.

For a simple rectangular enclosure, subtracting a controlled inner box from an outer box often expresses wall and floor dimensions more directly than shelling. Use offset when maintaining a normal thickness on a more complex exterior is the actual intent.

## Sources

- [Extrude, revolve, and loft tagged implementations](../../../../vendor/build123d-0.13.0/src/build123d/operations_part.py)
- [Boolean-supporting insert, fillet, chamfer, offset, and sweep APIs](../../../../vendor/build123d-0.13.0/src/build123d/operations_generic.py)
- [Direct topology operations and validation](../../../../vendor/build123d-0.13.0/src/build123d/topology/shape_core.py)
- [Edge/Wire parameter sampling](../../../../vendor/build123d-0.13.0/src/build123d/topology/one_d.py)
