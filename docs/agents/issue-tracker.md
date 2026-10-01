# GitHub issue tracker

All engineering work for this repository is tracked in [ShakataGaNai/b123d GitHub Issues](https://github.com/ShakataGaNai/b123d/issues), using the `gh` CLI. Use `--repo ShakataGaNai/b123d` explicitly so commands work before a remote is configured and do not target another repository accidentally.

## Work lifecycle

1. Search existing open and closed issues before creating a duplicate:
   ```sh
   gh issue list --repo ShakataGaNai/b123d --state all --search 'search terms'
   gh issue view 3 --repo ShakataGaNai/b123d
   ```
2. Create an issue for each independent work item if none exists. Include the problem or goal, relevant evidence, scope, and observable acceptance criteria. A large issue may use a checklist for its implementation steps; independently deferred work gets its own linked issue.
   ```sh
   gh issue create --repo ShakataGaNai/b123d --title 'Concise work-item title' --body-file /path/to/issue-body.md
   ```
3. Keep the issue current when scope changes, a blocker appears, or a root cause remains unresolved. Record discoveries even if they are outside the current request. Connect related issues with links rather than relying on an agent's conversation history.
4. Before deferring anything, create or link its issue. A TODO comment may point to the issue but must not be the sole record. State the blocker and what makes the work actionable.
5. On completion, record the actual verification and relevant commit/PR references. Close the issue when its acceptance criteria are met. Clearly distinguish locally completed but uncommitted work from merged or published changes; never imply a push, deployment, physical print, or test that did not happen.

GitHub Issues is the durable shared work queue. Personal task lists and global agent task-tool preferences do not replace this repository's tracker. Session checklists may mirror an issue's steps, but cannot be the only record of work. `TODO.md`, if introduced, is for documented known limitations with issue links, not another work queue. No such file is required now.

If issue creation fails, inspect authentication and repository access, then retry only after resolving the cause. If still blocked, report the exact blocker and preserve the proposed issue text for handoff; do not silently substitute another tracker or claim an issue exists.

## Planned publishing

- [#1 — GitHub Releases for versioned model downloads](https://github.com/ShakataGaNai/b123d/issues/1)
- [#2 — GitHub Pages model preview gallery](https://github.com/ShakataGaNai/b123d/issues/2)

These are follow-ups, not implemented services. The gallery is for this repository's models, not the optional upstream build123d documentation site.
