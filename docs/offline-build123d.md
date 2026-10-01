# Offline build123d reference

Use the **build123d 0.13.0** snapshot with this workspace's **uv Python 3.14** environment. Start with the [project skill](../.agents/skills/build123d/SKILL.md), then open only the references needed for the current model.

After checkout, run `uv sync --locked` and `uv run python scripts/init.py` once.
The original RST/Python reference is downloaded and checksum-verified; it is not
committed. See [initialization](initialization.md). Existing copies are verified
and reused without downloading. HTML and its optional dependencies are not needed
for agent lookup.

## Lookup workflow

1. Read the skill and choose the relevant topic below.
2. Search for a specific operation, parameter, or modeling concept:
   ```sh
   uv run --offline python scripts/docs.py search sweep
   uv run --offline python scripts/docs.py search sweep path --limit 3
   uv run --offline python scripts/docs.py search "revolute joint"
   ```
3. Read the returned **repo-relative file and line range**, plus the surrounding section if needed. Search returns at most six excerpts by default, five lines per excerpt, and two excerpts per file. It ranks exact terms, concentrated matches, definitions, and prose. Terms are case-insensitive literal substrings; all terms must occur within the same five-line window. Quoting groups shell arguments, not an exact-phrase search. No matches returns exit status 1; use fewer terms or the actual API spelling.
4. Confirm the installed API before coding:
   ```sh
   uv run --offline python scripts/docs.py api sweep
   uv run --offline python scripts/docs.py api Plane
   uv run --offline python scripts/docs.py api Solid.make_box
   uv run --offline python scripts/docs.py api RevoluteJoint --limit 35
   ```
   API lookup prints the installed signature, declared overloads when available, source location, and up to 20 docstring lines. `--limit N` changes the docstring bound; `--full` prints the complete docstring. Names may start with `build123d.`. An unknown symbol, expression, or non-callable property produces an error and exit status 1. For properties and constants, use search and source sections instead. API lookup rejects an installed version that differs from the snapshot.
5. Apply the confirmed API in the model. Follow the skill's build, measurement, export, and visual-inspection workflow. Do not reread the complete documentation or create a per-model test suite just to use the library.

The [lookup CLI](../scripts/docs.py) reads official `.rst`, `.md`, `.txt`, and `.py` files under `docs/`, `src/build123d/`, and `examples/`. It uses no network, search service, persisted index, or extra dependencies. Search does not import build123d. API lookup imports the installed library but does not evaluate expressions, instantiate the requested class, or execute example programs. It resolves data paths from the script location, independent of the working directory; outside this repo, invoke the script by its absolute path using this project's environment (for example, `uv run --offline --project /path/to/repo python /path/to/repo/scripts/docs.py api sweep`).

## Task-to-reference map

Read one relevant section, then use `api SYMBOL` for exact parameters. Example programs may include viewers, file writes, or optional dependencies: read and adapt the needed fragment instead of importing or running the whole example.

| Task | Official explanation | Source / example to inspect |
| --- | --- | --- |
| Choose builder or algebra modeling | [Builder concepts](../vendor/build123d-0.13.0/docs/key_concepts_builder.rst), [algebra concepts](../vendor/build123d-0.13.0/docs/key_concepts_algebra.rst) | [Builder examples](../vendor/build123d-0.13.0/docs/general_examples.py), [algebra counterparts](../vendor/build123d-0.13.0/docs/general_examples_algebra.py) |
| Build profiles, sketches, and solids | [BuildLine](../vendor/build123d-0.13.0/docs/build_line.rst), [BuildSketch](../vendor/build123d-0.13.0/docs/build_sketch.rst), [BuildPart](../vendor/build123d-0.13.0/docs/build_part.rst) | [Curve primitives](../vendor/build123d-0.13.0/src/build123d/objects_curve.py), [sketch primitives](../vendor/build123d-0.13.0/src/build123d/objects_sketch.py), [part primitives and holes](../vendor/build123d-0.13.0/src/build123d/objects_part.py) |
| Place parts, workplanes, or repeated features | [Moving objects](../vendor/build123d-0.13.0/docs/moving_objects.rst), [location arithmetic](../vendor/build123d-0.13.0/docs/location_arithmetic.rst) | [Plane, Location, Axis, Vector](../vendor/build123d-0.13.0/src/build123d/geometry.py); workplane and grid examples in [general examples](../vendor/build123d-0.13.0/docs/general_examples.py) |
| Select edges/faces for holes, fillets, or chamfers | [Topology selection](../vendor/build123d-0.13.0/docs/topology_selection.rst), [selector tutorial](../vendor/build123d-0.13.0/docs/tutorial_selectors.rst) | [Selection example](../vendor/build123d-0.13.0/docs/selector_example.py), [filter examples](../vendor/build123d-0.13.0/docs/topology_selection/filter_examples.rst), [sorting](../vendor/build123d-0.13.0/docs/topology_selection/sort_examples.rst), [grouping](../vendor/build123d-0.13.0/docs/topology_selection/group_examples.rst) |
| Extrude, loft, revolve, sweep, shell, or blend | [Operations](../vendor/build123d-0.13.0/docs/operations.rst) | [Part operations](../vendor/build123d-0.13.0/src/build123d/operations_part.py), [generic operations including sweep/fillet](../vendor/build123d-0.13.0/src/build123d/operations_generic.py), [algebra examples](../vendor/build123d-0.13.0/docs/general_examples_algebra.py) |
| Use direct topology methods such as `Solid.make_box` | [Direct API reference](../vendor/build123d-0.13.0/docs/direct_api_reference.rst) | [Solid](../vendor/build123d-0.13.0/src/build123d/topology/three_d.py), [Face and Shell](../vendor/build123d-0.13.0/src/build123d/topology/two_d.py), [Edge and Wire](../vendor/build123d-0.13.0/src/build123d/topology/one_d.py) |
| Model surfaces | [Surface modeling tutorial](../vendor/build123d-0.13.0/docs/tutorial_surface_modeling.rst), [heart token](../vendor/build123d-0.13.0/docs/tutorial_surface_heart_token.rst), [Gordon wing](../vendor/build123d-0.13.0/docs/tutorial_spitfire_wing_gordon.rst) | [Heart token code](../vendor/build123d-0.13.0/docs/heart_token.py), [wing code](../vendor/build123d-0.13.0/docs/spitfire_wing_gordon.py) |
| Assemble components or connect moving joints | [Assemblies](../vendor/build123d-0.13.0/docs/assemblies.rst), [joints](../vendor/build123d-0.13.0/docs/joints.rst), [joint tutorial](../vendor/build123d-0.13.0/docs/tutorial_joints.rst) | [Joint implementations](../vendor/build123d-0.13.0/src/build123d/joints.py), [hinge tutorial code](../vendor/build123d-0.13.0/docs/tutorial_joints.py) |
| Import CAD or export STEP, STL, SVG, DXF, or mesh formats | [Import/export](../vendor/build123d-0.13.0/docs/import_export.rst), [technical drawing tutorial](../vendor/build123d-0.13.0/docs/tech_drawing_tutorial.rst) | [Importers](../vendor/build123d-0.13.0/src/build123d/importers.py), [3D exporters](../vendor/build123d-0.13.0/src/build123d/exporters3d.py), [drawing code](../vendor/build123d-0.13.0/docs/technical_drawing.py) |
| Investigate unexpected geometry or API usage | [Tips](../vendor/build123d-0.13.0/docs/tips.rst), [debugging/logging](../vendor/build123d-0.13.0/docs/debugging_logging.rst) | Use bounded search, then inspect the matching implementation in [API source](../vendor/build123d-0.13.0/src/build123d/) or a focused upstream [test](../vendor/build123d-0.13.0/tests/) as reference; tests are not part of the CLI search corpus. |

## Complete reference and HTML

- [Official source table of contents](../vendor/build123d-0.13.0/docs/index.rst), [documentation directory and assets](../vendor/build123d-0.13.0/docs/).
- [Builder API reference](../vendor/build123d-0.13.0/docs/builder_api_reference.rst), [direct API reference](../vendor/build123d-0.13.0/docs/direct_api_reference.rst), [cheat sheet](../vendor/build123d-0.13.0/docs/cheat_sheet.rst).
- [Complete upstream examples](../vendor/build123d-0.13.0/examples/) and [tutorial contents](../vendor/build123d-0.13.0/docs/tutorials.rst). Some documentation examples also live in `docs/` and its subdirectories.
- [Pristine upstream snapshot](../vendor/build123d-0.13.0/) and [provenance/integrity notes](../vendor/README.md). Do not edit vendored files.
- [Generated HTML entry point](../outputs/docs/build123d-0.13.0/index.html), an optional human-facing view available after generation. Restore its extra assets with `uv run python scripts/init.py --html-assets`, install the locked documentation dependencies with `uv sync --locked --group docs`, and install system Graphviz (`dot` on `PATH`), then build without network:
  ```sh
  uv run --offline --group docs python scripts/build_docs.py
  ```
  Serve the output locally for interactive GLB examples, which need HTTP rather than a `file://` page:
  ```sh
  uv run --offline python -m http.server 8000 --directory outputs/docs/build123d-0.13.0
  ```
  Open `http://localhost:8000/`. Stop the server with Ctrl-C when finished.
  Use the HTML for rendered diagrams and navigation. Prefer bounded source/API lookups for agent context. Upstream prose includes links to external projects and websites; those destinations are not part of the local snapshot.

## HTML build notes

The optional builder resolves paths from its script location and blocks network
connections during generation. It renders the 50 upstream source pages plus
API-source and index pages. Source/API lookup does not depend on this build.

Sphinx reports four formatting warnings in upstream `ShapeList.group_by`, `ShapeList.sort_by`, and `Solid.extrude_until` docstrings. They do not prevent generation. The local overlay escapes absolute-curvature bars in another upstream docstring so RST renders `|κ|` correctly; it does not edit the snapshot or suppress warnings globally.

The HTML build uses local theme assets, MathJax/fonts, and a separately pinned [model-viewer bundle](../vendor/model-viewer-4.1.0.manifest.json). Remote hover tooltips/intersphinx lookups are disabled; local API pages and links remain. Followed external hyperlinks—including hosted PDF/EPUB downloads—still need internet. The three bundled GLBs need no optional remote decoder assets.

## Scope

The snapshot covers the official build123d 0.13.0 documentation, bundled assets, examples, API implementation, and upstream tests. It does not replace documentation for OCP/Open Cascade, CadQuery extensions, viewers, third-party libraries, or tools linked from the [external resources page](../vendor/build123d-0.13.0/docs/external.rst).

For real hardware, use the workspace's [object research workflow](../research/README.md) for manufacturer dimensions, revisions, tolerances, and evidence. Library examples cannot establish fit, strength, manufacturing suitability, or hardware dimensions. Some CAD tasks need additional algorithms, third-party tools, or new research; local documentation does not guarantee a solution to every possible design.
