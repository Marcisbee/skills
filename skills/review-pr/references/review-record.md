# Review evidence records

Keep one JSON record in scratch storage. Keep logs and other evidence in the same folder. Use this record across review passes. Do not put it in the PR or publish it without authorization.

The record contains review evidence. It does not replace source examination, candidate rejection or the final language audit. Use short notes for a small change. Keep all findings with evidence, with stable IDs and no count limit.

## Requirements and contracts

Record specified behavior from the PR, linked requirements and applicable contracts. Give each item a source. Map it to code and selected tests. Include affected API consumers and exported formats. Compare the specified behavior with the code, including behavior with no implementation.

For changed approval fields or validator rules, name the fields, values or boundary inputs in the requirement notes. Link the test or source evidence for each approval or verification entry point. Record a gap if a successful end-to-end test did not exercise one of those inputs.

Do not invent requirements to fill the map. Use an empty `requirements` array with `requirements_note` if you cannot find a requirement. Record missing code, missing tests and tests with limited scope as gaps. A gap alone is not a product defect. Find the trigger and effect before adding a finding.

## Test plans

Read CI configuration and package scripts before selecting commands. Include the changed package and affected consumers. A root command can exclude a changed package.

Record the command, working directory and scope before execution. Hash the configuration and script files that control the plan. For a direct source experiment, include the source file under examination. Use SHA-256 of Git blob bytes at `target.head`.

Use a saved plan only if its source hashes and target revision agree. If they change, read the new configuration and adjust the plan. Do not use previous results as results for a new revision.

Record the executed command, revision, exit code, result and log. Include added harness files with the evidence. State fixture dependencies and changes to the execution environment in the result. A hash does not show execution or sufficient test coverage. The reviewer must examine the command, harness, log and covered behavior.

Tests with no dependency on each other can run in parallel. Finish them before delivery, or state the unfinished scope. Select CI jobs from the review scope before execution.

## Browser plans

For affected UI behavior, record the route, viewport, actions, expected result and result from the browser. State the app revision and all fixture services. Include assertions in the linked check log. Include screenshots when they help show the result.

Use the app under review when possible. Identify a component harness or fixture as such. Do not describe a fixture result as a production result. Do the same behavior test again after a correction. Update the plan when the correction changes its inputs.

Do a browser test even when workers cannot run. The lead can do this work. If execution cannot start, record the cause and the behavior with no browser test.

## Record format

Include `target`, `files`, `requirements`, `findings`, `checks` and `browser`. Use empty arrays for sections with no items. Do not create tests or browser runs to fill a section.

| Section | Fields and meaning |
|---|---|
| `target` | `base_repo`, `head_repo`, `base_ref`, `base`, `head`, `merge_base`. Use full commit IDs. |
| `files` | One object per changed path: `path`, `status`, `note`. Status is `read` or `blocked`. |
| `requirements` | `id`, `text`, `source`, `paths`, `checks`, `gap`. Paths refer to source files at the head. |
| `findings` | `id`, `priority`, `location`, `trigger`, `effect`, `evidence`, `references`, `counterevidence`, `fix`, `checks`. |
| `checks` | `id`, `command`, `cwd`, `paths`, `sources`, `revision`, `status`, `exit_code`, `log`, `log_sha256`, `result`. |
| `browser` | `id`, `paths`, `revision`, `route`, `viewport`, `actions`, `expected`, `fixtures`, `result`, `status`, `check`, `artifacts`. |

Use different IDs for items in the same section. `checks` in a requirement or finding contains check IDs. A finding can have no executable test. Keep its source evidence in `evidence` and `references`.

In `files.note`, name the behavior and consumers read, or the access limit. A `read` label alone does not show coverage. For a rename, use the destination path. For a deletion, use the previous path.

Each code reference has `path`, `line` and `side`. `side` is `new` for the head or `old` for the merge-base. Use a changed line for the finding location. Evidence references can point outside the diff. For metadata changes without text hunks, use `line: null` and explain the location in `note`.

Keep rejected scanner candidates in scratch notes. Do not convert a candidate without evidence into a PR comment to fill the record. `counterevidence` states the guards, adapters or exceptions examined. A symbol name match does not show a call path.

For requirements, `gap` must contain text if code or selected tests are missing. It must also explain linked tests without a satisfactory result. Use `requirements_note` when the requirements array is empty. The map is a review plan. The reviewer must examine the implementation.

For checks, `paths` states package and consumer scope. `sources` maps source paths to SHA-256 hashes. `revision` must equal `target.head`. Status is `passed`, `failed`, `timeout`, `blocked` or `not_run`. Use `exit_code: 0` for `passed` and a nonzero integer for `failed`.

For `passed`, `failed` or `timeout`, include a log and its SHA-256 hash. Other statuses can have `exit_code: null`. Explain blocked or unfinished execution in `result`. Use artifact paths relative to the record folder. Keep artifacts in that folder.

For browser plans, use `[width, height]` for `viewport`. Use two positive integers. `actions` is an array of instructions. `check` links a completed plan to its check record. The two statuses must agree. Browser status is `passed`, `failed`, `blocked` or `not_run`. `artifacts` is an array of saved artifact paths. Use an empty array if no artifact applies.

## Validate before delivery

Run the helper against the source repository and review record:

```sh
python3 <skill-dir>/scripts/validate_review.py --repo <source-repo> <record-folder>/review.json
```

The helper reads Git objects and local evidence. It does not execute project commands, fetch code or post comments. It shows record faults together. Exit code `0` means that its record checks found no fault. Code `1` shows record faults. Code `2` shows an input or Git operation error.

It compares the changed-file inventory, source references, saved plan hashes, log hashes and recorded status links. It shows blocked scope. It cannot show defect correctness, test execution, complete contracts or remote PR identity. A record with no schema faults can contain a false claim. The lead must examine the evidence and get the current remote target.

Correct record faults before delivery. Do not remove a finding with evidence to get exit code `0`. If the helper cannot record evidence, examine it manually and state that validation limit. If Python or Git cannot run, do the record comparisons manually and state the limit. If the helper cannot finish, state the validation gap.

Include findings with evidence and scope limits that can change the review result in the final batch. Keep the full record in scratch storage.
