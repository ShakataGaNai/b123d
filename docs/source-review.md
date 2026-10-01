# CAD source review and adoption decisions

Reviewed 2026-10-01 for a Python 3.14, `build123d==0.13.0` modeling repository managed with uv. This record synthesizes the six requested sources. It does not vendor their skills, scripts, or prose. Findings below come from source inspection, not execution of third-party tools; geometric failure scenarios identified by inspection are inferences unless stated otherwise.

## Revision and license ledger

GitHub's ref API returned these commit SHAs. Links in the review use those revisions where possible; a branch's future contents may differ. Root licenses establish repository-level evidence, not the licensing of every bundled asset, dependency, or linked project.

| Requested source | Reviewed revision | Root license evidence | Decision |
|---|---|---|---|
| [earthtojake/text-to-cad, CAD skill][earth-skill] | [`dbcb77058db9a1168d36d587a2594a113a0c658e`][earth-ref] (`main`) | [MIT, copyright Thompson Labs LLC][earth-license] | **Adapt** its modeling and evidence workflow; do not install its runtime stack. |
| [wngfra/build123d-cad][wng-skill] | [`825729b28a8e28bf071d089766e50129c496cdcf`][wng-ref] (`main`) | [Apache-2.0][wng-license] | **Adapt** the small command/report concept; **reject** its validator as a correctness gate. |
| [cyberchitta/cad-khana][khana-readme] | [`d54897dc6d82fa88fd0dbb82207bfb21d94aaa1f`][khana-ref] (`main`) | [Apache-2.0][khana-license] | **Adapt** diagnostics and explicit claims; do not adopt its package or assembly DSL. |
| [baibai2013/build123d-cad][bai-skill] | [`6567fa96a8741fdad09a557c4f96e5c76b8a6c97`][bai-ref] (`main`) | [Apache-2.0][bai-license] | **Adapt selectively**; **reject** the broad orchestration stack and unchecked reference defaults. |
| [gumyr/build123d][build-readme] | [`38effd343e1508964673faf59300a5cc68fbedc1`][build-ref] (`v0.13.0`) | [Apache-2.0][build-license], [NOTICE][build-notice] | **Adopt** the pinned library and release-matched API as the modeling authority. |
| [phillipthelen/awesome-build123d][awesome-readme] | [`01c2313de3b26ea6bdddbfca7b4b336cdc8c43e6`][awesome-ref] (`main`) | [CC0-1.0][awesome-license] | **Adopt as a discovery index**, not a dependency list or compatibility guarantee. |

All six root licenses were reachable. This review did not audit transitive licenses or every file header. Preserve applicable license/copyright/NOTICE material if later copying implementation or assets. A catalog's license does not relicense the projects it links. Manufacturer drawings require their own redistribution review.

## 1. earthtojake/text-to-cad

**Useful ideas.** The [root CAD skill][earth-skill] keeps geometry construction inside functions, makes parameters explicit, defines millimeters and XY/+Z as defaults, and separates model generation from inspection of saved artifacts. Its [inspection reference][earth-inspection] distinguishes bounding envelopes from functional dimensions, identifies geometry selections and thresholds, and treats a failed computation as unverified rather than passed. Its [snapshot reference][earth-snapshots] asks for views that expose the feature under review and converts visual concerns into geometric checks. Adopt these principles in original local instructions.

**Fit and limits.** The actual entry point uses `cadgen` decorators, a model store, scene-reference IDs, and a viewer lifecycle. The skill pins [`cadgen[snapshot]==0.7.5`][earth-requirements] and requires a Chromium installation for snapshots. Its viewer instructions require a detached server and live links. These are package-specific contracts, not build123d conventions. Our headless PNG and offline HTML outputs should not require this daemon, browser installation, or decorator API. [Skill][earth-skill]; [export contract][earth-exports].

**Decision.** Adapt parameterless factories, source/output separation, saved-artifact checks, and evidence-driven handoff. Reject importing its cache/store/viewer architecture. Keep our own model contract explicit so an agent does not mistake `cadgen.read_scene`, `$step-parts`, or migration commands for installed local capabilities. Numeric scene references in that system are revision-scoped; the inspection reference explicitly warns against carrying them across rebuilds. [Inspection][earth-inspection].

## 2. wngfra/build123d-cad

**Useful ideas.** Separate generation, measurement, sectioning, and validation commands make agent feedback legible. JSON reports and explicit parameters are worth adapting. Its skill also asks authors to state material/process assumptions. [Skill][wng-skill].

**Concrete verification risks.** Inspection of [`cad_validate.py`][wng-validate] shows:

- The reported `min_clearance_mm` is distance between axis-aligned bounding boxes. Because the boxes contain the parts, this is a lower bound on actual separation, not a measurement of the mating geometry. Nested or concave non-touching parts can have overlapping boxes and report zero. Use boxes for broad-phase filtering; use geometric distance on the relevant bodies/faces for acceptance. This consequence follows from the implemented gap formula, not from an executed counterexample.
- Static interference ignores intersection volumes at or below `0.01 mm³`. That is an undocumented design allowance in the algorithm, not universal proof of non-interference. Contact and overlap need different policies.
- The purported swept volume unions a finite set of rotated poses. **Inference:** collisions between samples can escape detection. Report a sampled motion check as sampled, with its range, step, and tested poses; do not call it a continuous collision proof.
- Some errors enter detail records, and some rotation/export exceptions are swallowed. The final verdict counts overlap volumes and clearance violations, not all computation errors. **Inference from control flow:** a `PASS` can coexist with failed checks. Our checks should fail or report an explicit inconclusive result.

**Setup and design risks.** [`setup.sh`][wng-setup] installs an unpinned build123d; its plain-`python3` fallback does not enforce 3.12. The skill assumes `{baseDir}`, an `exec` tool, a skill-local virtual environment, and `~/.openclaw/workspace/cad-output/`. None belongs in this repository's portable interface. Its minimum fillet radii of 1 mm for plastic and 0.5 mm for metal lack a load case, stock/tooling constraint, scale, or cited material basis. Treat them as that author's heuristics, not acceptance requirements. [Skill][wng-skill].

**Decision.** Adapt machine-readable observations and material assumptions. Reject its setup conventions, universal fillet limits, and validator implementation as local dependencies.

## 3. cyberchitta/cad-khana

**Useful ideas.** Named design assertions, diagnostic files even on failure, and separation of verification geometry from exported product geometry help an agent avoid silent regressions. The [skill][khana-skill] calls out empty assertion sets, skipped claims, rest-pose-only results, multi-solid parts, and warnings that do not fail the command. Adopt the underlying reporting discipline: state what ran and what did not.

**Compatibility.** The reviewed [`pyproject.toml`][khana-project] requires Python `>=3.13,<3.14`, so this package does not fit our Python 3.14 target. It also depends on `bd-warehouse`, `ocp-vscode`, Pillow, pygltflib, Typer, and `build123d>=0.8` rather than this repository's exact release. The [README][khana-readme] calls the API early/changing; GLB export additionally needs the external `gltf-transform` CLI for a mandatory join pass. Do not silently inherit these dependencies.

**Limits worth preserving.** Its wall-thickness procedure samples rays from tessellated faces and can miss diagonal pinch points. A static distance claim cannot prove a removal path or full motion. Contact gives zero distance without necessarily implying interference. The [printability reference][khana-print] says `khana check` alone does not run printability inspection; a broad green summary elsewhere in the skill should not override that narrower command contract. Its FDM defaults are explicitly tied to printer/material assumptions and still require physical confirmation. [Skill limitations][khana-skill]; [printability][khana-print].

**Decision.** Adapt explicit per-design checks and conservative reports using native build123d shapes. Reject the dependency and DSL cutover. Do not turn approximate printability checks, a nonempty report, or exit zero into a claim of manufacturability.

## 4. baibai2013/build123d-cad

**Useful ideas.** The [parent skill][bai-skill] routes to task-specific references rather than loading its entire knowledge base. The [mechanical skill][bai-mechanical] encourages parameterized design intent, source/license research for reusable parts, geometric checks, and STEP round trips. Adapt targeted reference loading and preserving vendor evidence before modeling.

**Scope mismatch.** The parent coordinates 25 domains including electronics, firmware, robot simulation, manufacturing services, and digital-twin gates. The mechanical workflow assumes OCP viewer setup, exports inside model scripts, named agent/model assignments, hard-coded workspace conventions, and multiple human confirmation gates. Its environment section says Python ≥3.10 while the pinned build123d release requires ≥3.11. These instructions are not a portable installation or a suitable local model interface. [Parent][bai-skill]; [mechanical][bai-mechanical]; [release dependencies][build-project].

**Reference drift and numerical hazards.**

- The mechanical skill names `scripts/validate/check_geometry.py`, but that URL returned 404 at the reviewed commit. The [actual validation directory][bai-validation-tree] contains `validate_part.py`, `contract_verify.py`, `assembly_check.py`, and `visual_compare.py`. Verify linked commands before adopting them.
- [`validate_part.py`][bai-validator] captures exports by monkey-patching build123d, then measures the last captured shape. Its thin-feature warning uses the smallest *overall bounding-box dimension*. That cannot establish a minimum internal wall thickness. Prefer the explicit `build()` return and design-specific checks instead of capturing side effects.
- The [printing reference][bai-print] presents nozzle/process tolerance tables without machine calibration or a dimensional uncertainty budget. Its fit example adds `clearance` to a **radius** while describing the resulting **diameter** increase as that same clearance. The actual diameter increment is twice the radius increment. Name radial and diametral allowances separately.
- That reference uses `export_stl(..., linear_tolerance=...)` and labels angular tolerance in degrees. The pinned [upstream function][build-stl] accepts `tolerance`, not `linear_tolerance`. Consult the release implementation and kernel units rather than copying that example.

**Decision.** Adapt its information organization and verification layers. Reject the orchestration stack, mandatory viewer claims, unsupported script paths, and print tables as universal acceptance criteria. Print clearances depend on machine, material, orientation, slicer, shrinkage, and the actual interface. Record a process-specific assumption and use fit coupons or measured evidence before claiming fit.

## 5. gumyr/build123d

**Authority and fit.** The [release README][build-readme] documents native parametric BREP modeling on Open CASCADE, Builder and algebraic operations, selectors, and export support. The [v0.13.0 project metadata][build-project] supports Python ≥3.11,<3.15, including our 3.14 target. It requires `cadquery-ocp-novtk>=8.0,<8.1` and other version ranges; pinning build123d alone does not lock its dependency graph. Adopt a committed lockfile and exercise exports on the target platform.

**Important STL detail.** At this exact release, [`export_stl`][build-stl] forwards `tolerance` to `BRepMesh_IncrementalMesh` with its relative-deflection flag set to `True`. Consequently, a call with `tolerance=0.05` must not be documented as an absolute 0.05 mm chord bound. If the local CLI promises an absolute millimeter meshing parameter, explicitly select absolute meshing in the kernel and keep the STL writer from remeshing with relative settings. Report the requested meshing settings, not a measured maximum mesh error. OCCT's [meshing explanation][occt-mesh] distinguishes absolute model-unit deflection from relative scale factors and notes that shape tolerance can limit achievable deflection.

**Decision.** Adopt release-matched upstream behavior over community cheatsheets. Use the upstream source when documentation and examples disagree. A valid BREP and successful export establish geometric/file properties, not load capacity, printability, safe use, or manufacturer fit. Those remain design-specific evidence obligations.

## 6. phillipthelen/awesome-build123d

**Useful ideas.** The [catalog][awesome-readme] identifies viewers, portable installations, parametric part libraries such as `bd_warehouse`, screenshot tools, examples, and official documentation. It explicitly separates legacy entries, including an unmaintained Blender integration. It is useful for finding a candidate before investigating that candidate's own source.

**Limits and decision.** Adopt the catalog as a bookmark. Do not bulk-install its entries or infer that listing means compatibility with build123d 0.13.0, active maintenance, production suitability, or permission to copy assets. Review each candidate's release, license, dependencies, and maintenance state at the time of use. The catalog's [CC0 license][awesome-license] covers the catalog, not those external packages.

## Local policy derived from this review

### Authority hierarchy

1. **For object dimensions and interfaces:** exact manufacturer drawing/datasheet for the correct object revision, applicable standards, then measurements with method and uncertainty. Keep unresolved conflicts visible; do not silently average contradictory dimensions. Save this evidence under `research/objects/` before building around an external object.
2. **For API behavior:** the installed, pinned build123d/OCP versions and their matching source/tests; then matching official documentation. The [release metadata][build-project] and [STL implementation][build-stl] demonstrate why a floating `latest` page is insufficient.
3. **For local invocation:** this repository's README, `AGENTS.md`, and canonical `.agents/skills/build123d/SKILL.md`. These define local paths and output contracts, not upstream skills.
4. **For workflow ideas:** the reviewed community skills, checked against local requirements and upstream APIs.
5. **For discovery:** curated lists and search results, followed by primary-source review.

### Portable skill discovery

Keep one canonical skill at `.agents/skills/build123d/SKILL.md`. This layout is discoverable by OMP's Agents provider; root `AGENTS.md` also directs agents to it before CAD work. Clients without either discovery mechanism should be pointed at that file explicitly. Do not duplicate the skill into each client's directories. The different discovery/setup assumptions in [earthtojake][earth-skill], [wngfra][wng-skill], and [cad-khana][khana-readme] justify retaining an explicit local entry point.

### Verification boundaries

- Separate generic geometry/export checks from `check(shape)` design assertions. A missing custom check means those design requirements remain unverified.
- Inspect the generated views, then measure suspected defects. Neither an attractive image nor an unchanged volume proves hole placement, wall thickness, connectivity, or fit. [Snapshot diagnostics][earth-snapshots].
- Report intended solid count, validity, dimensions/volume where relevant, actual checks, and untested requirements. Check individual solids rather than letting aggregate volume hide a reversed or disconnected body. [Inspection guidance][earth-inspection].
- Keep geometric design allowances, kernel numerical tolerances, tessellation settings, and manufacturing tolerances as separate quantities with units. Do not infer print accuracy from STL resolution. [Pinned export implementation][build-stl]; [OCCT meshing][occt-mesh]; [printing-reference counterexamples][bai-print].

### Offline operation and maintenance

The following is the maintenance policy, not a claim that every dependency is already cached:

1. Commit original local skills/references, model source, research notes, dependency pins, and the lockfile. Record external drawing revisions and asset hashes; retain local assets only when redistribution permits it.
2. Before going offline, populate the environment and dependency cache for the actual Python/OS/architecture. Record that initial setup may need network access; a lockfile alone does not supply wheels, Python, or CAD kernel binaries.
3. Keep routine model builds free of upstream downloads. Generate self-contained previews without CDN imports or a mandatory viewer service. Local documentation should cover the normal workflow; external links provide deeper evidence.
4. Refresh this review when changing build123d, OCP, the Python version, meshing, or a reused reference. Capture a new immutable SHA, compare the relevant files and licenses, and update affected guidance together. Do not auto-update community skills from moving branches.
5. For an upgrade, regenerate representative simple, curved, boolean-heavy, and multipart models; check artifact round trips and inspect previews. Compare geometric behavior with tolerances rather than requiring byte-identical STEP output. Record the exercised platform and remaining gaps in the upgrade record.
6. If a link disappears, retain its recorded URL, revision/date, relevant original summary, and any legally saved asset checksum. Do not replace missing evidence with an invented dimension or an undocumented surrogate model.

## Primary-source links

[earth-ref]: https://api.github.com/repos/earthtojake/text-to-cad/git/ref/heads/main
[earth-skill]: https://github.com/earthtojake/text-to-cad/blob/dbcb77058db9a1168d36d587a2594a113a0c658e/skills/cad/SKILL.md
[earth-license]: https://github.com/earthtojake/text-to-cad/blob/dbcb77058db9a1168d36d587a2594a113a0c658e/LICENSE
[earth-requirements]: https://github.com/earthtojake/text-to-cad/blob/dbcb77058db9a1168d36d587a2594a113a0c658e/skills/cad/requirements.txt
[earth-inspection]: https://github.com/earthtojake/text-to-cad/blob/dbcb77058db9a1168d36d587a2594a113a0c658e/skills/cad/references/inspection-and-validation.md
[earth-snapshots]: https://github.com/earthtojake/text-to-cad/blob/dbcb77058db9a1168d36d587a2594a113a0c658e/skills/cad/references/snapshot-review.md
[earth-exports]: https://github.com/earthtojake/text-to-cad/blob/dbcb77058db9a1168d36d587a2594a113a0c658e/skills/cad/references/supported-exports.md
[wng-ref]: https://api.github.com/repos/wngfra/build123d-cad/git/ref/heads/main
[wng-skill]: https://github.com/wngfra/build123d-cad/blob/825729b28a8e28bf071d089766e50129c496cdcf/SKILL.md
[wng-license]: https://github.com/wngfra/build123d-cad/blob/825729b28a8e28bf071d089766e50129c496cdcf/LICENSE
[wng-setup]: https://github.com/wngfra/build123d-cad/blob/825729b28a8e28bf071d089766e50129c496cdcf/setup.sh
[wng-validate]: https://github.com/wngfra/build123d-cad/blob/825729b28a8e28bf071d089766e50129c496cdcf/scripts/cad_validate.py
[khana-ref]: https://api.github.com/repos/cyberchitta/cad-khana/git/ref/heads/main
[khana-readme]: https://github.com/cyberchitta/cad-khana/blob/d54897dc6d82fa88fd0dbb82207bfb21d94aaa1f/README.md
[khana-license]: https://github.com/cyberchitta/cad-khana/blob/d54897dc6d82fa88fd0dbb82207bfb21d94aaa1f/LICENSE
[khana-skill]: https://github.com/cyberchitta/cad-khana/blob/d54897dc6d82fa88fd0dbb82207bfb21d94aaa1f/skills/cad-khana/SKILL.md
[khana-project]: https://github.com/cyberchitta/cad-khana/blob/d54897dc6d82fa88fd0dbb82207bfb21d94aaa1f/pyproject.toml
[khana-print]: https://github.com/cyberchitta/cad-khana/blob/d54897dc6d82fa88fd0dbb82207bfb21d94aaa1f/skills/cad-khana/references/printability.md
[bai-ref]: https://api.github.com/repos/baibai2013/build123d-cad/git/ref/heads/main
[bai-skill]: https://github.com/baibai2013/build123d-cad/blob/6567fa96a8741fdad09a557c4f96e5c76b8a6c97/SKILL.md
[bai-license]: https://github.com/baibai2013/build123d-cad/blob/6567fa96a8741fdad09a557c4f96e5c76b8a6c97/LICENSE
[bai-mechanical]: https://github.com/baibai2013/build123d-cad/blob/6567fa96a8741fdad09a557c4f96e5c76b8a6c97/skills/mechanical/SKILL.md
[bai-print]: https://github.com/baibai2013/build123d-cad/blob/6567fa96a8741fdad09a557c4f96e5c76b8a6c97/skills/mechanical/references/process/3d-printing.md
[bai-validation-tree]: https://api.github.com/repos/baibai2013/build123d-cad/git/trees/0a3aee18fde1cd9bdd9fdc505d09f4ed9e122bb9
[bai-validator]: https://github.com/baibai2013/build123d-cad/blob/6567fa96a8741fdad09a557c4f96e5c76b8a6c97/skills/mechanical/scripts/validate/validate_part.py
[build-ref]: https://api.github.com/repos/gumyr/build123d/git/ref/tags/v0.13.0
[build-readme]: https://github.com/gumyr/build123d/blob/38effd343e1508964673faf59300a5cc68fbedc1/README.md
[build-license]: https://github.com/gumyr/build123d/blob/38effd343e1508964673faf59300a5cc68fbedc1/LICENSE
[build-notice]: https://github.com/gumyr/build123d/blob/38effd343e1508964673faf59300a5cc68fbedc1/NOTICE
[build-project]: https://github.com/gumyr/build123d/blob/38effd343e1508964673faf59300a5cc68fbedc1/pyproject.toml
[build-stl]: https://github.com/gumyr/build123d/blob/38effd343e1508964673faf59300a5cc68fbedc1/src/build123d/exporters3d.py#L444-L488
[occt-mesh]: https://github.com/Open-Cascade-SAS/OCCT/wiki/mesh
[awesome-ref]: https://api.github.com/repos/phillipthelen/awesome-build123d/git/ref/heads/main
[awesome-readme]: https://github.com/phillipthelen/awesome-build123d/blob/01c2313de3b26ea6bdddbfca7b4b336cdc8c43e6/README.md
[awesome-license]: https://github.com/phillipthelen/awesome-build123d/blob/01c2313de3b26ea6bdddbfca7b4b336cdc8c43e6/LICENSE
