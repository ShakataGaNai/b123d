"""Geometry and metadata boundaries exercised without importing catalog models."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

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
        names = ("bracket.step", "bracket.stl", "preview.png", "preview.html", "report.json")
        previous = {name: f"Previous artifact: {name}\n" for name in names}
        for name, content in previous.items():
            (output / name).write_text(content)
        index = self.root / "models" / "README.md"
        index.write_text("Previous catalog\n")
        original_path = sys.path.copy()
        with patch.object(pipeline, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "STEP design check failed"):
                pipeline.build(folder, 1, 0.05, 0.1)
        self.assertEqual(sys.path, original_path)
        self.assertEqual({path.name for path in output.iterdir()}, set(names))
        for name, content in previous.items():
            self.assertEqual((output / name).read_text(), content)
        self.assertEqual(index.read_text(), "Previous catalog\n")


if __name__ == "__main__":
    unittest.main()
