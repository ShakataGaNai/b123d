"""Centered interior-floor Multiboard deboss; millimeters, no import geometry."""

from math import isclose
from pathlib import Path

from build123d import Align, Box, Plane, Pos, Text, extrude
from matplotlib import get_data_path
from matplotlib.ft2font import FT2Font

LABEL_DEPTH = 0.2
LABEL_FONT_SIZE = 4.0
LENGTH_TOL = 1e-5  # Numerical CAD/STEP tolerance, not extra engraving depth.


def label_tool(text: str, *, floor_width: float, floor_depth: float,
               floor_height: float, font_size: float = LABEL_FONT_SIZE):
    """Return a 0.2 mm-deep glyph cutter below the inside floor at floor_height.

    Floor dimensions describe a centered, fully flat rectangular support region.
    A 0.25 mm footprint margin is required. Text +X/+Y maps to world +X/+Y,
    with letter tops toward the board (+Y), readable from the front (-Y).
    This flips the former underside text 180 degrees about Y. Use outside builders.
    """
    if not text or font_size <= 0 or floor_height <= LABEL_DEPTH:
        raise ValueError("Label needs text, positive font size and an intact floor")
    font_dir = Path(get_data_path()) / "fonts" / "ttf"
    font_path = font_dir / "DejaVuSans.ttf"
    if not font_path.is_file() or not (font_dir / "LICENSE_DEJAVU").is_file():
        raise ValueError("Bundled matplotlib DejaVuSans font and license are required")
    font = FT2Font(font_path)
    if any(font.get_char_index(ord(char)) == 0 for char in text):
        raise ValueError("Label contains unavailable glyphs")
    glyphs = Text(text, font_size=font_size, font_path=font_path)
    bounds = glyphs.bounding_box()
    if bounds.size.X + 0.5 > floor_width or bounds.size.Y + 0.5 > floor_depth:
        raise ValueError("Actual label glyph bounds do not fit the flat floor")
    glyphs = Pos(-(bounds.min.X + bounds.max.X) / 2,
                 -(bounds.min.Y + bounds.max.Y) / 2, 0) * glyphs
    floor = Plane(origin=(0, 0, floor_height), x_dir=(1, 0, 0), z_dir=(0, 0, 1))
    return extrude(floor * glyphs, amount=-LABEL_DEPTH)


def check_label(shape, text: str, *, floor_width: float, floor_depth: float,
                floor_height: float, font_size: float = LABEL_FONT_SIZE) -> None:
    """Prove exact glyph removal, depth, intact backing and surrounding floor."""
    tool = label_tool(text, floor_width=floor_width, floor_depth=floor_depth,
                      floor_height=floor_height, font_size=font_size)
    bounds = tool.bounding_box()
    # OCCT expands curved-glyph bounds by 1e-7; allow numerical tolerance only.
    if not (isclose(bounds.min.Z, floor_height - LABEL_DEPTH, rel_tol=0, abs_tol=LENGTH_TOL)
            and isclose(bounds.max.Z, floor_height, rel_tol=0, abs_tol=LENGTH_TOL)):
        raise ValueError("Label cutter must span exactly 0.2 mm below the inside floor")
    obstruction = shape & tool
    if obstruction is not None and obstruction.volume > 1e-6:
        raise ValueError("Inside-floor text is not fully debossed")
    # A complete rectangle around the lettering must equal the intended blind
    # cut, not merely a few probes that might miss an overcut or missing glyph.
    region = Box(bounds.size.X + 0.2, bounds.size.Y + 0.2, floor_height,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    intended = region - tool
    missing = intended - shape
    if missing is not None and missing.volume > 1e-6:
        raise ValueError("Label exceeds 0.2 mm depth or breaks through its floor")
    actual = shape & region
    if actual is None or not isclose(actual.volume, intended.volume, abs_tol=1e-6):
        raise ValueError("Label footprint or remaining floor differs from intended deboss")
