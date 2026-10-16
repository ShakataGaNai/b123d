"""Light-PCB display shelf: 40 x 30 mm clear deck, 10 mm front lip.

Millimeters, XY bed, +Y toward Multiboard. Open sides; no clamping or load rating.
"""

from math import cos, isclose, pi, radians, sin, tan

from build123d import Align, Box, Compound, Plane, Pos, RectangleRounded, Solid, extrude

from models.multiboard.peg import peg
from models.multiboard.finish import EDGE_RADIUS, OUTSIDE_CORNER_RADIUS, round_edges

WIDTH = 40.0
DEPTH = 30.0  # Usable deck between the front lip and back wall.
THICKNESS = 3.0
LIP_HEIGHT = 10.0  # Above the deck surface.
PEG_ACROSS_FLATS = 13.5
PEG_PROJECTION = 6.5
PEG_PITCH = 25.0
BACK_HEIGHT = max(THICKNESS + LIP_HEIGHT, PEG_ACROSS_FLATS)
JOIN_OVERLAP = 0.8  # Buried root bridges the R0.6 underside round.
LENGTH_TOL = 1e-5  # mm, numerical tolerance, not print fit.
VOLUME_TOL = 1e-5  # mm^3.


def _shelf_body():
    """Round exposed body edges before attaching the functional snap pegs."""
    body = Pos(0, DEPTH / 2, 0) * extrude(
        RectangleRounded(WIDTH, DEPTH + 2 * THICKNESS, OUTSIDE_CORNER_RADIUS),
        amount=BACK_HEIGHT,
    )
    deck_space = Pos(0, 0, THICKNESS) * Box(
        WIDTH + 2, DEPTH, BACK_HEIGHT + 1,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    front_trim = Pos(0, -THICKNESS - 1, THICKNESS + LIP_HEIGHT) * Box(
        WIDTH + 2, THICKNESS + 1, BACK_HEIGHT,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    body = body - deck_space - front_trim
    # Horizontal exposed edges; the two concave deck/wall joints stay square.
    exposed = []
    for edge in body.edges():
        bounds = edge.bounding_box()
        if not isclose(bounds.min.Z, bounds.max.Z, abs_tol=LENGTH_TOL):
            continue
        if (isclose(bounds.min.Z, THICKNESS, abs_tol=LENGTH_TOL)
                and any(isclose(bounds.min.Y, y, abs_tol=LENGTH_TOL)
                        and isclose(bounds.max.Y, y, abs_tol=LENGTH_TOL)
                        for y in (0, DEPTH))):
            continue
        exposed.append(edge)
    if len(exposed) != 18:
        raise ValueError(f"Expected 18 exposed shelf edges, found {len(exposed)}")
    return round_edges(exposed)


def build() -> Solid | Compound:
    """Return a fresh one-piece shelf with two registered snap pegs."""
    if min(WIDTH, DEPTH, THICKNESS, LIP_HEIGHT) <= 0:
        raise ValueError("Shelf dimensions must be positive")
    if not 0 < JOIN_OVERLAP < THICKNESS:
        raise ValueError("Peg root overlap must remain within the back wall")
    if PEG_PITCH + PEG_ACROSS_FLATS > WIDTH or PEG_PITCH <= PEG_ACROSS_FLATS:
        raise ValueError("Two separate pegs must fit within the shelf width")
    body = _shelf_body()
    for x in (-PEG_PITCH / 2, PEG_PITCH / 2):
        rear = Plane(origin=(x, DEPTH + THICKNESS, PEG_ACROSS_FLATS / 2),
                     x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        body = body + rear * peg(root_overlap=JOIN_OVERLAP)
    body.label = "circuit_board_multiboard_shelf"
    return body


def check(shape: Solid | Compound) -> None:
    """Check usable deck, lip height, solid supports and both mating interfaces."""
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Shelf must be one valid solid")
    bounds = shape.bounding_box()
    expected = (-WIDTH / 2, -THICKNESS, 0, WIDTH / 2,
                DEPTH + THICKNESS + PEG_PROJECTION, BACK_HEIGHT)
    for actual, target in zip((*bounds.min, *bounds.max), expected):
        if not isclose(actual, target, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError("Incorrect shelf envelope")

    delta = 0.001
    clear_deck = Pos(0, delta, THICKNESS + delta) * Box(
        WIDTH + 2, DEPTH - 2 * delta, BACK_HEIGHT + 20,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    obstruction = shape & clear_deck
    if obstruction is not None and obstruction.volume > VOLUME_TOL:
        raise ValueError("Usable deck or open sides are obstructed")
    for y, depth, bottom, height in (
        (-THICKNESS, DEPTH + 2 * THICKNESS, 0, THICKNESS),
        (-THICKNESS, THICKNESS, THICKNESS, LIP_HEIGHT),
        (DEPTH, THICKNESS, THICKNESS, BACK_HEIGHT - THICKNESS),
    ):
        core = Pos(0, y + EDGE_RADIUS, bottom + EDGE_RADIUS) * Box(
            WIDTH - 2 * OUTSIDE_CORNER_RADIUS,
            depth - 2 * EDGE_RADIUS, height - 2 * EDGE_RADIUS,
            align=(Align.CENTER, Align.MIN, Align.MIN),
        )
        missing = core - shape
        if missing is not None and missing.volume > VOLUME_TOL:
            raise ValueError("Deck, lip or back wall has missing material")
    solid = shape.solids()[0]
    for z, inside in ((THICKNESS + LIP_HEIGHT - delta, True),
                      (THICKNESS + LIP_HEIGHT + delta, False)):
        if solid.is_inside((0, -THICKNESS / 2, z)) != inside:
            raise ValueError("Front lip is not 10 mm above deck")

    peg_area = 2 * PEG_ACROSS_FLATS**2 * tan(pi / 8)
    for x in (-PEG_PITCH / 2, PEG_PITCH / 2):
        slab = Pos(x, DEPTH + THICKNESS + PEG_PROJECTION / 2,
                   PEG_ACROSS_FLATS / 2) * Box(PEG_ACROSS_FLATS + 1, 0.1,
                                              PEG_ACROSS_FLATS + 1)
        section = shape & slab
        if section is None or not isclose(section.volume, peg_area * 0.1,
                                          rel_tol=0, abs_tol=VOLUME_TOL):
            raise ValueError("Incorrect octagonal peg section")
        for actual, target in zip((*section.bounding_box().min,
                                   *section.bounding_box().size),
                                  (x - PEG_ACROSS_FLATS / 2,
                                   DEPTH + THICKNESS + PEG_PROJECTION / 2 - 0.05,
                                   0, PEG_ACROSS_FLATS, 0.1, PEG_ACROSS_FLATS)):
            if not isclose(actual, target, rel_tol=0, abs_tol=LENGTH_TOL):
                raise ValueError("Incorrect peg position or dimensions")
    # Actual standard-radius boundaries at the front outer corners and lower edge.
    for side in (-1, 1):
        cx = side * (WIDTH / 2 - OUTSIDE_CORNER_RADIUS)
        cy = -THICKNESS + OUTSIDE_CORNER_RADIUS
        for angle in (30, 45, 60):
            for offset, inside in ((-delta, True), (delta, False)):
                r = OUTSIDE_CORNER_RADIUS + offset
                if solid.is_inside((cx + side * r * cos(radians(angle)),
                                    cy - r * sin(radians(angle)), THICKNESS + 2)) != inside:
                    raise ValueError("Outside plan corner is not the standard radius")
    for angle in (30, 45, 60):
        for offset, inside in ((-delta, True), (delta, False)):
            r = EDGE_RADIUS + offset
            if solid.is_inside((0, -THICKNESS + EDGE_RADIUS - r * cos(radians(angle)),
                                EDGE_RADIUS - r * sin(radians(angle)))) != inside:
                raise ValueError("Bottom outside edge is not the standard round")
