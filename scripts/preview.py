"""Render an existing STL: headless PNG views and an offline HTML orbit viewer."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import numpy as np
import plotly.graph_objects as go
import trimesh


def load_mesh(path: Path) -> trimesh.Trimesh:
    # Merge STL's per-triangle vertices to inspect connectivity; no hole repair.
    mesh = trimesh.load_mesh(path, process=True)
    if not isinstance(mesh, trimesh.Trimesh) or mesh.is_empty:
        raise ValueError(f"No triangle mesh in {path}")
    if not np.isfinite(mesh.vertices).all():
        raise ValueError("Mesh contains non-finite coordinates")
    return mesh


def raster_view(
    mesh: trimesh.Trimesh, direction: tuple, up: tuple,
    face_colors: np.ndarray | None = None,
) -> np.ndarray:
    """Orthographic CPU z-buffer: no display server or painter-order artifacts."""
    forward = np.array(direction, dtype=float)
    forward /= np.linalg.norm(forward)
    right = np.cross(up, forward)
    right /= np.linalg.norm(right)
    vertical = np.cross(forward, right)
    points = (mesh.vertices - mesh.bounds.mean(axis=0)) @ np.array([right, vertical, forward]).T
    size = 700
    span = float(np.ptp(points[:, :2], axis=0).max()) * 1.12
    if span <= 0:
        raise ValueError("Mesh has zero projected extent")
    points[:, :2] = points[:, :2] * ((size - 1) / span) + (size - 1) / 2
    image = np.full((size, size, 3), 250, dtype=np.uint8)
    depth = np.full((size, size), -np.inf)
    light = forward + vertical * 0.6 - right * 0.3
    light /= np.linalg.norm(light)
    intensity = 0.4 + 0.6 * np.maximum(mesh.face_normals @ light, 0)
    colors = (intensity[:, None] * (
        np.array([69, 143, 181]) if face_colors is None else face_colors
    )).astype(np.uint8)
    for face_index, face in enumerate(mesh.faces):
        if mesh.face_normals[face_index] @ forward <= 0:
            continue
        triangle = points[face]
        low = np.maximum(np.floor(triangle[:, :2].min(axis=0)).astype(int), 0)
        high = np.minimum(np.ceil(triangle[:, :2].max(axis=0)).astype(int), size - 1)
        x0, y0 = low
        x1, y1 = high
        a, b, c = triangle
        determinant = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(determinant) < 1e-12 or x0 > x1 or y0 > y1:
            continue
        x, y = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
        wa = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / determinant
        wb = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / determinant
        wc = 1 - wa - wb
        z = wa * a[2] + wb * b[2] + wc * c[2]
        old = depth[y0:y1 + 1, x0:x1 + 1]
        visible = (wa >= -1e-9) & (wb >= -1e-9) & (wc >= -1e-9) & (z > old)
        old[visible] = z[visible]
        image[y0:y1 + 1, x0:x1 + 1][visible] = colors[face_index]
    # Head-on lighting alone hides embossed text and blind-pocket floors.
    # Tint by visible depth so orthographic views expose those features.
    surface = np.isfinite(depth)
    if face_colors is None and surface.any():
        nearest, farthest = depth[surface].max(), depth[surface].min()
        if nearest - farthest > 1e-6:
            fraction = ((depth[surface] - farthest) / (nearest - farthest))[:, None]
            near_color = np.array([69, 143, 181])
            far_color = np.array([210, 226, 236])
            tint = far_color + fraction * (near_color - far_color)
            illumination = image[surface].astype(float) / near_color
            image[surface] = np.clip(illumination * tint, 0, 255).astype(np.uint8)
    elif surface.any():
        # Keep recesses visible without replacing the configured material hue.
        recess = np.maximum(np.median(depth[surface]) - depth[surface], 0)
        if recess.max() > 1e-6:
            shade = 1 - 0.25 * recess / recess.max()
            image[surface] = (image[surface] * shade[:, None]).astype(np.uint8)
    return image[::-1]


def render(
    mesh: trimesh.Trimesh, output: Path, title: str, *,
    base_color: str | None = None, relief_z: float | None = None,
    relief_color: str = "#000000",
) -> None:
    """Preview the saved mesh, not a separately tessellated CAD shape."""
    face_colors = None
    if base_color is not None or relief_z is not None:
        body = np.array(to_rgb(base_color or "#d3d3d3")) * 255
        raised = np.array(to_rgb(relief_color)) * 255
        face_colors = np.tile(body, (len(mesh.faces), 1)).astype(np.uint8)
        if relief_z is not None:
            if not np.isfinite(relief_z):
                raise ValueError("relief_z must be finite millimeters")
            selected = mesh.triangles_center[:, 2] > relief_z + 1e-6
            if not selected.any():
                raise ValueError("No faces above relief_z; check the height in source millimeters")
            face_colors[selected] = raised
    output.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor="white")
    dimensions = " × ".join(f"{value:g}" for value in mesh.extents)
    color_note = ("Preview colors; not printer material assignments" if face_colors is not None
                  else "Depth tint for visibility; not material colors")
    figure.suptitle(f"{title}\nBounds: {dimensions} mm · orthographic views\n{color_note}", fontsize=14)
    views = (
        ("Isometric", (1, -1, 1), (0, 0, 1)),
        ("Top (+Z) · X right / Y up", (0, 0, 1), (0, 1, 0)),
        ("Bottom (−Z) · X left / Y up", (0, 0, -1), (0, 1, 0)),
        ("Front (−Y) · X right / Z up", (0, -1, 0), (0, 0, 1)),
    )
    for axis, (name, direction, up) in zip(axes.flat, views):
        axis.imshow(raster_view(mesh, direction, up, face_colors), interpolation="antialiased")
        axis.set_title(name, fontsize=11)
        axis.axis("off")
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    figure.savefig(output / "preview.png", dpi=150)
    plt.close(figure)

    vertices, faces = mesh.vertices, mesh.faces
    viewer = go.Figure(go.Mesh3d(
        x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
        i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
        color="#458fb5", flatshading=True,
        facecolor=None if face_colors is None else [
            f"rgb({r},{g},{b})" for r, g, b in face_colors
        ],
        # CAD triangulation includes very thin triangles. Plotly's default
        # face-normal epsilon visibly mis-shades them as recesses.
        lighting={"ambient": 0.5, "diffuse": 0.7, "specular": 0,
                  "facenormalsepsilon": 0, "vertexnormalsepsilon": 0},
        hovertemplate="X %{x:.2f} mm<br>Y %{y:.2f} mm<br>Z %{z:.2f} mm<extra></extra>",
    ))
    viewer.update_layout(
        title={"text": f"{escape(title)}<br><sup>mm · drag to orbit · scroll to zoom</sup>",
               "font": {"size": 18}},
        template="plotly_white", margin={"l": 0, "r": 0, "b": 0, "t": 75},
        scene={"aspectmode": "data", "xaxis_title": "X (mm)",
               "yaxis_title": "Y (mm)", "zaxis_title": "Z (mm)",
               "camera": {"up": {"x": 0, "y": 0, "z": 1},
                          "eye": {"x": 2.0, "y": -2.5, "z": 2.5},
                          "projection": {"type": "orthographic"}}},
    )
    page = viewer.to_html(include_plotlyjs=True, full_html=True,
                          config={"displaylogo": False, "responsive": True})
    page = page.replace("<head>", f"<head><title>{escape(title)} — CAD preview</title>", 1)
    (output / "preview.html").write_text(page)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stl", type=Path)
    parser.add_argument("--output", type=Path, help="Default: the STL's directory")
    parser.add_argument("--base-color", help="Body color, e.g. '#d3d3d3'")
    parser.add_argument("--relief-color", help="Color above --relief-z, default black")
    parser.add_argument("--relief-z", type=float, help="Raised-feature boundary in CAD millimeters")
    args = parser.parse_args()
    output = args.output or args.stl.parent
    report_path = args.stl.parent / "report.json"
    settings = json.loads(report_path.read_text()).get("preview", {}) if report_path.is_file() else {}
    for key in ("base_color", "relief_color", "relief_z"):
        if (value := getattr(args, key)) is not None:
            settings[key] = value
    if "relief_color" in settings and "relief_z" not in settings:
        parser.error("--relief-color requires --relief-z")
    render(load_mesh(args.stl), output, args.stl.stem, **settings)
    print(f"PNG: {(output / 'preview.png').resolve()}")
    print(f"HTML: {(output / 'preview.html').resolve()}")


if __name__ == "__main__":
    main()
