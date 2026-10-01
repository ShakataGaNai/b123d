"""Basic 3/4–5 ACME envelope; no claim of a certified thread tolerance class.

Profile: 29-degree included flank angle, pitch/2 basic radial depth.
Crest flat derived from half-pitch tooth width at the pitch cylinder.
"""

from math import radians, tan

from build123d import Align, Compound, Cylinder, Helix, Plane, Polygon, Pos, sweep

MAJOR_DIAMETER = 19.05
PITCH = 25.4 / 5
HALF_ANGLE = 14.5
BASIC_DEPTH = PITCH / 2
CREST_FLAT = PITCH / 2 - BASIC_DEPTH * tan(radians(HALF_ANGLE))
MINOR_RADIUS = MAJOR_DIAMETER / 2 - BASIC_DEPTH


def thread_envelope(
    bottom: float,
    length: float,
    radial_allowance: float = 0.0,
    axial_allowance: float = 0.0,
    root_relief: float = 0.0,
) -> Compound:
    """Male basic envelope, or enlarged female cutting tool, on world +Z.

    Extend a radial/axial trapezoid helix beyond both ends, then trim.
    At +X, tooth centers occur at bottom+n*PITCH. Frenet transport keeps
    the radial/axial section clocked along this cylindrical helix.
    """
    if length <= 0 or min(radial_allowance, axial_allowance, root_relief) < 0:
        raise ValueError("Thread length must be positive and allowances nonnegative")
    slope = tan(radians(HALF_ANGLE))
    inner = MINOR_RADIUS + radial_allowance
    crest = MAJOR_DIAMETER / 2 + radial_allowance
    outer = crest + root_relief
    overlap = 0.1  # Boolean overlap only, not a fit allowance.
    low = inner - overlap
    high_half = CREST_FLAT / 2 + axial_allowance - root_relief * slope
    low_half = CREST_FLAT / 2 + axial_allowance + (crest - low) * slope
    if high_half <= 0 or 2 * low_half >= PITCH:
        raise ValueError("Thread profile has no crest or overlaps adjacent turns")
    start = bottom - PITCH
    path_radius = (inner + crest) / 2
    path = Helix(PITCH, length + 2 * PITCH, path_radius, center=(0, 0, start))
    profile = Plane(origin=(0, 0, start), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * Polygon(
        (low, -low_half), (outer, -high_half),
        (outer, high_half), (low, low_half),
        align=(Align.NONE, Align.NONE),
    )
    ridge = sweep(profile, path=path, is_frenet=True)
    clip = Pos(0, 0, bottom) * Cylinder(
        outer + 1, length, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    core = Pos(0, 0, bottom) * Cylinder(
        inner, length, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    envelope = (core + ridge) & clip
    if not isinstance(envelope, Compound) or len(envelope.solids()) != 1:
        raise ValueError("Thread sweep must produce one solid envelope")
    return envelope
