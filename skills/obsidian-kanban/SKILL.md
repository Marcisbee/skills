---
name: obsidian-kanban
description: Manage tasks on an Obsidian Kanban board. Read the board, move tasks between columns, and update task status. Never creates or deletes the kanban file. Use when you need to track task progress on a Kanban board stored as an Obsidian markdown file.
license: MIT
metadata:
  author: Mārcis Bergmanis
  version: "1.0"
  keywords: kanban, obsidian, tasks, project management
---

# Obsidian Kanban

You manage project tasks on an Obsidian Kanban board. The kanban file location should be specified in the project's CLAUDE.md or provided by the user.

## Rules (Never break these)

1. **Never create or delete the kanban file** — only read and edit it in place
2. **Never modify the YAML front-matter** (the `---` block at the top)
3. **Never modify the `kanban:settings` block** at the bottom of the file (wrapped in `%% kanban:settings ... %%`)
4. **Preserve the exact column order** as found in the file
5. **Use the correct checkbox syntax**: `- [ ]` for open tasks, `- [x]` for completed tasks in Done

## Typical columns

| Column | Meaning |
|---|---|
| **Backlog** | Ideas and future work, not yet prioritized |
| **Todo** | Prioritized work, ready to be picked up |
| **High priority** | Urgent tasks that should be done next |
| **In progress** | Currently being worked on |
| **Done** | Completed tasks (use `- [x]` checkbox) |

Column names may vary per project — always read the file first to discover the actual columns.

## Workflow

When starting work on a task:
1. Read the kanban file
2. Move the task from its current column to **In progress** (keep it as `- [ ]`)

When finishing a task:
1. Read the kanban file
2. Move the task from **In progress** to **Done** and change `- [ ]` to `- [x]`

When asked to show/display the board:
1. Read the kanban file
2. Present the columns and tasks in a readable format

## How to move a task

Use the Edit tool to:
1. Remove the task line from its current column
2. Add the task line to the target column
3. If moving to Done, change `- [ ]` to `- [x]`
4. If moving out of Done, change `- [x]` to `- [ ]`
5. Keep blank lines between columns consistent — each column header should have tasks directly below it, followed by blank lines before the next column
