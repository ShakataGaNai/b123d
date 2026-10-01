"""Verify the printable Wi-Fi plaque through its public model and actual BREP.

The decoder sees an ideal orthographic projection sampled from solid occupancy,
not the encoder's matrix. This is not evidence of a successful physical print
scan: real plaques still need contrasting colors and a scan after printing.
"""

from dataclasses import fields, replace
import math
from pathlib import Path
import tempfile
import unittest

from PIL import Image
import zxingcpp

from models.wifi_qr.model import Parameters, build, qr_matrix, wifi_payload
from scripts.build import write_stl
from scripts.preview import load_mesh


def wifi_fields(payload: str) -> dict[str, str]:
    """Read escaped WIFI fields without splitting escaped delimiters."""
    if not payload.startswith("WIFI:"):
        raise ValueError("Not a Wi-Fi payload")
    result = {}
    field = []
    escaped = False
    for character in payload[5:]:
        if escaped:
            field.append(character)
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == ";":
            if field:
                key, value = "".join(field).split(":", 1)
                result[key] = value
                field = []
        else:
            field.append(character)
    if escaped or field:
        raise ValueError("Unterminated Wi-Fi field")
    return result


class WifiQRTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params = Parameters()
        cls.shape = build(cls.params)
        solids = cls.shape.solids()
        if len(solids) != 1:
            raise AssertionError("The plaque must be one connected printable solid")
        cls.solid = solids[0]

    def assert_bounds(self, shape, width, height, thickness):
        bounds = shape.bounding_box()
        for actual, expected in zip(
            (bounds.min.X, bounds.min.Y, bounds.min.Z,
             bounds.max.X, bounds.max.Y, bounds.max.Z),
            (0, 0, 0, width, height, thickness),
        ):
            self.assertAlmostEqual(actual, expected, delta=1e-5)

    def assert_pockets(self, solid, *, plate_width, plate_height, base_thickness, inset, radius, depth):
        centers = (
            (inset, inset),
            (plate_width - inset, inset),
            (inset, plate_height - inset),
            (plate_width - inset, plate_height - inset),
        )
        for x, y in centers:
            with self.subTest(magnet_center=(x, y)):
                self.assertFalse(solid.is_inside((x, y, 0.001)))
                self.assertFalse(solid.is_inside((x, y, depth - 0.05)))
                self.assertTrue(solid.is_inside((x, y, depth + 0.05)))
                self.assertTrue(solid.is_inside((x, y, base_thickness - 0.05)))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    self.assertFalse(solid.is_inside((
                        x + dx * (radius - 0.05),
                        y + dy * (radius - 0.05),
                        depth / 2,
                    )))
                    self.assertTrue(solid.is_inside((
                        x + dx * (radius + 0.05),
                        y + dy * (radius + 0.05),
                        depth / 2,
                    )))
        self.assertTrue(solid.is_inside((plate_width / 2, plate_height / 2, 0.001)))

    def assert_projected_qr(self, solid, params, expected_fields):
        matrix = qr_matrix(params)
        count = len(matrix)
        self.assertTrue(all(len(row) == count for row in matrix))
        pitch = params.qr_size / count
        left = (params.plate_width - params.qr_size) / 2
        top = params.plate_height - params.qr_top_margin
        z = params.base_thickness + params.relief_height / 2
        margin_corner = (left - pitch / 2, top + pitch / 2)
        self.assertTrue(solid.is_inside((*margin_corner, params.base_thickness - 0.001)))
        self.assertFalse(solid.is_inside((*margin_corner, params.base_thickness + 0.001)))
        # No encoded border: the finder starts at the symbol's outer edge.
        finder_center = (left + 3.5 * pitch, top - 3.5 * pitch)
        relief_top = params.base_thickness + params.relief_height
        self.assertTrue(solid.is_inside((*finder_center, params.base_thickness + 0.001)))
        self.assertTrue(solid.is_inside((*finder_center, relief_top - 0.001)))
        self.assertFalse(solid.is_inside((*finder_center, relief_top + 0.001)))
        # Image rows descend from the top of the plaque; CAD Y increases up.
        sampled = [
            [
                solid.is_inside((left + (column + 0.5) * pitch,
                                 top - (row + 0.5) * pitch, z))
                for column in range(count)
            ]
            for row in range(count)
        ]
        # Decoders can repair a mirrored symbol. Explicitly ensure construction
        # also preserves the public top-left matrix's row/column orientation.
        self.assertEqual(sampled, matrix)
        image = Image.new("L", (count, count))
        image.putdata([0 if dark else 255 for row in sampled for dark in row])
        image = image.resize((count * 8, count * 8), Image.Resampling.NEAREST)
        decoded = zxingcpp.read_barcode(
            image,
            formats=zxingcpp.BarcodeFormat.QRCode,
            try_rotate=False,
            try_downscale=False,
            try_invert=False,
        )
        self.assertIsNotNone(decoded, "The actual raised geometry must decode")
        self.assertTrue(decoded.valid)
        self.assertEqual(decoded.orientation, 0)
        self.assertEqual(decoded.text, wifi_payload(params))
        values = wifi_fields(decoded.text)
        for key, expected in expected_fields.items():
            self.assertEqual(values.get(key), expected, key)
        return values

    def assert_print_mesh(self, shape):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wifi.stl"
            write_stl(shape, path, 0.05, 0.1)
            mesh = load_mesh(path)
            self.assertTrue(mesh.is_watertight, "QR corner contacts must not create nonmanifold edges")
            self.assertTrue(mesh.is_winding_consistent)
            self.assertTrue(mesh.is_volume)
            self.assertEqual(mesh.body_count, 1)

    def test_saved_stl_is_watertight(self):
        self.assert_print_mesh(self.shape)

    def test_default_plate_dimensions_and_blind_magnet_pockets(self):
        self.assertTrue(self.shape.is_valid)
        self.assert_bounds(self.shape, 70, 80, 6)
        self.assert_pockets(
            self.solid, plate_width=70, plate_height=80, base_thickness=5,
            inset=9, radius=5.1, depth=3.1,
        )

    def test_default_raised_geometry_decodes_sample_wifi(self):
        values = self.assert_projected_qr(
            self.solid,
            replace(self.params, plate_width=70, plate_height=80, base_thickness=5, qr_size=60,
                    qr_top_margin=5, relief_height=1),
            {"T": "WPA", "S": "WorkshopWiFi", "P": "SamplePass123!"},
        )
        self.assertEqual(values.get("H", "false").lower(), "false")

    def test_alternate_dimensions_and_escaped_credentials(self):
        params = replace(
            self.params,
            plate_width=80.0,
            plate_height=90.0,
            base_thickness=6.0,
            qr_size=54.0,
            relief_height=0.8,
            magnet_diameter=8.0,
            magnet_depth=2.0,
            magnet_edge_inset=10.0,
            ssid="Lab;A",
            password='a\\b;c,d:e"f',
            hidden=True,
        )
        shape = build(params)
        self.assertTrue(shape.is_valid)
        self.assertEqual(len(shape.solids()), 1)
        solid = shape.solids()[0]
        self.assert_bounds(shape, 80, 90, 6.8)
        self.assert_pockets(
            solid, plate_width=80, plate_height=90, base_thickness=6,
            inset=10, radius=4.1, depth=2.1,
        )
        self.assert_projected_qr(
            solid, params,
            {"T": "WPA", "S": "Lab;A", "P": 'a\\b;c,d:e"f', "H": "true"},
        )
        self.assert_print_mesh(shape)

    def test_impossible_geometry_is_rejected(self):
        cases = (
            {"plate_width": 0.0},
            {"plate_height": 0.0},
            {"base_thickness": -1.0},
            {"qr_size": 0.0},
            {"qr_size": 71.0},
            {"qr_top_margin": -1.0},
            {"qr_top_margin": 25.0},
            {"relief_height": 0.0},
            {"qr_run_gap": 0.0},
            {"qr_run_gap": 0.5},
            {"magnet_diameter": -1.0},
            {"magnet_depth": 0.0},
            {"magnet_depth": 4.95},
            {"magnet_edge_inset": 3.0},
            {"magnet_edge_inset": 35.0},
            {"magnet_diametral_clearance": -0.1},
            {"magnet_depth_clearance": -0.1},
            {"text_height": 0.0},
            {"text_height": 30.0},
            {"ssid": "W" * 100},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    build(replace(self.params, **changes))

    def test_nonfinite_dimensions_are_rejected(self):
        dimensions = (
            field.name for field in fields(self.params)
            if isinstance(getattr(self.params, field.name), float)
        )
        for name in dimensions:
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(parameter=name, value=value):
                    with self.assertRaises(ValueError):
                        build(replace(self.params, **{name: value}))


if __name__ == "__main__":
    unittest.main()
