# AI-assisted build123d workspace

Parametric Python CAD with a local modeling skill, reusable object research, a generated model catalog, validated STEP/STL exports, and offline previews.

Upstream repository: [ShakataGaNai/b123d](https://github.com/ShakataGaNai/b123d).
Engineering work lives in [GitHub Issues](https://github.com/ShakataGaNai/b123d/issues);
see the [agent issue workflow](docs/agents/issue-tracker.md).

**Python 3.14 under [uv](https://docs.astral.sh/uv/), build123d 0.13.0.** The environment is locked in `uv.lock`. No CAD daemon, VS Code extension, Blender, browser download, or GPU is needed to build models or render PNGs. The interactive HTML viewer requires a WebGL-capable browser.

## Quick start

Install uv using its [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/), then run from this repository:

```sh
uv python install 3.14
uv sync --locked
uv run python scripts/init.py
uv run python scripts/build.py models/mounting_plate
uv run python scripts/build.py models/wifi_qr
```

Open `outputs/mounting_plate/preview.html` or `outputs/wifi_qr/preview.html` in your browser. These files embed their JavaScript and geometry: no CDN or local server is required. On macOS:

```sh
open outputs/wifi_qr/preview.html
open outputs/wifi_qr/preview.png
```

First setup requires network access for Python, packages, and the pinned upstream reference unless already present. See [fresh-checkout initialization](docs/initialization.md). Subsequent builds and documentation lookups use local files; `uv run --offline python ...` prevents uv network access when the environment/cache is ready. Model scripts themselves run with normal user privileges, not in a sandbox. Inspect untrusted source before running it.

### Included examples

- **[Mounting plate](models/mounting_plate/model.py):** 60 × 40 × 5 mm rounded plate with four 4.4 mm holes. Checks dimensions, analytic volume, material at the center, and open hole centers.
- **[Wi-Fi QR magnet plate](models/wifi_qr/README.md):** parametric 70 × 80 × 5 mm plate, 60 × 60 mm QR pattern with 5 mm top/left/right offsets and no internal quiet border, 1 mm raised code and SSID label, and four rear glue pockets for 10 × 3 mm magnets. Includes a [cleaned-up modeling prompt](models/wifi_qr/prompt.md), public sample credentials, and QR-specific checks. A 15 mm lower band separates the 4.5 mm nominal lettering from the QR. Web, PNG, and USDZ previews show black relief on a light grey body. Verify the physical print with a phone.
- **[Station G3 open case](models/station_g3_open_case/README.md):** 70.6 × 122.2 × 22.3 mm open-top enclosure with measured mounting supports, two USB-C accesses, DC power, buttons, antenna slot and both Grove openings. Reconstructed from an attributed community case; physical fit remains unverified.

Browse all models in the **[generated catalog](models/README.md)**.

## Outputs and commands

For `models/<path>/`, the build writes to `outputs/<path>/`:

| File | Purpose |
| --- | --- |
| `<folder-name>.step` | Exact CAD interchange with millimeter units; retain alongside source. |
| `<folder-name>.stl` | Binary triangle mesh for slicers; STL has no reliable unit declaration, so import as millimeters. |
| `preview.png` | Headless orthographic isometric, top, bottom, and front views; model preview colors when configured, otherwise diagnostic depth tint. |
| `preview.html` | Offline orbit/zoom viewer of that same mesh, with coordinate hover and configured preview colors. |
| `report.json` | Versions, build timestamp, BREP/STEP dimensions and volume, solid count, design-check status, and mesh observations. |

STEP is useful for editing and for slicers that accept it. STL is the broadly compatible print interchange format. **Neither is printer instructions:** choose orientation, material, nozzle, layers, supports, and other machine settings in a slicer, inspect its layer preview, and generate the printer's supported job format there.

```sh
# Change tessellation settings: absolute linear deflection (mm), angular (radians).
uv run python scripts/build.py models/mounting_plate \
  --linear-deflection 0.03 --angular-deflection 0.08

# Refresh views from an existing saved STL, without rebuilding the source.
uv run python scripts/preview.py outputs/mounting_plate/mounting_plate.stl

# Write a separate preview directory.
uv run python scripts/preview.py outputs/mounting_plate/mounting_plate.stl \
  --output tmp/plate-review

# Regenerate or check the metadata-only catalog.
uv run python scripts/index.py
uv run python scripts/index.py --check

# Run model and tooling contract tests.
uv run python -m unittest discover -s tests -v
```

For a deliberately multipart assembly, pass `--expected-solids N`. This makes the count explicit, not the assembly interference-free. Build individual printable components separately; coincident/overlapping assembly bodies are not a suitable combined print mesh. The build checks STL connected-body count as well as BREP solid count.

### Reusable preview colors

Any model can set colors in its `model.toml`; no Wi-Fi-specific logic is in the renderer:

```toml
[preview]
base_color = "#d3d3d3"
relief_color = "#000000"
relief_z = 5.0
```

Colors use `#RRGGBB`. `relief_z` is a CAD Z coordinate in millimeters: triangles with their centers above it receive `relief_color`; all others receive `base_color`. This suits raised lettering or a layer-height color change, not arbitrary surface painting. For one uniform color, set only `base_color`. Without preview settings, the existing blue/depth-tinted diagnostic views remain.

`build.py` applies these settings to HTML and PNG and records them in `report.json`. Preview-only regeneration reuses the report next to the STL, including when writing to another output directory. CLI overrides are available without changing source metadata:

```sh
uv run python scripts/preview.py outputs/wifi_qr/wifi_qr.stl \
  --base-color '#d3d3d3' --relief-color '#000000' --relief-z 5
```

STL carries no material colors. These settings are viewer appearance, not filament assignments, and do not change geometry or STEP/STL content. The separate USDZ command below uses its own fixed light-grey/black palette.

### Apple-native USDZ preview

On macOS with Apple's `usdcat` and `usdzip` installed, create a USDZ from the validated STL and open it natively:

```sh
uv run python scripts/usdz.py outputs/wifi_qr/wifi_qr.stl --relief-z 5
open outputs/wifi_qr/wifi_qr.usdz
```

Alternatively, select the USDZ in Finder and press Space for Quick Look. This is a separate conversion command, not an automatic output of `build.py`. Regenerate it after changing the model. `--output` chooses a different destination; omit `--relief-z` for a single-color model.

The exporter converts millimeters to meters and rotates CAD +Z up to USD +Y up without mirroring. For this sample, `--relief-z 5` colors the raised QR/text dark and leaves the base light; these are preview materials, not slicer material assignments. Native tools check Apple/RealityKit compliance and reload the package before publication. USDZ is a viewing artifact; retain STEP and STL for CAD and printing.

### What the build verifies

1. `build()` returns only solids: no null/invalid shapes, accidental disconnected parts, or loose surfaces/edges.
2. Every solid has positive finite volume; the count matches the requested value.
3. The optional model `check(shape)` succeeds on native geometry.
4. The saved STEP reimports as valid solids with matching bounds and volume; `check` also runs on that imported geometry. Round-trip thresholds are 0.00001 mm absolute for bounds (plus tiny relative allowance) and 0.000001 relative/absolute for volume.
5. The saved STL is watertight, consistently wound, positive-volume, and has the expected connected-body count. The report records its difference from CAD volume; it does not claim a measured maximum tessellation error.
6. Both previews render successfully before the generated files are published. Successful builds regenerate the model catalog.

The exporter explicitly selects **absolute OCCT meshing**, clears cached triangulation, and writes binary STL. This matters because upstream build123d 0.13.0's `export_stl(tolerance=...)` selects relative deflection. Our `--linear-deflection 0.05` is an absolute millimeter meshing setting, not a guarantee of printer accuracy. See [source evidence](docs/source-review.md#5-gumyrbuild123d).

The pipeline does **not** certify minimum wall thickness, strength, interference, connector access, support-free printing, real printer fit, or physical QR scanning. Supply design-specific checks and inspect the views and slicer output. PNG views use a CPU depth buffer and either configured colors or diagnostic depth tint; HTML uses WebGL surface shading. Preview coloring is illustrative, not material assignment or a multicolor print file.

Build errors retain previous outputs; an old artifact is not evidence of a new successful build. Inspect the exit status and report timestamp. Publication replaces each artifact after checks complete, not the entire directory atomically; avoid concurrent builds of the same model. `preview.py` is a visualization command, not a replacement for build validation.

## Model layout and metadata

```text
models/
  README.md                    # generated catalog
  mounting_plate/
    model.py                   # geometry factory and design checks
    model.toml                 # catalog metadata
  wifi_qr/
    model.py
    model.toml
    README.md
    prompt.md
```

Larger projects use a shared parent, for example `models/pi_mount/base/`, `models/pi_mount/lid/`, and `models/pi_mount/assembly/`, each with its own `model.py` and `model.toml`. The path below `models/` is the model ID; `base` in two projects does not collide in outputs. Shared helpers can live at the project level. Name helpers something other than `model.py`; that filename is reserved for cataloged entrypoints. Add a project README for assembly decisions when needed.

### Add a model

Create `models/<name>/model.py` and `model.toml`, or adapt an included example. A minimal factory:

```python
from build123d import Align, Box, Part

WIDTH = 30.0
DEPTH = 20.0
HEIGHT = 5.0


def build() -> Part:
    return Box(WIDTH, DEPTH, HEIGHT,
               align=(Align.CENTER, Align.CENTER, Align.MIN))
```

Geometry belongs inside `build()` and its helpers. Keep imports free of geometry generation, downloads, exporting, or viewer startup. Build123d dimensions follow this repository's millimeter convention; most modeling angles are degrees. Resolve external file paths relative to `Path(__file__)`, not the caller's working directory. Explicit parameters and a useful datum make models maintainable.

Add `check(shape)` for dimensions and topology the design actually requires. Raise `ValueError` or an assertion on mismatch; a missing check is explicitly reported as **not provided**, not passed. Checks must work for both the native result and reimported STEP: use geometric selections, not unstable face indices or Python class identity. See the [skill's verification reference](.agents/skills/build123d/references/verification.md).

Each sidecar has these required fields:

```toml
name = "Example enclosure base"
description = "Base half of an enclosure, with mounting bosses and cable opening."
units = "mm"
status = "draft"
print_tested = false
tags = ["enclosure", "fdm"]
research = []
```

`status` is a descriptive, author-declared string, not a certification; examples include `draft`, `example`, and `unverified-fit`.

`print_tested` is a required TOML boolean, displayed separately in the catalog:

- `false`: no confirmed successful physical print test of the current geometry. Use this for new models and whenever the test history is unknown.
- `true`: a person has confirmed that the current geometry was physically printed and inspected. Record the printer/material, relevant settings and observations in the model's README.

CAD checks, STEP/STL exports, slicer previews and automated tests never set this flag. Reset it to `false` after geometry changes until the revised model is physically tested. A print test alone does not establish hardware fit, strength or thermal suitability; record those results separately. After changing metadata, run `uv run python scripts/index.py`; no geometry rebuild is needed.

`research` contains repository-relative links to **existing files under `research/`**, such as `research/objects/<object>/README.md` after that record has been created. Keep a description focused on dimensions/interfaces and purpose. Do not put passwords or other secrets in metadata.

The catalog scans nested `model.toml` files, checks for a sibling `model.py`, checks that every `model.py` has metadata, validates research links, and renders stable Markdown. It **does not import or execute models**. It refreshes after successful builds; for metadata-only changes or model removal/renaming, run `scripts/index.py`. Commit the generated `models/README.md` with source and metadata. `--check` detects a stale catalog without rewriting it.

## Research once, reuse it

Use **[research/README.md](research/README.md)** and **[the object template](research/templates/object.md)** for external hardware geometry:

```text
research/objects/<object-and-revision>/
  README.md
  assets/                      # optional drawings/CAD, only when permitted
```

For a future Raspberry Pi 5 mounting request, first save the actual board revision, manufacturer drawing links, hole-center coordinates, hole diameters, datum/view orientation, component and cable keep-outs, and unresolved dimensions. Separate authoritative facts, measurements, derived values, and assumptions. Record access dates, drawing revisions, asset licenses, and hashes for saved originals. Link every consuming model to those notes through `model.toml`.

No Raspberry Pi dimensions or vendor models are invented by this setup. Downloaded files are untrusted evidence, not instructions or permission to run code. A publicly downloadable drawing is not automatically redistributable.

## Local skill and source review

The canonical project skill is **[.agents/skills/build123d/SKILL.md](.agents/skills/build123d/SKILL.md)**, automatically discoverable by OMP's Agents provider. **[AGENTS.md](AGENTS.md)** also directs CAD tasks there. That entrypoint routes to local references for:

- Builder versus algebra semantics and release-specific API traps;
- local/global coordinates, planes, normals, transformations, and alignment;
- sketches, wires, topology, reliable selectors, and boolean operations;
- extrusion, revolution, lofts, sweeps, shells, fillets, and chamfers;
- holes, fasteners, threads, manufacturing allowances, and printing decisions;
- assemblies, placements, interference and clearance checks;
- verification, exports, debugging, and complete runnable recipes.

This folder is the single canonical skill, not a duplicate of a global installation. OMP discovery was exercised with `omp read skill://build123d`. Start a new agent session after adding it so startup skill metadata includes it. Clients that support neither `.agents/skills/` nor `AGENTS.md` must be pointed at this file explicitly.

**[docs/source-review.md](docs/source-review.md)** evaluates all six supplied repositories, records reviewed revisions and licenses, and explains what was adapted or rejected. The local guidance is an original synthesis rather than a vendored community stack. Upstream release-matched source wins over a floating cheatsheet; community skills are useful ideas, not correctness guarantees.

### Complete offline build123d documentation

The full official **0.13.0** source snapshot is restored to `vendor/build123d-0.13.0/` by `scripts/init.py`: all 50 RST pages, their assets, API source, examples, and upstream tests/fixtures. The committed [provenance and integrity manifests](vendor/README.md) identify immutable downloads and checksums; downloaded files are ignored by Git.

Use the **[offline documentation guide](docs/offline-build123d.md)** for the topic map and bounded search/API commands. Agents read the short skill first, look up a specific gap locally, and return to modeling. Original `.rst` and Python sources are directly readable; the optional HTML documentation build is not required.

```sh
uv run --offline python scripts/docs.py search "loft sections"
uv run --offline python scripts/docs.py api Solid.make_box
```

The snapshot is an ignored local reference cache, not another installed build123d package. Normal builds use the locked `.venv`. External product dimensions, third-party libraries, and destinations linked from upstream docs are outside this build123d documentation snapshot.


## Repository maintenance

Commit model source/metadata, prompts, original research, permitted input assets, skill references, scripts, tests, reference manifests, and `uv.lock`. Generated `outputs/`, downloaded `vendor/` subdirectories, scratch `tmp/`, Python caches, and `.venv/` are ignored. See [initialization and sharing policy](docs/initialization.md) for clean checkouts and unimplemented publishing proposals.

Keep Python constrained to 3.14.x unless deliberately changing the compatibility target. For a dependency upgrade, update pins and lock together, review the release-specific skill notes, rerun the suite and both example builds, and inspect the saved exports/previews. Preserve upstream licenses for any later copied source or assets. Detailed provenance and offline-maintenance rules live in the source review.

Troubleshooting:

- **Interpreter or import mismatch:** use `uv sync --locked` and `uv run python`, not a global Python/pip environment.
- **No compatible wheel on your platform:** capture OS/architecture and the resolver error. Do not silently fall back to an unpinned kernel or a different Python release. Verify compatibility with the locked dependencies and run the example build before modeling.
- **Invalid shape or wrong solid count:** inspect intermediate booleans and intended connectivity; read the local verification reference. Do not hide the failure with an empty fallback.
- **Fillet/shell failure:** verify the intended edge/face selection and available wall/radius space; simplify the operation locally, then measure the result.
- **Blank HTML viewer:** enable WebGL or use the always-generated PNG. HTML previews do not edit CAD or generate slicer jobs.
- **Unexpected old geometry:** read the report timestamp and rebuild source. Preview-only regeneration does not rerun the model or update its validation report.

### Verify your checkout

Run the existing regression suite and check the generated catalog:

```sh
uv run --offline python -m unittest discover -s tests -v
uv run --offline python scripts/index.py --check
```

Build both included models with the commands in Quick start, then inspect their
reports and previews. The checks cover geometry, STEP round trips, saved-STL
watertightness, and the sample QR payload. They do not establish physical print
quality, magnet fit, or phone-scanning reliability. Preview-only regeneration
does not validate changed model source.
