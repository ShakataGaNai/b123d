"""Shared millimeter geometry; pipe axis +Z, all factory operations outside builders."""
from math import sqrt
from build123d import Align, Box, Cylinder, Cone, Pos, Rot, Plane, Polygon, extrude, loft, Rectangle

INSERT_D = 20.90
PIPE_OD = 26.67
WEB = 4.0
PLATE = 3.0
BORE = 18.30
SLEEVE = 24.0
PILOT = 3.4
A = (Align.CENTER, Align.CENTER, Align.MIN)

def cross(length):
    """Cross from z=0 to length with a 1 mm tapered entry at z=0."""
    if length <= 1:
        raise ValueError("Cross length must exceed the 1 mm entry taper")
    bars = Box(INSERT_D, WEB, length, align=A) + Box(WEB, INSERT_D, length, align=A)
    envelope = Cone(INSERT_D/2-0.6, INSERT_D/2, 1, align=A)
    envelope += Pos(0,0,1)*Cylinder(INSERT_D/2,length-1,align=A)
    return bars & envelope

def plate(z):
    return Pos(0,0,z)*Cylinder(PIPE_OD/2,PLATE,align=A)

def make(kind):
    if kind not in ('coupler', 'stake', 'laser_mount'):
        raise ValueError(kind)
    length = 12.7 if kind == 'coupler' else 25.4
    body = cross(length) + plate(length)
    top = length + PLATE
    if kind == 'coupler':
        body += Pos(0,0,top+length)*Rot(180,0,0)*cross(length)
    elif kind == 'stake':
        # Two tapered blades retain a cross section down to a short blunt tip.
        for angle in (0,90):
            blade = loft([Pos(0,0,top)*Rectangle(20.9,4),
                          Pos(0,0,top+90)*Rectangle(14,4),
                          Pos(0,0,top+120)*Rectangle(1.2,1.2)], ruled=True)
            body += Rot(0,0,angle)*blade
    else:
        r = BORE/2
        center = top + r + 2.5
        # Circular outside dome plus a solid plinth connecting it to the stop.
        body += Pos(0,0,top)*Box(24,SLEEVE,center-top,align=A)
        body += Pos(0,0,center)*Rot(90,0,0)*Cylinder(12,SLEEVE)
        # Tangent 45-degree roof relief leaves the lower 270 degrees circular.
        bore = Pos(0,0,center)*Rot(90,0,0)*Cylinder(r,SLEEVE+2)
        t = r/sqrt(2)
        roof = Plane.XZ * Polygon((-t,center+t),(0,center+r*sqrt(2)),(t,center+t),align=None)
        bore += extrude(roof,amount=SLEEVE/2+1,both=True)
        # Enclose peak with a roof above the otherwise round dome.
        outer = Plane.XZ * Polygon((-10,center+6),(0,center+16),(10,center+6),align=None)
        body += extrude(outer,amount=SLEEVE/2,both=True)
        body -= bore
        # Vertical roof pilots press the barrel down into its circular seat.
        for y in (-6,6):
            body -= Pos(0,y,center+12)*Cylinder(PILOT/2,12)
        # Trim projecting sleeve corners to the stop plate's circular footprint.
        body &= Cylinder(PIPE_OD/2, center+17, align=A)
    return body

def verify(shape,kind):
    assert shape.is_valid and len(shape.solids()) == 1
    length = 12.7 if kind == 'coupler' else 25.4
    height = 28.4 if kind == 'coupler' else (148.4 if kind == 'stake' else 56.05)
    bb=shape.bounding_box()
    assert abs(bb.min.Z)<1e-5 and abs(bb.size.Z-height)<1e-4, bb
    # Check the insert's actual material at a mid-depth slice and pipe clearance.
    sample = shape & Pos(0,0,5)*Box(40,40,0.2,align=A)
    expected = Pos(0,0,5)*( (Box(INSERT_D,WEB,.2,align=A)+Box(WEB,INSERT_D,.2,align=A)) & Cylinder(INSERT_D/2,.2,align=A))
    assert abs(sample.volume-expected.volume)<1e-5
    assert abs(sample.bounding_box().size.X-INSERT_D)<1e-4
    if kind == 'laser_mount':
        outside = shape - Cylinder(PIPE_OD/2, height+1, align=A)
        assert outside is None or outside.volume < 1e-5
        center=length+PLATE+BORE/2+2.5
        laser=Pos(0,0,center)*Rot(90,0,0)*Cylinder(9,SLEEVE+2)
        overlap = shape & laser
        assert overlap is None or overlap.volume<1e-5
        for y in (-6,6):
            pilot=Pos(0,y,center+12)*Cylinder(PILOT/2-.01,12)
            overlap = shape & pilot
            assert overlap is None or overlap.volume<1e-5
        # Side walls are intact at both previous pilot arrangements.
        for x in (-11,11):
            for y in (-6,0,6):
                assert shape.is_inside((x,y,center))
        assert shape.is_inside((0,0,length+PLATE+1))
