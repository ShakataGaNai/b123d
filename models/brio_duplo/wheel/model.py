"""Print four copies flat; circular treads run inside the wooden-track grooves."""

from math import isclose, pi

from build123d import Align, Compound, Cylinder, Pos, Solid

from models.brio_duplo import dimensions as d

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)


def build() -> Compound:
    wheel = Cylinder(d.WHEEL_DIAMETER/2, d.WHEEL_TREAD_WIDTH, align=BOTTOM)
    wheel += Pos(0, 0, d.WHEEL_TREAD_WIDTH) * Cylinder(
        d.WHEEL_HUB_DIAMETER/2, d.WHEEL_HUB_EXTENSION, align=BOTTOM
    )
    wheel -= Pos(0, 0, -1) * Cylinder(
        d.BORE_DIAMETER/2, d.WHEEL_TREAD_WIDTH+d.WHEEL_HUB_EXTENSION+2, align=BOTTOM
    )
    wheel.label = "wagon_wheel"
    return wheel


def check(shape: Compound | Solid) -> None:
    height = d.WHEEL_TREAD_WIDTH+d.WHEEL_HUB_EXTENSION
    bounds = shape.bounding_box()
    if any(not isclose(a, b, abs_tol=1e-5) for a, b in zip(
        bounds.size, (d.WHEEL_DIAMETER, d.WHEEL_DIAMETER, height)
    )) or not isclose(bounds.min.Z, 0, abs_tol=1e-5):
        raise ValueError("Incorrect wheel print envelope")
    expected = pi * (d.WHEEL_DIAMETER/2)**2 * d.WHEEL_TREAD_WIDTH
    expected += pi * (d.WHEEL_HUB_DIAMETER/2)**2 * d.WHEEL_HUB_EXTENSION
    expected -= pi * (d.BORE_DIAMETER/2)**2 * height
    if not isclose(shape.volume, expected, rel_tol=1e-7):
        raise ValueError("Wheel tread, hub or bore volume incorrect")
    solid = shape.solids()[0]
    for z in (.1, d.WHEEL_TREAD_WIDTH/2, height-.1):
        for sign in (-1, 1):
            if solid.is_inside((sign*(d.BORE_DIAMETER/2-.02), 0, z)):
                raise ValueError("Wheel bore missing or too small")
            if not solid.is_inside((sign*(d.BORE_DIAMETER/2+.02), 0, z)):
                raise ValueError("Wheel bore too large")
    if solid.is_inside((d.WHEEL_HUB_DIAMETER/2+.02, 0, height-.1)):
        raise ValueError("Hub too wide")
