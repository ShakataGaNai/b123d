"""Simple 12 mm-deep Unit C6L pocket; millimeters, XY bed, rear peg toward +Y.

Manufacturer U202 envelope: 24 x 8 mm. Fit clearance is an uncalibrated allowance.
Rounded XY corners preserve a constant wall offset; the floor covers Grove.
"""

from math import cos, isclose, pi, radians, sin, tan

from build123d import Align, Box, Compound, Plane, Pos, RectangleRounded, Solid, extrude

from models.multiboard.peg import peg

DEVICE_WIDTH = 24.0
DEVICE_THICKNESS = 8.0
FIT_CLEARANCE = 0.4  # Per side, not a manufacturer tolerance.
SLOT_WIDTH = DEVICE_WIDTH + 2 * FIT_CLEARANCE
SLOT_THICKNESS = DEVICE_THICKNESS + 2 * FIT_CLEARANCE
POCKET_DEPTH = 12.0
WALL = 2.5
FLOOR = 2.5
SLOT_RADIUS = 0.5
OUTER_RADIUS = SLOT_RADIUS + WALL
WIDTH = SLOT_WIDTH + 2 * WALL
THICKNESS = SLOT_THICKNESS + 2 * WALL
HEIGHT = FLOOR + POCKET_DEPTH
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_CENTER_Z = PEG_ACROSS_FLATS / 2
JOIN_OVERLAP = 0.2
CUT_OVERRUN = 1.0
LENGTH_TOL = 1e-5  # mm, CAD/STEP numerical tolerance only.
VOLUME_TOL = 1e-5  # mm^3.


def build() -> Solid | Compound:
    """Return a fresh single-solid holder, with the registered snap peg unchanged."""
    if not (FIT_CLEARANCE > 0 and WALL > 0 and FLOOR > 0 and POCKET_DEPTH > 0):
        raise ValueError("Clearance, walls, floor and insertion depth must be positive")
    if not (0 < SLOT_RADIUS < SLOT_THICKNESS / 2 < SLOT_WIDTH / 2):
        raise ValueError("Slot corner radius must fit the device opening")
    if not (0 < JOIN_OVERLAP < WALL and PEG_PROJECTION > 0):
        raise ValueError("Peg overlap must stay within the rear wall")
    if PEG_ACROSS_FLATS > HEIGHT or PEG_ACROSS_FLATS > WIDTH - 2 * OUTER_RADIUS:
        raise ValueError("Bottom-aligned peg must fit the flat rear wall")

    body = extrude(RectangleRounded(WIDTH, THICKNESS, OUTER_RADIUS), amount=HEIGHT)
    pocket = Pos(0, 0, FLOOR) * extrude(
        RectangleRounded(SLOT_WIDTH, SLOT_THICKNESS, SLOT_RADIUS),
        amount=POCKET_DEPTH + CUT_OVERRUN,
    )
    rear = Plane(
        origin=(0, THICKNESS / 2, PEG_CENTER_Z),
        x_dir=(1, 0, 0), z_dir=(0, 1, 0),
    )
    mounted_peg = rear * peg(
        across_flats=PEG_ACROSS_FLATS, projection=PEG_PROJECTION,
        root_overlap=JOIN_OVERLAP,
    )
    result = body - pocket + mounted_peg
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Holder did not produce solid geometry")
    result.label = "unit_c6l_multiboard_holder"
    return result


def check(shape: Solid | Compound) -> None:
    """Check the actual seat, insertion path, rounded walls and snap interface."""
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Holder must be one valid solid")
    solid = shape.solids()[0]
    bounds = shape.bounding_box()
    for actual, expected in zip(
        (*bounds.min, *bounds.max),
        (-WIDTH / 2, -THICKNESS / 2, 0,
         WIDTH / 2, THICKNESS / 2 + PEG_PROJECTION, HEIGHT),
    ):
        if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Unexpected holder envelope: {bounds}")

    # A conservative square-cornered device envelope must drop straight in.
    device_path = Pos(0, 0, FLOOR + 0.001) * Box(
        DEVICE_WIDTH, DEVICE_THICKNESS, POCKET_DEPTH + CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    obstruction = shape & device_path
    if obstruction is not None and obstruction.volume > VOLUME_TOL:
        raise ValueError("Nominal device is obstructed during insertion")

    delta = 0.001
    for x, y in ((0, 0), (DEVICE_WIDTH / 2 - 1, 0), (-DEVICE_WIDTH / 2 + 1, 0)):
        for offset, expected in ((-delta, True), (delta, False)):
            if solid.is_inside((x, y, FLOOR + offset)) != expected:
                raise ValueError("Pocket floor is not at the specified insertion depth")

    # Probe inner/outer straight boundaries at two heights; rear outer wall is
    # checked off-center to avoid the intentionally projecting peg.
    for z in (FLOOR + 1, HEIGHT - delta):
        for side in (-1, 1):
            for boundary, inside_before in ((SLOT_WIDTH / 2, False), (WIDTH / 2, True)):
                for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                    if solid.is_inside((side * (boundary + offset), 0, z)) != expected:
                        raise ValueError("Slot width or side-wall thickness is incorrect")
            for boundary, inside_before in ((SLOT_THICKNESS / 2, False), (THICKNESS / 2, True)):
                for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                    if solid.is_inside((9, side * (boundary + offset), z)) != expected:
                        raise ValueError("Slot thickness or front/rear wall is incorrect")

    # The inner and outer corner arcs are concentric: their radius difference
    # establishes the same 2.5 mm normal wall through the rounded left/right sides.
    cx = SLOT_WIDTH / 2 - SLOT_RADIUS
    cy = SLOT_THICKNESS / 2 - SLOT_RADIUS
    for sx in (-1, 1):
        for sy in (-1, 1):
            for angle in (30, 45, 60):
                for radius, inside_before in ((SLOT_RADIUS, False), (OUTER_RADIUS, True)):
                    for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                        r = radius + offset
                        point = (sx * (cx + r * cos(radians(angle))),
                                 sy * (cy + r * sin(radians(angle))), FLOOR + 1)
                        if solid.is_inside(point) != expected:
                            raise ValueError("Rounded side radius or normal wall is incorrect")

    # Analytical volume catches an incomplete cut or extra internal material.
    outer_area = WIDTH * THICKNESS - (4 - pi) * OUTER_RADIUS**2
    inner_area = SLOT_WIDTH * SLOT_THICKNESS - (4 - pi) * SLOT_RADIUS**2
    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(radians(22.5))
    expected_volume = outer_area * HEIGHT - inner_area * POCKET_DEPTH + peg_area * PEG_PROJECTION
    if not isclose(shape.volume, expected_volume, rel_tol=0, abs_tol=VOLUME_TOL):
        raise ValueError("Pocket/floor/peg volume differs from the analytic design")

    slab_thickness = 0.1
    slab = Pos(0, THICKNESS / 2 + PEG_PROJECTION / 2, PEG_CENTER_Z) * Box(
        PEG_ACROSS_FLATS + 2, slab_thickness, PEG_ACROSS_FLATS + 2,
    )
    section = shape & slab
    if section is None or section.is_null:
        raise ValueError("Rear snap peg is missing")
    if not isclose(section.volume, peg_area * slab_thickness, rel_tol=0, abs_tol=VOLUME_TOL):
        raise ValueError("Snap peg section is not the required octagon")
    for actual, expected in zip(section.bounding_box().size,
                                (PEG_ACROSS_FLATS, slab_thickness, PEG_ACROSS_FLATS)):
        if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError("Snap peg dimensions are incorrect")
    if not isclose(section.bounding_box().min.Z, 0, rel_tol=0, abs_tol=LENGTH_TOL):
        raise ValueError("Snap peg must be bottom-aligned with the print bed")
