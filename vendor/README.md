# Local upstream build123d reference

`build123d-0.13.0/` is a complete, unmodified source snapshot of the official [gumyr/build123d](https://github.com/gumyr/build123d) repository at the release used by this workspace. It is an ignored local download, restored by `uv run python scripts/init.py` after checkout. Only this README and the root-level integrity manifests belong in Git.

| Field | Value |
| --- | --- |
| Release | `v0.13.0` |
| Commit | `38effd343e1508964673faf59300a5cc68fbedc1` |
| Archive | [Immutable commit archive](https://codeload.github.com/gumyr/build123d/tar.gz/38effd343e1508964673faf59300a5cc68fbedc1) |
| Archive SHA-256 | `b1a10b9f4a6d40eac8fb37513afd1974a63013d2c745ee7df5d0af2e6fdf6698` |
| Integrity inventory | [build123d-0.13.0.manifest.json](build123d-0.13.0.manifest.json) |
| License | [Upstream LICENSE](build123d-0.13.0/LICENSE) |
| Attribution | [Upstream NOTICE](build123d-0.13.0/NOTICE) |

All 712 upstream files were compared byte-for-byte by SHA-256 against the commit archive when installed. This includes 468 documentation files (50 reStructuredText pages plus assets and build support), 68 example files, 46 API source files, and 104 upstream test/fixture files. These categories are not the entire tree; release metadata and other upstream files are retained too.

The snapshot is reference material, not a second runtime installation. The workspace uses the locked `build123d==0.13.0` package in `.venv`. Do not edit the snapshot to fix this project's models, execute arbitrary example programs merely to search them, or run the upstream test suite for ordinary modeling. Keep the license, notice, and embedded attribution intact when redistributing it.

## Use locally

Start with the [offline documentation guide](../docs/offline-build123d.md), not a recursive read of the entire snapshot. The source documentation, examples, and API implementation require no network. Rendered HTML is generated separately under `outputs/docs/build123d-0.13.0/` and is not a source of truth.

This snapshot includes build123d's own documentation and repository files. It does not mirror every external website they cite, all Open Cascade documentation, or separate third-party gear/fastener libraries. Embedded remote demos and external links are not offline reference content unless separately captured and licensed.

## Supplemental offline viewer

The optional, ignored `model-viewer-4.1.0/` directory contains the pinned browser runtime used by the three upstream interactive GLB examples. Restore it with `uv run python scripts/init.py --html-assets`. Its [committed provenance manifest](model-viewer-4.1.0.manifest.json) pins the archive and files; the downloaded bundle retains package metadata and its Apache-2.0 license. The documentation overlay substitutes this local runtime for upstream's CDN URL. MathJax, fonts, and Sphinx theme assets come from the locked optional `docs` dependency group. None of these HTML extras is needed by agents.

## Updating deliberately

Keep the manifests in version control, not the downloaded trees. Initialization verifies an existing copy without downloading; ordinary lookups and builds never fetch documentation. When deliberately upgrading build123d:

1. Change the runtime pin and lockfile as part of the same upgrade.
2. Resolve the matching upstream release to an immutable commit and download its archive explicitly.
3. Replace the snapshot as a complete versioned directory, retaining upstream licensing and attribution. Do not merge unrelated releases.
4. Regenerate the integrity manifest, update versioned paths in initialization, documentation tooling, and local guidance, and review changed API behavior.
5. Exercise initialization, local lookup, and the model/export workflow. Rebuild HTML only if using that optional view.

Do not force-add downloaded reference directories: the repository's `.gitignore` intentionally excludes them, regardless of upstream's own ignore rules. Licenses and attribution remain in the restored copies.

The manifest records the original archive digest and every extracted file digest. It is an integrity record, not a cryptographic signature from upstream.
