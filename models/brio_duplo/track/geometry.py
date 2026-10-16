"""Basic wooden-railway track: grooved body and level end connectors.

Flat curves use exact circular sweeps. Grades use a smooth loft through explicitly
oriented sections; check_track bounds section deviation from the ideal route.
No junctions, imported third-party geometry, or physical-fit guarantees.
"""

from math import cos, degrees, isclose, isfinite, radians, sin, sqrt

from build123d import (
    Align, Box, CenterArc, Compound, Cylinder, Edge, Face, Line, Plane, Pos,
    Rectangle, Rot, Solid, Vector, Wire, loft, sweep,
)

from models.brio_duplo import dimensions as d
from models.brio_duplo.track.config import TrackConfig

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
SECTION_TOL = 0.04  # mm: CAD sampling tolerance, not a manufacturing allowance.


def _span(config: TrackConfig) -> float:
    return config.length if config.turn_angle == 0 else config.turn_radius*abs(radians(config.turn_angle))


def _validate(config: TrackConfig) -> None:
    numbers = (config.length, config.turn_radius, config.turn_angle, config.rise, config.end_flat)
    if any(not isfinite(value) for value in numbers):
        raise ValueError("Track dimensions must be finite")
    if config.length <= 0 or config.turn_radius <= d.TRACK_WIDTH/2:
        raise ValueError("Length must be positive; turn radius must exceed half the track width")
    if abs(config.turn_angle) > 180:
        raise ValueError("Basic curve angle must be within -180..180 degrees")
    if len(config.ends) != 2 or any(end not in ("male", "female") for end in config.ends):
        raise ValueError("Track requires two male/female end names")
    if config.end_flat < d.CONNECTOR_CENTER_OFFSET+d.SOCKET_DIAMETER/2+1:
        raise ValueError("Level end pads must contain the complete female pocket")
    if _span(config) < 2*(d.CONNECTOR_CENTER_OFFSET+d.SOCKET_DIAMETER/2)+1:
        raise ValueError("Track is too short for independent end connector pockets")
    if config.rise:
        middle = _span(config)-2*config.end_flat
        if middle <= 0 or 1.5*abs(config.rise)/middle > .5:
            raise ValueError("Grade requires a positive transition and eased maximum slope <= 0.5")


def _route(config: TrackConfig, distance: float) -> tuple[Vector, Vector, Vector]:
    """Ideal bottom-centre position, width direction, section-up direction."""
    span = _span(config)
    base = max(0.0, -config.rise)
    if config.turn_angle:
        sign = 1 if config.turn_angle > 0 else -1
        heading = sign*distance/config.turn_radius
        x = config.turn_radius*sin(distance/config.turn_radius)
        y = sign*config.turn_radius*(1-cos(distance/config.turn_radius))
    else:
        heading, x, y = 0.0, distance, 0.0
    slope, z = 0.0, base
    if config.rise:
        t = max(0.0, min(1.0, (distance-config.end_flat)/(span-2*config.end_flat)))
        z += config.rise*t*t*(3-2*t)
        slope = config.rise*6*t*(1-t)/(span-2*config.end_flat)
    side = Vector(-sin(heading), cos(heading), 0)
    up = Vector(-slope*cos(heading), -slope*sin(heading), 1)/sqrt(1+slope*slope)
    return Vector(x, y, z), side, up


def _level_edge(config: TrackConfig, start: float, end: float) -> Edge:
    if not config.turn_angle:
        return Line(_route(config, start)[0], _route(config, end)[0])
    sign = 1 if config.turn_angle > 0 else -1
    z = _route(config, start)[0].Z
    return Pos(0, 0, z)*CenterArc(
        (0, sign*config.turn_radius), config.turn_radius,
        -sign*90+sign*degrees(start/config.turn_radius),
        sign*degrees((end-start)/config.turn_radius),
    )




def build_track(config: TrackConfig) -> Compound:
    """Return a fresh single solid, start shoulder at X=Y=0 and +X tangent."""
    _validate(config)
    profile = Rectangle(d.TRACK_WIDTH, d.TRACK_HEIGHT, align=(Align.CENTER, Align.MIN))
    for y in (-d.GROOVE_GAUGE/2, d.GROOVE_GAUGE/2):
        profile -= Pos(y, d.GROOVE_FLOOR)*Rectangle(
            d.GROOVE_WIDTH, d.GROOVE_DEPTH+1, align=(Align.CENTER, Align.MIN)
        )
        if config.double_sided:
            profile -= Pos(y, -1)*Rectangle(
                d.GROOVE_WIDTH, d.GROOVE_DEPTH+1, align=(Align.CENTER, Align.MIN)
            )
    faces = profile.faces()
    if len(faces) != 1:
        raise ValueError("Grooved profile must be a single connected face")
    profile_face = faces[0]
    span = _span(config)
    if not config.rise:
        body = sweep(Pos(_route(config, 0)[0])*Plane.YZ*profile_face, Wire(_level_edge(config, 0, span)))
    else:
        start, end = config.end_flat, span-config.end_flat
        count = max(32, int((end-start)/3)+1)
        sections: list[Face] = []
        for i in range(count+1):
            point, side, up = _route(config, start+(end-start)*i/count)
            tangent = side.cross(up)
            sections.append(Plane(origin=point, x_dir=side, z_dir=tangent)*profile_face)
        body = loft(sections)
        for a, b in ((0.0, start), (end, span)):
            point, side, up = _route(config, a)
            section = Plane(origin=point, x_dir=side, z_dir=side.cross(up))*profile_face
            body += sweep(section, Wire(_level_edge(config, a, b)))
    for index, end in enumerate(config.ends):
        point = _route(config, _span(config)*index)[0]
        yaw = (config.turn_angle if index else 180.0)
        placement = Pos(point)*Rot(0, 0, yaw)
        if end == "male":
            neck = Box(d.CONNECTOR_CENTER_OFFSET, d.PEG_NECK_WIDTH, d.TRACK_HEIGHT,
                       align=(Align.MIN, Align.CENTER, Align.MIN))
            head = Pos(d.CONNECTOR_CENTER_OFFSET, 0, 0)*Cylinder(
                d.PEG_DIAMETER/2, d.TRACK_HEIGHT, align=BOTTOM
            )
            body += placement*(neck+head)
        else:
            pocket = Pos(-d.CONNECTOR_CENTER_OFFSET, 0, -1)*Cylinder(
                d.SOCKET_DIAMETER/2, d.TRACK_HEIGHT+2, align=BOTTOM
            )
            throat = Pos(1, 0, -1)*Box(
                d.CONNECTOR_CENTER_OFFSET+1, d.SOCKET_THROAT, d.TRACK_HEIGHT+2,
                align=(Align.MAX, Align.CENTER, Align.MIN),
            )
            body -= placement*(pocket+throat)
    if not isinstance(body, Compound) or len(body.solids()) != 1 or not body.is_valid:
        raise ValueError("Configured track must produce one valid solid")
    body.label = "configured_basic_track"
    return body


def check_track(shape: Compound | Solid, config: TrackConfig) -> None:
    """Check exported interfaces against ideal route and actual solid material."""
    _validate(config)
    if shape.is_null or not shape.is_valid or len(shape.solids()) != 1:
        raise ValueError("Track must be one valid solid")
    bounds = shape.bounding_box()
    if not isclose(bounds.min.Z, 0, abs_tol=1e-4):
        raise ValueError(f"Lowest track endpoint must sit on Z=0: {bounds.min.Z}")
    if not isclose(bounds.max.Z, d.TRACK_HEIGHT+abs(config.rise), abs_tol=1e-4):
        raise ValueError("Track height does not match rise/fall")
    if not config.turn_angle:
        extension = d.CONNECTOR_CENTER_OFFSET+d.PEG_DIAMETER/2
        length = config.length+config.ends.count("male")*extension
        min_x = -extension if config.ends[0] == "male" else 0
        if not isclose(bounds.size.X, length, abs_tol=1e-4) or not isclose(bounds.min.X, min_x, abs_tol=1e-4):
            raise ValueError("Incorrect straight shoulder contribution or peg extension")
    solid = shape.solids()[0]
    tol = SECTION_TOL
    # Avoid the central connector cuts, but sample groove and outside lands along the route.
    for i in range(1, 20):
        point, side, up = _route(config, _span(config)*i/20)
        for y in (-d.GROOVE_GAUGE/2, d.GROOVE_GAUGE/2):
            def material(width: float, height: float) -> bool:
                return solid.is_inside(point+side*width+up*height)
            if material(y, d.GROOVE_FLOOR+tol) or not material(y, d.GROOVE_FLOOR-tol):
                raise ValueError(f"Top groove floor/profile error at station {i}")
            for sign in (-1, 1):
                if material(y+sign*(d.GROOVE_WIDTH/2-tol), 11):
                    raise ValueError(f"Groove too narrow or offset at station {i}")
                if not material(y+sign*(d.GROOVE_WIDTH/2+tol), 11):
                    raise ValueError(f"Groove too wide or offset at station {i}")
            if config.double_sided:
                if material(y, d.GROOVE_DEPTH-tol) or not material(y, d.GROOVE_DEPTH+tol):
                    raise ValueError(f"Bottom groove/web error at station {i}")
                for sign in (-1, 1):
                    if material(y+sign*(d.GROOVE_WIDTH/2-tol), 1) or not material(y+sign*(d.GROOVE_WIDTH/2+tol), 1):
                        raise ValueError(f"Bottom groove width/gauge error at station {i}")
            elif not material(y, tol):
                raise ValueError("Single-sided track underside must remain solid")
        for sign in (-1, 1):
            if not solid.is_inside(point+side*(sign*(d.TRACK_WIDTH/2-tol))+up*6):
                raise ValueError("Body width too small")
            if solid.is_inside(point+side*(sign*(d.TRACK_WIDTH/2+tol))+up*6):
                raise ValueError("Body width too large")
    for index, end in enumerate(config.ends):
        point = _route(config, _span(config)*index)[0]
        yaw = radians(config.turn_angle if index else 180)
        out = Vector(cos(yaw), sin(yaw), 0)
        side = Vector(-sin(yaw), cos(yaw), 0)
        center = point+out*d.CONNECTOR_CENTER_OFFSET*(1 if end == "male" else -1)
        radius = (d.PEG_DIAMETER if end == "male" else d.SOCKET_DIAMETER)/2
        neck_width = d.PEG_NECK_WIDTH if end == "male" else d.SOCKET_THROAT
        neck = point+out*(1 if end == "male" else -1)
        for z in (.1, d.TRACK_HEIGHT/2, d.TRACK_HEIGHT-.1):
            for sign in (-1, 1):
                inner = solid.is_inside(center+side*(sign*(radius-tol))+Vector(0, 0, z))
                outer = solid.is_inside(center+side*(sign*(radius+tol))+Vector(0, 0, z))
                if inner != (end == "male") or outer != (end == "female"):
                    raise ValueError(f"Incorrect {end} circle at endpoint {index}")
                inner = solid.is_inside(neck+side*(sign*(neck_width/2-tol))+Vector(0, 0, z))
                outer = solid.is_inside(neck+side*(sign*(neck_width/2+tol))+Vector(0, 0, z))
                if inner != (end == "male") or outer != (end == "female"):
                    raise ValueError(f"Incorrect {end} neck/throat at endpoint {index}")
