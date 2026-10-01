# Runnable reference recipes

Each Python block in this file is a complete independent program with explicit imports, `build()`, `check(shape)`, and a command-line smoke entrypoint. Copy **one** block into a model folder's `model.py`; add the metadata sidecar using the repository convention. Run through `uv run python scripts/build.py models/<name>` for exports and previews. The final recipe intentionally needs `--expected-solids 2`.

These are geometric examples, not load-rated designs or universal fit recommendations. All dimensions are mm. Checks cover meaningful dimensions or analytical geometry; adapt them when changing the design. No viewer package or optional hardware library is required.

## Rounded mounting plate

A filled sketch with four cutout disks produces one extrusion. This avoids fragile post-extrusion hole edge indexing. Hole size is a named diameter converted once to a radius.

```python
from math import isclose, pi
from build123d import (
    BuildPart, BuildSketch, Circle, GeomType, Locations, Mode, Part,
    RectangleRounded, extrude,
)

WIDTH = 80.0
DEPTH = 50.0
THICKNESS = 6.0
CORNER_RADIUS = 4.0
HOLE_DIAMETER = 4.4
HOLE_CENTERS = [(-28.0, -14.0), (28.0, -14.0),
                (-28.0, 14.0), (28.0, 14.0)]


def build() -> Part:
    assert 0 < 2 * CORNER_RADIUS < min(WIDTH, DEPTH)
    with BuildPart() as plate:
        with BuildSketch():
            RectangleRounded(WIDTH, DEPTH, CORNER_RADIUS)
            with Locations(*HOLE_CENTERS):
                Circle(HOLE_DIAMETER / 2, mode=Mode.SUBTRACT)
        extrude(amount=THICKNESS)
    plate.part.label = "rounded_mounting_plate"
    return plate.part


def check(shape: Part) -> None:
    assert not shape.is_null and shape.is_valid
    assert len(shape.solids()) == 1
    box = shape.bounding_box()
    assert isclose(box.size.X, WIDTH, abs_tol=1e-5)
    assert isclose(box.size.Y, DEPTH, abs_tol=1e-5)
    assert isclose(box.min.Z, 0, abs_tol=1e-5)
    assert isclose(box.max.Z, THICKNESS, abs_tol=1e-5)
    plan_area = WIDTH * DEPTH - (4 - pi) * CORNER_RADIUS**2
    plan_area -= len(HOLE_CENTERS) * pi * (HOLE_DIAMETER / 2)**2
    assert isclose(shape.volume, plan_area * THICKNESS, rel_tol=1e-7)
    # One rim per hole at the top datum; rounded outer corners have another radius.
    rims = [
        edge for edge in shape.edges().filter_by(GeomType.CIRCLE)
        if isclose(edge.radius, HOLE_DIAMETER / 2, rel_tol=0, abs_tol=1e-5)
        and isclose(edge.arc_center.Z, THICKNESS, rel_tol=0, abs_tol=1e-5)
    ]
    assert len(rims) == len(HOLE_CENTERS)
    for x, y in HOLE_CENTERS:
        matches = [
            edge for edge in rims
            if isclose(edge.arc_center.X, x, rel_tol=0, abs_tol=1e-5)
            and isclose(edge.arc_center.Y, y, rel_tol=0, abs_tol=1e-5)
        ]
        assert len(matches) == 1, f"Missing or duplicate hole at {(x, y)}"


if __name__ == "__main__":
    result = build()
    check(result)
    print(f"plate: {result.volume:.3f} mm^3")
```

## Open enclosure with controlled wall and floor

Outer and inner rounded rectangles maintain the same corner centers: the inner radius is outer radius minus wall. The cavity extends above the box, while its bottom defines the exact floor thickness. This is deliberately simpler than a shell operation whose failure might depend on a small exterior feature.

```python
from math import isclose, pi
from build123d import GeomType, Part, Plane, RectangleRounded, extrude

WIDTH = 60.0
DEPTH = 40.0
HEIGHT = 24.0
WALL = 2.0
FLOOR = 2.4
OUTER_RADIUS = 4.0
CUT_MARGIN = 1.0


def rounded_area(width: float, depth: float, radius: float) -> float:
    return width * depth - (4 - pi) * radius**2


def build() -> Part:
    assert 0 < WALL < OUTER_RADIUS < min(WIDTH, DEPTH) / 2
    assert 0 < FLOOR < HEIGHT
    outside = extrude(RectangleRounded(WIDTH, DEPTH, OUTER_RADIUS), HEIGHT)
    inner_profile = Plane.XY.offset(FLOOR) * RectangleRounded(
        WIDTH - 2 * WALL, DEPTH - 2 * WALL, OUTER_RADIUS - WALL,
    )
    cavity = extrude(inner_profile, HEIGHT - FLOOR + CUT_MARGIN)
    result = outside - cavity
    result.label = "open_enclosure"
    return result


def check(shape: Part) -> None:
    assert not shape.is_null and shape.is_valid
    assert len(shape.solids()) == 1
    assert isclose(shape.bounding_box().size.Z, HEIGHT, abs_tol=1e-5)
    outside_volume = rounded_area(WIDTH, DEPTH, OUTER_RADIUS) * HEIGHT
    cavity_volume = rounded_area(
        WIDTH - 2 * WALL, DEPTH - 2 * WALL, OUTER_RADIUS - WALL,
    ) * (HEIGHT - FLOOR)
    assert isclose(shape.volume, outside_volume - cavity_volume, rel_tol=1e-7)
    # The cavity's lowest upward planar face is its floor, not the rim.
    floors = [f for f in shape.faces().filter_by(GeomType.PLANE)
              if abs(f.center().Z - FLOOR) < 1e-5
              and f.normal_at().Z > 0.999]
    assert len(floors) == 1


if __name__ == "__main__":
    result = build()
    check(result)
    print(f"enclosure: {result.volume:.3f} mm^3")
```

## Turned bushing: revolve

The XZ sketch uses local X as radius and local Y as world height. Its inner boundary never crosses the axis. The flange and sleeve are one revolved region, with a continuous central bore.

```python
from math import isclose, pi
from build123d import Axis, Part, Plane, Polygon, revolve

BORE_RADIUS = 4.0
BODY_RADIUS = 8.0
FLANGE_RADIUS = 12.0
HEIGHT = 20.0
FLANGE_HEIGHT = 4.0


def build() -> Part:
    assert 0 < BORE_RADIUS < BODY_RADIUS < FLANGE_RADIUS
    assert 0 < FLANGE_HEIGHT < HEIGHT
    section = Plane.XZ * Polygon(
        (BORE_RADIUS, 0), (FLANGE_RADIUS, 0),
        (FLANGE_RADIUS, FLANGE_HEIGHT), (BODY_RADIUS, FLANGE_HEIGHT),
        (BODY_RADIUS, HEIGHT), (BORE_RADIUS, HEIGHT),
    )
    result = revolve(section, axis=Axis.Z)
    result.label = "flanged_bushing"
    return result


def check(shape: Part) -> None:
    assert not shape.is_null and shape.is_valid
    assert len(shape.solids()) == 1
    expected = pi * (FLANGE_RADIUS**2 - BORE_RADIUS**2) * FLANGE_HEIGHT
    expected += pi * (BODY_RADIUS**2 - BORE_RADIUS**2) * (HEIGHT - FLANGE_HEIGHT)
    assert isclose(shape.volume, expected, rel_tol=1e-7)
    assert isclose(shape.bounding_box().size.Z, HEIGHT, abs_tol=1e-5)
    assert isclose(shape.bounding_box().size.X, 2 * FLANGE_RADIUS, abs_tol=1e-5)


if __name__ == "__main__":
    result = build()
    check(result)
    print(f"bushing: {result.volume:.3f} mm^3")
```

## Curved round bar: sweep

A circular section follows a quarter-circle path. Its start plane is perpendicular to the actual path tangent, not guessed from a world plane. A circular section avoids clocking ambiguity; a rectangular section would require an explicit frame orientation.

```python
from math import isclose, pi, sqrt
from build123d import Circle, Part, Plane, ThreePointArc, sweep

BEND_RADIUS = 30.0
BAR_RADIUS = 3.0


def build() -> Part:
    assert BEND_RADIUS > BAR_RADIUS > 0
    r, z = BEND_RADIUS, BAR_RADIUS
    path = ThreePointArc(
        (0, 0, z),
        (r / sqrt(2), r - r / sqrt(2), z),
        (r, r, z),
    )
    section = Plane(origin=path @ 0, z_dir=path % 0) * Circle(BAR_RADIUS)
    result = sweep(section, path=path)
    result.label = "quarter_circle_bar"
    return result


def check(shape: Part) -> None:
    assert not shape.is_null and shape.is_valid
    assert len(shape.solids()) == 1
    expected = pi * BAR_RADIUS**2 * (pi * BEND_RADIUS / 2)
    assert isclose(shape.volume, expected, rel_tol=1e-6)
    box = shape.bounding_box()
    assert isclose(box.min.Z, 0, abs_tol=1e-5)
    assert isclose(box.max.Z, 2 * BAR_RADIUS, abs_tol=1e-5)


if __name__ == "__main__":
    result = build()
    check(result)
    print(f"swept bar: {result.volume:.3f} mm^3")
```

## Circular transition: loft

A ruled loft between concentric circles is a frustum with a known analytical volume. This offers a reliable starting point before introducing noncircular sections, offsets, extra stations, or smooth bulging transitions.

```python
from math import isclose, pi
from build123d import Circle, Part, Plane, loft

BOTTOM_RADIUS = 14.0
TOP_RADIUS = 8.0
HEIGHT = 30.0


def build() -> Part:
    assert BOTTOM_RADIUS > 0 and TOP_RADIUS > 0 and HEIGHT > 0
    bottom = Circle(BOTTOM_RADIUS)
    top = Plane.XY.offset(HEIGHT) * Circle(TOP_RADIUS)
    result = loft([bottom, top], ruled=True)
    result.label = "circular_transition"
    return result


def check(shape: Part) -> None:
    assert not shape.is_null and shape.is_valid
    assert len(shape.solids()) == 1
    expected = pi * HEIGHT / 3 * (
        BOTTOM_RADIUS**2 + BOTTOM_RADIUS * TOP_RADIUS + TOP_RADIUS**2
    )
    assert isclose(shape.volume, expected, rel_tol=1e-6)
    box = shape.bounding_box()
    assert isclose(box.min.Z, 0, abs_tol=1e-5)
    assert isclose(box.max.Z, HEIGHT, abs_tol=1e-5)


if __name__ == "__main__":
    result = build()
    check(result)
    print(f"loft: {result.volume:.3f} mm^3")
```

## Pin and bushing assembly

Two independently labeled parts are grouped, not fused. The example radial clearance of 0.3 mm is an explicit demonstration parameter, not a fit specification. Both components rest at Z=0 but the pin is shown inside the bushing; use a separate layout for printing them independently.

```python
from math import isclose
from build123d import Align, Compound, Cylinder

PIN_RADIUS = 4.0
RADIAL_CLEARANCE = 0.3
OUTER_RADIUS = 8.0
HEIGHT = 12.0
BED_ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)


def build() -> Compound:
    bore_radius = PIN_RADIUS + RADIAL_CLEARANCE
    assert 0 < PIN_RADIUS < bore_radius < OUTER_RADIUS
    bushing = (
        Cylinder(OUTER_RADIUS, HEIGHT, align=BED_ALIGN)
        - Cylinder(bore_radius, HEIGHT, align=BED_ALIGN)
    )
    pin = Cylinder(PIN_RADIUS, HEIGHT, align=BED_ALIGN)
    bushing.label = "bushing"
    pin.label = "pin"
    return Compound(children=[bushing, pin], label="pin_and_bushing")


def check(shape: Compound) -> None:
    assert not shape.is_null and shape.is_valid
    assert len(shape.solids()) == 2
    # Solid queries also work after STEP import; assembly child order is not a datum.
    a, b = shape.solids()
    common = a & b
    overlap = 0.0 if common is None else sum(s.volume for s in common.solids())
    assert overlap < 1e-7
    assert isclose(a.distance_to(b), RADIAL_CLEARANCE, rel_tol=0, abs_tol=1e-6)
    assert isclose(shape.bounding_box().min.Z, 0, abs_tol=1e-5)


if __name__ == "__main__":
    result = build()
    check(result)
    print(f"assembly: {len(result.solids())} solids")
```

## Sources and adaptation

These recipes are original examples derived from checked API contracts, not copied upstream example programs.

- [0.13.0 sketch objects](../../../../vendor/build123d-0.13.0/src/build123d/objects_sketch.py)
- [0.13.0 part operations](../../../../vendor/build123d-0.13.0/src/build123d/operations_part.py)
- [Sweep and generic operations](../../../../vendor/build123d-0.13.0/src/build123d/operations_generic.py)
- [Assemblies and placement semantics](../../../../vendor/build123d-0.13.0/docs/assemblies.rst)

After adapting a recipe, retain the checks that still express requirements and replace formulas that no longer describe the geometry. A success message from this file checks the BREP only; run the repository export command and inspect its previews for the deliverable.
