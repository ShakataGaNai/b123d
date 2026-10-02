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
5. When acceptance criteria pass, follow [commit-driven completion](#commit-driven-completion). Record the verification in the fixing commit or PR and let GitHub close the issue when the work reaches the default branch.

GitHub Issues is the durable shared work queue. Personal task lists and global agent task-tool preferences do not replace this repository's tracker. Session checklists may mirror an issue's steps, but cannot be the only record of work. `TODO.md`, if introduced, is for documented known limitations with issue links, not another work queue. No such file is required now.

If issue creation fails, inspect authentication and repository access, then retry only after resolving the cause. If still blocked, report the exact blocker and preserve the proposed issue text for handoff; do not silently substitute another tracker or claim an issue exists.

## Commit-driven completion

1. **Link the fix in the commit message.** For each issue fully resolved by the
   verified change, include a separate closing reference in the commit body:
   ```text
   Fixes #123
   Fixes #124
   ```
   Use `Fixes owner/repository#123` for another repository. `Closes` and
   `Resolves` also work; use `Fixes` here for consistency. For partial or related
   work, use `Refs #123` instead and leave that issue open.
2. **Publish through the default branch.** When authorized, push the fixing
   commit to the repository's default branch or merge it there through a PR.
   GitHub then closes the referenced issues automatically. A local commit or a
   push to a non-default branch does not complete this lifecycle. For PRs, also
   put the closing references in the PR description; preserve them in the final
   squash commit message when relying on commit-based closure.
3. **Verify the result.** Resolve the current default branch rather than assume
   its name, confirm publication succeeded, and inspect the issue state:
   ```sh
   gh repo view ShakataGaNai/b123d --json defaultBranchRef --jq '.defaultBranchRef.name'
   gh issue view 123 --repo ShakataGaNai/b123d --json state,stateReason,closedAt
   ```
   If it remains open, check the published commit/PR closing references and target
   branch. Diagnose the missing automation rather than substituting a manual close.

Keep issues open while their fixes are uncommitted, unpushed, or awaiting merge.
Do not manually close commit-delivered work or post a "completed, not committed
yet" closure comment. Put verification in the commit/PR; routine completion
comments duplicating GitHub's automatic closing event are unnecessary.
Manual closure is for explicit non-implementation decisions, such as a user's
cancellation or a duplicate issue; record that reason without claiming a fix.
Closure does not establish a deployment, physical print, or test beyond the
verification actually performed.

Source: [GitHub's closing-keyword and default-branch rules](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

## Planned publishing

- [#1 — GitHub Releases for versioned model downloads](https://github.com/ShakataGaNai/b123d/issues/1)
- [#2 — GitHub Pages model preview gallery](https://github.com/ShakataGaNai/b123d/issues/2)

These are open follow-ups, not implemented services. The gallery is for this repository's models, not the optional upstream build123d documentation site.
