"""Offline overlay; the versioned upstream source tree remains unmodified."""

from contextlib import chdir
from pathlib import Path
import runpy
import shutil
import sys

import build123d

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "vendor" / "build123d-0.13.0" / "docs"
VIEWER = ROOT / "vendor" / "model-viewer-4.1.0"

# Preserve every upstream documentation option, but resolve its cwd-sensitive
# paths here. Autodoc uses the checked installed package, not a second import
# of the vendored source tree. Upstream RST uses bare names such as geometry.
_original_path = sys.path.copy()
try:
    with chdir(UPSTREAM):
        _upstream_config = runpy.run_path(str(UPSTREAM / "conf.py"))
finally:
    sys.path[:] = _original_path
for _name, _value in _upstream_config.items():
    if not _name.startswith("_") and _name not in {"os", "sys", "build123d"}:
        globals()[_name] = _value
sys.path.insert(0, str(Path(build123d.__file__).resolve().parent))
sys.path.insert(0, str(UPSTREAM))

# Hoverxref's Read the Docs API tooltips and remote inventories are not needed
# for the full reference pages. Normal local cross-references remain enabled.
extensions = [
    name for name in extensions
    if name not in {"hoverxref.extension", "sphinx.ext.intersphinx"}
]
extensions += ["sphinx.ext.mathjax", "sphinx-mathjax-offline"]
intersphinx_mapping = {}
html_baseurl = ""
llms_txt_uri_template = "{docname}.html"
html_static_path = [str(UPSTREAM / "_static")]
templates_path = [str(UPSTREAM / "_templates")] if (UPSTREAM / "_templates").is_dir() else []
html_logo = str(UPSTREAM / "assets" / "build123d_logo" / "logo.svg")
html_favicon = str(UPSTREAM / "_static" / "build123d-favicon.ico")
autodoc_typehints = "signature"  # Upstream uses a list where Sphinx requires a string.
graphviz_output_format = "svg"
html_last_updated_fmt = None

# The upstream CDN embeds use three self-contained, uncompressed GLBs. This
# bundled viewer needs no Draco/Basis/Lottie decoder downloads for those files.
_EMBEDS = {
    "index": ("tea_cup", "tea_cup.png"),
    "tutorial_spitfire_wing_gordon": (
        "spitfire_wing", "assets/surface_modeling/spitfire_wing.png"
    ),
    "tutorial_surface_heart_token": (
        "heart_token", "assets/surface_modeling/heart_token.png"
    ),
}
_CDN_VIEWER = "https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"


def localize_embeds(app, docname, source):
    """Rewrite only generated input, retaining interactive upstream examples."""
    if docname not in _EMBEDS:
        return
    name, _ = _EMBEDS[docname]
    poster = f"_static/offline-posters/{name}.png"
    source[0] = source[0].replace(
        _CDN_VIEWER, "_static/model-viewer/model-viewer.min.js"
    ).replace(f"_images/{name}.png", poster).replace(
        "</model-viewer>",
        "</model-viewer>\n"
        f'    <noscript><img src="{poster}" alt="{name.replace("_", " ")}"></noscript>\n'
        f'    <p><a href="_static/{name}.glb" download>Download this 3D model (GLB)</a>. '
        "Interactive viewing requires a WebGL-capable browser and a local HTTP server; "
        "no internet connection is needed.</p>",
    )


def copy_viewer_assets(app, exception):
    if exception is not None:
        return
    static = Path(app.outdir) / "_static"
    viewer = static / "model-viewer"
    viewer.mkdir(parents=True, exist_ok=True)
    shutil.copy2(VIEWER / "dist" / "model-viewer.min.js", viewer / "model-viewer.min.js")
    for filename in ("LICENSE", "package.json"):
        shutil.copy2(VIEWER / filename, viewer / filename)
    shutil.copy2(ROOT / "vendor" / "model-viewer-4.1.0.manifest.json", viewer / "provenance.json")
    posters = static / "offline-posters"
    posters.mkdir(parents=True, exist_ok=True)
    for name, source in _EMBEDS.values():
        shutil.copy2(UPSTREAM / source, posters / f"{name}.png")


def escape_curvature_bars(app, what, name, obj, options, lines):
    """Preserve absolute-curvature notation instead of an RST substitution."""
    if name.endswith(".curvature_comb"):
        for index, line in enumerate(lines):
            lines[index] = line.replace("|κ|", r"\|κ\|")


def setup(app):
    app.connect("source-read", localize_embeds)
    app.connect("autodoc-process-docstring", escape_curvature_bars)
    app.connect("build-finished", copy_viewer_assets)
