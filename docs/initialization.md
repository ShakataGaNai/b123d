# Fresh checkout and sharing

## Initialize for agent-assisted modeling

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run from the repository root:

```sh
uv python install 3.14
uv sync --locked
uv run python scripts/init.py
uv run --offline python scripts/docs.py search "loft sections" --limit 3
uv run --offline python scripts/docs.py api Solid.make_box
uv run --offline python scripts/build.py models/mounting_plate
```

Initialization downloads the **pinned build123d 0.13.0 source archive**, checks its SHA-256 and every inventoried file, then installs it under `vendor/build123d-0.13.0/`. This supplies the original RST documentation, Python API source/docstrings, examples, and assets. Agents read these directly through the [skill](../.agents/skills/build123d/SKILL.md) and [bounded lookup workflow](offline-build123d.md); no HTML build, Graphviz, or Sphinx is needed.

The script uses the Python standard library and resolves paths from its own location. It downloads no Python packages and does not run upstream code. Runtime dependencies are the separate `uv sync --locked` step.

- Initial setup needs network access to obtain missing Python/packages and the reference archive.
- Repeating initialization verifies existing references and makes no download when they match. Ordinary model builds and lookups never invoke initialization implicitly.
- A corrupt or incomplete existing reference produces an error and is left untouched. Move that directory aside, then rerun initialization; do not edit checksum pins to accept unexpected bytes.
- Downloads are unpacked in a temporary directory and published only after verification. Failed initialization does not publish a partial reference tree.
- For an air-gapped machine, provision the locked Python environment and copy the matching `vendor/build123d-0.13.0/` tree beforehand. Initialization can verify that copy without network. A Git checkout alone intentionally does not contain third-party reference data.
- Your platform needs compatible wheels for the locked dependencies. Run the example build to check the environment before modeling. USDZ conversion is a separate macOS-only option.

Model exports appear under `outputs/mounting_plate/`: STL + 3MF, PNG/HTML previews, and a validation report. Add `--step` to the build command for STEP export and reimport checks. The 3MF is geometry-only with millimeter units, not a slicer project or material assignment. Review the geometry and report; exporting successfully does not certify a physical print or fit.

## What belongs in Git

| Keep in Git | Keep out of Git |
| --- | --- |
| `models/` source, metadata, prompts, model notes, generated Markdown catalog | Generated `outputs/`: STL/3MF/STEP/USDZ, previews, reports, rendered documentation |
| `.agents/skills/`, `AGENTS.md`, project-authored `docs/`, README | Downloaded upstream reference directories under `vendor/` |
| `scripts/`, `tests/`, `pyproject.toml`, `.python-version`, `uv.lock` | `.venv/`, Python caches, scratch `tmp/` |
| Root-level `vendor/*.manifest.json` and `vendor/README.md` | Download archives and optional browser documentation runtime |
| Original research and licensed, necessary model inputs | Private credentials, confidential inputs, or assets without redistribution permission |

The generated Markdown model catalog is intentionally retained: it is small, useful when browsing the repository, and regenerated from model metadata. Binary outputs are derived artifacts and would otherwise grow Git history on every edit. Keep indispensable input geometry beside the model or research notes—not in `outputs/`—with provenance and license information.

Ignore rules do not untrack files already in Git. Before the initial commit, make sure no downloaded reference trees or outputs are staged. Do not force-add ignored directories.

## Sharing designs

**Default: source in Git, finished printable designs on Printables.** Publish reviewed STL/3MF files, optionally STEP for remixing (build with `--step`), photos/previews, dimensions, material/orientation guidance, and the license you choose. Link the source revision or tag in the listing. Check for private data before publishing, especially Wi-Fi credentials encoded in QR geometry.

Use a **GitHub Release** when you want downloadable exports alongside their exact source version:

1. Commit the intended source and dependency lockfile; use a clean working tree.
2. Tag that revision with a meaningful release name, such as `wifi-qr-v1.0.0`.
3. Build the model from that tagged source and inspect the saved artifacts.
4. Attach a bundle of the model's STL/3MF, optional STEP (requested with `--step`), previews, and `report.json` to the release. Name it after the model and tag; record the full Git commit SHA in the release notes along with the build command and any parameter overrides.

The report records library versions, build time, and geometry checks; it does **not** currently record Git revision. Filename/tag plus release notes provide that association. A Git SHA identifies source, not proof of a successful build or byte-identical CAD exports across platforms.

**Planned publishing lives in GitHub Issues:** [#1 — GitHub Releases downloads](https://github.com/ShakataGaNai/b123d/issues/1) and [#2 — GitHub Pages model preview gallery](https://github.com/ShakataGaNai/b123d/issues/2). Implementation and the choice of manual publishing versus CI are deferred to those issues. Generated artifacts should remain outside the source branch. Pages will be a gallery of model previews, not the optional upstream library documentation site. No publishing service is configured yet; use the [issue workflow](agents/issue-tracker.md) for all additional engineering work.

## Optional human-readable library site

Only if you want the upstream HTML documentation:

```sh
uv run python scripts/init.py --html-assets
uv sync --locked --group docs
# Install system Graphviz separately so `dot` is on PATH.
uv run --offline --group docs python scripts/build_docs.py
```

`--html-assets` also restores the pinned model-viewer runtime used by the upstream interactive examples. Both downloaded directories and generated HTML remain ignored. See [offline documentation](offline-build123d.md) for local serving instructions. These steps are unrelated to the model preview HTML generated by normal CAD builds.
