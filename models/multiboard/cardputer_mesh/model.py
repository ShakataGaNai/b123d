"""Shallow landscape Cardputer pocket. Millimeters; XY bed, rear +Y, up +Z."""

from math import isclose, radians, tan, sqrt

from build123d import Align, Axis, Box, Compound, Cylinder, Plane, Pos, Rot, Solid, fillet
from models.multiboard.peg import peg

DEVICE_WIDTH = 84.0
SIDE_ALLOWANCE = 0.4
SLOT_WIDTH = DEVICE_WIDTH + 2 * SIDE_ALLOWANCE
SLOT_THICKNESS = 17.0  # User-selected finished opening, buttons and clearance included.
POCKET_DEPTH = 10.0
FLOOR = 3.5
WALL = 2.5
HEIGHT = FLOOR + POCKET_DEPTH
WIDTH = SLOT_WIDTH + 2 * WALL
DEPTH = SLOT_THICKNESS + 2 * WALL
OUTER_RADIUS = 1.0
ENTRY_RADIUS = 0.5
REAR_GAP = 20.0  # Slot rear boundary to peg-root shoulder, not peg tip.
CAP_REAR_RESERVE = 16.0  # User-reported rear protrusion, upright.
MIN_REAR_CLEARANCE = 4.0
ASSUMED_ASSEMBLY_HEIGHT = 70.0
PEG_AF = 13.5
PEG_PROJECTION = 6.5
PEG_CENTERS_X = (-25.0, 25.0)
ARM_WIDTH = 20.0
ROOT_OVERLAP = 0.2
ROOT_Y = SLOT_THICKNESS / 2 + REAR_GAP
ARM_RADIUS = 2.0
ANTENNA_DIAMETER = 10.0
ANTENNA_RADIUS = ANTENNA_DIAMETER / 2
ANTENNA_Y = (DEPTH / 2 + ROOT_Y) / 2
LENGTH_TOL = 1e-5
VOLUME_TOL = 1e-5


def box_at(x, y, z, width, depth, height):
    return Pos(x, y, z) * Box(width, depth, height,
                              align=(Align.CENTER, Align.CENTER, Align.MIN))


def build() -> Solid | Compound:
    """Return a fresh pocket and two integral bed-supported spacer arms."""
    if not (FLOOR > 0 and POCKET_DEPTH > 0 and 0 < ENTRY_RADIUS < WALL / 2):
        raise ValueError("Invalid floor, engagement or entry radius")
    if HEIGHT < PEG_AF or ARM_WIDTH <= PEG_AF or ROOT_OVERLAP >= WALL:
        raise ValueError("Arms must fully support the peg roots")
    if REAR_GAP < CAP_REAR_RESERVE + MIN_REAR_CLEARANCE:
        raise ValueError("Rear spacing consumes the upright cap clearance budget")
    body = box_at(0, 0, 0, WIDTH, DEPTH, HEIGHT)
    corners = body.edges().filter_by(Axis.Z)
    if len(corners) != 4:
        raise ValueError("Expected four exterior corners")
    body = fillet(corners, radius=OUTER_RADIUS)
    body -= box_at(0, 0, FLOOR, SLOT_WIDTH, SLOT_THICKNESS, POCKET_DEPTH + 1)
    entrance = [e for e in body.edges()
                if isclose(e.bounding_box().min.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and isclose(e.bounding_box().max.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and (isclose(abs(e.center().X), SLOT_WIDTH / 2, abs_tol=LENGTH_TOL)
                     or isclose(abs(e.center().Y), SLOT_THICKNESS / 2, abs_tol=LENGTH_TOL))]
    if len(entrance) != 4:
        raise ValueError("Expected four inner mouth edges")
    body = fillet(entrance, radius=ENTRY_RADIUS)
    arm_start = DEPTH / 2 - ROOT_OVERLAP
    for x in PEG_CENTERS_X:
        body += box_at(x, (arm_start + ROOT_Y) / 2, 0,
                       ARM_WIDTH, ROOT_Y - arm_start, HEIGHT)
    # Round the four rear vertical corners and the two concave inner roots.
    rounded = []
    for edge in body.edges().filter_by(Axis.Z):
        c = edge.center()
        is_rear = isclose(c.Y, ROOT_Y, abs_tol=LENGTH_TOL)
        is_inner_root = (isclose(c.Y, DEPTH / 2, abs_tol=LENGTH_TOL)
                         and isclose(abs(c.X), abs(PEG_CENTERS_X[0]) - ARM_WIDTH / 2,
                                     abs_tol=LENGTH_TOL))
        if is_rear or is_inner_root:
            rounded.append(edge)
    if len(rounded) != 6:
        raise ValueError("Expected four rear corners and two inside arm roots")
    body = fillet(rounded, radius=ARM_RADIUS)
    if not (0 < ANTENNA_RADIUS < HEIGHT and
            ANTENNA_RADIUS + ARM_RADIUS < (ROOT_Y - DEPTH / 2) / 2):
        raise ValueError("Antenna saddle must leave a web and clear rounded ends")
    # Axis along X; cylinder center on the top face makes an exact half circle.
    cutter = Pos(0, ANTENNA_Y, HEIGHT) * Rot(Y=90) * Cylinder(
        ANTENNA_RADIUS, WIDTH + 2)
    body -= cutter
    for x in PEG_CENTERS_X:
        rear = Plane(origin=(x, ROOT_Y, PEG_AF / 2),
                     x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        body += rear * peg(across_flats=PEG_AF, projection=PEG_PROJECTION,
                           root_overlap=ROOT_OVERLAP)
    body.label = "cardputer_mesh"
    return body


def check(shape) -> None:
    """Check cavity, walls/floor, both peg sections and nominal rear keep-out."""
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Holder must be one valid solid")
    solid = shape.solids()[0]
    bounds = shape.bounding_box()
    expected = (-WIDTH / 2, -DEPTH / 2, 0, WIDTH / 2,
                ROOT_Y + PEG_PROJECTION, HEIGHT)
    for actual, target in zip((*bounds.min, *bounds.max), expected):
        if not isclose(actual, target, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Incorrect envelope: {bounds}")
    insertion = box_at(0, 0, FLOOR + 0.001, SLOT_WIDTH - 0.002,
                       SLOT_THICKNESS - 0.002, ASSUMED_ASSEMBLY_HEIGHT)
    overlap = shape & insertion
    if overlap is not None and overlap.volume > VOLUME_TOL:
        raise ValueError("Vertical insertion path is obstructed")
    delta = 0.001
    for x in (-DEVICE_WIDTH / 3, 0, DEVICE_WIDTH / 3):
        for z, inside in ((FLOOR - delta, True), (FLOOR + delta, False)):
            if solid.is_inside((x, 0, z)) != inside:
                raise ValueError("Floor height incorrect")
    for z in (FLOOR + 1, HEIGHT - ENTRY_RADIUS - 0.1):
        for x, y in ((SLOT_WIDTH / 2, 0), (-SLOT_WIDTH / 2, 0),
                     (0, SLOT_THICKNESS / 2), (0, -SLOT_THICKNESS / 2)):
            for scale, inside in ((1 - delta, False), (1 + delta, True)):
                if solid.is_inside((x * scale, y * scale, z)) != inside:
                    raise ValueError("Incorrect slot wall boundary")
    # Check full floor and uninterrupted wall cores, not only point probes.
    cores = [box_at(0, 0, 0.001, SLOT_WIDTH, SLOT_THICKNESS, FLOOR - 0.002),
             box_at(0, -(SLOT_THICKNESS + WALL) / 2, 0.001,
                    SLOT_WIDTH, WALL - 0.002, HEIGHT - ENTRY_RADIUS - 0.002),
             box_at(0, (SLOT_THICKNESS + WALL) / 2, 0.001,
                    SLOT_WIDTH, WALL - 0.002, HEIGHT - ENTRY_RADIUS - 0.002)]
    for x in (-1, 1):
        cores.append(box_at(x * (SLOT_WIDTH + WALL) / 2, 0, 0.001,
                            WALL - 0.002, SLOT_THICKNESS,
                            HEIGHT - ENTRY_RADIUS - 0.002))
    for core in cores:
        if (core - shape).volume > VOLUME_TOL:
            raise ValueError("Missing wall or floor material")
    for x in PEG_CENTERS_X:
        core = box_at(x, (DEPTH / 2 + ROOT_Y) / 2, 0.001,
                      ARM_WIDTH - 2 * ARM_RADIUS - 0.002, ROOT_Y - DEPTH / 2,
                      HEIGHT - ANTENNA_RADIUS - 0.002)
        if (core - shape).volume > VOLUME_TOL:
            raise ValueError("Spacer arm is interrupted")
        # Probe the actual circular support boundary along each saddle.
        for dx in (-ARM_WIDTH / 3, 0, ARM_WIDTH / 3):
            for dy in (-4.0, -2.5, 0, 2.5, 4.0):
                z = HEIGHT - sqrt(ANTENNA_RADIUS**2 - dy**2)
                for dz, inside in ((-delta, True), (delta, False)):
                    if solid.is_inside((x + dx, ANTENNA_Y + dy, z + dz)) != inside:
                        raise ValueError("Incorrect circular antenna-rest profile")
        # Material outside each nominal R2 rear arc must be removed.
        for side in (-1, 1):
            corner_x = x + side * ARM_WIDTH / 2
            if solid.is_inside((corner_x - side * 0.1, ROOT_Y - 0.1, 2)):
                raise ValueError("Rear arm corner was not rounded")
        inner_x = x - (1 if x > 0 else -1) * ARM_WIDTH / 2
        toward_gap = -1 if x > 0 else 1
        if not solid.is_inside((inner_x + toward_gap * 0.1, DEPTH / 2 + 0.1, 2)):
            raise ValueError("Inside arm root radius is missing")
        section = shape & box_at(x, ROOT_Y + PEG_PROJECTION / 2, -1,
                                 PEG_AF + 2, 0.1, PEG_AF + 2)
        area = 2 * PEG_AF**2 * tan(radians(22.5))
        if section is None or not isclose(section.volume, area * 0.1,
                                          rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError("Incorrect snap peg section")
        b = section.bounding_box()
        for actual, target in zip((*b.min, *b.max),
                                  (x - PEG_AF / 2, ROOT_Y + PEG_PROJECTION / 2 - 0.05, 0,
                                   x + PEG_AF / 2, ROOT_Y + PEG_PROJECTION / 2 + 0.05, PEG_AF)):
            if not isclose(actual, target, rel_tol=0, abs_tol=LENGTH_TOL):
                raise ValueError("Incorrect peg placement or dimensions")
    # Upright reported cap envelope only; rocking clearance is not certified.
    rear_limit = SLOT_THICKNESS / 2 + CAP_REAR_RESERVE
    backplane = box_at(0, ROOT_Y + 0.5, 0, WIDTH + 20, 1, 100)
    keepout = box_at(0, (SLOT_THICKNESS / 2 + rear_limit) / 2,
                     HEIGHT + 0.1, DEVICE_WIDTH, rear_limit - SLOT_THICKNESS / 2,
                     ASSUMED_ASSEMBLY_HEIGHT)
    if keepout.distance_to(backplane) < MIN_REAR_CLEARANCE - LENGTH_TOL:
        raise ValueError("Nominal upright cap envelope too close to backplane")
    overlap = shape & keepout
    if overlap is not None and overlap.volume > VOLUME_TOL:
        raise ValueError("Holder enters upper rear keep-out")
