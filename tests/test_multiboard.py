"""Public geometry invariants for reusable Multiboard connector factories."""

from math import pi, sqrt, tan
import unittest
from typing import cast

from build123d import Box, BuildPart

from models.multiboard.peg import peg
from models.multiboard.rail import rail_cutout


class MultiboardGeometryTests(unittest.TestCase):
    def test_peg_flat_convention_and_overlap_preserve_exposed_projection(self) -> None:
        shape = peg(across_flats=13.5, projection=6.5, root_overlap=0.2)
        self.assertTrue(shape.is_valid)
        self.assertEqual(len(shape.solids()), 1)
        bounds = shape.bounding_box()
        for actual, expected in zip((*bounds.min, *bounds.max),
                                    (-6.75, -6.75, -0.2, 6.75, 6.75, 6.5)):
            self.assertAlmostEqual(actual, expected, places=6)
        self.assertAlmostEqual(shape.volume, 2 * 13.5**2 * tan(pi / 8) * 6.7, places=6)
        for x, y in ((6.75, 0), (0, 6.75), (6.75 / sqrt(2), 6.75 / sqrt(2))):
            with self.subTest(flat=(x, y)):
                self.assertTrue(shape.is_inside((x * 0.999, y * 0.999, 3)))
                self.assertFalse(shape.is_inside((x * 1.001, y * 1.001, 3)))

    def test_rail_taper_shoulders_and_closed_end_survive_loft(self) -> None:
        shape = rail_cutout(overrun=0)
        self.assertTrue(shape.is_valid)
        # Prismoidal integral of the two documented profiles and their midpoint.
        self.assertAlmostEqual(shape.volume, 1100.916666666667, places=5)
        for z in (-2.1, -1.1, -0.1):
            half_width = 7 - 1.5 * z / 2.2
            for y in (3, 20):
                with self.subTest(z=z, y=y):
                    self.assertTrue(shape.is_inside((half_width - 0.001, y, z)))
                    self.assertFalse(shape.is_inside((half_width + 0.001, y, z)))
            self.assertTrue(shape.is_inside((8.49, 12.5, z)))
            self.assertFalse(shape.is_inside((8.51, 12.5, z)))
        self.assertTrue(shape.is_inside((0, 33, -2.1)))
        self.assertFalse(shape.is_inside((0, 33, -0.1)))
        self.assertFalse(shape.is_inside((0, 34, -1.1)))

    def test_rail_repeat_pitch_and_cutting_overrun(self) -> None:
        shape = rail_cutout(repeats=2, overrun=0.4)
        self.assertTrue(shape.is_valid)
        self.assertEqual(len(shape.solids()), 1)
        bounds = shape.bounding_box()
        for actual, expected in zip((*bounds.min, *bounds.max),
                                    (-8.5, -0.4, -2.2, 8.5, 58.5, 0.4)):
            self.assertAlmostEqual(actual, expected, places=5)
        for y in (12.5, 37.5):
            self.assertTrue(shape.is_inside((8.49, y, 0.2)))
            self.assertFalse(shape.is_inside((8.51, y, 0.2)))
        self.assertFalse(shape.is_inside((8, 45, 0.2)))
        self.assertTrue(shape.is_inside((0, -0.2, -1)))
        self.assertFalse(shape.is_inside((0, 58.6, -2.1)))

    def test_factories_do_not_implicitly_modify_an_active_builder(self) -> None:
        with BuildPart() as host:
            Box(20, 20, 5)
            peg(root_overlap=0.2)
            rail_cutout()
        assert host.part is not None
        self.assertAlmostEqual(host.part.volume, 2000, places=6)
        self.assertEqual(len(host.part.solids()), 1)

    def test_invalid_dimensions_fail_before_geometry_construction(self) -> None:
        for value in (0, -1, float('nan'), float('inf'), True):
            for key in ('across_flats', 'projection'):
                with self.subTest(key=key, value=value):
                    with self.assertRaises(ValueError):
                        peg(**{key: value})
        for value in (-1, float('nan'), float('inf'), True):
            with self.subTest(overlap=value):
                with self.assertRaises(ValueError):
                    peg(root_overlap=value)
                with self.assertRaises(ValueError):
                    rail_cutout(overrun=value)
        for count in (0, -1, 1.5, True):
            with self.subTest(repeats=count):
                with self.assertRaises(ValueError):
                    rail_cutout(repeats=cast(int, count))


if __name__ == '__main__':
    unittest.main()
