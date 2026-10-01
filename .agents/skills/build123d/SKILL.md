---
name: build123d
description: Model and revise mechanical CAD with build123d; diagnose geometry failures, place assemblies, verify dimensions and clearances, and prepare STEP/STL for manufacturing.
---

# build123d mechanical modeling

Use this skill for Python-authored boundary-representation CAD in this repository. Target **build123d 0.13.0 / Python 3.14**, managed with uv. API facts below are checked against the upstream `v0.13.0` tag; manufacturing suggestions are starting points requiring process-specific validation.

## Workflow

1. **Define the contract.** Record overall envelope, datums, mating dimensions, hole diameters/centers, wall/floor thickness, expected number of solids, and manufacturing process. Separate required dimensions from assumptions. Use millimeters and degrees; the print bed is XY and +Z is up.
2. **Choose a construction.** Use sketch/extrude for prismatic parts, revolve for rotational profiles, loft for changing sections, and sweep for constant sections along paths. Prefer a small number of meaningful features to a tessellation-like pile of primitives. Read the corresponding reference below before using an unfamiliar operation.
3. **Build the functional geometry.** Put construction inside parameterless `build()` in `models/<name>/model.py`, with a `model.toml` metadata sidecar; nested `models/<project>/<part>/` folders are supported. Return a build123d `Part`, `Solid`, or `Compound`, not a builder. Keep named design parameters and derived dimensions separate. Finish primary volumes and cuts before cosmetic edge treatments. Store reusable real-object dimensions and source evidence in `research/objects/<object>/README.md`, and link that path in the model metadata's `research` list rather than duplicating research.
4. **Make intent checkable.** Add `check(shape)` for design-specific assertions: envelope, critical wall/floor thickness, hole position/radius, analytical volume where available, or mating gap. Assert expected selector cardinality before modifying selected features. Validate parameter relationships before constructing geometry.
5. **Run the actual export path.** Run `uv run python scripts/build.py models/<name>`. One solid is the default; declare intentional multipart geometry with `--expected-solids N`. Inspect the STEP/STL, `preview.png`, offline `preview.html`, and `report.json` under `outputs/<relative model path>/`. Successful builds regenerate `models/README.md` from metadata; `uv run python scripts/index.py` regenerates the index without executing geometry. A successful export does not establish dimensional correctness.
6. **Inspect and iterate.** Review the generated iso/top/bottom/front views and inspect interior sections separately where relevant. Check every critical dimension and fit. If a boolean or edge treatment fails, isolate the first failing operation rather than hiding it. Finish only when exported geometry, checks, and visual inspection agree with the contract.

## Task-to-reference map

| Task or uncertainty | Read |
| --- | --- |
| Choose builder/algebra, prevent accidental state changes, look up common primitive dimensions | [API and construction semantics](references/api-and-semantics.md) |
| Place/rotate a feature, work on an angled face, reason about normals or `Align` | [Coordinate frames and placements](references/coordinates.md) |
| Select edges robustly, repair an open sketch, build faces with holes | [Topology and sketch validity](references/topology-and-sketches.md) |
| Extrude, revolve, loft, sweep, boolean, fillet, chamfer, or shell | [Feature operations](references/operations.md) |
| Size holes, counterbores, countersinks, thread interfaces, fasteners, or print allowances | [Hardware and manufacturing](references/hardware-and-manufacturing.md) |
| Model around a real object or reuse dimensions/assets | [Object research contract](../../../research/README.md) before geometry |
| Recover dimensions/feature depths from STL, register exported parts, or reconstruct mesh-derived CAD | [STL measurement skill](../stl-measurement/SKILL.md) before choosing parametric features |
| Add reproducible text or a scannable QR marking | [Wi-Fi QR example](../../../models/wifi_qr/README.md): explicit `font_path` and quiet zone/contrast; use the research contract above for actual reused hardware |
| Position separate components, preserve a BOM-like tree, measure interference/clearance | [Assemblies](references/assemblies.md) |
| Validate geometry, investigate a failure, distinguish CAD validity from print readiness | [Verification and troubleshooting](references/verification.md) |
| Start from a complete plate, enclosure, turned part, sweep, loft, or assembly | [Runnable recipes](references/recipes.md) |
| Trace upstream material and distinguish inspiration from checked API evidence | [Canonical source review](../../../docs/source-review.md) |
| Find an uncommon API, an advanced technique, or full official documentation | [Offline documentation guide](../../../docs/offline-build123d.md): bounded local search, API lookup, and the complete pinned upstream snapshot |

## Version guardrails

- `shape.is_valid`, `shape.is_null`, and `shape.is_manifold` are **properties**, not calls. `shape.bounding_box()`, `shape.solids()`, and `face.normal_at()` are methods. A null shape can report valid: check both emptiness and validity.
- Use `insert()` to place prebuilt geometry into a builder; `add()` is deprecated in 0.13.0.
- Builders construct locally and apply output placements when publishing results. A constructor inside a builder has already affected its state before a chained `.moved(...)` runs. Use `Locations` before construction.
- Radii are not diameters. `Circle`, `Cylinder`, `Hole`, `CounterBoreHole`, and `CounterSinkHole` use radii. Convert named diameters once at the API boundary.
- `extrude(amount=h, both=True)` produces **2h** total extent. Explicit `Hole(depth=d)` in 0.13.0 constructs a symmetric cutter extending `d` each side of its origin; use an explicitly positioned cylinder for controlled blind cuts.
- Library lookup stays local: use the relevant reference first, then `uv run --offline python scripts/docs.py search "topic"` or `api SYMBOL`, then read only the returned source range. The complete official 0.13.0 docs, assets, examples, and API source live in `vendor/build123d-0.13.0/`. Do not browse upstream for routine modeling or reread the whole snapshot. Network research is for external hardware, separate libraries, or a deliberate version upgrade—not facts already available locally.
