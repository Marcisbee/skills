# Save the review as one HTML file

Generate one HTML report for each PR when local Git objects and Python 3.9 or later are available. Use the validated review record and the same final comments as the chat. The report reads the merge base and head directly from Git. It includes all changed files and puts comments at their recorded diff locations. It includes the check status, scope notes and selected screenshots. The review path links to groups of files. The reader can mark files as viewed.

Write a presentation JSON file in scratch storage. Use final ASD-STE100 prose for its visible text. Include this text in the same language audit as the chat batch. Use plain text with optional backticks for code names in comment titles and bodies.

```json
{
  "title": "Update quote refresh",
  "label": "Repository PR 42",
  "change_groups": [
    {"title": "Quote refresh", "summary": "Follow the form input to the quote request.", "paths": ["src/quote.ts"]}
  ],
  "summary": ["The update waits for a new quote."],
  "limits": ["The browser used local API fixtures."],
  "notes": ["Can the form use the shared date picker?"],
  "comments": {
    "F1": {
      "title": "Keep the current quote",
      "body": "When the form changes, discard the previous quote.",
      "thread": "https://example.com/pull/42#previous-comment"
    }
  },
  "check_notes": {"UI": "The browser used a local API fixture."},
  "screenshots": [{"path": "artifacts/form.png", "caption": "Policy form at 375 pixels."}]
}
```

Use the PR title or a short description of the change as the title. Put the PR number in the optional label. Use one or two sentences to explain what changed. Do not repeat the title, comments or test counts.

Use optional `change_groups` to give the reader an order for the changed behavior. Give each group exact changed paths. Add a short description only if it tells the reader what to examine. Use the new path for a rename. List each path once. The report adds other paths and keeps them available. Open a group to read its comments and file diffs in place. The Files view lets the reader select one file. If you have no basis for a custom order, use the default order.

Use exactly one comment for each finding ID. Use an empty object if there are no findings. Only `title` and `comments` are mandatory. The `thread` is an optional HTTPS link. Use `check_notes` for each result that affects the review. Include failures that show a defect and setup errors that prevent a necessary check. Use the check IDs from the record. Give each note a short outcome. The overview shows these results and links to the full run history. Use CI results for the same revision and scope when available. State a material CI result with its source in the review response. Put questions and possible simplifications in `notes`. Use `limits` for gaps that affect the result.

Use these optional fields to write the overview. Use evidence from the reviewed revision.

- `plan` lists items with `title`, `status` and `requirement`. Copy each requirement ID from the record. Use `done`, `issue`, `partial` or `unverified`. Use `outside` for a material change outside the plan. Add a short `evidence` sentence for `done` and `issue`. A requirement with a gap cannot use `done`.
- `merge_findings` lists finding IDs that need attention before merge. P0 and P1 findings appear there automatically. Use `merge_notes` items with `text` for actions such as a coordinated release. Give the action and the reason.
- `check_history` maps additional run IDs to a short `label`. Use `kind: "setup"` for a setup error or `kind: "observation"` for a run that collected evidence without a pass or fail assertion. Use the evidence for each label. The history keeps the recorded run status.
- `project_checks` maps check IDs to an item with a `label`. The command comes from the record. Add `duration` only if the results give a duration. The status comes from the record. Routine passing project checks appear in the run history.
- `flows` lists behavior paths with a `title` and ordered `steps`. Give each step its `text` and `state` of `new`, `changed` or `existing`. Use short paths that help the reviewer follow the change. The report shows the steps without a disclosure control.
- `group_focus` maps change group titles to `focus` or `skim`. Put higher-risk changes first.
- `coverage` gives the LCOV `path` relative to the record folder, full head `revision` and a short `scope`. Use repository-relative file paths in LCOV. The report counts only added lines with measurements. State which suites ran and give material measurement limits. Omit this field if you have no measurement. Use `test_gaps` for material gaps in the available results.

A plan item, merge note or flow step can link to a changed `path` and an optional new-side `line` in the displayed diff. Use only locations you can verify. Project commands come from recorded runs.

Select screenshots that explain a comment or show a material check. Use PNG or JPEG files under the review record folder. Use captions that describe the state, fixture or width when applicable. Examine the selected images and prose before inclusion. The report contains source changes from the PR and copies of the selected images. Keep it within the user's authorized delivery scope. Keep raw logs, rejected candidates and private scratch notes in scratch storage.

```sh
python3 <skill-dir>/scripts/render_review.py --repo <source-repo> <record.json> <presentation.json> <report.html>
```

Choose a new output path. Open the report in a browser when available. Make sure that the comment count agrees with the final batch and that a comment link opens its diff. Make sure that serious comments are open on the overview. Examine the selected images and a narrow viewport. Make sure a file can be marked as viewed and the count changes. Link the file in the final response. If Git objects or the renderer are unavailable, deliver the complete batch with the available locations and state the report limit.
