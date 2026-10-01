"""Open-top Station G3 case, reconstructed from beanfield's Printables 1855194.

Millimeters; source shell axes, floor at Z=0. See README.md for attribution,
measured interfaces, deliberate simplifications, and unverified physical fit.
Builds analytically without importing the reference STL or requiring network access.
"""

from dataclasses import dataclass
from math import isclose

from build123d import (
    Align, Box, Circle, Compound, Cone, Cylinder, Part, Plane, Pos,
    Rectangle, RectangleRounded, SlotOverall, Solid, extrude,
)

# Keep the measured inner port-wall planes fixed; wall changes grow outward.
INNER_WIDTH = 65.8
INNER_DEPTH = 117.4
WALL = 2.4
HEIGHT = 22.3
OUTER_RADIUS = 4.0
FLOOR_Z = 4.3
BOSS_TOP = 5.3
BOSS_DIAMETER = 7.0
MOUNT_DIAMETER = 2.5
BORE_BOTTOM = 1.5
PIN_SHOULDER_Z = 6.5
PIN_TOP = 7.3
PIN_DIAMETER = 3.5
PIN_TIP_DIAMETER = 1.9
CUT_MARGIN = 0.5
RECESS_LIP = 1.07
LENGTH_TOL = 1e-5
VOLUME_TOL = 1e-6
Z_MIN = (Align.CENTER, Align.CENTER, Align.MIN)

MOUNT_CENTERS = (
    (-29.0, -51.2), (29.0, -51.2),
    (-29.0, -28.2), (29.0, -28.2),
    (-29.0, 53.8), (2.3, 53.8), (29.0, 53.8),
)
SUPPORT_CENTERS = ((0.0, -51.2), (0.0, -28.2), (-18.5, 12.9))
PIN_CENTERS = ((3.9, 12.9), (26.9, 12.9))


@dataclass(frozen=True)
class Opening:
    """u is world Y on X walls and world X on Y walls; z is world Z."""

    name: str
    side: str
    u: float
    z: float
    width: float
    height: float
    profile: str = "rectangle"


# Aperture dimensions are reference clearances, not bare connector dimensions.
# Rectangular cutouts retain the measured bounding opening, including its corners.
OPENINGS = (
    Opening("usb_c_power", "left", -5.7, 8.9, 9.02, 3.02, "slot"),
    Opening("dc5521_power", "left", -17.7, 13.85, 8.02, 8.02, "circle"),
    Opening("power_good_button", "left", 4.3, 8.95, 3.62, 3.52),
    Opening("power_led_1", "left", 8.6, 7.6, 1.02, 2.02),
    Opening("power_led_2", "left", 10.6, 7.6, 1.02, 2.02),
    Opening("power_led_3", "left", 12.6, 7.6, 1.02, 2.02),
    Opening("power_led_4", "left", 14.7, 7.6, 1.02, 2.02),
    Opening("grove_lower", "right", 1.3, 11.4, 12.02, 8.02),
    Opening("grove_upper", "right", 24.3, 11.4, 12.02, 8.02),
    Opening("mcu_side_button", "right", -40.3, 12.55, 7.02, 3.52),
    Opening("usb_c_data", "front", -14.05, 12.8, 9.02, 3.02, "slot"),
    Opening("mcu_button_left", "front", -24.5, 12.55, 7.02, 3.52),
    Opening("mcu_button_right", "front", -3.6, 12.55, 7.02, 3.52),
)
ANTENNA_X = 12.9
ANTENNA_BOTTOM_Z = 15.09
ANTENNA_WIDTH = 6.42

# Conservative rectangular envelopes of the source's flared exterior mouths.
# These stop at the inner lip; they are not enlarged through-holes.
RECESSES = (
    Opening("power_plug_recess", "left", -11.45, 12.625, 26.5, 16.45),
    Opening("power_button_recess", "left", 4.3, 8.95, 4.24, 4.14),
    Opening("grove_lower_recess", "right", 1.3, 11.4, 17.8, 13.8),
    Opening("grove_upper_recess", "right", 24.3, 11.4, 17.8, 13.8),
    Opening("side_button_recess", "right", -40.3, 12.55, 12.8, 9.3),
    Opening("front_controls_recess", "front", -14.05, 12.55, 33.7, 9.3),
)
ANTENNA_RECESS_BOTTOM = 9.8
ANTENNA_RECESS_WIDTH = 20.2


def _wall_plane(side: str, u: float, z: float) -> Plane:
    """Cut from outside left/rear, from inside right/front; local Y is +Z."""
    if side == "left":
        origin = (-INNER_WIDTH / 2 - WALL - CUT_MARGIN, u, z)
    elif side == "right":
        origin = (INNER_WIDTH / 2 - CUT_MARGIN, u, z)
    elif side == "front":
        origin = (u, -INNER_DEPTH / 2 + CUT_MARGIN, z)
    elif side == "rear":
        origin = (u, INNER_DEPTH / 2 + WALL + CUT_MARGIN, z)
    else:
        raise ValueError(f"Unknown case wall: {side}")
    if side in ("left", "right"):
        return Plane(origin=origin, x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    return Plane(origin=origin, x_dir=(1, 0, 0), z_dir=(0, -1, 0))


def _opening_tool(opening: Opening) -> Part:
    if opening.profile == "circle":
        profile = Circle(opening.width / 2)
    elif opening.profile == "slot":
        profile = SlotOverall(opening.width, opening.height)
    else:
        profile = Rectangle(opening.width, opening.height)
    return extrude(_wall_plane(opening.side, opening.u, opening.z) * profile,
                   amount=WALL + 2 * CUT_MARGIN)


def _antenna_tool() -> Part:
    rise = HEIGHT - ANTENNA_BOTTOM_Z + CUT_MARGIN
    plane = _wall_plane("rear", ANTENNA_X, ANTENNA_BOTTOM_Z + rise / 2)
    return extrude(plane * Rectangle(ANTENNA_WIDTH, rise),
                   amount=WALL + 2 * CUT_MARGIN)


def _recess_tool(recess: Opening) -> Part:
    plane = _wall_plane(recess.side, recess.u, recess.z)
    if recess.side in ("right", "front"):
        plane = plane.offset(RECESS_LIP + CUT_MARGIN)
    return extrude(plane * Rectangle(recess.width, recess.height),
                   amount=WALL - RECESS_LIP + CUT_MARGIN)


def _antenna_recess() -> Opening:
    rise = HEIGHT - ANTENNA_RECESS_BOTTOM + CUT_MARGIN
    return Opening("antenna_outer_recess", "rear", ANTENNA_X,
                   ANTENNA_RECESS_BOTTOM + rise / 2, ANTENNA_RECESS_WIDTH, rise)


def _validate_dimensions() -> None:
    if not 0 < RECESS_LIP < WALL < OUTER_RADIUS < min(INNER_WIDTH, INNER_DEPTH) / 2:
        raise ValueError("Wall/corner dimensions cannot form the rounded cavity")
    if HEIGHT < 22.3 or not 0 < BORE_BOTTOM < FLOOR_Z < BOSS_TOP < PIN_TOP < HEIGHT:
        raise ValueError("Height/base dimensions would obstruct the reference stack")
    for opening in OPENINGS:
        if opening.width <= 0 or opening.height <= 0:
            raise ValueError(f"Nonpositive opening dimensions: {opening.name}")
        if opening.z - opening.height / 2 <= FLOOR_Z:
            raise ValueError(f"Opening intersects the functional floor: {opening.name}")
        if opening.z + opening.height / 2 >= HEIGHT:
            raise ValueError(f"Opening intersects the rim: {opening.name}")


def build() -> Compound:
    _validate_dimensions()
    width, depth = INNER_WIDTH + 2 * WALL, INNER_DEPTH + 2 * WALL
    outside = extrude(RectangleRounded(width, depth, OUTER_RADIUS), amount=HEIGHT)
    cavity_profile = Plane.XY.offset(FLOOR_Z) * RectangleRounded(
        INNER_WIDTH, INNER_DEPTH, OUTER_RADIUS - WALL,
    )
    result = outside - extrude(cavity_profile, amount=HEIGHT - FLOOR_Z + CUT_MARGIN)

    for x, y in MOUNT_CENTERS + SUPPORT_CENTERS + PIN_CENTERS:
        result += Pos(x, y, FLOOR_Z - CUT_MARGIN) * Cylinder(
            BOSS_DIAMETER / 2, BOSS_TOP - FLOOR_Z + CUT_MARGIN, align=Z_MIN,
        )
    for x, y in PIN_CENTERS:
        result += Pos(x, y, BOSS_TOP - CUT_MARGIN) * Cylinder(
            PIN_DIAMETER / 2, PIN_SHOULDER_Z - BOSS_TOP + CUT_MARGIN, align=Z_MIN,
        )
        # A conical lead-in lies inside the reference rounded tip envelope.
        result += Pos(x, y, PIN_SHOULDER_Z) * Cone(
            PIN_DIAMETER / 2, PIN_TIP_DIAMETER / 2,
            PIN_TOP - PIN_SHOULDER_Z, align=Z_MIN,
        )
    for x, y in MOUNT_CENTERS:
        result -= Pos(x, y, BORE_BOTTOM) * Cylinder(
            MOUNT_DIAMETER / 2, BOSS_TOP - BORE_BOTTOM + CUT_MARGIN, align=Z_MIN,
        )

    # Preserve the full mouth of the source's underside-component relief.
    # Straight sides remove more material than its source bottom fillet.
    result -= Pos(-21.5, -17.7, 3.0) * Box(15.2, 14.2, FLOOR_Z - 3.0 + CUT_MARGIN,
                                          align=Z_MIN)
    for opening in OPENINGS:
        result -= _opening_tool(opening)
    result -= _antenna_tool()
    for recess in (*RECESSES, _antenna_recess()):
        result -= _recess_tool(recess)
    if not isinstance(result, Compound):
        raise ValueError("Case construction did not produce a solid compound")
    result.label = "station_g3_open_case"
    return result


def check(shape: Compound | Solid) -> None:
    """Functional geometry checks on the native result and imported STEP."""
    _validate_dimensions()
    bounds = shape.bounding_box()
    expected = (INNER_WIDTH + 2 * WALL, INNER_DEPTH + 2 * WALL, HEIGHT)
    for actual, wanted in zip(bounds.size, expected):
        if not isclose(actual, wanted, rel_tol=0, abs_tol=LENGTH_TOL):
            raise ValueError(f"Wrong case envelope: {bounds.size}")
    if not isclose(bounds.min.Z, 0.0, rel_tol=0, abs_tol=LENGTH_TOL):
        raise ValueError("Case does not rest on Z=0")
    solid = shape.solids()[0]

    def material(point: tuple[float, float, float], wanted: bool, feature: str) -> None:
        if solid.is_inside(point) != wanted:
            raise ValueError(f"Incorrect material at {feature}: {point}")

    material((0, 0, FLOOR_Z - 0.05), True, "floor top")
    material((0, 0, FLOOR_Z + 0.05), False, "open cavity")
    material((0, 0, HEIGHT - 0.05), False, "open top")
    for x, y in MOUNT_CENTERS:
        material((x, y, BORE_BOTTOM - 0.05), True, "blind bore floor")
        material((x, y, BORE_BOTTOM + 0.05), False, "blind bore start")
        material((x, y, BOSS_TOP - 0.05), False, "mounting bore mouth")
        material((x + 2.0, y, BOSS_TOP - 0.05), True, "mounting seat")
        material((x + 2.0, y, BOSS_TOP + 0.05), False, "mounting seat height")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for radius, present in ((MOUNT_DIAMETER / 2 - 0.05, False),
                                    (MOUNT_DIAMETER / 2 + 0.05, True)):
                material((x + radius * dx, y + radius * dy, 3.5), present,
                         "mounting bore diameter")
    for x, y in SUPPORT_CENTERS:
        material((x, y, BOSS_TOP - 0.05), True, "PCB support")
        material((x, y, BOSS_TOP + 0.05), False, "PCB support height")
    for x, y in PIN_CENTERS:
        material((x, y, PIN_TOP - 0.05), True, "locator tip")
        material((x + PIN_DIAMETER / 2 + 0.05, y, 6.0), False, "locator diameter")
    material((-21.5, -17.7, 2.95), True, "component relief floor")
    material((-21.5, -17.7, 3.05), False, "component relief cavity")

    for opening in OPENINGS:
        obstruction = shape & _opening_tool(opening)
        if obstruction is not None and obstruction.volume > VOLUME_TOL:
            raise ValueError(f"Blocked {opening.name}: {obstruction.volume} mm^3")
    antenna_obstruction = shape & _antenna_tool()
    if antenna_obstruction is not None and antenna_obstruction.volume > VOLUME_TOL:
        raise ValueError("Antenna insertion slot is obstructed")
    for recess in (*RECESSES, _antenna_recess()):
        obstruction = shape & _recess_tool(recess)
        if obstruction is not None and obstruction.volume > VOLUME_TOL:
            raise ValueError(f"Blocked {recess.name}: {obstruction.volume} mm^3")
    material((INNER_WIDTH / 2 + RECESS_LIP / 2, -6.5, 11.4), True,
             "Grove recess retains its inner lip")
    material((6.0, INNER_DEPTH / 2 + RECESS_LIP / 2, 16.0), True,
             "antenna recess retains its inner lip")
    for point in ((-INNER_WIDTH / 2 - WALL / 2, 45, HEIGHT - 0.5),
                  (INNER_WIDTH / 2 + WALL / 2, 45, HEIGHT - 0.5),
                  (15, -INNER_DEPTH / 2 - WALL / 2, HEIGHT - 0.5),
                  (0, INNER_DEPTH / 2 + WALL / 2, HEIGHT - 0.5)):
        material(point, True, "full-height perimeter wall")
