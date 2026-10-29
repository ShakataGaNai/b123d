# GitHub issue tracker

Use [GitHub Issues](https://github.com/ShakataGaNai/b123d/issues) selectively,
through `gh --repo ShakataGaNai/b123d`.

## When to track work

- Create an issue when the user requests one, or for substantial bugs, projects
  or deferred work that benefit from a durable shared record.
- Handle routine requests, small fixes, model iterations and research steps in
  the current task. An issue is not a prerequisite for doing or committing work.
- Keep related work together. Search existing open and closed issues before
  creating one; update an existing issue when its scope already covers the work.
- Record ordinary uncertainties and print limitations in model documentation.
  Pending physical feedback alone does not require a follow-up issue or keep a
  delivered modeling task open. Keep print-tested status separate from delivery.
- Create deferred-work issues only for concrete, worthwhile future actions,
  rather than every possible improvement or unverified assumption.

## Work lifecycle

For tracked work, describe the problem, scope and observable acceptance criteria.
Keep the issue current when its scope changes. Store validation evidence in the
model documentation, report, issue or PR. Close completed work promptly after
publication; retain only actual remaining scope in an open issue.

Prefer commit closing references for implementation work. If the user explicitly
asks to close an issue, close it directly with an accurate reason: completed for
already-delivered work, not planned for cancelled or declined future work. Do
not create an extra commit or replacement issue solely to permit closure.

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

For normal commit-driven completion, keep issues open until the fixing change
is published. Explicit user-requested closure and cancellations follow the
manual closure rule above. Closure never establishes physical print, fit or
safety approval beyond the evidence actually recorded.

Source: [GitHub's closing-keyword and default-branch rules](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

### Concise commit example

```text
Add XIAO Multiboard cradle and record X1 approval

* Added Seeed Studio XIAO Multiboard cradle with antenna slot.
* Seeed X1 Multiboard cradle has been print tested and approved.
```

Append the applicable `Fixes`/`Refs` lines and the final attribution required by
[AGENTS.md](../../AGENTS.md#git-commit-attribution). Print approval is a model-status
change; build commands and validation results belong outside the commit message.

## Planned publishing

- [#1 — GitHub Releases for versioned model downloads](https://github.com/ShakataGaNai/b123d/issues/1)
- [#2 — GitHub Pages model preview gallery](https://github.com/ShakataGaNai/b123d/issues/2)

These are open follow-ups, not implemented services. The gallery is for this repository's models, not the optional upstream build123d documentation site.
