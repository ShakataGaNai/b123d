"""Look up the pinned build123d documentation and installed API without network access."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from importlib.metadata import version
import inspect
from pathlib import Path
import re
import sys
from typing import get_overloads

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.13.0"
SNAPSHOT = ROOT / "vendor" / f"build123d-{VERSION}"
SEARCH_ROOTS = (SNAPSHOT / "docs", SNAPSHOT / "src" / "build123d", SNAPSHOT / "examples")


@dataclass(frozen=True)
class Hit:
    score: int
    path: Path
    start: int
    lines: tuple[str, ...]


def positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def search(query: str, limit: int) -> int:
    terms = tuple(dict.fromkeys(query.casefold().split()))
    if not terms:
        raise ValueError("Search query must contain at least one term")
    patterns = [re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)") for term in terms]
    hits: list[Hit] = []
    for folder in SEARCH_ROOTS:
        if not folder.is_dir():
            raise ValueError(
                f"Missing local documentation: {relative(folder)}. "
                "Run uv run python scripts/init.py once after checkout."
            )
        for path in sorted(folder.rglob("*")):
            if path.suffix not in {".rst", ".md", ".py", ".txt"} or not path.is_file():
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            folded = [line.casefold() for line in lines]
            candidates: list[Hit] = []
            for index, line in enumerate(folded):
                if not any(term in line for term in terms):
                    continue
                start, end = max(0, index - 2), min(len(lines), index + 3)
                definition = re.match(r"\s*(?:def|class)\s+(\w+)", line)
                if definition:
                    start, end = index, min(len(lines), index + 5)
                window = "\n".join(folded[start:end])
                if not all(term in window for term in terms):
                    continue
                # Prefer concentrated, exact terms, definitions, and prose over incidental uses.
                score = 12 * sum(term in line for term in terms)
                score += 5 * sum(bool(pattern.search(line)) for pattern in patterns)
                score += 8 * (" ".join(terms) in line)
                score += 4 * sum(term in path.stem.casefold() for term in terms)
                score += 3 * (path.suffix == ".rst")
                if definition and definition.group(1) in terms:
                    score += 15
                while start < end and not lines[start].strip():
                    start += 1
                while end > start and not lines[end - 1].strip():
                    end -= 1
                candidates.append(Hit(score, path, start + 1, tuple(lines[start:end])))
            # Keep two nonoverlapping excerpts per file so one large module cannot flood results.
            chosen: list[Hit] = []
            for hit in sorted(candidates, key=lambda hit: (-hit.score, hit.start)):
                if any(hit.start < old.start + len(old.lines)
                       and old.start < hit.start + len(hit.lines) for old in chosen):
                    continue
                chosen.append(hit)
                if len(chosen) == 2:
                    break
            hits.extend(chosen)
    hits.sort(key=lambda hit: (-hit.score, hit.path.as_posix(), hit.start))
    if not hits:
        print(f"No local matches for {query!r}. Try fewer terms or an API name.", file=sys.stderr)
        return 1
    selected = hits[:limit]
    print(f"build123d {VERSION}: {len(selected)} ranked excerpts (all terms within five lines).")
    for hit in selected:
        print(f"\n{relative(hit.path)}:{hit.start}")
        for number, line in enumerate(hit.lines, hit.start):
            snippet = line if len(line) <= 180 else line[:177] + "..."
            print(f"  {number}: {snippet}")
    if len(hits) > limit:
        print("\nMore excerpts available: narrow the query or increase --limit.")
    return 0


def resolve_api(module: object, symbol: str) -> object:
    parts = symbol.split(".")
    if parts[0] == "build123d":
        parts = parts[1:]
    if not parts or any(not part.isidentifier() or part.startswith("_") for part in parts):
        raise ValueError("Use a public dotted API name, e.g. sweep or Solid.make_box; expressions are not accepted")
    obj = module
    for part in parts:
        try:
            member = inspect.getattr_static(obj, part)
        except AttributeError:
            raise ValueError(f"Unknown build123d API symbol: {symbol}") from None
        if isinstance(member, classmethod):
            member = member.__get__(None, obj)
        elif isinstance(member, staticmethod):
            member = member.__func__
        obj = member
    if not (inspect.isclass(obj) or inspect.isroutine(obj)):
        raise ValueError(f"{symbol} is not a function, class, or method; search its documentation instead")
    if not getattr(obj, "__module__", "").startswith("build123d"):
        raise ValueError(f"{symbol} is not defined by build123d; consult that dependency's documentation")
    return obj


def api(symbol: str, limit: int, full: bool) -> int:
    # Import only the installed library, never a vendored example or documentation program.
    import build123d

    installed = version("build123d")
    if installed != VERSION:
        raise ValueError(f"Installed build123d is {installed}; local snapshot is {VERSION}. Run uv sync --locked")
    obj = resolve_api(build123d, symbol)
    print(f"build123d {installed} (installed API)")
    print(f"{symbol}{inspect.signature(obj)}")
    target = obj.__init__ if inspect.isclass(obj) else obj
    overloads = get_overloads(target)
    if overloads:
        print("Declared overloads:")
        for overload in overloads:
            signature = inspect.signature(overload)
            if inspect.isclass(obj) or inspect.ismethod(obj):
                signature = signature.replace(parameters=list(signature.parameters.values())[1:])
            print(f"  {symbol}{signature}")
    source = inspect.getsourcefile(obj)
    if source:
        source_path = Path(source).resolve()
        _, line = inspect.getsourcelines(obj)
        print(f"Installed source: {relative(source_path)}:{line}")
        package_path = Path(build123d.__file__).resolve().parent
        if source_path.is_relative_to(package_path):
            snapshot_path = SNAPSHOT / "src" / "build123d" / source_path.relative_to(package_path)
            if snapshot_path.is_file():
                print(f"Snapshot source: {relative(snapshot_path)}")
    doc = inspect.getdoc(obj)
    if not doc:
        print("\nNo docstring available; use the source or local search.")
        return 0
    lines = doc.splitlines()
    print()
    print("\n".join(lines if full else lines[:limit]))
    if not full and len(lines) > limit:
        print(f"\n[Docstring: showing {limit}/{len(lines)} lines; use --limit N or --full.]")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    search_parser = commands.add_parser("search", help="Rank bounded excerpts from official docs, API source, and examples")
    search_parser.add_argument("query", nargs="+", help="Case-insensitive literal terms; all must occur within five lines")
    search_parser.add_argument("--limit", type=positive, default=6, help="Maximum excerpts (default: 6; at most two per file)")
    api_parser = commands.add_parser("api", help="Show installed signature, docstring, and local source")
    api_parser.add_argument("symbol", help="Public name such as Plane, sweep, or Solid.make_box")
    api_parser.add_argument("--limit", type=positive, default=20, help="Maximum docstring lines (default: 20)")
    api_parser.add_argument("--full", action="store_true", help="Show the complete docstring")
    args = parser.parse_args()
    try:
        status = search(" ".join(args.query), args.limit) if args.command == "search" else api(args.symbol, args.limit, args.full)
    except (ValueError, TypeError, OSError, ImportError) as error:
        parser.exit(1, f"Documentation lookup error: {error}\n")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
