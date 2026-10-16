"""20 mm-deep portrait WisMesh Tag pocket; mm, XY bed, pegs toward +Y.

RAK finished enclosure: 92 high x 59 wide x 7.5 thick; see research record.
Clearance and pocket radii are design allowances, not measured case geometry.
"""

from math import cos, isclose, pi, radians, sin, tan

from build123d import Align, Box, Compound, Plane, Pos, RectangleRounded, Solid, extrude

from models.multiboard.peg import peg
from models.multiboard.finish import EDGE_RADIUS, OUTSIDE_CORNER_RADIUS, rounded_blank, round_edges
from models.multiboard.label import label_tool, check_label

DEVICE_WIDTH = 59.0
DEVICE_THICKNESS = 7.5
DEVICE_HEIGHT = 92.0
FIT_CLEARANCE = 0.4  # Per side, uncalibrated FDM allowance.
SLOT_WIDTH = DEVICE_WIDTH + 2 * FIT_CLEARANCE
SLOT_THICKNESS = DEVICE_THICKNESS + 2 * FIT_CLEARANCE
POCKET_DEPTH = 20.0  # Vertical rim-to-seat distance, not front/back gap.
WALL = 2.5
FLOOR = 2.5
SLOT_RADIUS = 0.5
OUTER_RADIUS = OUTSIDE_CORNER_RADIUS
WIDTH = SLOT_WIDTH + 2 * WALL
THICKNESS = SLOT_THICKNESS + 2 * WALL
HEIGHT = FLOOR + POCKET_DEPTH
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_PITCH = 25.0
PEG_CENTERS_X = (-PEG_PITCH / 2, PEG_PITCH / 2)
PEG_CENTER_Z = PEG_ACROSS_FLATS / 2
JOIN_OVERLAP = 0.8  # Overlap exceeds the R0.6 bottom round; projection unchanged.
CUT_OVERRUN = 1.0
LENGTH_TOL = 1e-5  # Numerical CAD/STEP tolerance, mm.
VOLUME_TOL = 1e-5  # Numerical CAD/STEP tolerance, mm^3.


def build() -> Solid | Compound:
    """Return a fresh rounded pocket with two unchanged registered snap pegs."""
    if not (FIT_CLEARANCE > 0 and WALL > 0 and FLOOR > 0 and 0 < POCKET_DEPTH < DEVICE_HEIGHT):
        raise ValueError("Clearance/walls/floor must be positive; device must extend above rim")
    if not (0 < SLOT_RADIUS < SLOT_THICKNESS / 2 < SLOT_WIDTH / 2):
        raise ValueError("Pocket radius must fit its opening")
    if not (0 < JOIN_OVERLAP < WALL and PEG_PROJECTION > 0):
        raise ValueError("Peg overlap must remain inside rear wall")
    if PEG_PITCH <= PEG_ACROSS_FLATS or PEG_ACROSS_FLATS > HEIGHT:
        raise ValueError("Pegs must be separate and fit rear wall height")
    if any(abs(x) + PEG_ACROSS_FLATS / 2 > WIDTH / 2 - OUTER_RADIUS for x in PEG_CENTERS_X):
        raise ValueError("Pegs must fit entirely on the flat rear wall")

    body = rounded_blank(WIDTH, THICKNESS, HEIGHT)
    pocket = Pos(0, 0, FLOOR) * extrude(
        RectangleRounded(SLOT_WIDTH, SLOT_THICKNESS, SLOT_RADIUS),
        amount=POCKET_DEPTH + CUT_OVERRUN,
    )
    result = body - pocket
    entrance = [edge for edge in result.edges()
                if isclose(edge.bounding_box().min.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and isclose(edge.bounding_box().max.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and abs(edge.center().X) <= SLOT_WIDTH / 2 + LENGTH_TOL
                and abs(edge.center().Y) <= SLOT_THICKNESS / 2 + LENGTH_TOL]
    if len(entrance) != 8:
        raise ValueError("Expected eight rounded-slot entrance edges")
    result = round_edges(entrance)
    result = result - label_tool("Wis Tag", floor_width=SLOT_WIDTH - 2 * SLOT_RADIUS,
                                 floor_depth=SLOT_THICKNESS - 2 * SLOT_RADIUS,
                                 floor_height=FLOOR)
    for x in PEG_CENTERS_X:
        rear = Plane(origin=(x, THICKNESS / 2, PEG_CENTER_Z),
                     x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        result = result + rear * peg(across_flats=PEG_ACROSS_FLATS,
                                    projection=PEG_PROJECTION, root_overlap=JOIN_OVERLAP)
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Holder did not produce solid geometry")
    result.label = "wismesh_tag_multiboard_holder"
    return result


def check(shape: Solid | Compound) -> None:
    """Check insertion sweep, seat, walls, floor and both actual peg interfaces."""
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

    delta = 0.001
    # Union of the conservative full device envelope throughout vertical insertion
    # from just above the rim to its seated position. No attached cable is modeled.
    device_path = Pos(0, 0, FLOOR + delta) * Box(
        DEVICE_WIDTH, DEVICE_THICKNESS, DEVICE_HEIGHT + POCKET_DEPTH + CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    obstruction = shape & device_path
    if obstruction is not None and obstruction.volume > VOLUME_TOL:
        raise ValueError("Nominal device is obstructed during insertion")

    # Seat probes avoid the centered lettering; check_label proves its backing.
    for x in (-DEVICE_WIDTH / 2 + 1, DEVICE_WIDTH / 2 - 1):
        for z, expected in ((-delta, False), (delta, True),
                            (FLOOR - delta, True), (FLOOR + delta, False)):
            if solid.is_inside((x, 0, z)) != expected:
                raise ValueError("Floor thickness or rim-to-seat insertion depth is incorrect")

    # Front/rear probes are between the two pegs, not through a projecting peg.
    for z in (FLOOR + 1, HEIGHT - EDGE_RADIUS - delta):
        for side in (-1, 1):
            for boundary, before in ((SLOT_WIDTH / 2, False), (WIDTH / 2, True)):
                for offset, expected in ((-delta, before), (delta, not before)):
                    if solid.is_inside((side * (boundary + offset), 0, z)) != expected:
                        raise ValueError("Slot width or side-wall thickness is incorrect")
            for boundary, before in ((SLOT_THICKNESS / 2, False), (THICKNESS / 2, True)):
                for offset, expected in ((-delta, before), (delta, not before)):
                    if solid.is_inside((0, side * (boundary + offset), z)) != expected:
                        raise ValueError("Slot thickness or front/rear wall is incorrect")

    # Concentric inner/outer arcs establish WALL normal thickness at corners.
    cx = SLOT_WIDTH / 2 - SLOT_RADIUS
    cy = SLOT_THICKNESS / 2 - SLOT_RADIUS
    for sx in (-1, 1):
        for sy in (-1, 1):
            for angle in (30, 45, 60):
                for radius, before in ((SLOT_RADIUS, False), (OUTER_RADIUS, True)):
                    for offset, expected in ((-delta, before), (delta, not before)):
                        r = radius + offset
                        point = (sx * (cx + r * cos(radians(angle))),
                                 sy * (cy + r * sin(radians(angle))), FLOOR + 1)
                        if solid.is_inside(point) != expected:
                            raise ValueError("Rounded wall radius or normal thickness is incorrect")

    # A mid-height horizontal section retains the exact analytic wall area.
    # Global prism volume no longer applies to the rounded rims and deboss.
    outer_area = WIDTH * THICKNESS - (4 - pi) * OUTER_RADIUS**2
    inner_area = SLOT_WIDTH * SLOT_THICKNESS - (4 - pi) * SLOT_RADIUS**2
    wall_slab = Pos(0, 0, HEIGHT - 2 * EDGE_RADIUS) * Box(WIDTH + 2, THICKNESS, 0.1)
    wall_section = shape & wall_slab
    if wall_section is None or not isclose(
        wall_section.volume, (outer_area - inner_area) * 0.1, abs_tol=VOLUME_TOL,
    ):
        raise ValueError("Rounded wall section does not match analytical area")
    check_label(shape, "Wis Tag", floor_width=SLOT_WIDTH - 2 * SLOT_RADIUS,
                floor_depth=SLOT_THICKNESS - 2 * SLOT_RADIUS, floor_height=FLOOR)
    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(radians(22.5))

    slab_thickness = 0.1
    section_y = THICKNESS / 2 + PEG_PROJECTION / 2
    for x in PEG_CENTERS_X:
        slab = Pos(x, section_y, PEG_CENTER_Z) * Box(
            PEG_ACROSS_FLATS + 2, slab_thickness, PEG_ACROSS_FLATS + 2,
        )
        section = shape & slab
        if section is None or section.is_null or len(section.solids()) != 1:
            raise ValueError("Rear snap peg is missing or disconnected")
        if not isclose(section.volume, peg_area * slab_thickness, rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError("Snap peg section is not the specified octagon")
        peg_bounds = section.bounding_box()
        for actual, expected in zip(
            (*peg_bounds.min, *peg_bounds.max),
            (x - PEG_ACROSS_FLATS / 2, section_y - slab_thickness / 2, 0,
             x + PEG_ACROSS_FLATS / 2, section_y + slab_thickness / 2, PEG_ACROSS_FLATS),
        ):
            if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
                raise ValueError("Peg size, center spacing or bottom alignment is incorrect")
