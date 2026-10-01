"""Inspect original STL coordinates and axis-aligned sections; never repair a mesh."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import trimesh


CIRCLE_RELATIVE_TOLERANCE = 0.005
SAMPLE_COUNT = 256


def load_stl(path: Path) -> tuple[trimesh.Trimesh, dict]:
    # Open only STL data, irrespective of filename; never dispatch to other loaders.
    with path.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
        source.seek(0)
        mesh = trimesh.load_mesh(source, file_type="stl", process=False)
    if not isinstance(mesh, trimesh.Trimesh) or mesh.is_empty:
        raise ValueError("STL contains no triangles")
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces)
    if not np.isfinite(vertices).all():
        raise ValueError("STL contains non-finite vertex coordinates")
    if faces.ndim != 2 or faces.shape[1] != 3 or faces.min() < 0 or faces.max() >= len(vertices):
        raise ValueError("STL contains invalid triangle indices")
    # STL repeats vertices per triangle. Exact indexing changes no coordinates,
    # triangles or winding, unlike process=True's tolerance-based cleanup.
    unique, inverse = np.unique(vertices, axis=0, return_inverse=True)
    mesh = trimesh.Trimesh(vertices=unique, faces=inverse[faces], process=False)
    spans = np.ptp(unique, axis=0)
    if not np.isfinite(spans).all() or float(spans.max()) <= 0:
        raise ValueError("STL has unusable or zero extent")
    area = mesh.area_faces
    if not np.isfinite(area).all() or not np.any(area > 0):
        raise ValueError("STL has non-finite or entirely degenerate triangle areas")
    degenerate = int(np.count_nonzero(area <= 0))
    warnings = []
    if degenerate:
        warnings.append("Zero-area triangles retained; sections may be ambiguous")
    if not mesh.is_watertight:
        warnings.append("Open/non-manifold mesh: closed sections do not prove a solid")
    if not mesh.is_winding_consistent:
        warnings.append("Inconsistent winding: inside/outside interpretation is unreliable")
    report = {
        "file": path.as_posix(),
        "sha256": digest,
        "units": {"status": "unknown", "coordinates": "native STL units", "reason": "STL has no unit declaration"},
        "versions": {"numpy": np.__version__, "trimesh": trimesh.__version__},
        "triangles": len(faces),
        "exact_unique_vertices": len(unique),
        "bounds_xyz": mesh.bounds.tolist(),
        "spans_xyz": spans.tolist(),
        "mesh_checks": {
            "finite_coordinates": True,
            "degenerate_triangles": degenerate,
            "watertight": bool(mesh.is_watertight),
            "winding_consistent": bool(mesh.is_winding_consistent),
            "self_intersections": "not checked",
            "physical_validity": "not established",
        },
        "processing": "Exact-coordinate vertex indexing only; no repair, scaling or recentering",
        "warnings": warnings,
    }
    return mesh, report


def circle_fit(points: np.ndarray, closed: bool) -> dict:
    """Fit the entire perimeter, not just vertices that can hide polygon corners."""
    rejected = {"accepted": False}
    if not closed:
        return rejected | {"reason": "open contour; no full-circle fit"}
    if len(points) < 4:
        return rejected | {"reason": "too few contour points"}
    # Center first for large translated coordinates, then normalize conditioning.
    origin = points.min(axis=0) + np.ptp(points, axis=0) / 2
    scale = float(np.ptp(points, axis=0).max())
    if not math.isfinite(scale) or scale <= 0:
        return rejected | {"reason": "degenerate contour extent"}
    local = (points - origin) / scale
    end = np.roll(local, -1, axis=0)
    lengths = np.linalg.norm(end - local, axis=1)
    keep = lengths > 0
    local, end, lengths = local[keep], end[keep], lengths[keep]
    if len(local) < 3:
        return rejected | {"reason": "degenerate contour perimeter"}
    cumulative = np.concatenate(([0.0], np.cumsum(lengths)))
    distances = np.arange(SAMPLE_COUNT) * cumulative[-1] / SAMPLE_COUNT
    indices = np.searchsorted(cumulative, distances, side="right") - 1
    fraction = (distances - cumulative[indices]) / lengths[indices]
    samples = local[indices] + fraction[:, None] * (end[indices] - local[indices])
    design = np.column_stack((2 * samples, np.ones(SAMPLE_COUNT)))
    solution, _, rank, singular = np.linalg.lstsq(design, np.sum(samples * samples, axis=1), rcond=None)
    if rank != 3 or singular[-1] / singular[0] < 1e-8:
        return rejected | {"reason": "ill-conditioned circle fit"}
    center = solution[:2]
    radius_squared = solution[2] + center @ center
    if not math.isfinite(radius_squared) or radius_squared <= 0:
        return rejected | {"reason": "no finite positive radius"}
    radius = math.sqrt(radius_squared)
    # Geometric least squares after the algebraic initialization. Retain every
    # sample: trimming outliers could disguise a slot, notch or flattened arc.
    for _ in range(12):
        delta = samples - center
        radial = np.linalg.norm(delta, axis=1)
        if np.any(radial <= 1e-12):
            return rejected | {"reason": "unstable circle center"}
        jacobian = np.column_stack((-delta / radial[:, None], -np.ones(SAMPLE_COUNT)))
        step, _, rank, _ = np.linalg.lstsq(jacobian, radius - radial, rcond=None)
        if rank != 3 or not np.isfinite(step).all():
            return rejected | {"reason": "unstable geometric circle fit"}
        center += step[:2]
        radius += step[2]
        if radius <= 0 or not np.isfinite(center).all() or not math.isfinite(radius):
            return rejected | {"reason": "no finite positive geometric radius"}
        if np.linalg.norm(step) < 1e-12:
            break
    # A partial arc can have an enormous, meaningless extrapolated radius.
    if radius > 2 or radius < 1e-8:
        return rejected | {"reason": "radius incompatible with full-contour span"}
    # Check all original vertices AND closest points on every segment, not just
    # the fixed sampling grid. This catches narrow notches and long chord edges.
    edges = end - local
    projection = np.clip(np.sum((center - local) * edges, axis=1) / lengths**2, 0, 1)
    closest = local + projection[:, None] * edges
    vertex_radial = np.linalg.norm(local - center, axis=1)
    nearest_radial = np.linalg.norm(closest - center, axis=1)
    maximum = float(np.max(np.abs(np.concatenate((vertex_radial, nearest_radial)) - radius)))
    residuals = np.linalg.norm(samples - center, axis=1) - radius
    rms = float(np.sqrt(np.mean(residuals**2)))
    angles = np.arctan2(local[:, 1] - center[1], local[:, 0] - center[0])
    changes = (np.roll(angles, -1) - angles + np.pi) % (2 * np.pi) - np.pi
    winding = float(np.sum(changes) / (2 * np.pi))
    ordered_angles = np.sort(angles % (2 * np.pi))
    largest_gap = float(np.diff(np.append(ordered_angles, ordered_angles[0] + 2 * np.pi)).max())
    reasons = []
    if abs(abs(winding) - 1) > 1e-6 or not (np.all(changes >= -1e-8) or np.all(changes <= 1e-8)):
        reasons.append("contour does not wind once monotonically around center")
    if largest_gap > np.pi / 4:
        reasons.append("insufficient angular coverage or coarse faceting")
    if maximum / radius > CIRCLE_RELATIVE_TOLERANCE:
        reasons.append("whole-perimeter radial residual exceeds tolerance")
    result = {
        "accepted": not reasons,
        "reason": "; ".join(reasons) if reasons else "full near-circular contour; feature type unclassified",
        "residual_rms": rms * scale,
        "residual_max": maximum * scale,
        "residual_max_over_radius": maximum / radius,
        "largest_vertex_angle_gap_degrees": math.degrees(largest_gap),
    }
    # Rejected contours retain diagnostics, not a misleading center/diameter.
    if not reasons:
        result.update(center_uv=(origin + center * scale).tolist(), diameter=2 * radius * scale)
    return result


def section_report(mesh: trimesh.Trimesh, axis: str, offset: float, start: int, limit: int) -> dict:
    normal_axis = "xyz".index(axis)
    plane_axes = [index for index in range(3) if index != normal_axis]
    normal = np.zeros(3)
    normal[normal_axis] = 1
    origin = np.zeros(3)
    origin[normal_axis] = offset
    section = mesh.section(plane_normal=normal, plane_origin=origin)
    contours = []
    if section is not None:
        # Path.discrete/polygons may pull in optional networkx/shapely. STL
        # sections already carry ordered polyline vertex indices on entities.
        for entity in section.entities:
            points = np.asarray(section.vertices[entity.points])[:, plane_axes]
            if not len(points) or not np.isfinite(points).all():
                raise ValueError("Section produced empty or non-finite contour coordinates")
            closed = bool(entity.closed)
            if closed:
                points = points[:-1]
            if not len(points):
                raise ValueError("Section produced an empty closed contour")
            bounds = np.array([points.min(axis=0), points.max(axis=0)])
            contours.append({
                "closed": closed,
                "vertices": len(points),
                "bounds_uv": bounds.tolist(),
                "spans_uv": (bounds[1] - bounds[0]).tolist(),
                "circle": circle_fit(points, closed),
            })
    contours.sort(key=lambda item: tuple(np.array(item["bounds_uv"]).ravel()))
    for index, contour in enumerate(contours):
        contour["index"] = index
    return {
        "axis": axis,
        "offset": offset,
        "plane_axes_uv": "".join("xyz"[index] for index in plane_axes),
        "status": "intersection" if contours else "no intersection",
        "contour_count": len(contours),
        "closed_contour_count": sum(item["closed"] for item in contours),
        "accepted_circle_count": sum(item["circle"]["accepted"] for item in contours),
        "circle_policy": {
            "maximum_radial_residual_over_radius": CIRCLE_RELATIVE_TOLERANCE,
            "maximum_vertex_angle_gap_degrees": 45,
            "perimeter_fit_samples": SAMPLE_COUNT,
            "feature_type": "unclassified: circle is not proof of a hole or through-cut",
        },
        "start": start,
        "returned": len(contours[start:start + limit]),
        "omitted": len(contours) - len(contours[start:start + limit]),
        "contours": contours[start:start + limit],
        "caveats": [
            "Spans are axis-aligned bounds, not diameters",
            "Sections use trimesh intersection/path tolerances; near-coplanar or tiny features need independent checks",
            "Repeat offsets away from coplanar faces; one closed contour cannot establish a blind bottom or through-hole",
        ],
    }


def finite_number(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise argparse.ArgumentTypeError("must be finite")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="hash, bounds, units status and non-repairing mesh checks")
    inspect.add_argument("file", type=Path)
    section = commands.add_parser("section", help="axis-aligned plane contours and conservative circle candidates")
    section.add_argument("file", type=Path)
    section.add_argument("--axis", choices=("x", "y", "z"), required=True)
    section.add_argument("--offset", type=finite_number, required=True, help="plane coordinate in unchanged native units")
    section.add_argument("--start", type=int, default=0, help="first contour index, sorted by bounds")
    section.add_argument("--max-loops", type=int, default=40, help="maximum returned contours, 1..200 (default 40)")
    args = parser.parse_args()
    if args.command == "section" and (args.start < 0 or not 1 <= args.max_loops <= 200):
        parser.error("--start must be nonnegative and --max-loops must be 1..200")
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            mesh, report = load_stl(args.file)
            if args.command == "section":
                report["section"] = section_report(mesh, args.axis, args.offset, args.start, args.max_loops)
        print(json.dumps(report, indent=2, allow_nan=False))
    except (OSError, ValueError, TypeError, IndexError, FloatingPointError, np.linalg.LinAlgError) as error:
        print(json.dumps({"error": str(error), "file": args.file.as_posix()}, allow_nan=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
