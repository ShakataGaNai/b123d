"""Parametric Wi-Fi QR plaque. Sample credentials are public, not secrets.

The QR pattern excludes an encoded quiet border; surrounding plate margins
provide the light background. Matrix rows run toward decreasing world Y.
Print black relief on a light grey base; monochrome relief is not reliable.
"""

from dataclasses import dataclass, fields
from itertools import groupby
from math import isclose, isfinite, pi
from pathlib import Path

from build123d import Compound, Plane, SkipClean, Solid, Text
from matplotlib import get_data_path
from matplotlib.ft2font import FT2Font
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.exceptions import DataOverflowError


@dataclass(frozen=True)
class Parameters:
    plate_width: float = 70.0
    plate_height: float = 80.0
    base_thickness: float = 5.0
    qr_size: float = 60.0
    qr_top_margin: float = 5.0
    relief_height: float = 1.0
    qr_run_gap: float = 0.02
    magnet_diameter: float = 10.0
    magnet_depth: float = 3.0
    magnet_diametral_clearance: float = 0.2
    magnet_depth_clearance: float = 0.1
    magnet_edge_inset: float = 9.0
    text_height: float = 4.5
    ssid: str = "WorkshopWiFi"
    password: str = "SamplePass123!"
    auth: str = "WPA"
    hidden: bool = False


_TEXT_MARGIN = 0.25


def wifi_payload(params: Parameters) -> str:
    """Return the standard WIFI payload, escaping reserved field characters."""
    if params.auth not in ("WPA", "WEP", "nopass"):
        raise ValueError("auth must be WPA, WEP, or nopass")
    if not isinstance(params.hidden, bool):
        raise ValueError("hidden must be a bool")
    for name in ("ssid", "password"):
        value = getattr(params, name)
        if not isinstance(value, str) or any(not char.isprintable() for char in value):
            raise ValueError(f"{name} must contain only printable characters")
    if not params.ssid:
        raise ValueError("ssid must not be empty")
    if params.auth != "nopass" and not params.password:
        raise ValueError("A secured Wi-Fi network requires a password")
    if params.auth == "nopass" and params.password:
        raise ValueError("An open network must use an empty password")

    def escape(value: str) -> str:
        return "".join("\\" + char if char in '\\;,:"' else char for char in value)

    return (
        f"WIFI:T:{params.auth};S:{escape(params.ssid)};"
        f"P:{escape(params.password)};H:{str(params.hidden).lower()};;"
    )


def qr_matrix(params: Parameters) -> list[list[bool]]:
    """Encode the symbol only, with auto version and error correction M."""
    qr = QRCode(version=None, error_correction=ERROR_CORRECT_M, border=0)
    qr.add_data(wifi_payload(params))
    try:
        qr.make(fit=True)
    except DataOverflowError as exc:
        raise ValueError("Wi-Fi payload exceeds QR capacity") from exc
    return [[bool(module) for module in row] for row in qr.get_matrix()]


def _validate(params: Parameters) -> None:
    clearances = {"magnet_diametral_clearance", "magnet_depth_clearance"}
    for field in fields(params):
        if field.name in {"ssid", "password", "auth", "hidden"}:
            continue
        value = getattr(params, field.name)
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not isfinite(value):
            raise ValueError(f"{field.name} must be a finite number")
        if value < 0 or (value == 0 and field.name not in clearances):
            raise ValueError(f"{field.name} must be {'nonnegative' if field.name in clearances else 'positive'}")
    wifi_payload(params)
    if params.qr_size >= params.plate_width:
        raise ValueError("QR field must fit inside the plate with positive side margins")
    band = params.plate_height - params.qr_top_margin - params.qr_size
    if band <= 2 * _TEXT_MARGIN:
        raise ValueError("QR field must leave a lower text band with 0.25 mm edge clearances")
    radius = (params.magnet_diameter + params.magnet_diametral_clearance) / 2
    inset = params.magnet_edge_inset
    if min(inset, params.plate_width - inset, params.plate_height - inset) <= radius:
        raise ValueError("Magnet pockets must not touch or break through plate edges")
    if min(params.plate_width, params.plate_height) - 2 * inset <= 2 * radius:
        raise ValueError("Magnet pockets must not overlap or touch")
    if params.magnet_depth + params.magnet_depth_clearance >= params.base_thickness:
        raise ValueError("Magnet pockets require positive roof thickness")


def _magnet_centers(params: Parameters) -> tuple[tuple[float, float], ...]:
    near = params.magnet_edge_inset
    far_x = params.plate_width - near
    far_y = params.plate_height - near
    return ((near, near), (far_x, near), (near, far_y), (far_x, far_y))


def _text_profile(params: Parameters) -> Text:
    # Use the font and license shipped by the locked matplotlib distribution,
    # never a platform-dependent font-name lookup or a system font fallback.
    font_dir = Path(get_data_path()) / "fonts" / "ttf"
    font_path = font_dir / "DejaVuSans.ttf"
    if not font_path.is_file() or not (font_dir / "LICENSE_DEJAVU").is_file():
        raise ValueError("The locked matplotlib DejaVuSans font and license are required")
    label = "Wifi SSID: " + params.ssid
    font = FT2Font(font_path)
    if any(font.get_char_index(ord(char)) == 0 for char in label):
        raise ValueError("SSID contains characters unavailable in the bundled DejaVuSans font")
    text = Text(label, font_size=params.text_height, font_path=font_path)
    bounds = text.bounding_box()
    band = params.plate_height - params.qr_top_margin - params.qr_size
    if (
        bounds.size.X <= 0
        or bounds.size.Y <= 0
        or bounds.size.X > params.plate_width - 2 * _TEXT_MARGIN
        or bounds.size.Y > band - 2 * _TEXT_MARGIN
    ):
        raise ValueError("SSID text does not fit its lower band at the requested text_height")
    return text.translate(
        (
            (params.plate_width - bounds.size.X) / 2 - bounds.min.X,
            (band - bounds.size.Y) / 2 - bounds.min.Y,
            params.base_thickness - bounds.min.Z,
        )
    )


def _dark_runs(matrix: list[list[bool]]):
    """Yield row, start column, and width for each contiguous dark run."""
    for row_index, row in enumerate(matrix):
        column = 0
        for dark, group in groupby(row):
            width = sum(1 for _ in group)
            if dark:
                yield row_index, column, width
            column += width


def _qr_rectangles(params: Parameters, matrix: list[list[bool]]):
    """Keep exterior symbol bounds exact; inset only internal run edges."""
    count = len(matrix)
    pitch = params.qr_size / count
    inset = params.qr_run_gap / 2
    left = (params.plate_width - params.qr_size) / 2
    top = params.plate_height - params.qr_top_margin
    for row, start, width in _dark_runs(matrix):
        x0 = left + start * pitch + (inset if start else 0)
        x1 = left + (start + width) * pitch - (inset if start + width < count else 0)
        y0 = top - (row + 1) * pitch + (inset if row + 1 < count else 0)
        y1 = top - row * pitch - (inset if row else 0)
        yield x0, y0, x1 - x0, y1 - y0


def build(params: Parameters | None = None) -> Solid:
    """Build one fused solid without writing files or changing the parameters."""
    params = Parameters() if params is None else params
    _validate(params)
    matrix = qr_matrix(params)
    pitch = params.qr_size / len(matrix)
    gap = params.qr_run_gap
    if gap > pitch * 0.05:
        raise ValueError("qr_run_gap must be at most 5% of QR module pitch")
    text = _text_profile(params)  # Fail on text overflow before making any solids.
    top = params.plate_height - params.qr_top_margin
    # Preserve coplanar row seams. OCCT 8's mesher can leave open triangles
    # in a single large face perforated by hundreds of narrow relief footprints.
    # These are face partitions inside one solid, not physical cuts or gaps.
    rows = [0.0, *(top - row * pitch for row in range(len(matrix), -1, -1)), params.plate_height]
    strips = [
        Solid.make_box(params.plate_width, end - start, params.base_thickness,
                       Plane(origin=(0, start, 0)))
        for start, end in zip(rows, rows[1:])
    ]
    radius = (params.magnet_diameter + params.magnet_diametral_clearance) / 2
    depth = params.magnet_depth + params.magnet_depth_clearance
    pockets = [
        Solid.make_cylinder(radius, depth, Plane(origin=(x, y, 0)))
        for x, y in _magnet_centers(params)
    ]
    with SkipClean():
        base = strips[0].fuse(*strips[1:]).cut(*pockets)
    # A tiny gap prevents diagonal runs from sharing only a vertical edge:
    # that contact is a valid BREP but produces four-facet nonmanifold STL edges.
    reliefs = [
        Solid.make_box(
            width, height, params.relief_height,
            Plane(origin=(x, y, params.base_thickness)),
        )
        for x, y, width, height in _qr_rectangles(params, matrix)
    ]
    reliefs.extend(Solid.extrude(face, (0, 0, params.relief_height)) for face in text.faces())
    with SkipClean():
        fused = base.fuse(*reliefs)
    solids = fused.solids()
    if len(solids) != 1 or not fused.is_valid:
        raise ValueError("Wi-Fi plaque must be one valid fused solid")
    result = solids[0]
    result.label = "wifi_qr"
    return result


def check(shape: Compound | Solid) -> None:
    """Check default-design BREP invariants, including reimported STEP geometry."""
    params = Parameters()
    solids = shape.solids()
    if len(solids) != 1 or not shape.is_valid:
        raise ValueError("Wi-Fi plaque must be one valid solid")
    solid = solids[0]
    bounds = shape.bounding_box()
    for actual, expected in zip(bounds.min, (0, 0, 0)):
        if not isclose(actual, expected, abs_tol=1e-5):
            raise ValueError("Wi-Fi plaque must start at (0, 0, 0)")
    for actual, expected in zip(bounds.size, (params.plate_width, params.plate_height, params.base_thickness + params.relief_height)):
        if not isclose(actual, expected, abs_tol=1e-5):
            raise ValueError("Unexpected Wi-Fi plaque overall dimensions")
    radius = (params.magnet_diameter + params.magnet_diametral_clearance) / 2
    depth = params.magnet_depth + params.magnet_depth_clearance
    roof_z = (depth + params.base_thickness) / 2
    for x, y in _magnet_centers(params):
        for dx, dy in ((0, 0), (0.99 * radius, 0), (-0.99 * radius, 0), (0, 0.99 * radius), (0, -0.99 * radius)):
            for z in (0.01, depth / 2, depth - 0.01):
                if solid.is_inside((x + dx, y + dy, z)):
                    raise ValueError(f"Missing or undersized rear magnet pocket at {(x, y)}")
            if not solid.is_inside((x + dx, y + dy, roof_z)):
                raise ValueError(f"Missing magnet-pocket roof at {(x, y)}")
        for dx, dy in ((radius + 0.01, 0), (-radius - 0.01, 0), (0, radius + 0.01), (0, -radius - 0.01)):
            if not solid.is_inside((x + dx, y + dy, depth / 2)):
                raise ValueError(f"Oversized rear magnet pocket at {(x, y)}")
    matrix = qr_matrix(params)
    pitch = params.qr_size / len(matrix)
    left = (params.plate_width - params.qr_size) / 2
    top = params.plate_height - params.qr_top_margin
    for row_index, row in enumerate(matrix):
        for column, dark in enumerate(row):
            x = left + (column + 0.5) * pitch
            y = top - (row_index + 0.5) * pitch
            if solid.is_inside((x, y, params.base_thickness + params.relief_height / 2)) != dark:
                raise ValueError(f"Incorrect raised QR module at row {row_index}, column {column}")
            if not solid.is_inside((x, y, roof_z)):
                raise ValueError("QR field must have a continuous supporting base")
    text = _text_profile(params)
    dark_area = sum(
        width * height
        for _, _, width, height in _qr_rectangles(params, matrix)
    )
    expected_volume = (
        params.plate_width * params.plate_height * params.base_thickness
        - 4 * pi * radius**2 * depth
        + (dark_area + text.area) * params.relief_height
    )
    if not isclose(shape.volume, expected_volume, rel_tol=1e-7, abs_tol=1e-5):
        raise ValueError("Plaque volume does not match the base, four pockets, QR, and SSID text")
