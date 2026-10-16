"""Inspection assembly: track, chassis, four wheels, two shafts, four collars.

Hardware solids are smooth clearance envelopes, not printable parts or vendor CAD.
"""

from math import isclose, pi

from build123d import Compound, Cylinder, Pos, Rot, Solid

from models.brio_duplo import dimensions as d
from models.brio_duplo.track.config import TrackConfig
from models.brio_duplo.track.geometry import build_track
from models.brio_duplo.wagon.model import build as chassis_build
from models.brio_duplo.wheel.model import build as wheel_build


def build() -> Compound:
    # Inspection scene deliberately uses the default straight, independent of preset selection.
    config = TrackConfig()
    parts = [Pos(-config.length/2, 0, 0)*build_track(config),
             Pos(0, 0, d.CHASSIS_LIFT) * chassis_build()]
    for x in d.AXLE_X:
        axle = Pos(x, 0, d.ASSEMBLED_AXLE_Z) * Rot(90, 0, 0) * Cylinder(
            d.AXLE_DIAMETER/2, d.AXLE_LENGTH
        )
        axle.label = f"purchased_3mm_shaft_{x}"
        parts.append(axle)
        for sign in (-1, 1):
            outer_y = sign*(d.GROOVE_GAUGE/2+d.WHEEL_TREAD_WIDTH/2)
            wheel = Pos(x, outer_y, d.ASSEMBLED_AXLE_Z) * Rot(sign*90, 0, 0) * wheel_build()
            wheel.label = f"wheel_{x}_{sign}"
            parts.append(wheel)
            collar_y = outer_y+sign*(d.COLLAR_ENDPLAY+d.COLLAR_WIDTH/2)
            collar = Cylinder(d.COLLAR_MAX_DIAMETER/2, d.COLLAR_WIDTH)
            collar -= Cylinder(d.COLLAR_BORE_DIAMETER/2, d.COLLAR_WIDTH+2)
            collar = Pos(x, collar_y, d.ASSEMBLED_AXLE_Z) * Rot(90, 0, 0) * collar
            collar.label = f"purchased_collar_envelope_{x}_{sign}"
            parts.append(collar)
    return Compound(children=parts, label="brio_duplo_trial_assembly")


def check(shape: Compound | Solid) -> None:
    solids = list(shape.solids())
    if len(solids) != 12:
        raise ValueError("Assembly requires track, chassis, 4 wheels, 2 shafts, 4 collars")
    wheel_volume = pi*((d.WHEEL_DIAMETER/2)**2*d.WHEEL_TREAD_WIDTH
                      +(d.WHEEL_HUB_DIAMETER/2)**2*d.WHEEL_HUB_EXTENSION
                      -(d.BORE_DIAMETER/2)**2*(d.WHEEL_TREAD_WIDTH+d.WHEEL_HUB_EXTENSION))
    wheels = [s for s in solids if isclose(s.volume, wheel_volume, rel_tol=1e-7)]
    if len(wheels) != 4:
        raise ValueError("Assembly wheel geometry/count incorrect")
    expected_centers = {(x, sign*(d.GROOVE_GAUGE/2-.5*d.WHEEL_HUB_EXTENSION))
                        for x in d.AXLE_X for sign in (-1, 1)}
    for wheel in wheels:
        bounds = wheel.bounding_box()
        center = (round((bounds.min.X+bounds.max.X)/2, 5),
                  round((bounds.min.Y+bounds.max.Y)/2, 5))
        if center not in expected_centers:
            raise ValueError(f"Wheel misaligned or duplicated: {center}")
        expected_centers.remove(center)
        if not isclose(bounds.min.Z, d.GROOVE_FLOOR, abs_tol=1e-5):
            raise ValueError("Wheel does not contact groove floor")
    # Check material intersections, including wheels under the studded deck.
    for index, first in enumerate(solids):
        for second in solids[index+1:]:
            common = first & second
            if common is not None and common.volume > 1e-6:
                raise ValueError(f"Assembly interference: {common.volume} mm^3")
    tread_side_gap = (d.GROOVE_WIDTH-d.WHEEL_TREAD_WIDTH)/2
    hub_gap = d.GROOVE_GAUGE/2-d.WHEEL_TREAD_WIDTH/2-d.WHEEL_HUB_EXTENSION-d.KEEL_WIDTH/2
    deck_gap = d.CHASSIS_LIFT+d.KEEL_HEIGHT-(d.ASSEMBLED_AXLE_Z+d.WHEEL_DIAMETER/2)
    if tread_side_gap < 1 or hub_gap < 1 or deck_gap < 1:
        raise ValueError("Insufficient nominal tread, hub or deck clearance")
    if d.CHASSIS_LIFT-d.TRACK_HEIGHT < 2:
        raise ValueError("Chassis underside too close to track lands")
    if d.AXLE_LENGTH/2 < d.GROOVE_GAUGE/2+d.WHEEL_TREAD_WIDTH/2+d.COLLAR_ENDPLAY+d.COLLAR_WIDTH:
        raise ValueError("Axles do not span collars")
