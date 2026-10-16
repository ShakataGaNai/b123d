"""Single-body 2×4 DUPLO trial-fit wagon chassis; print studs up with supports."""

from math import isclose, pi

from build123d import Align, Box, Compound, Cone, Cylinder, Pos, Rot, Solid

from models.brio_duplo import dimensions as d

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)


def build() -> Compound:
    body = Box(d.DECK_LENGTH, d.KEEL_WIDTH, d.KEEL_HEIGHT, align=BOTTOM)
    body += Pos(0, 0, d.KEEL_HEIGHT) * Box(
        d.DECK_LENGTH, d.DECK_WIDTH, d.DECK_THICKNESS, align=BOTTOM
    )
    radius = d.STUD_DIAMETER / 2
    for x in d.STUD_X:
        for y in d.STUD_Y:
            body += Pos(x, y, d.DECK_TOP) * Cylinder(
                radius, d.STUD_HEIGHT - d.STUD_LEAD_IN, align=BOTTOM
            )
            body += Pos(x, y, d.DECK_TOP + d.STUD_HEIGHT - d.STUD_LEAD_IN) * Cone(
                radius, radius - d.STUD_LEAD_IN, d.STUD_LEAD_IN, align=BOTTOM
            )
    for x in d.AXLE_X:
        body -= Pos(x, 0, d.AXLE_Z) * Rot(90, 0, 0) * Cylinder(
            d.BORE_DIAMETER / 2, d.KEEL_WIDTH + 2
        )
    body.label = "duplo_wagon_chassis"
    return body


def check(shape: Compound | Solid) -> None:
    bounds = shape.bounding_box()
    expected = (d.DECK_LENGTH, d.DECK_WIDTH, d.DECK_TOP + d.STUD_HEIGHT)
    if any(not isclose(a, b, abs_tol=1e-5) for a, b in zip(bounds.size, expected)):
        raise ValueError(f"Incorrect chassis envelope: {bounds.size}")
    if not isclose(bounds.min.Z, 0, abs_tol=1e-5):
        raise ValueError("Chassis must sit at Z=0")
    r = d.STUD_DIAMETER / 2
    top_r = r - d.STUD_LEAD_IN
    stud_volume = pi * r*r * (d.STUD_HEIGHT - d.STUD_LEAD_IN)
    stud_volume += pi * d.STUD_LEAD_IN / 3 * (r*r + r*top_r + top_r*top_r)
    expected_volume = d.DECK_LENGTH * d.KEEL_WIDTH * d.KEEL_HEIGHT
    expected_volume += d.DECK_LENGTH * d.DECK_WIDTH * d.DECK_THICKNESS
    expected_volume += len(d.STUD_X) * len(d.STUD_Y) * stud_volume
    expected_volume -= len(d.AXLE_X) * pi * (d.BORE_DIAMETER/2)**2 * d.KEEL_WIDTH
    if not isclose(shape.volume, expected_volume, rel_tol=1e-7):
        raise ValueError("Chassis volume disagrees with deck, studs and axle bores")
    solid = shape.solids()[0]
    for x in d.STUD_X:
        for y in d.STUD_Y:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                z = d.DECK_TOP + 2
                if not solid.is_inside((x + dx*(r-.02), y + dy*(r-.02), z)):
                    raise ValueError("Stud location or diameter too small")
                if solid.is_inside((x + dx*(r+.02), y + dy*(r+.02), z)):
                    raise ValueError("Stud diameter too large")
            if solid.is_inside((x + top_r+.02, y, d.DECK_TOP+d.STUD_HEIGHT-.01)):
                raise ValueError("Missing stud insertion lead-in")
    for x in d.AXLE_X:
        for y in (-d.KEEL_WIDTH/2+.1, 0, d.KEEL_WIDTH/2-.1):
            for sign in (-1, 1):
                if solid.is_inside((x, y, d.AXLE_Z + sign*(d.BORE_DIAMETER/2-.02))):
                    raise ValueError("Axle bore missing, offset or too small")
                if not solid.is_inside((x, y, d.AXLE_Z + sign*(d.BORE_DIAMETER/2+.02))):
                    raise ValueError("Axle bore too large or insufficient bearing wall")
