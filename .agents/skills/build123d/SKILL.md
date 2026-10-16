---
name: build123d
description: Model and revise mechanical CAD with build123d; diagnose geometry failures, place assemblies, verify dimensions and clearances, and prepare STL/3MF or optional STEP for manufacturing.
---

# build123d mechanical modeling

Use this skill for Python-authored boundary-representation CAD in this repository. Target **build123d 0.13.0 / Python 3.14**, managed with uv. API facts below are checked against the upstream `v0.13.0` tag; manufacturing suggestions are starting points requiring process-specific validation.

## Sources and model layout

- Find existing work in [models/README.md](../../../models/README.md). Each model
  lives in `models/<name>/` or `models/<project>/<part>/`, with `model.py` and
  `model.toml`. Model IDs are relative folder paths. Edit source, never exports.
- Before modeling around hardware, read [the research contract](../../../research/README.md)
  and reuse or create `research/objects/<object>/`. Record sources, dimensions,
  datums, hardware revisions, uncertainties and downloaded-asset provenance;
  link the record in `model.toml`'s `research` array. A product name alone does not
  establish mounting geometry. Keep source facts separate from design allowances.
- **Measure first:** measure the object or reference mesh, then use simple primitives
  and rounded estimates with explicit fit allowances for ordinary holders. Reserve
  exact contour reconstruction for complexity or mating requirements that need it.
  For STL measurements, read [the STL skill](../stl-measurement/SKILL.md) before
  choosing features; use its section helper, registration and evidence handoff.
- Keep reusable helpers beside the model or in its project folder; reserve `model.py`
  for entrypoints. Put inputs beside source, not under `outputs/`, and resolve them
  from `__file__`. Treat downloaded Python as executable untrusted code.

Before constructing geometry, **read [models/MODULES.md](../../../models/MODULES.md)**.
Reuse matching modules instead of rebuilding their geometry. When adding,
changing, renaming, or removing a reusable module, update that registry's index
and contract in the same change. Follow its entry requirements and consumer
revalidation rules; this is part of completion, not optional follow-up.

## Modeling workflow

Use a modeling workflow, not TDD: build, measure critical geometry, export and
visually inspect. Separate per-model test suites are optional for explicitly
requested checks or unusual risks such as QR decoding. Maintain existing checks
when changing a model; do not create a test suite for every new part.

1. **Define the contract.** Record envelope, functional datums, mating dimensions,
   holes, wall/floor thickness, expected solids, material/process assumptions and
   calibrated fit allowances. Use millimeters and degrees, XY as the bed and +Z up
   unless a different manufacturing orientation is documented.
2. **Construct the model.** Prefer simple features: sketch/extrude for prismatic
   parts, revolve for rotational profiles, loft for transitions, sweep for paths.
   Read the matching reference before unfamiliar operations. Keep geometry inside
   functions: parameterless `build()` returns a fresh Solid, Part, or Compound of
   solids, not a builder. Imports must not build, export or open viewers. Separate
   named parameters from derived values; finish primary geometry before cosmetic edges.
3. **Check design intent.** Define `check(shape)` and raise on incorrect dimensions,
   interfaces, holes or other requirements. Validate parameter relationships and
   selector cardinality. The export CLI runs this on native geometry and, with
   `--step`, the saved/reimported STEP. Kernel validity alone does not establish fit.

## Completion gate

1. Run `uv run python scripts/build.py models/<path>` for STL + 3MF, previews and
   report. Add `--step` when exact CAD exchange and round-trip checks are needed.
   Exactly one solid is required by default; use `--expected-solids N` only for
   intentional multipart results. Export printable assembly components independently.
2. Read [the export verification contract](references/verification.md#at-export).
   Inspect `outputs/<path>/report.json`, `preview.png`, and relevant `preview.html`
   views. Both previews show the saved STL, not proof of exact BREP topology.
   Check critical geometry and hidden interiors separately; resolve failures at
   their first operation. Generic validity/watertightness does not establish fit,
   interference, strength, wall thickness or printability. Use the slicer before
   claiming readiness to print.
3. Keep `model.toml` accurate. Successful builds regenerate `models/README.md`;
   after adding/renaming/removing models or changing metadata alone, run
   `uv run python scripts/index.py`. Never hand-edit the catalog.
4. Report source/artifact paths, actual checks, units, researched hardware revision,
   assumptions and remaining limitations. Failed builds may leave old outputs;
   check report timestamps. 3MF is geometry-only, without slicer settings or an
   assembly tree. A successful default build removes an older same-stem STEP.
5. Before committing/publishing, follow [commit-driven completion](../../../docs/agents/issue-tracker.md#commit-driven-completion)
   and [commit-message rules](../../../AGENTS.md#git-commit-messages). Keep validation
   evidence in documentation, reports, issues or PRs, never in commit messages.

## Task-to-reference map

| Task or uncertainty | Read |
| --- | --- |
| Choose builder/algebra, prevent accidental state changes, look up common primitive dimensions | [API and construction semantics](references/api-and-semantics.md) |
| Place/rotate a feature, work on an angled face, reason about normals or `Align` | [Coordinate frames and placements](references/coordinates.md) |
| Select edges robustly, repair an open sketch, build faces with holes | [Topology and sketch validity](references/topology-and-sketches.md) |
| Extrude, revolve, loft, sweep, boolean, fillet, chamfer, or shell | [Feature operations](references/operations.md) |
| Size holes, counterbores, countersinks, thread interfaces, fasteners, or print allowances | [Hardware and manufacturing](references/hardware-and-manufacturing.md) |
| Model around a real object or reuse dimensions/assets | [Object research contract](../../../research/README.md) before geometry |
| Find, reuse, add, or change a reusable geometry module | [Module registry](../../../models/MODULES.md): imports, parameters, coordinate frames, examples, source/fit limits and maintenance requirements |
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
