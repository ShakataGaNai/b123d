"""Restore ignored upstream references; runtime setup is `uv sync --locked`.

Run once after checkout: uv run python scripts/init.py
Optional HTML documentation assets: add --html-assets.
Existing references are verified and reused without network access.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"


def verify(folder: Path, files: dict[str, str]) -> None:
    for name, expected in files.items():
        path = folder / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or non-regular reference file: {path}")
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != expected:
            raise ValueError(f"Reference checksum mismatch: {path}")


def restore(name: str, manifest_path: Path, prefix: str, url_key: str) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest["files"]
    for relative in files:
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise ValueError(f"Unsafe reference path in {manifest_path}: {relative}")
    if manifest.get("symlinks"):
        raise ValueError(f"Symlink references are not supported: {manifest_path}")
    target = VENDOR / name
    if target.exists() or target.is_symlink():
        if target.is_symlink() or not target.is_dir():
            raise ValueError(f"Reference destination must be a directory: {target}")
        try:
            verify(target, files)
        except ValueError as error:
            raise ValueError(
                f"{error}\nExisting files were left untouched. Move {target} aside "
                "and rerun initialization to restore the pinned copy."
            ) from error
        print(f"Verified existing {name}: {len(files)} files (no download)")
        return

    # Stage beside the destination so publication is a same-filesystem rename.
    with tempfile.TemporaryDirectory(prefix=".init-", dir=VENDOR) as temporary:
        stage = Path(temporary)
        archive = stage / "source.tar.gz"
        print(f"Downloading {name} from {manifest[url_key]}", flush=True)
        with urlopen(manifest[url_key], timeout=60) as response, archive.open("wb") as output:
            shutil.copyfileobj(response, output)
        with archive.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != manifest["archive_sha256"]:
            raise ValueError(f"Archive checksum mismatch for {name}; nothing installed")

        unpacked = stage / "reference"
        unpacked.mkdir()
        with tarfile.open(archive, "r:gz") as bundle:
            # Read only explicitly inventoried regular files. Never extract archive
            # paths, links, permissions, or unlisted members into the workspace.
            for relative in files:
                member = bundle.getmember(f"{prefix}/{relative}")
                if not member.isfile():
                    raise ValueError(f"Non-regular archive member: {member.name}")
                source = bundle.extractfile(member)
                if source is None:
                    raise ValueError(f"Unreadable archive member: {member.name}")
                destination = unpacked / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                with source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
        verify(unpacked, files)
        if target.exists() or target.is_symlink():
            raise ValueError(f"Reference destination appeared during initialization: {target}")
        unpacked.rename(target)
    print(f"Installed {name}: {len(files)} verified files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-assets", action="store_true", help="Also restore the optional HTML documentation viewer")
    args = parser.parse_args()
    try:
        core_manifest = VENDOR / "build123d-0.13.0.manifest.json"
        commit = json.loads(core_manifest.read_text(encoding="utf-8"))["commit"]
        restore("build123d-0.13.0", core_manifest, f"build123d-{commit}", "archive_url")
        if args.html_assets:
            restore("model-viewer-4.1.0", VENDOR / "model-viewer-4.1.0.manifest.json", "package", "source")
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        parser.exit(1, f"Initialization failed: {error}\n")


if __name__ == "__main__":
    main()
