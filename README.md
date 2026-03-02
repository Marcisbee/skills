# skills

A collection of Claude Code skills — reusable knowledge packs that give Claude domain expertise on specific libraries and tools.

## Structure

Each skill lives in its own directory and contains:

- `SKILL.md` — the main skill definition with frontmatter metadata and core documentation
- `references/` — supplementary guides (e.g. framework-specific integrations)

## Available Skills

| Skill | Description |
|-------|-------------|
| [exome](skills/exome/SKILL.md) | Exome.js state management — deeply nested stores, actions, framework integrations (React, Vue, Svelte, Solid, Lit, Angular, RxJS, vanilla) |
| [obsidian-kanban](skills/obsidian-kanban/SKILL.md) | Manage tasks on an Obsidian Kanban board — move tasks between columns, update status, track progress |

## Usage

List available skills:

```bash
npx skills add marcisbee/skills --list
```

Install a skill:

```bash
npx skills add marcisbee/skills --skill exome
```

## License

MIT
