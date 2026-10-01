"""Build the complete pinned build123d HTML documentation without network access.

Setup (once): install Graphviz, then run ``uv sync --locked --group docs``.
Build: ``uv run --offline --group docs python scripts/build_docs.py``.
All paths are relative to this script, not the caller's working directory.
"""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.13.0"
SOURCE = ROOT / "vendor" / f"build123d-{VERSION}" / "docs"
OUTPUT = ROOT / "outputs" / "docs" / f"build123d-{VERSION}"


def deny_network(event: str, args: tuple[object, ...]) -> None:
    """Fail closed if a documentation extension attempts a network connection."""
    if event in {"socket.connect", "socket.getaddrinfo", "socket.sendto"}:
        raise RuntimeError(f"Offline documentation build blocked {event}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    # In particular, importing the upstream lexer must not create __pycache__
    # inside the pristine source snapshot.
    sys.dont_write_bytecode = True
    sys.addaudithook(deny_network)
    try:
        installed = version("build123d")
        if installed != VERSION:
            raise ValueError(f"Expected build123d {VERSION}; installed {installed}")
        import build123d

        if build123d.__version__ != VERSION:
            raise ValueError(
                f"Imported build123d {build123d.__version__}; expected {VERSION}"
            )
        from sphinx.cmd.build import build_main

        if not SOURCE.joinpath("index.rst").is_file():
            raise ValueError(
                f"Missing upstream documentation snapshot: {SOURCE}. "
                "Run uv run python scripts/init.py --html-assets first."
            )
        if not (ROOT / "vendor" / "model-viewer-4.1.0" / "dist" / "model-viewer.min.js").is_file():
            raise ValueError("Missing optional viewer; run uv run python scripts/init.py --html-assets first")
        if shutil.which("dot") is None:
            raise ValueError(
                "Graphviz 'dot' is required for inheritance diagrams. "
                "Install Graphviz explicitly (macOS: brew install graphviz)."
            )
        status = build_main([
            "-E", "-a", "-b", "html",
            "-c", str(ROOT / "docs" / "sphinx"),
            "-d", str(OUTPUT / ".doctrees"),
            str(SOURCE), str(OUTPUT),
        ])
        if status:
            return status
        index = OUTPUT / "index.html"
        if not index.is_file():
            raise ValueError(f"Sphinx did not produce {index}")
        print(f"\nOffline documentation: {index}")
        print("For interactive GLB examples, serve this directory with python -m http.server.")
        return 0
    except (ImportError, PackageNotFoundError) as error:
        parser.exit(1, f"Documentation dependency error: {error}\nRun uv sync --locked --group docs first.\n")
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Documentation build error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
