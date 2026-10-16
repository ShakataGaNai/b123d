"""Station G2 rounded drop-in pocket, mm; rear +Y, antenna +Z.

User-corrected body: 110 x 58 x 12 mm, excluding ~5 mm rear screws.
The full-body-width 6.5 mm rear corridor clears the entire insertion sweep.
"""

from math import isclose, radians, sqrt, tan

from build123d import Align, Box, Compound, Plane, Pos, RectangleRounded, Solid, extrude

from models.multiboard.peg import peg
from models.multiboard.finish import (
    EDGE_RADIUS, OUTSIDE_CORNER_RADIUS, rounded_blank, round_edges,
)

DEVICE_WIDTH = 58.0
DEVICE_THICKNESS = 12.0
DEVICE_HEIGHT = 110.0
SIDE_CLEARANCE = 0.6
FRONT_CLEARANCE = 0.6
REAR_SCREW_PROJECTION = 5.0  # User observation; not an inferred screw standard.
SCREW_CLEARANCE = 1.5
REAR_RELIEF = REAR_SCREW_PROJECTION + SCREW_CLEARANCE
WALL = 2.5
FLOOR = 2.5
POCKET_DEPTH = 20.0
INNER_RADIUS = 0.5  # Below side clearance: full 58 mm screw band reaches rear datum.
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_PITCH = 25.0
PEG_X = (-PEG_PITCH / 2, PEG_PITCH / 2)
PEG_CENTER_Z = PEG_ACROSS_FLATS / 2
JOIN_OVERLAP = 0.8  # Extends beyond the R0.6 underside round into the rear wall.
CUT_OVERRUN = 1.0
LENGTH_TOL = 1e-5  # mm, CAD/STEP numeric tolerance only.
VOLUME_TOL = 1e-5  # mm^3, interference/section numerical tolerance.
PROBE_OFFSET = 0.001
SLOT_WIDTH = DEVICE_WIDTH + 2 * SIDE_CLEARANCE
FRONT_INNER = -DEVICE_THICKNESS / 2 - FRONT_CLEARANCE
REAR_INNER = DEVICE_THICKNESS / 2 + REAR_RELIEF
FRONT_OUTER = FRONT_INNER - WALL
REAR_OUTER = REAR_INNER + WALL
WIDTH = SLOT_WIDTH + 2 * WALL
HEIGHT = FLOOR + POCKET_DEPTH
DEPTH = REAR_OUTER - FRONT_OUTER
SLOT_DEPTH = REAR_INNER - FRONT_INNER
CENTER_Y = (FRONT_INNER + REAR_INNER) / 2


def _box(width: float, front: float, rear: float, bottom: float, height: float):
    """A centered-X box with explicit Y/Z datums, outside builder contexts."""
    return Pos(0, front, bottom) * Box(
        width, rear - front, height, align=(Align.CENTER, Align.MIN, Align.MIN),
    )


def build() -> Solid | Compound:
    """Return one fresh solid; no import-time construction or export."""
    if min(SIDE_CLEARANCE, FRONT_CLEARANCE, SCREW_CLEARANCE, WALL, FLOOR) <= 0:
        raise ValueError("Fit allowances, walls and floor must be positive")
    if not 0 < POCKET_DEPTH < DEVICE_HEIGHT:
        raise ValueError("Pocket must leave the upper device uncovered")
    if INNER_RADIUS * (1 - 1 / sqrt(2)) >= min(SIDE_CLEARANCE, FRONT_CLEARANCE):
        raise ValueError("Rounded slot corners would intrude into the square body")
    if INNER_RADIUS >= SIDE_CLEARANCE:
        raise ValueError("Rear corner rounds must preserve full-body-width screw relief")
    if not EDGE_RADIUS < JOIN_OVERLAP < WALL:
        raise ValueError("Peg overlap must bridge the underside round within the wall")
    if PEG_ACROSS_FLATS > HEIGHT or PEG_PITCH <= PEG_ACROSS_FLATS:
        raise ValueError("Pegs must fit the back and remain separate")
    if PEG_PITCH + PEG_ACROSS_FLATS > WIDTH:
        raise ValueError("Pegs must remain within the rear wall width")

    body = Pos(0, CENTER_Y, 0) * rounded_blank(WIDTH, DEPTH, HEIGHT)
    pocket = Pos(0, CENTER_Y, FLOOR) * extrude(
        RectangleRounded(SLOT_WIDTH, SLOT_DEPTH, INNER_RADIUS),
        amount=POCKET_DEPTH + CUT_OVERRUN,
    )
    result = body - pocket
    mouth = [
        edge for edge in result.edges()
        if isclose(edge.bounding_box().min.Z, HEIGHT, abs_tol=LENGTH_TOL)
        and isclose(edge.bounding_box().max.Z, HEIGHT, abs_tol=LENGTH_TOL)
        and edge.bounding_box().min.X >= -SLOT_WIDTH / 2 - LENGTH_TOL
        and edge.bounding_box().max.X <= SLOT_WIDTH / 2 + LENGTH_TOL
        and edge.bounding_box().min.Y >= FRONT_INNER - LENGTH_TOL
        and edge.bounding_box().max.Y <= REAR_INNER + LENGTH_TOL
    ]
    if len(mouth) != 8:
        raise ValueError("Expected four straight and four rounded slot-mouth edges")
    result = round_edges(mouth)
    for x in PEG_X:
        rear = Plane(origin=(x, REAR_OUTER, PEG_CENTER_Z),
                     x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        result = result + rear * peg(
            across_flats=PEG_ACROSS_FLATS, projection=PEG_PROJECTION,
            root_overlap=JOIN_OVERLAP,
        )
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Cradle did not produce solid geometry")
    result.label = "station_g2_multiboard_holder"
    return result


def check(shape: Solid | Compound) -> None:
    """Check support, insertion sweep, full-width screw relief and snap interfaces."""
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Cradle must be one valid solid")
    solid = shape.solids()[0]
    bounds = shape.bounding_box()
    for actual, expected in zip(
        (*bounds.min, *bounds.max),
        (-WIDTH / 2, FRONT_OUTER, 0, WIDTH / 2,
         REAR_OUTER + PEG_PROJECTION, HEIGHT),
    ):
        if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Unexpected cradle envelope: {bounds}")

    delta = PROBE_OFFSET
    # The union of every device position during a vertical drop is a prism.
    # Extend beyond the holder and above a complete device, not merely its seat.
    body_sweep = _box(
        DEVICE_WIDTH, -DEVICE_THICKNESS / 2, DEVICE_THICKNESS / 2,
        FLOOR + delta, DEVICE_HEIGHT + HEIGHT,
    )
    # Expanded full-width band includes the 5 mm screws AND 1.5 mm clearance.
    # It needs no screw-center/head-diameter assumption within the body silhouette.
    screw_sweep = _box(
        DEVICE_WIDTH, DEVICE_THICKNESS / 2, REAR_INNER - delta,
        FLOOR + delta, DEVICE_HEIGHT + HEIGHT,
    )
    # Probe the actual rounded opening, not a rectangle that crosses its corners.
    opening_sweep = Pos(0, CENTER_Y, FLOOR + delta) * extrude(
        RectangleRounded(SLOT_WIDTH - 2 * delta, SLOT_DEPTH - 2 * delta,
                         INNER_RADIUS - delta),
        amount=DEVICE_HEIGHT + HEIGHT,
    )
    for name, tool in (("12 mm body insertion", body_sweep),
                       ("full-width rear screw insertion", screw_sweep),
                       ("rounded clearance opening", opening_sweep)):
        obstruction = shape & tool
        if obstruction is not None and obstruction.volume > VOLUME_TOL:
            raise ValueError(f"Obstructed {name}")

    # Closed floor supports the entire nominal body, including the center.
    support = _box(DEVICE_WIDTH, -DEVICE_THICKNESS / 2, DEVICE_THICKNESS / 2,
                   delta, FLOOR - 2 * delta)
    missing = support - shape
    if missing is not None and missing.volume > VOLUME_TOL:
        raise ValueError("Continuous device-bearing floor is incomplete")
    for x in (-DEVICE_WIDTH / 2, 0, DEVICE_WIDTH / 2):
        for offset, expected in ((-delta, True), (delta, False)):
            if solid.is_inside((x, 0, FLOOR + offset)) != expected:
                raise ValueError("Floor seat height is incorrect")

    # Straight-wall probes stay clear of intentional top/bottom edge rounds.
    for z in (FLOOR + 1, HEIGHT - EDGE_RADIUS - 1):
        for side in (-1, 1):
            for boundary, inside_before in ((SLOT_WIDTH / 2, False), (WIDTH / 2, True)):
                for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                    if solid.is_inside((side * (boundary + offset), CENTER_Y, z)) != expected:
                        raise ValueError("Side-wall or opening width is incorrect")
        for boundary, inside_before in (
            (FRONT_OUTER, False), (FRONT_INNER, True),
            (REAR_INNER, False), (REAR_OUTER, True),
        ):
            for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                if solid.is_inside((0, boundary + offset, z)) != expected:
                    raise ValueError("Continuous front/rear wall or screw relief is incorrect")

    # Radial probes distinguish R3 outside / R0.5 inside corners from box corners.
    for sx in (-1, 1):
        for sy in (-1, 1):
            for radius, half_x, half_y, inside_before in (
                (OUTSIDE_CORNER_RADIUS, WIDTH / 2, DEPTH / 2, True),
                (INNER_RADIUS, SLOT_WIDTH / 2, SLOT_DEPTH / 2, False),
            ):
                cx = sx * (half_x - radius)
                cy = CENTER_Y + sy * (half_y - radius)
                for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
                    radial = (radius + offset) / sqrt(2)
                    if solid.is_inside((cx + sx * radial, cy + sy * radial,
                                        FLOOR + POCKET_DEPTH / 2)) != expected:
                        raise ValueError("Rounded plan corner radius is incorrect")

    # Cross-sections through straight front edges establish all three R0.6 rounds.
    for cy, cz, dy, dz, inside_before in (
        (FRONT_OUTER + EDGE_RADIUS, EDGE_RADIUS, -1, -1, True),
        (FRONT_OUTER + EDGE_RADIUS, HEIGHT - EDGE_RADIUS, -1, 1, True),
        (FRONT_INNER - EDGE_RADIUS, HEIGHT - EDGE_RADIUS, 1, 1, True),
    ):
        for offset, expected in ((-delta, inside_before), (delta, not inside_before)):
            radial = (EDGE_RADIUS + offset) / sqrt(2)
            if solid.is_inside((0, cy + dy * radial, cz + dz * radial)) != expected:
                raise ValueError("Outside or slot-mouth R0.6 edge round is incorrect")

    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(radians(22.5))
    slab_thickness = 0.1
    for x in PEG_X:
        slab = Pos(x, REAR_OUTER + PEG_PROJECTION / 2, PEG_CENTER_Z) * Box(
            PEG_ACROSS_FLATS + 2, slab_thickness, PEG_ACROSS_FLATS + 2,
        )
        section = shape & slab
        if section is None or section.is_null:
            raise ValueError("A rear snap peg is missing")
        if not isclose(section.volume, peg_area * slab_thickness,
                       rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError("Snap peg does not have the required octagonal section")
        section_bounds = section.bounding_box()
        for actual, expected in zip(section_bounds.size,
                                    (PEG_ACROSS_FLATS, slab_thickness, PEG_ACROSS_FLATS)):
            if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
                raise ValueError("Snap peg dimensions are incorrect")
        if not isclose(section_bounds.min.X, x - PEG_ACROSS_FLATS / 2,
                       rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError("Snap peg spacing is incorrect")
        if not isclose(section_bounds.min.Z, 0, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError("Snap peg must be bottom-aligned")
