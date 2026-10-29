"""Manufacturer-informed rounded-bottom Plus cradle; mm, pegs toward +Y.

The shell's lower broad face is a B-spline, not an exact R16. Our conservative
rounded approximation and STEP measurements are documented in object research.
"""

from math import cos, isclose, pi, radians, sin, sqrt, tan

from build123d import Align, Box, Compound, Plane, Pos, RectangleRounded, Solid, extrude

from models.multiboard.finish import EDGE_RADIUS, OUTSIDE_CORNER_RADIUS, round_edges, rounded_blank
from models.multiboard.peg import peg

DEVICE_WIDTH = 72.0  # Lower shell, not the 73.14 mm upper button envelope.
DEVICE_THICKNESS = 20.4  # Whole-shell thickness; lower section measures 19 mm.
DEVICE_HEIGHT = 115.0
DEVICE_XY_RADIUS = 1.4  # Conservative envelope, not a claimed factory radius.
LOWER_RADIUS = 16.0  # Conservative broad-face approximation of measured B-splines.
FIT_CLEARANCE = 0.8  # Per side; uncalibrated, not manufacturer tolerance.
SLOT_WIDTH = DEVICE_WIDTH + 2 * FIT_CLEARANCE
SLOT_THICKNESS = DEVICE_THICKNESS + 2 * FIT_CLEARANCE
SLOT_RADIUS = DEVICE_XY_RADIUS + FIT_CLEARANCE
SEAT_RADIUS = LOWER_RADIUS + FIT_CLEARANCE
POCKET_DEPTH = 20.0
WALL = 2.5
FLOOR = 2.5
WIDTH = SLOT_WIDTH + 2 * WALL
THICKNESS = SLOT_THICKNESS + 2 * WALL
HEIGHT = FLOOR + POCKET_DEPTH
USB_RELIEF_WIDTH = 24.0  # Broad opening, not a measured connector dimension.
CABLE_WIDTH = 20.0
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_X = (-12.5, 12.5)
PEG_CENTER_Z = PEG_ACROSS_FLATS / 2
JOIN_OVERLAP = 0.8  # Bridges the R0.6 rounded underside without altering projection.
CUT_OVERRUN = 1.0
LENGTH_TOL = 1e-5
VOLUME_TOL = 1e-5
# Independent measured section extrema of the original manufacturer's lower shell.
LOWER_SECTIONS = (
    (1.0, -14.9270, 19.0438), (2.0, -20.7960, 23.4333),
    (4.0, -27.2586, 28.4543), (6.0, -30.9267, 31.4154),
    (8.0, -33.1939, 33.3309), (10.0, -34.6001, 34.5890),
    (12.0, -35.4276, 35.3826), (16.0, -35.9762, 35.9758),
    (20.0, -35.9777, 35.9777),
)


def _lower_envelope(clearance: float, bottom: float) -> Solid | Compound:
    """Continuous upward insertion envelope, with rounded XY and XZ profiles.

    Only the lower shell enters the holder. Extend its widest section above the
    rim; the far-away upper rounding of this construction never enters the part.
    Clearance offsets horizontally; bottom stays on the supporting floor datum.
    """
    width = DEVICE_WIDTH + 2 * clearance
    thickness = DEVICE_THICKNESS + 2 * clearance
    sweep_height = DEVICE_HEIGHT + POCKET_DEPTH
    xy = Pos(0, 0, bottom) * extrude(
        RectangleRounded(width, thickness, DEVICE_XY_RADIUS + clearance),
        amount=sweep_height,
    )
    broad_plane = Plane(origin=(0, thickness / 2, bottom),
                        x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    broad = extrude(broad_plane * RectangleRounded(
        width, sweep_height, LOWER_RADIUS + clearance,
        align=(Align.CENTER, Align.MIN),
    ), amount=thickness)
    return xy & broad


def build() -> Solid | Compound:
    """Return a fresh rounded lower-seat cradle with USB relief and two pegs."""
    if not (FIT_CLEARANCE > 0 and WALL > 2 * EDGE_RADIUS and FLOOR > 2 * EDGE_RADIUS):
        raise ValueError("Clearance, wall and floor must accommodate the edge finish")
    if not (0 < SEAT_RADIUS < POCKET_DEPTH < DEVICE_HEIGHT):
        raise ValueError("Rounded lower seat must transition below the mouth")
    if not (0 < SLOT_RADIUS < SLOT_THICKNESS / 2 < SLOT_WIDTH / 2):
        raise ValueError("Pocket radii must fit the opening")
    if not (0 < CABLE_WIDTH < USB_RELIEF_WIDTH < DEVICE_WIDTH - 2 * LOWER_RADIUS):
        raise ValueError("USB opening must retain flat support on both sides")
    if not (EDGE_RADIUS < JOIN_OVERLAP < WALL and PEG_PROJECTION > 0):
        raise ValueError("Peg root must bridge the rounded underside within the wall")
    if PEG_ACROSS_FLATS > HEIGHT or max(abs(x) for x in PEG_X) + PEG_ACROSS_FLATS / 2 > WIDTH / 2 - OUTSIDE_CORNER_RADIUS:
        raise ValueError("Pegs must fit the flat rear wall")
    if not isclose(PEG_X[1] - PEG_X[0], 25.0, abs_tol=LENGTH_TOL):
        raise ValueError("Peg spacing must follow the 25 mm grid")

    result = rounded_blank(WIDTH, THICKNESS, HEIGHT) - _lower_envelope(FIT_CLEARANCE, FLOOR)
    mouth = [edge for edge in result.edges()
             if isclose(edge.bounding_box().min.Z, HEIGHT, abs_tol=LENGTH_TOL)
             and isclose(edge.bounding_box().max.Z, HEIGHT, abs_tol=LENGTH_TOL)
             and edge.bounding_box().min.X >= -SLOT_WIDTH / 2 - LENGTH_TOL
             and edge.bounding_box().max.X <= SLOT_WIDTH / 2 + LENGTH_TOL
             and edge.bounding_box().min.Y >= -SLOT_THICKNESS / 2 - LENGTH_TOL
             and edge.bounding_box().max.Y <= SLOT_THICKNESS / 2 + LENGTH_TOL]
    if len(mouth) != 8:
        raise ValueError("Expected eight rounded-section mouth edges")
    result = round_edges(mouth)
    usb_relief = Pos(0, 0, -CUT_OVERRUN) * Box(
        USB_RELIEF_WIDTH, SLOT_THICKNESS, FLOOR + 2 * CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    result = result - usb_relief
    # Round the four underside aperture edges, not the functional seat profile.
    aperture = [edge for edge in result.edges()
                if isclose(edge.bounding_box().min.Z, 0, abs_tol=LENGTH_TOL)
                and isclose(edge.bounding_box().max.Z, 0, abs_tol=LENGTH_TOL)
                and edge.bounding_box().min.X >= -USB_RELIEF_WIDTH / 2 - LENGTH_TOL
                and edge.bounding_box().max.X <= USB_RELIEF_WIDTH / 2 + LENGTH_TOL
                and edge.bounding_box().min.Y >= -SLOT_THICKNESS / 2 - LENGTH_TOL
                and edge.bounding_box().max.Y <= SLOT_THICKNESS / 2 + LENGTH_TOL]
    if len(aperture) != 4:
        raise ValueError("Expected four underside USB aperture edges")
    result = round_edges(aperture)
    for x in PEG_X:
        rear = Plane(origin=(x, THICKNESS / 2, PEG_CENTER_Z),
                     x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        result = result + rear * peg(across_flats=PEG_ACROSS_FLATS,
                                    projection=PEG_PROJECTION, root_overlap=JOIN_OVERLAP)
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Holder did not produce solid geometry")
    result.label = "lilygo_tdeck"
    return result


def check(shape: Solid | Compound) -> None:
    """Exercise rounded support, manufacturer-derived insertion and real finish."""
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
    device_path = _lower_envelope(0, FLOOR + delta)
    cable_path = Pos(0, 0, -20) * Box(
        CABLE_WIDTH, SLOT_THICKNESS - 2 * delta, 20 + FLOOR + delta,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    for name, tool in (("rounded-shell insertion", device_path), ("bottom cable", cable_path)):
        obstruction = shape & tool
        if obstruction is not None and obstruction.volume > VOLUME_TOL:
            raise ValueError(f"Obstructed {name} path")

    # Independent source witnesses, including heights where square-pocket checks
    # would miss the newly required rising lower seat.
    for height, left, right in LOWER_SECTIONS:
        for x in (left, right):
            if solid.is_inside((x, 0, FLOOR + height)):
                raise ValueError("Measured manufacturer lower silhouette hits seat")
    for side in (-1, 1):
        for x in (17.0, 24.0, 28.0, 32.0, 35.0):
            dx = max(0.0, x - (SLOT_WIDTH / 2 - SEAT_RADIUS))
            seat_z = FLOOR + SEAT_RADIUS - sqrt(SEAT_RADIUS**2 - dx**2)
            for offset, expected in ((-delta, True), (delta, False)):
                if solid.is_inside((side * x, 0, seat_z + offset)) != expected:
                    raise ValueError("Rounded lower seat profile or supporting material is incorrect")
        for z, expected in ((-delta, False), (delta, True),
                            (FLOOR - delta, True), (FLOOR + delta, False)):
            if solid.is_inside((side * 17, 0, z)) != expected:
                raise ValueError("Flat support ledge is missing or has wrong floor thickness")
        for offset, expected in ((-delta, False), (delta, True)):
            if solid.is_inside((side * (USB_RELIEF_WIDTH / 2 + offset), 0, FLOOR / 2)) != expected:
                raise ValueError("USB opening width is incorrect away from underside round")

    # An unrounded mid-wall section preserves the analytical XY profile despite
    # the functional lower seat and cosmetic upper/lower edge treatments.
    z = HEIGHT - 2 * EDGE_RADIUS
    outer_area = WIDTH * THICKNESS - (4 - pi) * OUTSIDE_CORNER_RADIUS**2
    inner_area = SLOT_WIDTH * SLOT_THICKNESS - (4 - pi) * SLOT_RADIUS**2
    slab_thickness = 0.1
    section = shape & (Pos(0, 0, z) * Box(WIDTH + 2, THICKNESS, slab_thickness))
    if section is None or not isclose(section.volume, (outer_area - inner_area) * slab_thickness,
                                      rel_tol=0, abs_tol=VOLUME_TOL):
        raise ValueError("Upper wall section does not match rounded XY profile")
    for side in (-1, 1):
        for boundary, inside_before in ((SLOT_WIDTH / 2, False), (WIDTH / 2, True)):
            for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                if solid.is_inside((side * (boundary + offset), 0, z)) != expected:
                    raise ValueError("Straight side wall thickness is incorrect")
        # Verify R0.6 quarter circles at the exterior top/bottom and mouth.
        for a in (30, 45, 60):
            for offset, expected in ((-delta, True), (delta, False)):
                r = EDGE_RADIUS + offset
                x = side * (WIDTH / 2 - EDGE_RADIUS + r * cos(radians(a)))
                for edge_z, sign in ((EDGE_RADIUS, -1), (HEIGHT - EDGE_RADIUS, 1)):
                    if solid.is_inside((x, 0, edge_z + sign * r * sin(radians(a)))) != expected:
                        raise ValueError("External R0.6 finish is incorrect")
            for offset, expected in ((-delta, True), (delta, False)):
                r = EDGE_RADIUS + offset
                x = side * (SLOT_WIDTH / 2 + EDGE_RADIUS - r * cos(radians(a)))
                if solid.is_inside((x, 0, HEIGHT - EDGE_RADIUS + r * sin(radians(a)))) != expected:
                    raise ValueError("Pocket mouth R0.6 finish is incorrect")

    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(radians(22.5))
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
