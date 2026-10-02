"""Geometry and metadata boundaries exercised without importing catalog models."""

import json
import locale
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import numpy as np
import trimesh

from build123d import Box, Compound, Face, Pos, Solid, export_step, import_step

from scripts import build as pipeline
from scripts.index import catalog, discover


class GeometryValidationTests(unittest.TestCase):
    def test_disconnected_solids_require_explicit_count(self) -> None:
        shape = Compound([Box(2, 3, 4), Pos(10, 0, 0) * Box(2, 3, 4)])
        with self.assertRaisesRegex(ValueError, "Expected 1 solid"):
            pipeline.validate(shape, 1)
        report = pipeline.validate(shape, 2)
        self.assertEqual(report["solid_count"], 2)
        self.assertAlmostEqual(report["volume_mm3"], 48)

    def test_loose_face_is_rejected_even_inside_nested_compound(self) -> None:
        face = Face.make_rect(2, 3)
        shape = Compound([Box(2, 3, 4), Compound([face])])
        with self.assertRaisesRegex(ValueError, "loose faces"):
            pipeline.validate(shape, 1)

    def test_non_solid_and_null_geometry_are_rejected(self) -> None:
        for shape in (Face.make_rect(2, 3), Solid(), object()):
            with self.subTest(shape=type(shape).__name__):
                with self.assertRaises(ValueError):
                    pipeline.validate(shape, 1)

    def test_solid_count_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 1"):
            pipeline.validate(Box(2, 3, 4), 0)

    def test_step_round_trip_preserves_real_shape(self) -> None:
        shape = Pos(10, -5, 2) * Box(2, 3, 4)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "part.step"
            self.assertTrue(export_step(shape, path))
            restored = import_step(path)
            pipeline.check_round_trip(
                pipeline.validate(shape, 1), pipeline.validate(restored, 1)
            )
            self.assertAlmostEqual(restored.volume, 24)
            self.assertAlmostEqual(restored.bounding_box().min.X, 9)

    def test_step_volume_mismatch_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "changed volume"):
            pipeline.check_round_trip(
                pipeline.validate(Box(2, 3, 4), 1),
                pipeline.validate(Box(2, 3, 5), 1),
            )

    def test_step_translation_is_rejected_despite_equal_volume(self) -> None:
        with self.assertRaisesRegex(ValueError, "changed bounds"):
            pipeline.check_round_trip(
                pipeline.validate(Box(2, 3, 4), 1),
                pipeline.validate(Pos(0, 0, 1) * Box(2, 3, 4), 1),
            )


class WorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "models").mkdir()
        self.research = self.root / "research" / "objects" / "test fixture"
        self.research.mkdir(parents=True)
        (self.research / "README.md").write_text("Measured fixture dimensions.\n")

    def model(self, name: str, source: str, reference: str = "research/objects/test fixture/README.md") -> Path:
        folder = self.root / "models" / name
        folder.mkdir(parents=True)
        (folder / "model.py").write_text(source)
        (folder / "model.toml").write_text(
            'name = "Fixture bracket"\n'
            'description = "Bracket for measured hardware"\n'
            'units = "mm"\n'
            'status = "draft"\n'
            'print_tested = false\n'
            'tags = ["fixture", "mount"]\n'
            f'research = ["{reference}"]\n'
        )
        return folder

    def test_nested_catalog_links_metadata_without_executing_models(self) -> None:
        self.model("fixture/left bracket", "raise RuntimeError('catalog executed model')\n")
        models = discover(self.root)
        self.assertEqual([model.folder.relative_to(self.root / "models").as_posix()
                          for model in models], ["fixture/left bracket"])
        text = catalog(self.root)
        self.assertIn("(fixture/left%20bracket/model.py)", text)
        self.assertIn("(../research/objects/test%20fixture/README.md)", text)

    def test_print_tested_requires_an_explicit_boolean(self) -> None:
        folder = self.model("fixture/print-status", "")
        metadata = folder / "model.toml"
        original = metadata.read_text()
        for value in (None, '"false"', '"true"', "0", "1", "[]"):
            with self.subTest(value=value):
                field = "" if value is None else f"print_tested = {value}\n"
                metadata.write_text(original.replace("print_tested = false\n", field))
                with self.assertRaisesRegex(ValueError, "print_tested must be a boolean"):
                    discover(self.root)

    def test_source_without_metadata_fails_discovery(self) -> None:
        folder = self.model("fixture/missing", "raise RuntimeError('must not execute')\n")
        (folder / "model.toml").unlink()
        with self.assertRaisesRegex(ValueError, "missing model.toml"):
            catalog(self.root)

    def test_metadata_without_source_fails_discovery(self) -> None:
        folder = self.model("fixture/missing", "")
        (folder / "model.py").unlink()
        with self.assertRaisesRegex(ValueError, "missing model.py"):
            catalog(self.root)

    def test_missing_external_and_absolute_research_links_are_rejected(self) -> None:
        outside = self.root / "outside.md"
        outside.write_text("Not research.\n")
        references = (
            "research/objects/missing.md",
            "research/../outside.md",
            str(self.research / "README.md"),
            "https://example.com/hardware",
        )
        for index, reference in enumerate(references):
            with self.subTest(reference=reference):
                folder = self.model(f"invalid-{index}", "", reference)
                with self.assertRaisesRegex(ValueError, "existing file under research/"):
                    catalog(self.root)
                (folder / "model.py").unlink()
                (folder / "model.toml").unlink()

    def test_symlink_cannot_escape_research_directory(self) -> None:
        outside = self.root / "outside.md"
        outside.write_text("Outside research.\n")
        (self.root / "research" / "escape.md").symlink_to(outside)
        self.model("escape", "", "research/escape.md")
        with self.assertRaisesRegex(ValueError, "existing file under research/"):
            catalog(self.root)

    def test_failed_model_import_restores_search_path(self) -> None:
        folder = self.model("broken", "raise RuntimeError('import failed')\n")
        original_path = sys.path.copy()
        with patch.object(pipeline, "ROOT", self.root):
            with self.assertRaisesRegex(RuntimeError, "import failed"):
                pipeline.build(folder, 1, 0.05, 0.1)
        self.assertEqual(sys.path, original_path)
        self.assertFalse((self.root / "outputs").exists())

    def test_failed_step_check_keeps_previous_artifacts_and_search_path(self) -> None:
        folder = self.model(
            "fixture/bracket",
            "from build123d import Box\n"
            "checks = 0\n"
            "def build():\n"
            "    return Box(2, 3, 4)\n"
            "def check(shape):\n"
            "    global checks\n"
            "    checks += 1\n"
            "    if checks == 2:\n"
            "        raise ValueError('STEP design check failed')\n",
        )
        output = self.root / "outputs" / "fixture" / "bracket"
        output.mkdir(parents=True)
        names = ("bracket.step", "bracket.stl", "bracket.3mf",
                 "preview.png", "preview.html", "report.json")
        previous = {name: f"Previous artifact: {name}\n" for name in names}
        for name, content in previous.items():
            (output / name).write_text(content)
        index = self.root / "models" / "README.md"
        index.write_text("Previous catalog\n")
        original_path = sys.path.copy()
        with patch.object(pipeline, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "STEP design check failed"):
                pipeline.build(folder, 1, 0.05, 0.1, step=True)
        self.assertEqual(sys.path, original_path)
        self.assertEqual({path.name for path in output.iterdir()}, set(names))
        for name, content in previous.items():
            self.assertEqual((output / name).read_text(), content)
        self.assertEqual(index.read_text(), "Previous catalog\n")

    def test_3mf_build_preserves_locale_and_unicode_preview(self) -> None:
        original_locale = locale.setlocale(locale.LC_ALL)
        self.addCleanup(locale.setlocale, locale.LC_ALL, original_locale)
        folder = self.model(
            "unicode-bracket",
            "from build123d import Box\n"
            "def build():\n"
            "    return Box(2, 3, 4)\n",
        )
        metadata = folder / "model.toml"
        metadata.write_text(
            metadata.read_text().replace("Fixture bracket", "Peg – rail"),
            encoding="utf-8",
        )
        with patch.object(pipeline, "ROOT", self.root):
            output = pipeline.build(folder, 1, 0.05, 0.1)
        self.assertEqual(locale.setlocale(locale.LC_ALL), original_locale)
        self.assertIn("Peg – rail", (output / "preview.html").read_text(encoding="utf-8"))
        self.assertIn("Peg – rail", (self.root / "models" / "README.md").read_text(encoding="utf-8"))

    @staticmethod
    def write_previews(mesh, folder: Path, title: str, **options) -> None:
        (folder / "preview.png").write_bytes(b"Test preview")
        (folder / "preview.html").write_text("<html>Test preview</html>")

    def read_3mf_mesh(self, path: Path) -> trimesh.Trimesh:
        """Read the consumer's mesh directly, independently of the export library."""
        with ZipFile(path) as package:
            models = [name for name in package.namelist() if name.endswith(".model")]
            self.assertEqual(len(models), 1)
            model = ET.fromstring(package.read(models[0]))
        ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
        self.assertEqual(model.get("unit"), "millimeter")
        items = model.findall("m:build/m:item", ns)
        self.assertEqual(len(items), 1)
        objects = {obj.get("id"): obj for obj in model.findall("m:resources/m:object", ns)}
        obj = objects[items[0].get("objectid")]
        self.assertIsNone(obj.find("m:components", ns))
        vertices = np.array([
            [float(vertex.attrib[axis]) for axis in ("x", "y", "z")]
            for vertex in obj.findall("m:mesh/m:vertices/m:vertex", ns)
        ])
        triangles = np.array([
            [int(triangle.attrib[corner]) for corner in ("v1", "v2", "v3")]
            for triangle in obj.findall("m:mesh/m:triangles/m:triangle", ns)
        ])
        transform = items[0].get("transform")
        if transform is not None:
            matrix = np.array([float(value) for value in transform.split()]).reshape(4, 3)
            vertices = vertices @ matrix[:3] + matrix[3]
        return trimesh.Trimesh(vertices=vertices, faces=triangles, process=True)

    def test_default_rebuild_removes_step_and_preserves_multipart_3mf_geometry(self) -> None:
        folder = self.model(
            "fixture/bracket",
            "from build123d import Box, Pos\n"
            "def build():\n"
            "    return Pos(10, -5, 2) * Box(2, 3, 4)\n"
            "def check(shape):\n"
            "    assert abs(shape.volume - 24) < 1e-6\n",
        )
        with patch.object(pipeline, "ROOT", self.root), \
                patch.object(pipeline, "render", side_effect=self.write_previews):
            output = pipeline.build(folder, 1, 0.05, 0.1, step=True)
            step_path = output / "bracket.step"
            self.assertAlmostEqual(import_step(step_path).volume, 24)
            initial = json.loads((output / "report.json").read_text())
            self.assertEqual(set(initial["formats"]), {"stl", "3mf", "step"})
            self.assertEqual(initial["design_check"], "passed on native and STEP")
            self.assertAlmostEqual(initial["step_round_trip"]["volume_mm3"], 24)

            (folder / "model.py").write_text(
                "from build123d import Box, Compound, Pos\n"
                "checks = 0\n"
                "def build():\n"
                "    return Compound([Pos(10, -5, 2) * Box(2, 3, 4),\n"
                "                     Pos(-8, 7, 11) * Box(4, 2, 6)])\n"
                "def check(shape):\n"
                "    global checks\n"
                "    checks += 1\n"
                "    assert checks == 1, 'Unrequested STEP design check'\n"
                "    assert abs(shape.volume - 72) < 1e-6\n"
            )
            pipeline.build(folder, 2, 0.05, 0.1)

        self.assertFalse(step_path.exists())
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(set(report["formats"]), {"stl", "3mf"})
        self.assertIsNone(report["step_round_trip"])
        self.assertEqual(report["design_check"], "passed on native")
        self.assertEqual(report["mesh_3mf"], {"units": "mm", "round_trip": "passed"})
        self.assertEqual(report["mesh"]["connected_bodies"], 2)
        self.assertAlmostEqual(report["mesh"]["volume_mm3"], 72)
        stl = trimesh.load_mesh(output / "bracket.stl")
        mesh_3mf = self.read_3mf_mesh(output / "bracket.3mf")
        for mesh in (stl, mesh_3mf):
            self.assertTrue(mesh.is_watertight)
            self.assertTrue(mesh.is_winding_consistent)
            self.assertTrue(mesh.is_volume)
            self.assertEqual(mesh.body_count, 2)
            self.assertAlmostEqual(mesh.volume, 72)
            parts = sorted(mesh.split(), key=lambda part: part.bounds[0, 0])
            self.assertEqual(len(parts), 2)
            np.testing.assert_allclose(parts[0].bounds, [[-10, 6, 8], [-6, 8, 14]])
            np.testing.assert_allclose(parts[1].bounds, [[9, -6.5, 0], [11, -3.5, 4]])
            self.assertAlmostEqual(parts[0].volume, 48)
            self.assertAlmostEqual(parts[1].volume, 24)
        self.assertEqual(len(mesh_3mf.faces), len(stl.faces))
        self.assertEqual(len(mesh_3mf.faces), report["mesh"]["triangles"])

    def test_failed_default_rebuild_keeps_step_and_all_previous_outputs(self) -> None:
        folder = self.model(
            "fixture/bracket",
            "from build123d import Box\n"
            "def build():\n"
            "    return Box(2, 3, 4)\n",
        )
        with patch.object(pipeline, "ROOT", self.root), \
                patch.object(pipeline, "render", side_effect=self.write_previews):
            output = pipeline.build(folder, 1, 0.05, 0.1, step=True)
        previous = {path.name: path.read_bytes() for path in output.iterdir()}
        self.assertIn("bracket.step", previous)
        self.assertIn("bracket.3mf", previous)
        self.assertEqual(json.loads(previous["report.json"])["design_check"], "not provided")
        index = self.root / "models" / "README.md"
        previous_catalog = index.read_bytes()
        (folder / "model.py").write_text(
            "from build123d import Box\n"
            "def build():\n"
            "    return Box(5, 6, 7)\n"
        )
        original_path = sys.path.copy()
        with patch.object(pipeline, "ROOT", self.root), \
                patch.object(pipeline, "render", side_effect=RuntimeError("preview failed")):
            with self.assertRaisesRegex(RuntimeError, "preview failed"):
                pipeline.build(folder, 1, 0.05, 0.1)
        self.assertEqual(sys.path, original_path)
        self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, previous)
        self.assertEqual(index.read_bytes(), previous_catalog)


if __name__ == "__main__":
    unittest.main()
