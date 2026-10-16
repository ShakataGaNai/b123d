# AI CAD workspace

## Environment

Use Python **3.14 under uv**: `uv sync --locked`, then `uv run python ...`.
`pyproject.toml`, `.python-version`, and `uv.lock` own the environment; commit the
lockfile and refresh it only for an intentional dependency change. On a fresh
checkout, follow [initialization](docs/initialization.md), including
`uv run python scripts/init.py` to restore the pinned offline reference.
Keep generated artifacts, `vendor/`, `.venv/`, and scratch work in ignored locations.
Model code runs with normal user privileges; this workspace is not a sandbox.

## CAD work

For creating, modifying, inspecting, or exporting CAD, read the canonical
[build123d skill](.agents/skills/build123d/SKILL.md), then only its task-relevant
references. It owns model layout, research, construction and completion rules;
it is discoverable by OMP's Agents provider. Do not install a second copy.
For STL measurement/reconstruction, also read the
[STL measurement skill](.agents/skills/stl-measurement/SKILL.md).

Find models in [the catalog](models/README.md). **Measure first; edit source,
never generated exports.** Use the pinned APIs and local documentation for
routine library questions and builds; see [offline lookup](docs/offline-build123d.md).

For tooling changes, run `uv run python -m unittest discover -s tests -v` and
exercise the affected CLI end to end. Model-specific checks belong to the CAD workflow.

## Issue tracking

Before starting, deferring, committing or publishing work, read
[the GitHub issue lifecycle](docs/agents/issue-tracker.md).
**Every engineering work item needs a GitHub issue**, including bugs found during
other work, deferred follow-ups, unresolved root causes and TODOs. This tracker
takes precedence over personal trackers; session checklists do not replace it.
`TODO.md` is for known limitations only. Use commit closing references and
verify automatic closure after authorized publication to the default branch.

## Commit scope in a shared workspace

- Before editing, inspect `git status --short`, `git diff`, and `git diff --cached`.
  Track your files/hunks; a dirty file or regenerated catalog is not proof of ownership.
- Commit only the authorized task's changes, including delegated work. Stage explicit
  paths when their entire diff is yours; otherwise use `git add -p` or a reviewed patch.
  Do not use `git add .`, `git add -A`, or `git commit -a` for scoped work.
- The index is shared. Coordinate with other agents; if unrelated changes are staged,
  pause the commit and resolve ownership. Never unstage, stash, reset, discard or
  overwrite others' work to isolate yours. Use separate worktrees when needed.
- Immediately before committing, inspect the entire `git diff --cached` and
  `git diff --cached --name-only`. Resolve ambiguous ownership, overlapping edits,
  or index changes before proceeding.
- Leave unrelated changes untouched and report the committed scope. Do not amend or
  rewrite another agent's commit without explicit authorization.

## Git commit messages

Keep messages brief and high-level: name the model added or what was fixed/changed.
For tooling/docs, name the behavior or guidance changed. A short subject is often
enough; add a few short bullets only when useful. Omit measurements and implementation
details. **Never include validation information**: no commands, check results, test
counts, export checks or inspection logs. Keep evidence in docs, reports, issues or PRs.
User-confirmed print-tested/approved status may be stated as a model-status change.
Include applicable issue references; remove validation details from squash messages.

## Git commit attribution

Every commit created or amended MUST end with this final nonempty line, preceded
by a blank line; put all other trailers above it:

```text
Co-Authored-By: <agent-name>/<current-agent-version> (<current-model-name>)
```

Resolve values at commit time: actual committing agent, running version from session
runtime or its CLI (`codex --version`, `claude --version`, `omp --version`), and active
session model—not a configured default or subagent. Obtain missing values; never guess.
When amending, replace the committing-agent attribution with current values.

## Documentation

Keep public docs portable: use project-relative paths and platform requirements;
omit personal profiles, account details, absolute machine paths and setup-session history.
