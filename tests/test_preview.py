"""Preserve visible raster behavior while optimizing mesh property access."""

import unittest

import numpy as np
import trimesh

from scripts.preview import raster_view


class RasterViewTests(unittest.TestCase):
    def test_crossing_triangles_occlude_by_depth_not_face_order(self) -> None:
        # Identical projections, but each triangle is nearer on a different side.
        vertices = np.array([
            [-1, -1, -0.5], [1, -1, 0.5], [0, 1, 0],
            [-1, -1, 0.5], [1, -1, -0.5], [0, 1, 0],
        ])
        faces = np.array([[0, 1, 2], [3, 4, 5]])
        colors = np.array([[255, 0, 0], [0, 255, 0]])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
        image = raster_view(mesh, (0, 0, 1), (0, 1, 0), colors)

        # Interior pixels away from the equal-depth crossing and silhouette.
        self.assertGreater(image[400, 250, 1], 0)
        self.assertEqual(image[400, 250, 0], 0)
        self.assertGreater(image[400, 450, 0], 0)
        self.assertEqual(image[400, 450, 1], 0)

        reversed_mesh = trimesh.Trimesh(
            vertices=vertices, faces=faces[::-1], process=False,
        )
        reversed_image = raster_view(
            reversed_mesh, (0, 0, 1), (0, 1, 0), colors[::-1],
        )
        np.testing.assert_array_equal(image, reversed_image)

    def test_geometry_mutation_refreshes_normals_for_each_view(self) -> None:
        mesh = trimesh.Trimesh(
            vertices=[[-1, -1, 0], [1, -1, 0], [0, 1, 0]],
            faces=[[0, 1, 2]], process=False,
        )
        colors = np.array([[255, 0, 0]])
        before = raster_view(mesh, (0, 0, 1), (0, 1, 0), colors)
        self.assertGreater(before[350, 350, 0], 0)
        np.testing.assert_array_equal(before[350, 350, 1:], [0, 0])

        # Reflecting geometry reverses the normal without changing the bounds.
        mesh.vertices[:, 0] *= -1
        after = raster_view(mesh, (0, 0, 1), (0, 1, 0), colors)
        np.testing.assert_array_equal(after, np.full_like(after, 250))

        bottom = raster_view(mesh, (0, 0, -1), (0, 1, 0), colors)
        self.assertGreater(bottom[350, 350, 0], 0)
        np.testing.assert_array_equal(bottom[350, 350, 1:], [0, 0])


if __name__ == "__main__":
    unittest.main()
