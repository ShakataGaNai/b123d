"""Trial-fit screw-on L bracket for CooptryPoul ASIN B0D8BB46Y6.

Millimeters; assembly frame, pole axis +Z. Panel extends back beside pole.
See linked research: 5 TPI, handedness and 40 mm collar are assumptions.
"""

from math import cos, isclose, pi, sin

from build123d import Align, Box, Compound, Cone, Cylinder, GeomType, Pos, Solid

from models.pole_l_bracket.thread import MAJOR_DIAMETER, MINOR_RADIUS, PITCH, thread_envelope

PANEL_WIDTH = 20.0
PANEL_HEIGHT = 50.0
PANEL_THICKNESS = 2.0
PANEL_INNER_X = 25.0
ASSUMED_COLLAR_DIAMETER = 40.0
SOCKET_DIAMETER = 30.0
SOCKET_DEPTH = 22.0
CAP_THICKNESS = 4.0
ARM_THICKNESS = 4.0
ARM_START_X = 10.0
RADIAL_THREAD_ALLOWANCE = 0.25
AXIAL_FLANK_ALLOWANCE = 0.15
ROOT_RELIEF = 0.254
ENTRY_LENGTH = 1.5
ENTRY_RADIAL_RELIEF = 0.6

CAP_BOTTOM = PANEL_HEIGHT - CAP_THICKNESS
MOUTH_Z = CAP_BOTTOM - SOCKET_DEPTH
BORE_RADIUS = MINOR_RADIUS + RADIAL_THREAD_ALLOWANCE
GROOVE_RADIUS = MAJOR_DIAMETER / 2 + RADIAL_THREAD_ALLOWANCE + ROOT_RELIEF
LENGTH_TOLERANCE = 1e-5  # mm; geometric/STEP numerical tolerance, not print fit.
VOLUME_TOLERANCE = 1e-5  # mm^3
CENTERED_FOOT = (Align.CENTER, Align.CENTER, Align.MIN)


def build() -> Compound:
    """Fresh one-piece bracket; the socket mouth faces the pole, toward −Z."""
    if PANEL_INNER_X <= ASSUMED_COLLAR_DIAMETER / 2:
        raise ValueError("Panel intersects the assumed collar envelope")
    if GROOVE_RADIUS + ENTRY_RADIAL_RELIEF >= SOCKET_DIAMETER / 2:
        raise ValueError("Thread entry breaks through the socket wall")
    if not 0 < ARM_START_X < SOCKET_DIAMETER / 2 < PANEL_INNER_X:
        raise ValueError("Offset arm must overlap the socket and reach the panel")
    body = Pos(0, 0, MOUTH_Z) * Cylinder(
        SOCKET_DIAMETER / 2, SOCKET_DEPTH + CAP_THICKNESS, align=CENTERED_FOOT
    )
    cavity = thread_envelope(
        MOUTH_Z, SOCKET_DEPTH,
        RADIAL_THREAD_ALLOWANCE, AXIAL_FLANK_ALLOWANCE, ROOT_RELIEF,
    )
    entry = Pos(0, 0, MOUTH_Z) * Cone(
        GROOVE_RADIUS + ENTRY_RADIAL_RELIEF, BORE_RADIUS,
        ENTRY_LENGTH, align=CENTERED_FOOT,
    )
    socket = body - cavity - entry
    panel = Pos(PANEL_INNER_X, 0, 0) * Box(
        PANEL_THICKNESS, PANEL_WIDTH, PANEL_HEIGHT,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    )
    arm = Pos(ARM_START_X, 0, PANEL_HEIGHT - ARM_THICKNESS) * Box(
        PANEL_INNER_X + PANEL_THICKNESS - ARM_START_X,
        PANEL_WIDTH, ARM_THICKNESS,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    )
    bracket = socket + arm + panel
    if not isinstance(bracket, Compound):
        raise ValueError("Bracket construction did not produce a compound of solids")
    bracket.label = "pole_l_bracket"
    return bracket


def check(shape: Compound | Solid) -> None:
    """Measure actual features on native BREP and the saved/reimported STEP."""
    solids = shape.solids()
    if len(solids) != 1:
        raise ValueError("Socket, arm and panel must form one solid")
    solid = solids[0]
    bounds = shape.bounding_box()
    expected_min = (-SOCKET_DIAMETER / 2, -SOCKET_DIAMETER / 2, 0)
    expected_max = (PANEL_INNER_X + PANEL_THICKNESS, SOCKET_DIAMETER / 2, PANEL_HEIGHT)
    for actual, expected in zip((*bounds.min, *bounds.max), (*expected_min, *expected_max)):
        if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOLERANCE):
            raise ValueError(f"Unexpected bracket envelope: {bounds}")

    # Full uninterrupted exterior face, not merely an overall bounding box.
    faces = [face for face in shape.faces() if face.geom_type == GeomType.PLANE
             and face.normal_at().X > 0.999
             and isclose(face.center().X, expected_max[0], abs_tol=LENGTH_TOLERANCE)]
    if len(faces) != 1:
        raise ValueError("Panel must have one plain exterior face")
    face = faces[0]
    for actual, expected in zip(face.bounding_box().size, (0, PANEL_WIDTH, PANEL_HEIGHT)):
        if not isclose(actual, expected, rel_tol=0, abs_tol=LENGTH_TOLERANCE):
            raise ValueError("Panel face is not 20 × 50 mm")
    if not isclose(face.area, PANEL_WIDTH * PANEL_HEIGHT, rel_tol=0, abs_tol=1e-4):
        raise ValueError("Panel exterior is not an uninterrupted rectangle")
    gauge = Pos(PANEL_INNER_X - 1, 0, 2) * Box(
        PANEL_THICKNESS + 2, PANEL_WIDTH, 40,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    )
    measured_panel = shape & gauge
    if measured_panel is None:
        raise ValueError("Missing panel material")
    if not isclose(measured_panel.volume, PANEL_THICKNESS * PANEL_WIDTH * 40,
                   rel_tol=0, abs_tol=VOLUME_TOLERANCE):
        raise ValueError("Panel thickness is not 2 mm throughout the free panel")

    # Blind bore and continuous cap; its thickness is independent of thread detail.
    cap_gauge = Pos(0, 0, CAP_BOTTOM) * Cylinder(BORE_RADIUS, CAP_THICKNESS, align=CENTERED_FOOT)
    measured_cap = shape & cap_gauge
    if measured_cap is None or not isclose(measured_cap.volume, cap_gauge.volume,
                   rel_tol=0, abs_tol=VOLUME_TOLERANCE):
        raise ValueError("Blind socket cap is not a solid 4 mm roof")
    for z in (MOUTH_Z + 0.2, CAP_BOTTOM - 0.2):
        if solid.is_inside((0, 0, z)):
            raise ValueError("Socket bore is blocked or shorter than 22 mm")

    # Exclude intentional shoulder seating at mouth Z; clear the assumed collar.
    collar = Cylinder(ASSUMED_COLLAR_DIAMETER / 2, MOUTH_Z - 0.1, align=CENTERED_FOOT)
    interference = shape & collar
    if interference is not None and interference.volume > VOLUME_TOLERANCE:
        raise ValueError("Bracket intersects the assumed 40 mm collar keep-out")
    if not isclose(measured_panel.distance_to(collar),
                   PANEL_INNER_X - ASSUMED_COLLAR_DIAMETER / 2,
                   rel_tol=0, abs_tol=LENGTH_TOLERANCE):
        raise ValueError("Panel-to-assumed-collar radial gap is not 5 mm")

    # At +X a groove repeats every 5.08 mm; half-pitch locations are lands.
    probe_radius = (BORE_RADIUS + GROOVE_RADIUS) / 2
    for turn in (1, 2, 3):
        z = MOUTH_Z + turn * PITCH
        if solid.is_inside((probe_radius, 0, z)):
            raise ValueError(f"Missing helical groove at Z={z}")
        if not solid.is_inside((probe_radius, 0, z + PITCH / 2)):
            raise ValueError(f"Missing thread land at Z={z + PITCH / 2}")
    for angle in range(0, 360, 45):
        a = angle * pi / 180
        if not solid.is_inside((BORE_RADIUS * cos(a), BORE_RADIUS * sin(a), CAP_BOTTOM + 1)):
            raise ValueError("Socket cap is discontinuous")
        if not solid.is_inside((14.5 * cos(a), 14.5 * sin(a), MOUTH_Z + 4)):
            raise ValueError("Socket outer wall is discontinuous")
