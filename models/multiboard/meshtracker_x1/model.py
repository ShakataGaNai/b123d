"""25 mm top-entry X1 pocket with two snap-mounted octagonal pegs.

Millimeters. XY is the print bed; +Z is up; the rear peg points +Y.
The 0.4 mm per-side pocket clearance is an uncalibrated design allowance.
See README.md for source evidence, supports, and physical-fit limitations.
"""

from math import isclose, sqrt, tan, radians

from build123d import (
    Align, Box, Compound, Plane, Polygon, Pos, Solid, extrude,
)

from models.multiboard.peg import peg
from models.multiboard.finish import EDGE_RADIUS, OUTSIDE_CORNER_RADIUS, rounded_blank, round_edges
from models.multiboard.label import label_tool, check_label

X1_WIDTH = 57.0
X1_THICKNESS = 8.0  # Rounded STL estimate for the lower 22.5 mm, not the whole envelope.
# Measured lower sides: 5 mm inward run over 10 mm vertical rise.
BASE_RUN = 5.0
BASE_RISE = 10.0
FIT_CLEARANCE = 0.4  # Per side; not a measured printing tolerance.
HEIGHT = 25.0
WALL = 2.5
FLOOR = 2.5
ENTRY_FILLET = EDGE_RADIUS
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_CENTERS_X = (-12.5, 12.5)
PEG_CENTER_Z = PEG_ACROSS_FLATS / 2  # Lowest peg flat is flush with Z=0.
JOIN_OVERLAP = 0.8  # Exceeds the bottom round; exposed projection is unchanged.
CUT_OVERRUN = 1.0

SLOT_WIDTH = X1_WIDTH + 2 * FIT_CLEARANCE
SLOT_DEPTH = X1_THICKNESS + 2 * FIT_CLEARANCE
BASE_SLOPE = BASE_RUN / BASE_RISE
BASE_HALF_WIDTH = X1_WIDTH / 2 - BASE_RUN
SLOT_BASE_HALF_WIDTH = BASE_HALF_WIDTH + FIT_CLEARANCE * sqrt(1 + BASE_SLOPE**2)
SLOT_SHOULDER_Z = FLOOR + (SLOT_WIDTH / 2 - SLOT_BASE_HALF_WIDTH) / BASE_SLOPE
WIDTH = SLOT_WIDTH + 2 * WALL
DEPTH = SLOT_DEPTH + 2 * WALL
LENGTH_TOL = 1e-5
VOLUME_TOL = 1e-5


def build() -> Solid | Compound:
    """Fresh single-solid pocket, filleted before adding the unmodified peg."""
    if not (0 < FLOOR < HEIGHT and 0 < ENTRY_FILLET < WALL / 2):
        raise ValueError("Floor and entry fillet must fit within the pocket")
    if FIT_CLEARANCE <= 0:
        raise ValueError("Clearance must be positive")
    if any(abs(x) + PEG_ACROSS_FLATS / 2 >= WIDTH / 2 - OUTSIDE_CORNER_RADIUS
           for x in PEG_CENTERS_X):
        raise ValueError("Both pegs must fit the flat rear wall")
    if PEG_CENTER_Z - PEG_ACROSS_FLATS / 2 < 0:
        raise ValueError("Peg must not extend below the print bed")
    if PEG_CENTER_Z + PEG_ACROSS_FLATS / 2 >= HEIGHT - EDGE_RADIUS:
        raise ValueError("Peg must remain below the rounded top rim")
    if not (0 < JOIN_OVERLAP < WALL and PEG_PROJECTION > 0):
        raise ValueError("Peg overlap must remain inside the rear wall")
    if not (0 < BASE_RUN < X1_WIDTH / 2 and 0 < BASE_RISE):
        raise ValueError("Base slope must leave a positive flat center")
    if not (FLOOR < SLOT_SHOULDER_Z < HEIGHT - ENTRY_FILLET):
        raise ValueError("Angled base must join the straight slot below its entry")

    body = rounded_blank(WIDTH, DEPTH, HEIGHT)

    profile = Polygon(
        (-SLOT_BASE_HALF_WIDTH, FLOOR), (SLOT_BASE_HALF_WIDTH, FLOOR),
        (SLOT_WIDTH / 2, SLOT_SHOULDER_Z),
        (SLOT_WIDTH / 2, HEIGHT + CUT_OVERRUN),
        (-SLOT_WIDTH / 2, HEIGHT + CUT_OVERRUN),
        (-SLOT_WIDTH / 2, SLOT_SHOULDER_Z),
    )
    pocket_plane = Plane(
        origin=(0, SLOT_DEPTH / 2, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0),
    )
    pocket = extrude(pocket_plane * profile, amount=SLOT_DEPTH)
    body = body - pocket
    entrance = [edge for edge in body.edges()
                if isclose(edge.bounding_box().min.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and isclose(edge.bounding_box().max.Z, HEIGHT, abs_tol=LENGTH_TOL)
                and (isclose(abs(edge.center().X), SLOT_WIDTH / 2, abs_tol=LENGTH_TOL)
                     or isclose(abs(edge.center().Y), SLOT_DEPTH / 2, abs_tol=LENGTH_TOL))]
    if len(entrance) != 4:
        raise ValueError("Expected four inner slot-entrance edges")
    body = round_edges(entrance)
    body = body - label_tool("X1", floor_width=2 * SLOT_BASE_HALF_WIDTH,
                             floor_depth=SLOT_DEPTH, floor_height=FLOOR)
    result = body
    for x in PEG_CENTERS_X:
        rear = Plane(
            origin=(x, DEPTH / 2, PEG_CENTER_Z),
            x_dir=(1, 0, 0), z_dir=(0, 1, 0),
        )
        result = result + rear * peg(
            across_flats=PEG_ACROSS_FLATS, projection=PEG_PROJECTION,
            root_overlap=JOIN_OVERLAP,
        )
    if not isinstance(result, (Solid, Compound)):
        raise ValueError("Holder fusion did not produce solid geometry")
    result.label = "meshtracker_x1"
    return result


def check(shape: Compound | Solid) -> None:
    """Angled floor/slot boundaries, open entry and bottom-aligned rear peg."""
    solids = shape.solids()
    if shape.is_null or not shape.is_valid or len(solids) != 1:
        raise ValueError("Holder must be one valid solid")
    solid = solids[0]
    bounds = shape.bounding_box()
    expected_min = (-WIDTH / 2, -DEPTH / 2, 0)
    expected_max = (WIDTH / 2, DEPTH / 2 + PEG_PROJECTION, HEIGHT)
    for observed, expected in zip((*bounds.min, *bounds.max), (*expected_min, *expected_max)):
        if not isclose(observed, expected, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Unexpected holder envelope: {bounds}")

    # Above the shoulder, the full-width slot must stay open to the top.
    insertion = Pos(0, 0, SLOT_SHOULDER_Z + 0.001) * Box(
        SLOT_WIDTH - 0.002, SLOT_DEPTH - 0.002,
        HEIGHT - SLOT_SHOULDER_Z + CUT_OVERRUN,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    obstruction = shape & insertion
    if obstruction is not None and obstruction.volume > VOLUME_TOL:
        raise ValueError("Pocket is obstructed along its top-entry insertion path")

    delta = 0.001
    for z, expected_inside in ((FLOOR - delta, True), (FLOOR + delta, False)):
        if solid.is_inside((SLOT_BASE_HALF_WIDTH - 1, 0, z)) != expected_inside:
            raise ValueError("Pocket floor is not at the specified height")
    for x, y in ((SLOT_WIDTH / 2, 0), (-SLOT_WIDTH / 2, 0),
                 (0, SLOT_DEPTH / 2), (0, -SLOT_DEPTH / 2)):
        for scale, expected_inside in ((1 - delta, False), (1 + delta, True)):
            if solid.is_inside((x * scale, y * scale, HEIGHT / 2)) != expected_inside:
                raise ValueError("Pocket width/depth or straight wall boundary is incorrect")

    # Each measured slope must have supporting material below/outside it.
    # These probes reject the old square-bottom cutout, not just collisions.
    for z in (FLOOR + 2, FLOOR + 5, FLOOR + 8):
        half_width = SLOT_BASE_HALF_WIDTH + BASE_SLOPE * (z - FLOOR)
        for side in (-1, 1):
            for y in (0, -SLOT_DEPTH / 3, SLOT_DEPTH / 3):
                for offset, expected_inside in ((-delta, False), (delta, True)):
                    if solid.is_inside((side * (half_width + offset), y, z)) != expected_inside:
                        raise ValueError("Missing or misplaced angled pocket support")
    if not solid.is_inside((SLOT_WIDTH / 2 - 0.5, 0, FLOOR + 1)):
        raise ValueError("The lower outside corner must support the angled base")

    check_label(shape, "X1", floor_width=2 * SLOT_BASE_HALF_WIDTH,
                floor_depth=SLOT_DEPTH, floor_height=FLOOR)
    # Measure both pegs away from the root, preserving area and diagonal flats.
    peg_y = DEPTH / 2 + PEG_PROJECTION / 2
    slab_thickness = 0.1
    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(radians(22.5))
    diagonal = PEG_ACROSS_FLATS / (2 * sqrt(2))
    for x in PEG_CENTERS_X:
        slab = Pos(x, peg_y, PEG_CENTER_Z) * Box(
            PEG_ACROSS_FLATS + 2, slab_thickness, PEG_ACROSS_FLATS + 2,
        )
        section = shape & slab
        if section is None or section.is_null or len(section.solids()) != 1:
            raise ValueError("Rear peg section is missing")
        if not isclose(section.volume, peg_area * slab_thickness, rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError("Rear peg section does not match the octagon area")
        bounds = section.bounding_box()
        for actual, expected in zip(
            (*bounds.min, *bounds.max),
            (x - PEG_ACROSS_FLATS / 2, peg_y - slab_thickness / 2, 0,
             x + PEG_ACROSS_FLATS / 2, peg_y + slab_thickness / 2, PEG_ACROSS_FLATS),
        ):
            if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOL):
                raise ValueError("Rear peg size, pitch or bottom alignment is incorrect")
        for sx, sz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            for offset, expected_inside in ((-delta, True), (delta, False)):
                point = (x + sx * (diagonal + offset), peg_y,
                         PEG_CENTER_Z + sz * (diagonal + offset))
                if solid.is_inside(point) != expected_inside:
                    raise ValueError("Rear peg diagonal flats are incorrect")
