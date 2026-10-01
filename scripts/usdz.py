"""Convert a millimeter STL to Apple USDZ using macOS usdcat and usdzip."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

import numpy as np
import trimesh


def export_usdz(source: Path, output: Path, relief_z: float | None = None) -> None:
    """Preserve physical size; rotate CAD +Z up to USD +Y up, without reflection."""
    tools = {}
    for name in ("usdcat", "usdzip"):
        executable = shutil.which(name)
        if executable is None:
            raise RuntimeError(f"{name} is required; this command uses Apple's native USD tools")
        tools[name] = executable
    mesh = trimesh.load_mesh(source, process=True)
    if not mesh.is_volume or not mesh.is_watertight:
        raise ValueError("USDZ preview requires a watertight, consistently oriented STL")
    if not np.isfinite(mesh.vertices).all():
        raise ValueError("Mesh contains non-finite coordinates")
    if relief_z is not None and not np.isfinite(relief_z):
        raise ValueError("--relief-z must be finite")
    if output.suffix.lower() != ".usdz":
        raise ValueError("Output must have a .usdz extension")

    # Explicit meters avoid unit ambiguity in Apple viewers and AR placement.
    points = mesh.vertices[:, [0, 2, 1]].copy() * 0.001
    points[:, 2] *= -1
    normals = mesh.face_normals[:, [0, 2, 1]].copy()
    normals[:, 2] *= -1

    def vectors(values: np.ndarray) -> str:
        return ", ".join("(" + ", ".join(f"{float(v):.9g}" for v in row) + ")" for row in values)

    def integers(values) -> str:
        return ", ".join(str(int(value)) for value in values)

    relief = ""
    if relief_z is not None:
        selected = np.flatnonzero(mesh.triangles_center[:, 2] > relief_z + 1e-6)
        if not len(selected):
            raise ValueError("No faces above --relief-z; check the height in source millimeters")
        relief = f'''
        def GeomSubset "RaisedFeatures" (
            prepend apiSchemas = ["MaterialBindingAPI"]
        ) {{
            uniform token elementType = "face"
            uniform token familyName = "materialBind"
            int[] indices = [{integers(selected)}]
            rel material:binding = </Model/Materials/Dark>
        }}
'''
    stage = f'''#usda 1.0
(
    defaultPrim = "Model"
    metersPerUnit = 1
    upAxis = "Y"
)
def Xform "Model" (kind = "component") {{
    def Scope "Materials" {{
        def Material "Base" {{
            token outputs:surface.connect = </Model/Materials/Base/Surface.outputs:surface>
            def Shader "Surface" {{
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (0.65, 0.65, 0.65)
                float inputs:roughness = 0.65
                token outputs:surface
            }}
        }}
        def Material "Dark" {{
            token outputs:surface.connect = </Model/Materials/Dark/Surface.outputs:surface>
            def Shader "Surface" {{
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (0, 0, 0)
                float inputs:roughness = 0.65
                token outputs:surface
            }}
        }}
    }}
    def Mesh "Geometry" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    ) {{
        uniform token subdivisionScheme = "none"
        uniform token orientation = "rightHanded"
        point3f[] points = [{vectors(points)}]
        int[] faceVertexCounts = [{integers(np.full(len(mesh.faces), 3))}]
        int[] faceVertexIndices = [{integers(mesh.faces.ravel())}]
        normal3f[] normals = [{vectors(normals)}] (interpolation = "uniform")
        float3[] extent = [{vectors(np.array([points.min(axis=0), points.max(axis=0)]))}]
        rel material:binding = </Model/Materials/Base>
        uniform token subsetFamily:materialBind:familyType = "nonOverlapping"
        {relief}
    }}
}}
'''
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".usdz-", dir=output.parent) as directory:
        work = Path(directory)
        text, binary, package = work / "model.usda", work / "model.usdc", work / output.name
        text.write_text(stage)
        subprocess.run([tools["usdcat"], str(text), "-o", str(binary)], check=True)
        subprocess.run([tools["usdzip"], "--arkitAsset", str(binary),
                        "--checkCompliance", str(package)], check=True)
        subprocess.run([tools["usdcat"], "--loadOnly", str(package)], check=True)
        package.replace(output)
    print(f"USDZ: {output}")
    print(f"Dimensions (CAD mm): {mesh.extents.tolist()}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stl", type=Path)
    parser.add_argument("--output", type=Path, help="Default: STL path with .usdz extension")
    parser.add_argument("--relief-z", type=float,
                        help="Color faces above this CAD Z height (mm) dark; preview materials only")
    args = parser.parse_args()
    export_usdz(args.stl, args.output or args.stl.with_suffix(".usdz"), args.relief_z)


if __name__ == "__main__":
    main()
