"""Pins-down XIAO cradle with a rear upright LoRa antenna slot and snap peg.

Millimeters. XY is the bed, +Z is up, USB faces -Y, snap peg points +Y.
Header plastic seats at Z=13.5; pins enter downward. The center is open.
An assumed 8 x 1 mm antenna enters the rear 8.4 x 1.4 x 8 mm blind slot.
See the linked research for manufacturer coordinates and assumed header stock.
"""

from math import cos, isclose, pi, radians, sin, tan

from build123d import Align, Axis, Box, Compound, Plane, Pos, Solid, fillet

from models.multiboard.peg import peg

# Manufacturer through-hole footprint; not the different SMD carrier pads.
ROW_SPACING = 15.24
PIN_PITCH = 2.54
PINS_PER_ROW = 7
PCB_WIDTH = 17.8
PCB_LENGTH = 21.0

# Assumed ordinary male header, not a measured specimen or universal standard.
PIN_WIDTH = 0.64
PIN_PROJECTION = 6.0
HEADER_WIDTH = 2.54
HEADER_LENGTH = PINS_PER_ROW * PIN_PITCH
HEADER_HEIGHT = 2.5

OUTER_WALL = 1.5
INNER_WALL = OUTER_WALL
FRONT_Y = -13.0
CENTER_REAR = 11.0
HEIGHT = 13.5
OUTER_RADIUS = 1.0
INNER_RADIUS = 1.0
SLOT_WIDTH = 1.4
SLOT_LENGTH = 17.0
SLOT_DEPTH = 8.0
CENTER_WIDTH = ROW_SPACING - SLOT_WIDTH - 2 * INNER_WALL
REAR_WALL = 2.0
# User-approved antenna approximation; clearance is per side, not calibrated.
ANTENNA_WIDTH = 8.0
ANTENNA_THICKNESS = 1.0
ANTENNA_CLEARANCE = 0.2
ANTENNA_SLOT_DEPTH = 8.0
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
JOIN_OVERLAP = 0.2
CUT_OVERRUN = 1.0
LENGTH_TOL = 1e-5
VOLUME_TOL = 1e-5

WIDTH = ROW_SPACING + SLOT_WIDTH + 2 * OUTER_WALL
SLOT_FLOOR = HEIGHT - SLOT_DEPTH
ANTENNA_SLOT_WIDTH = ANTENNA_WIDTH + 2 * ANTENNA_CLEARANCE
ANTENNA_SLOT_THICKNESS = ANTENNA_THICKNESS + 2 * ANTENNA_CLEARANCE
ANTENNA_SLOT_FLOOR = HEIGHT - ANTENNA_SLOT_DEPTH
ANTENNA_CENTER_Y = CENTER_REAR + REAR_WALL + ANTENNA_SLOT_THICKNESS / 2
REAR_Y = ANTENNA_CENTER_Y + ANTENNA_SLOT_THICKNESS / 2 + REAR_WALL
DEPTH = REAR_Y - FRONT_Y
CENTER_LENGTH = CENTER_REAR - FRONT_Y
PIN_ARRAY_LENGTH = (PINS_PER_ROW - 1) * PIN_PITCH + PIN_WIDTH


def build() -> Solid | Compound:
    """Return a fresh single-solid cradle without building on import."""
    if not (PIN_WIDTH < SLOT_WIDTH < HEADER_WIDTH):
        raise ValueError("Slots must clear pins but support header plastic")
    if not (PIN_ARRAY_LENGTH < SLOT_LENGTH < HEADER_LENGTH < DEPTH):
        raise ValueError("Slots must clear the complete seven-pin array")
    if not (PIN_PROJECTION + 0.5 <= SLOT_DEPTH < HEIGHT):
        raise ValueError("Pin tips need bottom clearance and a closed slot floor")
    if not (0 < CENTER_WIDTH < ROW_SPACING - HEADER_WIDTH):
        raise ValueError("Center relief must preserve both header support ledges")
    if not (ROW_SPACING + HEADER_WIDTH < WIDTH
            and FRONT_Y + OUTER_RADIUS < -HEADER_LENGTH / 2
            and REAR_Y - OUTER_RADIUS > HEADER_LENGTH / 2):
        raise ValueError("Header support must remain inside the straight rail tops")
    if not (PCB_LENGTH / 2 < CENTER_REAR and 0 < JOIN_OVERLAP < REAR_WALL):
        raise ValueError("Rear spine must clear the PCB and contain the peg root")
    if not (0 < PEG_ACROSS_FLATS <= HEIGHT and PEG_ACROSS_FLATS < WIDTH):
        raise ValueError("Peg must fit the back and stay above the print bed")
    if not (ANTENNA_WIDTH > 0 and ANTENNA_THICKNESS > 0 and ANTENNA_CLEARANCE > 0):
        raise ValueError("Antenna dimensions and per-side clearance must be positive")
    if not (0 < ANTENNA_SLOT_DEPTH <= 10 and ANTENNA_SLOT_DEPTH < HEIGHT):
        raise ValueError("Antenna slot must be blind and no more than 10 mm deep")
    if ANTENNA_SLOT_WIDTH + 2 * REAR_WALL >= WIDTH - 2 * OUTER_RADIUS:
        raise ValueError("Antenna slot must leave solid end walls inside the corners")
    if not (0 < INNER_RADIUS < CENTER_WIDTH / 2
            and INNER_RADIUS + OUTER_RADIUS < (WIDTH - CENTER_WIDTH) / 2):
        raise ValueError("Inner radii must fit the opening and prong tips")
    if not (FRONT_Y + INNER_RADIUS < -HEADER_LENGTH / 2
            and CENTER_REAR - INNER_RADIUS > HEADER_LENGTH / 2):
        raise ValueError("Inner corner fillets must remain beyond the header seats")

    body = Pos(0, (FRONT_Y + REAR_Y) / 2, 0) * Box(
        WIDTH, DEPTH, HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    corners = body.edges().filter_by(Axis.Z)
    if len(corners) != 4:
        raise ValueError("Expected four outside vertical corners")
    body = fillet(corners, radius=OUTER_RADIUS)
    # Open front/underside: only the two side rails and rear spine remain.
    center = Pos(0, CENTER_REAR, -CUT_OVERRUN) * Box(
        CENTER_WIDTH, CENTER_LENGTH + CUT_OVERRUN, HEIGHT + 2 * CUT_OVERRUN,
        align=(Align.CENTER, Align.MAX, Align.MIN),
    )
    body = body - center
    for x in (-ROW_SPACING / 2, ROW_SPACING / 2):
        slot = Pos(x, 0, SLOT_FLOOR) * Box(
            SLOT_WIDTH, SLOT_LENGTH, SLOT_DEPTH + CUT_OVERRUN,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        body = body - slot
    antenna_slot = Pos(0, ANTENNA_CENTER_Y, ANTENNA_SLOT_FLOOR) * Box(
        ANTENNA_SLOT_WIDTH, ANTENNA_SLOT_THICKNESS, ANTENNA_SLOT_DEPTH + CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body = body - antenna_slot
    inner_corners = [
        edge for edge in body.edges().filter_by(Axis.Z)
        if isclose(abs(edge.center().X), CENTER_WIDTH / 2,
                   rel_tol=0, abs_tol=LENGTH_TOL)
        and any(isclose(edge.center().Y, y, rel_tol=0, abs_tol=LENGTH_TOL)
                for y in (FRONT_Y, CENTER_REAR))
    ]
    if len(inner_corners) != 4:
        raise ValueError("Expected two front and two rear inner prong corners")
    body = fillet(inner_corners, radius=INNER_RADIUS)

    rear = Plane(
        origin=(0, REAR_Y, PEG_ACROSS_FLATS / 2),
        x_dir=(1, 0, 0), z_dir=(0, 1, 0),
    )
    result = body + rear * peg(
        across_flats=PEG_ACROSS_FLATS, projection=PEG_PROJECTION,
        root_overlap=JOIN_OVERLAP,
    )
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Cradle fusion did not produce solid geometry")
    result.label = "xiao_multiboard_holder"
    return result


def check(shape: Solid | Compound) -> None:
    """Measure slots, load-bearing seats, insertion clearance and rear interface."""
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Cradle must be one valid solid")
    solid = shape.solids()[0]
    bounds = shape.bounding_box()
    expected = (-WIDTH / 2, FRONT_Y, 0,
                WIDTH / 2, REAR_Y + PEG_PROJECTION, HEIGHT)
    for actual, target in zip((*bounds.min, *bounds.max), expected):
        if not isclose(actual, target, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Unexpected cradle envelope: {bounds}")

    def require_clear(tool: Solid | Compound, feature: str) -> None:
        overlap = shape & tool
        if overlap is not None and overlap.volume > VOLUME_TOL:
            raise ValueError(f"Obstructed {feature}: {overlap.volume} mm^3")

    def require_material(tool: Solid | Compound, feature: str) -> None:
        overlap = shape & tool
        if overlap is None or not isclose(overlap.volume, tool.volume,
                                         rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError(f"Missing material at {feature}")

    delta = 0.01
    for x in (-ROW_SPACING / 2, ROW_SPACING / 2):
        require_clear(Pos(x, 0, SLOT_FLOOR) * Box(
            SLOT_WIDTH, SLOT_LENGTH, SLOT_DEPTH + CUT_OVERRUN,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), "continuous full-depth pin slot")
        require_clear(Pos(x, 0, HEIGHT - PIN_PROJECTION) * Box(
            PIN_WIDTH, PIN_ARRAY_LENGTH, PIN_PROJECTION + 10,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), "complete pin-array insertion sweep")
        side = -1 if x < 0 else 1
        outer_wall_x = x + side * (SLOT_WIDTH / 2 + OUTER_WALL / 2)
        require_material(Pos(outer_wall_x, 0, HEIGHT / 2) * Box(
            OUTER_WALL, SLOT_LENGTH, HEIGHT,
        ), "full-length outer pin-slot wall")
        inner_wall_x = x - side * (SLOT_WIDTH / 2 + INNER_WALL / 2)
        require_material(Pos(inner_wall_x, 0, HEIGHT / 2) * Box(
            INNER_WALL, SLOT_LENGTH, HEIGHT,
        ), "full-length inner pin-slot wall")
        require_clear(Pos(side * (WIDTH / 2 + delta), 0, HEIGHT / 2) * Box(
            delta, SLOT_LENGTH, HEIGHT,
        ), "space outside the thinned arm")
        # Boundary probes reject enlarged, shallow, shifted or through slots.
        for y in (-SLOT_LENGTH / 2 + delta, 0, SLOT_LENGTH / 2 - delta):
            for z, inside in ((SLOT_FLOOR - delta, True),
                              (SLOT_FLOOR + delta, False)):
                if solid.is_inside((x, y, z)) != inside:
                    raise ValueError("Slot floor is missing or at the wrong depth")
            for side in (-1, 1):
                if not solid.is_inside((x + side * (SLOT_WIDTH / 2 + delta),
                                        y, HEIGHT - 1)):
                    raise ValueError("Slot side wall is missing or misplaced")
        for side in (-1, 1):
            if not solid.is_inside((x, side * (SLOT_LENGTH / 2 + delta), HEIGHT - 1)):
                raise ValueError("Slot end wall is missing or misplaced")
            ledge_width = (HEADER_WIDTH - SLOT_WIDTH) / 2
            ledge_x = x + side * (SLOT_WIDTH / 2 + ledge_width / 2)
            require_material(Pos(ledge_x, 0, HEIGHT - 0.1) * Box(
                ledge_width, HEADER_LENGTH, 0.1,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ), "header-plastic support ledge")

    # Preserve the straight channel and the narrower strip between rear arcs.
    require_clear(Pos(0, CENTER_REAR - INNER_RADIUS, -CUT_OVERRUN) * Box(
        CENTER_WIDTH, CENTER_LENGTH - INNER_RADIUS + CUT_OVERRUN,
        HEIGHT + 2 * CUT_OVERRUN,
        align=(Align.CENTER, Align.MAX, Align.MIN),
    ), "open underside and USB-side access")
    require_clear(Pos(0, CENTER_REAR, -CUT_OVERRUN) * Box(
        CENTER_WIDTH - 2 * INNER_RADIUS, CENTER_LENGTH + CUT_OVERRUN,
        HEIGHT + 2 * CUT_OVERRUN,
        align=(Align.CENTER, Align.MAX, Align.MIN),
    ), "clear center between rounded rear joins")
    # Probe both sides of each quarter-circle through the full-height feature.
    # Front rounding removes material; rear rounding adds it inside the opening.
    for side in (-1, 1):
        for rear in (False, True):
            center_x = side * (CENTER_WIDTH / 2 + (-1 if rear else 1) * INNER_RADIUS)
            center_y = CENTER_REAR - INNER_RADIUS if rear else FRONT_Y + INNER_RADIUS
            direction = 1 if rear else -1
            for angle in (15, 45, 75):
                for offset in (-delta, delta):
                    radius = INNER_RADIUS + offset
                    point_x = center_x + side * direction * radius * cos(radians(angle))
                    point_y = center_y + direction * radius * sin(radians(angle))
                    expected_inside = offset > 0 if rear else offset < 0
                    for z in (delta, HEIGHT / 2, HEIGHT - delta):
                        if solid.is_inside((point_x, point_y, z)) != expected_inside:
                            raise ValueError("Missing or incorrect inner prong fillet")
    require_clear(Pos(0, 0, HEIGHT + HEADER_HEIGHT) * Box(
        PCB_WIDTH, PCB_LENGTH, 10,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ), "nominal PCB and upper electronics keep-out")
    # Both webs connect the rails; the rear web also contains the peg root.
    for y in (CENTER_REAR + REAR_WALL / 2, REAR_Y - REAR_WALL / 2):
        require_material(Pos(0, y, HEIGHT / 2) * Box(
            CENTER_WIDTH, REAR_WALL, HEIGHT,
        ), "antenna front/rear spine web")

    require_clear(Pos(0, ANTENNA_CENTER_Y, ANTENNA_SLOT_FLOOR) * Box(
        ANTENNA_SLOT_WIDTH, ANTENNA_SLOT_THICKNESS, ANTENNA_SLOT_DEPTH + CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ), "full-depth antenna slot and top entry")
    require_clear(Pos(0, ANTENNA_CENTER_Y, ANTENNA_SLOT_FLOOR) * Box(
        ANTENNA_WIDTH, ANTENNA_THICKNESS, ANTENNA_SLOT_DEPTH + 20,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ), "nominal upright antenna insertion sweep")
    require_material(Pos(0, ANTENNA_CENTER_Y, ANTENNA_SLOT_FLOOR - 0.1) * Box(
        ANTENNA_SLOT_WIDTH, ANTENNA_SLOT_THICKNESS, 0.1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ), "closed antenna slot floor")
    for side in (-1, 1):
        require_material(Pos(side * (ANTENNA_SLOT_WIDTH / 2 + 0.05),
                             ANTENNA_CENTER_Y, ANTENNA_SLOT_FLOOR) * Box(
            0.1, ANTENNA_SLOT_THICKNESS, ANTENNA_SLOT_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), "antenna slot width boundary")
        require_material(Pos(0, ANTENNA_CENTER_Y
                             + side * (ANTENNA_SLOT_THICKNESS / 2 + 0.05),
                             ANTENNA_SLOT_FLOOR) * Box(
            ANTENNA_SLOT_WIDTH, 0.1, ANTENNA_SLOT_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), "antenna slot thickness boundary")

    slab_thickness = 0.1
    section = shape & (Pos(0, REAR_Y + PEG_PROJECTION / 2,
                           PEG_ACROSS_FLATS / 2) * Box(
        PEG_ACROSS_FLATS + 2, slab_thickness, PEG_ACROSS_FLATS + 2,
    ))
    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(pi / 8)
    if section is None or not isclose(section.volume, peg_area * slab_thickness,
                                      rel_tol=0, abs_tol=VOLUME_TOL):
        raise ValueError("Peg section is not the specified octagon")
    for actual, target in zip(section.bounding_box().size,
                              (PEG_ACROSS_FLATS, slab_thickness, PEG_ACROSS_FLATS)):
        if not isclose(actual, target, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError("Peg across-flats dimension is incorrect")
    if not isclose(section.bounding_box().min.Z, 0, rel_tol=0, abs_tol=LENGTH_TOL):
        raise ValueError("Peg bottom must be flush with the print bed")

    # Independent analytic volume catches unintended cuts/additions elsewhere.
    # Equal-radius front removals and rear additions cancel exactly in volume.
    expected_volume = ((WIDTH * DEPTH - (4 - pi) * OUTER_RADIUS**2) * HEIGHT
                       - CENTER_WIDTH * CENTER_LENGTH * HEIGHT
                       - 2 * SLOT_WIDTH * SLOT_LENGTH * SLOT_DEPTH
                       - ANTENNA_SLOT_WIDTH * ANTENNA_SLOT_THICKNESS * ANTENNA_SLOT_DEPTH
                       + peg_area * PEG_PROJECTION)
    if not isclose(shape.volume, expected_volume, rel_tol=0, abs_tol=VOLUME_TOL):
        raise ValueError("Cradle volume differs from the dimensioned construction")
