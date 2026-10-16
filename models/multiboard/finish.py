"""Shared Multiboard holder finish; millimeters, no import-time geometry.

R3 outside plan corners and R0.6 exposed edges. Apply before adding mating pegs.
Functional cavity profiles, flat support datums and snap interfaces are separate.
"""

from math import isclose

from build123d import RectangleRounded, extrude, fillet

OUTSIDE_CORNER_RADIUS = 3.0
EDGE_RADIUS = 0.6
LENGTH_TOL = 1e-5


def rounded_blank(width: float, depth: float, height: float):
    """Fresh centered-XY blank, bottom Z=0, R3 corners and R0.6 top/bottom.

    Construct outside active builders. Cut functional cavities afterward, round
    their exposed cutout edges explicitly, then add the unchanged mating pegs.
    """
    if min(width, depth) <= 2 * OUTSIDE_CORNER_RADIUS or height <= 2 * EDGE_RADIUS:
        raise ValueError("Blank is too small for the standard outside rounds")
    body = extrude(RectangleRounded(width, depth, OUTSIDE_CORNER_RADIUS), amount=height)
    perimeter = [edge for edge in body.edges()
                 if any(isclose(edge.bounding_box().min.Z, z, abs_tol=LENGTH_TOL)
                        and isclose(edge.bounding_box().max.Z, z, abs_tol=LENGTH_TOL)
                        for z in (0.0, height))]
    if len(perimeter) != 16:
        raise ValueError("Expected eight top and eight bottom perimeter edges")
    return fillet(perimeter, radius=EDGE_RADIUS)


def round_edges(edges):
    """Round an explicit nonempty set of current-shape exposed edges by R0.6.

    The caller selects and validates edges; never include peg mating edges or
    silently omit failed rounds. Return the containing modified shape.
    """
    selected = list(edges)
    if not selected:
        raise ValueError("Expected exposed edges for the standard round")
    return fillet(selected, radius=EDGE_RADIUS)
