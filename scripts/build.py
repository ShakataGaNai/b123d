"""Build validated STL/3MF and previews; optionally export STEP with --step."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import locale
import math
from pathlib import Path
import platform
import runpy
import sys
import tempfile
import json
from typing import Literal, TypedDict, cast

from build123d import Compound, Mesher, Solid, Unit, export_step, import_step
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from OCP.StlAPI import StlAPI_Writer
import numpy as np
from trimesh import Trimesh

# Direct invocation puts scripts/, not the workspace, on sys.path. Limit this
# bootstrap to imports; loading a model has its own exception-safe search path.
_direct_execution = __package__ in (None, "")
if _direct_execution:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from scripts.index import ROOT, catalog, read_model
    from scripts.preview import load_mesh, render
finally:
    if _direct_execution:
        del sys.path[0]


CADShape = Compound | Solid


class Bounds(TypedDict):
    min: list[float]
    max: list[float]
    size: list[float]


class ShapeReport(TypedDict):
    valid: bool
    solid_count: int
    volume_mm3: float
    bounds_mm: Bounds


def validate(shape: object, expected_solids: int) -> ShapeReport:
    """Accept only valid, positive-volume solids, not sketches or loose topology."""
    if expected_solids < 1:
        raise ValueError("Expected solid count must be at least 1")
    if not isinstance(shape, (Compound, Solid)):
        raise ValueError("build() must return a Solid, Part, or Compound of solids")
    if shape.is_null or not shape.is_valid:
        raise ValueError("CAD shape is empty or invalid")

    def require_solid_leaves(node: CADShape) -> None:
        if isinstance(node, Solid):
            return
        for child in node:
            if not isinstance(child, (Compound, Solid)):
                raise ValueError("Model contains loose faces, shells, wires, or edges")
            require_solid_leaves(child)

    require_solid_leaves(shape)
    solids = shape.solids()
    if len(solids) != expected_solids:
        raise ValueError(f"Expected {expected_solids} solid(s), got {len(solids)}")
    if any(not solid.is_valid or not math.isfinite(solid.volume) or solid.volume <= 0
           for solid in solids):
        raise ValueError("Every solid must be valid and have positive finite volume")
    bounds = shape.bounding_box()
    if not all(math.isfinite(value) for value in (*bounds.min, *bounds.max)):
        raise ValueError("CAD bounds contain non-finite coordinates")
    return {
        "valid": True,
        "solid_count": len(solids),
        "volume_mm3": shape.volume,
        "bounds_mm": {"min": list(bounds.min), "max": list(bounds.max),
                      "size": list(bounds.size)},
    }


def write_stl(shape: CADShape, path: Path, linear: float, angular: float) -> None:
    # build123d 0.13 export_stl uses relative deflection. Use OCCT directly to
    # make --linear-deflection an absolute millimeter setting. Clear cached mesh
    # so an earlier coarse tessellation cannot override the requested settings.
    BRepTools.Clean_s(shape.wrapped)
    mesher = BRepMesh_IncrementalMesh(shape.wrapped, linear, False, angular, True)
    mesher.Perform()
    if not mesher.IsDone():
        raise ValueError("OCCT tessellation failed")
    writer = StlAPI_Writer()
    writer.ASCIIMode = False
    if not writer.Write(shape.wrapped, str(path)):
        raise ValueError("STL export failed")


def _write_3mf(stl_path: Path, path: Path, mesh: Trimesh) -> None:
    """Package the validated STL without remeshing; verify the saved 3MF."""
    # lib3mf's writer sets the process-wide locale to C. Restore every category
    # even on failure so later previews/catalog writes retain their encoding.
    original_locale = locale.setlocale(locale.LC_ALL)
    try:
        package = Mesher(unit=Unit.MM)
        assert package.model is not None, "lib3mf did not create an export model"
        unit = package.model.GetUnit()
        reader = package.model.QueryReader("stl")
        reader.SetStrictModeActive(True)
        reader.ReadFromFile(str(stl_path))
        if reader.GetWarningCount():
            raise ValueError(f"3MF STL import warning: {reader.GetWarning(0)}")
        package.model.SetUnit(unit)
        package.write(path)

        # Use the native mesh API: Mesher.read() needlessly constructs CAD topology
        # for every triangle. The strict reader checks the 3MF package itself.
        restored = Mesher(unit=Unit.MM)
        assert restored.model is not None, "lib3mf did not create an import model"
        reader = restored.model.QueryReader("3mf")
        reader.SetStrictModeActive(True)
        reader.ReadFromFile(str(path))
        if reader.GetWarningCount():
            raise ValueError(f"3MF import warning: {reader.GetWarning(0)}")
        if restored.model.GetUnit() != unit:
            raise ValueError("Saved 3MF does not declare millimeter units")
        with tempfile.TemporaryDirectory(prefix=".3mf-check-", dir=path.parent) as temporary:
            round_trip_path = Path(temporary) / "round_trip.stl"
            restored.write(round_trip_path)
            round_trip = load_mesh(round_trip_path)
    finally:
        locale.setlocale(locale.LC_ALL, original_locale)
    if (not round_trip.is_watertight or not round_trip.is_winding_consistent
            or not round_trip.is_volume):
        raise ValueError("Saved 3MF is not a watertight, consistently oriented positive volume")
    if (round_trip.body_count != mesh.body_count
            or len(round_trip.faces) != len(mesh.faces)
            or not np.allclose(round_trip.bounds, mesh.bounds, rtol=1e-9, atol=1e-5)
            or not math.isclose(round_trip.volume, mesh.volume, rel_tol=1e-6, abs_tol=1e-6)):
        raise ValueError("3MF round-trip changed mesh bodies, triangles, bounds, or volume")


def check_round_trip(native: ShapeReport, restored: ShapeReport) -> None:
    if not math.isclose(native["volume_mm3"], restored["volume_mm3"], rel_tol=1e-6, abs_tol=1e-6):
        raise ValueError("STEP round-trip changed volume beyond tolerance")
    end: Literal["min", "max"]
    for end in ("min", "max"):
        for before, after in zip(native["bounds_mm"][end], restored["bounds_mm"][end]):
            if not math.isclose(before, after, rel_tol=1e-9, abs_tol=1e-5):
                raise ValueError("STEP round-trip changed bounds beyond tolerance")


def build(folder: Path, expected_solids: int, linear: float, angular: float,
          *, step: bool = False) -> Path:
    folder = folder.resolve()
    models_root = (ROOT / "models").resolve()
    if not folder.is_relative_to(models_root) or folder == models_root:
        raise ValueError("Choose a model folder below models/")
    metadata = read_model(folder, ROOT)
    # Validate the entire catalog before publishing this model's outputs.
    index_text = catalog(ROOT)
    source = folder / "model.py"
    original_path = sys.path.copy()
    try:
        sys.path[:0] = [str(folder), str(ROOT)]
        namespace: dict[str, object] = runpy.run_path(str(source), run_name="_cad_model")
        factory = namespace.get("build")
        if not callable(factory):
            raise ValueError(f"{source} must define a parameterless build()")
        shape: object = factory()
        native = validate(shape, expected_solids)
        cad_shape = cast(CADShape, shape)  # validate established the runtime type.
        check = namespace.get("check")
        if check is not None and not callable(check):
            raise ValueError("check must be a callable accepting the built shape")
        if check is not None:
            check(shape)
        relative = folder.relative_to(models_root)
        output = ROOT / "outputs" / relative
        output.mkdir(parents=True, exist_ok=True)
        stem = folder.name
        # Only publish after all geometry checks and both previews succeed.
        # Failed runs retain the previous artifacts; their report timestamp is old.
        with tempfile.TemporaryDirectory(prefix=".build-", dir=output) as staging:
            stage = Path(staging)
            stl_path = stage / f"{stem}.stl"
            round_trip = None
            if step:
                step_path = stage / f"{stem}.step"
                if not export_step(cad_shape, step_path, unit=Unit.MM):
                    raise ValueError("STEP export failed")
                restored = import_step(step_path)
                round_trip = validate(restored, expected_solids)
                check_round_trip(native, round_trip)
                if check is not None:
                    check(restored)
            write_stl(cad_shape, stl_path, linear, angular)
            mesh = load_mesh(stl_path)
            if not mesh.is_watertight or not mesh.is_winding_consistent or not mesh.is_volume:
                raise ValueError("Saved STL is not a watertight, consistently oriented positive volume")
            if mesh.body_count != expected_solids:
                raise ValueError(f"STL has {mesh.body_count} connected bodies; expected {expected_solids}")
            _write_3mf(stl_path, stage / f"{stem}.3mf", mesh)
            render(mesh, stage, metadata.name, **metadata.preview)
            report = {
                "model": relative.as_posix(), "units": "mm",
                "built_at_utc": datetime.now(timezone.utc).isoformat(),
                "python": platform.python_version(), "build123d": version("build123d"),
                "ocp": version("cadquery-ocp-novtk"),
                "formats": ["stl", "3mf", "step"] if step else ["stl", "3mf"],
                "native": native, "step_round_trip": round_trip,
                "design_check": ("passed on native and STEP" if step else "passed on native")
                                if check else "not provided",
                "mesh_3mf": {"units": "mm", "round_trip": "passed"},
                "preview": metadata.preview,
                "mesh": {"watertight": bool(mesh.is_watertight),
                         "winding_consistent": bool(mesh.is_winding_consistent),
                         "connected_bodies": int(mesh.body_count),
                         "triangles": len(mesh.faces), "volume_mm3": float(mesh.volume),
                         "volume_relative_difference": abs(float(mesh.volume) - cad_shape.volume) / cad_shape.volume,
                         "linear_deflection_mm": linear, "angular_deflection_rad": angular,
                         "relative_deflection": False},
                "limitations": ["Not a wall-thickness, clearance, self-intersection, or printability certification.",
                                "Multipart models require separate interference and fit checks."],
            }
            (stage / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
            names = [f"{stem}.stl", f"{stem}.3mf", "preview.png", "preview.html"]
            if step:
                names.append(f"{stem}.step")
            else:
                # A successful mesh-only build must not leave a stale CAD export.
                (output / f"{stem}.step").unlink(missing_ok=True)
            for name in [*names, "report.json"]:
                (stage / name).replace(output / name)
        (ROOT / "models" / "README.md").write_text(index_text)
        return output
    finally:
        sys.path[:] = original_path


def positive_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise argparse.ArgumentTypeError("must be positive and finite")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="Folder containing model.py and model.toml")
    parser.add_argument("--step", action="store_true",
                        help="Also export STEP and run STEP round-trip checks")
    parser.add_argument("--expected-solids", type=int, default=1,
                        help="Explicit opt-in for multipart models (default: 1)")
    parser.add_argument("--linear-deflection", type=positive_float, default=0.05,
                        help="Absolute tessellation deflection in mm (default: 0.05)")
    parser.add_argument("--angular-deflection", type=positive_float, default=0.1,
                        help="Tessellation angular deflection in radians (default: 0.1)")
    args = parser.parse_args()
    if args.expected_solids < 1:
        parser.error("--expected-solids must be at least 1")
    if args.angular_deflection > math.pi:
        parser.error("--angular-deflection must be at most pi radians")
    output = build(args.model, args.expected_solids, args.linear_deflection,
                   args.angular_deflection, step=args.step)
    print(f"Built and validated: {output}")
    print(f"Preview: {(output / 'preview.html').as_uri()}")
    print(f"Report: {output / 'report.json'}")


if __name__ == "__main__":
    main()
