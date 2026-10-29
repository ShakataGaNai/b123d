"""Original WisMesh Pocket V1 cradle, mm; XY bed and snap pegs toward +Y.

V1-specific reseller envelope is 52 x 30 x 94 mm, not a manufacturer drawing.
Bottom USB and open side reliefs are broad allowances, not port templates.
"""

from math import cos, isclose, radians, sin, tan

from build123d import Align, Box, Compound, Plane, Pos, RectangleRounded, Solid, extrude, fillet

from models.multiboard.peg import peg
from models.multiboard.finish import (
    EDGE_RADIUS, OUTSIDE_CORNER_RADIUS, round_edges,
)

DEVICE_WIDTH = 52.0
DEVICE_THICKNESS = 30.0
DEVICE_HEIGHT = 94.0
FIT_CLEARANCE = 0.8  # Per face, uncalibrated.
SLOT_WIDTH = DEVICE_WIDTH + 2 * FIT_CLEARANCE
SLOT_THICKNESS = DEVICE_THICKNESS + 2 * FIT_CLEARANCE
POCKET_DEPTH = 20.0
WALL = 2.5
FLOOR = 2.5
SLOT_RADIUS = 0.5
OUTER_RADIUS = OUTSIDE_CORNER_RADIUS
WIDTH = SLOT_WIDTH + 2 * WALL
THICKNESS = SLOT_THICKNESS + 2 * WALL
HEIGHT = FLOOR + POCKET_DEPTH
USB_RELIEF_WIDTH = 24.0
CABLE_WIDTH = 20.0
SIDE_RETAINED_STRIP = 4.0
SIDE_RELIEF_WIDTH = SLOT_THICKNESS - 2 * SIDE_RETAINED_STRIP
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_X = (-12.5, 12.5)
PEG_CENTER_Z = PEG_ACROSS_FLATS / 2
JOIN_OVERLAP = 0.8  # Buried root bridges the R0.6 underside round.
CUT_OVERRUN = 1.0
LENGTH_TOL = 1e-5  # CAD/STEP tolerance only.
VOLUME_TOL = 1e-5


def build() -> Solid | Compound:
    """Return a fresh single-solid cradle with USB and side-switch access."""
    if not (FIT_CLEARANCE > 0 and WALL > 0 and FLOOR > 0 and 0 < POCKET_DEPTH < DEVICE_HEIGHT):
        raise ValueError("Clearance, walls, floor and insertion depth are invalid")
    if not (0 < SLOT_RADIUS < SLOT_THICKNESS / 2 < SLOT_WIDTH / 2):
        raise ValueError("Pocket radii must fit the opening")
    if not (0 < CABLE_WIDTH < USB_RELIEF_WIDTH < SLOT_WIDTH - 2 * SLOT_RADIUS):
        raise ValueError("USB relief must leave two supporting floor ledges")
    if not (SLOT_RADIUS < SIDE_RETAINED_STRIP < SLOT_THICKNESS / 2):
        raise ValueError("Side relief must preserve the rounded corner walls")
    if not (0 < JOIN_OVERLAP < WALL and PEG_PROJECTION > 0):
        raise ValueError("Peg root must overlap only the rear wall")
    if PEG_ACROSS_FLATS > HEIGHT or max(abs(x) for x in PEG_X) + PEG_ACROSS_FLATS / 2 > WIDTH / 2 - OUTER_RADIUS:
        raise ValueError("Pegs must fit the flat rear wall")
    if not isclose(PEG_X[1] - PEG_X[0], 25.0, abs_tol=LENGTH_TOL):
        raise ValueError("Peg spacing must follow the 25 mm grid")

    body = extrude(RectangleRounded(WIDTH, THICKNESS, OUTER_RADIUS), amount=HEIGHT)
    pocket = Pos(0, 0, FLOOR) * extrude(
        RectangleRounded(SLOT_WIDTH, SLOT_THICKNESS, SLOT_RADIUS),
        amount=POCKET_DEPTH + CUT_OVERRUN,
    )
    usb_relief = Pos(0, 0, -CUT_OVERRUN) * Box(
        USB_RELIEF_WIDTH, SLOT_THICKNESS, FLOOR + 2 * CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    # A single crosswise tool opens both side walls, preserving all floor ledges.
    side_relief = Pos(0, 0, FLOOR) * Box(
        WIDTH + 2 * CUT_OVERRUN, SIDE_RELIEF_WIDTH, POCKET_DEPTH + CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    result = body - pocket - usb_relief - side_relief
    # R3 free-end profile corners, followed by the shared R0.6 edge break.
    # Distinct profile/edge radii avoid spherical-pole STL degeneracies.
    end_corners = [
        edge for edge in result.edges()
        if isclose(edge.bounding_box().min.Z, HEIGHT, abs_tol=LENGTH_TOL)
        and isclose(edge.bounding_box().max.Z, HEIGHT, abs_tol=LENGTH_TOL)
        and isclose(abs(edge.center().Y), SIDE_RELIEF_WIDTH / 2, abs_tol=LENGTH_TOL)
        and isclose(edge.length, WALL, abs_tol=LENGTH_TOL)
    ]
    if len(end_corners) != 4:
        raise ValueError("Expected four free-end profile corners")
    result = fillet(end_corners, radius=OUTSIDE_CORNER_RADIUS)
    exposed = []
    for edge in result.edges():
        b = edge.bounding_box()
        horizontal = isclose(b.min.Z, b.max.Z, abs_tol=LENGTH_TOL)
        # The R3 end round meets the top tangentially: this seam is not an edge break.
        if (horizontal and isclose(b.min.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and isclose(abs(edge.center().Y),
                            SIDE_RELIEF_WIDTH / 2 + OUTSIDE_CORNER_RADIUS,
                            abs_tol=LENGTH_TOL)):
            continue
        at_top_or_bottom = horizontal and (
            isclose(b.min.Z, HEIGHT, abs_tol=LENGTH_TOL)
            or isclose(b.min.Z, 0, abs_tol=LENGTH_TOL))
        side_plane = any(
            isclose(abs(b.min.X), x, abs_tol=LENGTH_TOL)
            and isclose(b.min.X, b.max.X, abs_tol=LENGTH_TOL)
            for x in (WIDTH / 2, SLOT_WIDTH / 2))
        end_profile = side_plane and (
            isclose(abs(edge.center().Y), SIDE_RELIEF_WIDTH / 2, abs_tol=LENGTH_TOL)
            or b.min.Z >= HEIGHT - OUTSIDE_CORNER_RADIUS - LENGTH_TOL)
        open_deck = horizontal and isclose(b.min.Z, FLOOR, abs_tol=LENGTH_TOL) and (
            isclose(abs(edge.center().X), WIDTH / 2, abs_tol=LENGTH_TOL))
        if at_top_or_bottom or end_profile or open_deck:
            exposed.append(edge)
    if len(exposed) != 50:
        raise ValueError(f"Expected 50 exposed perimeter edges, found {len(exposed)}")
    result = round_edges(exposed)
    for x in PEG_X:
        rear = Plane(origin=(x, THICKNESS / 2, PEG_CENTER_Z),
                     x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        result = result + rear * peg(across_flats=PEG_ACROSS_FLATS,
                                    projection=PEG_PROJECTION, root_overlap=JOIN_OVERLAP)
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Holder did not produce solid geometry")
    result.label = "wismesh_pocket"
    return result


def check(shape: Solid | Compound) -> None:
    """Check device, cable/switch paths, retained walls/seat and both snap pegs."""
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Holder must be one valid solid")
    solid = shape.solids()[0]
    bounds = shape.bounding_box()
    for actual, expected in zip((*bounds.min, *bounds.max),
                                (-WIDTH / 2, -THICKNESS / 2, 0,
                                 WIDTH / 2, THICKNESS / 2 + PEG_PROJECTION, HEIGHT)):
        if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Unexpected holder envelope: {bounds}")

    delta = 0.001
    device_path = Pos(0, 0, FLOOR + delta) * Box(
        DEVICE_WIDTH, DEVICE_THICKNESS, DEVICE_HEIGHT + POCKET_DEPTH,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cable_path = Pos(0, 0, -20) * Box(
        CABLE_WIDTH, SLOT_THICKNESS - 2 * delta, 20 + FLOOR + delta,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    switch_path = Pos(0, 0, FLOOR + delta) * Box(
        WIDTH + 2, SIDE_RELIEF_WIDTH - 2 * delta, POCKET_DEPTH,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    for name, tool in (("device insertion", device_path), ("bottom cable", cable_path),
                       ("side switch", switch_path)):
        obstruction = shape & tool
        if obstruction is not None and obstruction.volume > VOLUME_TOL:
            raise ValueError(f"Obstructed {name} path")

    for side in (-1, 1):
        seat_x = side * (USB_RELIEF_WIDTH / 2 + 5)
        for z, expected in ((-delta, False), (delta, True),
                            (FLOOR - delta, True), (FLOOR + delta, False)):
            if solid.is_inside((seat_x, 0, z)) != expected:
                raise ValueError("Floor ledge thickness or seat height is incorrect")
        for offset, expected in ((-delta, False), (delta, True)):
            if solid.is_inside((side * (USB_RELIEF_WIDTH / 2 + offset), 0, FLOOR / 2)) != expected:
                raise ValueError("USB floor opening width is incorrect")
            if solid.is_inside((0, side * (SLOT_THICKNESS / 2 + offset), FLOOR / 2)) != expected:
                raise ValueError("USB floor opening thickness is incorrect")

    retained_y = SLOT_THICKNESS / 2 - SIDE_RETAINED_STRIP / 2
    for z in (FLOOR + 1, HEIGHT - OUTSIDE_CORNER_RADIUS - EDGE_RADIUS - delta):
        for side in (-1, 1):
            for boundary, inside_before in ((SLOT_WIDTH / 2, False), (WIDTH / 2, True)):
                for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                    for sy in (-1, 1):
                        if solid.is_inside((side * (boundary + offset), sy * retained_y, z)) != expected:
                            raise ValueError("Retained side wall or slot width is incorrect")
            for boundary, inside_before in ((SLOT_THICKNESS / 2, False), (THICKNESS / 2, True)):
                for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                    if solid.is_inside((0, side * (boundary + offset), z)) != expected:
                        raise ValueError("Front/rear wall or slot thickness is incorrect")
            for sy in (-1, 1):
                for offset, expected in ((-delta, False), (delta, True)):
                    point = (side * (SLOT_WIDTH / 2 + WALL / 2),
                             sy * (SIDE_RELIEF_WIDTH / 2 + offset), z)
                    if solid.is_inside(point) != expected:
                        raise ValueError("Side opening width or retained strip is incorrect")
        if not solid.is_inside((SLOT_WIDTH / 2 + WALL / 2, 0, FLOOR - delta)):
            raise ValueError("Side relief incorrectly removes the supporting floor")

    cx, cy = SLOT_WIDTH / 2 - SLOT_RADIUS, SLOT_THICKNESS / 2 - SLOT_RADIUS
    for sx in (-1, 1):
        for sy in (-1, 1):
            for angle in (30, 45, 60):
                for radius, inside_before in ((SLOT_RADIUS, False), (OUTER_RADIUS, True)):
                    for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                        r = radius + offset
                        point = (sx * (cx + r * cos(radians(angle))),
                                 sy * (cy + r * sin(radians(angle))), FLOOR + 1)
                        if solid.is_inside(point) != expected:
                            raise ValueError("Rounded wall normal thickness is incorrect")

    # Check material throughout the ledges, excluding deliberately rounded edges.
    for side in (-1, 1):
        core = Pos(side * (USB_RELIEF_WIDTH / 2 + 6), 0, FLOOR / 2) * Box(
            10, SLOT_THICKNESS - 2 * EDGE_RADIUS, FLOOR - 2 * EDGE_RADIUS,
        )
        missing = core - shape
        if missing is not None and missing.volume > VOLUME_TOL:
            raise ValueError("Supporting floor ledge has missing material")
    for zcenter, zsign in ((EDGE_RADIUS, -1), (HEIGHT - EDGE_RADIUS, 1)):
        for angle in (30, 45, 60):
            for offset, inside in ((-delta, True), (delta, False)):
                r = EDGE_RADIUS + offset
                point = (0, -THICKNESS / 2 + EDGE_RADIUS - r * cos(radians(angle)),
                         zcenter + zsign * r * sin(radians(angle)))
                if solid.is_inside(point) != inside:
                    raise ValueError("Outside rim is not the standard R0.6")

    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(radians(22.5))

    slab_thickness = 0.1
    for x in PEG_X:
        slab = Pos(x, THICKNESS / 2 + PEG_PROJECTION / 2, PEG_CENTER_Z) * Box(
            PEG_ACROSS_FLATS + 2, slab_thickness, PEG_ACROSS_FLATS + 2,
        )
        section = shape & slab
        if section is None or section.is_null:
            raise ValueError("Snap peg is missing")
        if not isclose(section.volume, peg_area * slab_thickness, rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError("Snap peg section is not the required octagon")
        for actual, expected in zip((*section.bounding_box().min, *section.bounding_box().max),
                                    (x - PEG_ACROSS_FLATS / 2,
                                     THICKNESS / 2 + PEG_PROJECTION / 2 - slab_thickness / 2, 0,
                                     x + PEG_ACROSS_FLATS / 2,
                                     THICKNESS / 2 + PEG_PROJECTION / 2 + slab_thickness / 2,
                                     PEG_ACROSS_FLATS)):
            if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
                raise ValueError("Snap peg placement or dimensions are incorrect")
