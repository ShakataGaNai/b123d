# AI CAD workspace

## Start here

For creating, modifying, inspecting, or exporting CAD, read
[`.agents/skills/build123d/SKILL.md`](.agents/skills/build123d/SKILL.md), then only
the references matching the task. This is the canonical project skill,
discoverable by OMP's Agents provider; do not install a second copy.

Use Python **3.14 under uv** (`uv sync --locked`; `uv run python ...`).
`pyproject.toml`, `.python-version`, and `uv.lock` own the environment. Use the
pinned build123d APIs, not examples for a different release.
On a fresh checkout, follow [initialization](docs/initialization.md):
`uv sync --locked`, then `uv run python scripts/init.py` to restore the pinned
agent-readable reference. Downloaded `vendor/` trees and `outputs/` stay out of Git.

For build123d questions beyond the skill, use the
[offline documentation guide](docs/offline-build123d.md). Official 0.13.0
docs, assets, examples, and API source are in `vendor/build123d-0.13.0/`.
Use bounded local lookup and read the relevant section, not the whole tree.
Routine library questions and model builds require no web research.

## Source and research

- Find existing work in [`models/README.md`](models/README.md). Each model lives
  in `models/<name>/`, or `models/<project>/<part>/`, with `model.py` and
  `model.toml`. Edit source, never generated STEP/STL.
- Before modeling around real hardware, reuse or create object research under
  `research/objects/<object>/`. Read [`research/README.md`](research/README.md)
  for the evidence contract and template. Save sources, dimensions, datums,
  hardware revisions, uncertainties, and downloaded-asset provenance. Link the
  notes in the model's `model.toml` `research` array. A nominal product name is
  not evidence for its mounting geometry.
- For measurements or reconstruction from existing STL files, read
  [the STL measurement skill](.agents/skills/stl-measurement/SKILL.md) for its
  runnable section helper, coordinate registration and evidence-to-CAD handoff.
- Keep reusable geometry helpers beside the model or in its project folder;
  reserve `model.py` for model entrypoints. Model IDs are their relative folder
  paths. Put inputs beside source, not under `outputs/`. Resolve file inputs
  from `__file__`, and treat downloaded Python as executable untrusted code.
- `build()` returns a fresh Solid, Part, or Compound of solids. Build geometry
  inside functions; imports do not export files, open viewers, or run builds.
  Define `check(shape)` for design-specific dimensions, interfaces, and holes;
  raise on failure. It runs on native geometry and the saved/reimported STEP.
- Use millimeters and degrees for geometry, with XY as the bed and +Z up unless
  the model explicitly documents a different manufacturing orientation.
  Explain functional datums, critical dimensions, material/process assumptions,
  and calibrated fit allowances. Keep design intent separate from source facts.

## Completion gate
Use a modeling workflow, not TDD: build, measure critical geometry, export,
and visually inspect. Separate per-model test suites are optional, reserved
for explicitly requested checks or unusual risks such as QR decoding.
Maintain existing checks when changing their model; do not create a test
suite for every new part.


1. Run `uv run python scripts/build.py models/<path>`. Exactly one solid is
   required by default; use `--expected-solids N` only for intentional multipart
   results. Export printable assembly components independently.
2. Inspect `outputs/<path>/report.json`, `preview.png`, and relevant views in
   `preview.html`. Both previews show the exported STL, not proof of exact BREP
   topology. Generic validity/watertightness checks are not fit, interference,
   strength, wall-thickness, or printability checks. Add requirement-specific
   measurements and use the slicer before claiming readiness to print.
3. Keep `model.toml` accurate. Successful builds regenerate `models/README.md`;
   after adding/renaming/removing models or editing metadata alone, run
   `uv run python scripts/index.py`. Never hand-edit the catalog.
4. Report source and artifact paths, actual checks, units, researched hardware
   revision, assumptions, and remaining limitations. A failed build may leave
   older outputs; check the report timestamp rather than claiming they are new.

For tooling changes, run `uv run python -m unittest discover -s tests -v` and
exercise the affected CLI end to end. Keep generated artifacts, `.venv/`, and
scratch work in the ignored locations. Commit `uv.lock`; refresh it only as an
intentional dependency change. Model code runs with normal user privileges;
this workspace is not a sandbox.

## Agent skills

### Issue tracker

Issues live in GitHub Issues (`ShakataGaNai/b123d`), via the `gh` CLI.
See [docs/agents/issue-tracker.md](docs/agents/issue-tracker.md).

**Every engineering work item goes here—no exceptions.** Bugs found during other
work, deferred follow-ups, unresolved root causes, and TODOs all need GitHub issues.
This repository's tracker takes precedence over personal task-tracker preferences
in global/user agent instructions. Personal task lists are not an engineering
tracker. Session checklists may mirror issue steps; they do not replace the shared
record. `TODO.md` is known limitations only, not a work queue.

Keep public documentation portable. Omit personal profiles, local account details,
absolute machine paths, and setup-session history. Use project-relative paths and
document platform requirements rather than a contributor's machine configuration.
