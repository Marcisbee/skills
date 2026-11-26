# GitHub review evidence

Prefer an available GitHub connector when it supplies all needed data. Otherwise use the authenticated `gh` CLI. Do not print tokens or change authentication. These are read operations; posting needs an explicit user instruction.

## Freeze and collect

Use explicit owner/repo and PR number. Examples use `OWNER/REPO` and `NUMBER` as placeholders.

```sh
gh api repos/OWNER/REPO/pulls/NUMBER
gh api --paginate repos/OWNER/REPO/pulls/NUMBER/files
gh api --paginate repos/OWNER/REPO/pulls/NUMBER/comments
gh api --paginate repos/OWNER/REPO/pulls/NUMBER/reviews
gh api --paginate repos/OWNER/REPO/issues/NUMBER/comments
gh api --paginate repos/OWNER/REPO/pulls/NUMBER/commits
```

Record `base.repo.id`, `head.repo.id`, `base.ref`, `base.sha` and `head.sha`, including fork identity. The PR API's base SHA is not necessarily its merge-base. Get the merge-base from available git objects or the compare API. Use it for the change scope. Check the PR response again before delivery. Compare both repo identities, the base ref and both SHAs, not only the head. A changed base branch can change the merge-base with an unchanged head. Recompute scope and recheck affected evidence when the target changes.

REST inline comments include replies and outdated locations. Group by reply ID/review and inspect current code; do not assume an old comment is still applicable. Read review bodies as well as inline threads and PR discussion. GraphQL connections also need complete pagination. Handle deleted/hidden content as a gap.

## Inspect immutable code

Use existing git objects or an isolated scratch checkout when needed. Fetch only the required refs/commits; preserve the user's current checkout. With available immutable commits:

```sh
git merge-base BASE_SHA HEAD_SHA
git diff --name-status MERGE_BASE HEAD_SHA
git diff --find-renames MERGE_BASE HEAD_SHA
git show HEAD_SHA:path/to/file
```

Read whole affected functions and relevant consumers, not only the API's patch field. GitHub's file API is limited to 3,000 files and patch text can be absent/truncated, especially for binary/generated files. If the inventory exceeds API limits, use git or report incomplete scope. A compare endpoint has its own file limit; do not use it as an unlimited inventory. A missing patch is not an empty change. Verify renames and deleted paths.

For immutable line links use `https://github.com/OWNER/REPO/blob/HEAD_SHA/path#LNUMBER` (the recorded merge-base SHA and old-side line for removed lines). The latest base tip can have different old-side line numbers. Use current diff anchors or the host's verified PR-diff format when required. Do not claim a line was checked without reading that revision. `gh pr diff` reads current remote state; it is not a frozen snapshot if the PR moves.

Read the PR check results and their job links first. Include external CI status contexts when the project uses them. Verify the revision and job scope before you use a result. Run local checks that fill a material gap and suit the authorized environment. Keep exact commands/results. Use isolated temporary tests when needed, without changing the PR. Do not run deployments, network mutations or costly live integrations as an automatic review step.

Official mechanics: [PR REST API](https://docs.github.com/en/rest/pulls/pulls), [review comments](https://docs.github.com/en/rest/pulls/comments), [reviews](https://docs.github.com/en/rest/pulls/reviews), [compare commits](https://docs.github.com/en/rest/commits/commits#compare-two-commits).
