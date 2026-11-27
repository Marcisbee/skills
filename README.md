# skills

A collection of agent skills for Claude Code, Codex, and compatible tools — reusable knowledge packs for specific libraries, tools, and workflows.

## Structure

Each skill lives in its own directory and contains:

- `SKILL.md` — the main skill definition with frontmatter metadata and core documentation
- `references/` — supplementary guides (e.g. framework-specific integrations)
- `agents/` — optional agent-specific display and invocation metadata

## Available Skills

| Skill | Description |
|-------|-------------|
| [car-concept-to-blender](skills/car-concept-to-blender/SKILL.md) | Generate and revise a car concept, then build an editable Blender model after design approval. |
| [character-concept-to-blender](skills/character-concept-to-blender/SKILL.md) | Review a character or garment concept, then build a rigged body or fit removable clothing to multiple characters in Blender. |
| [exome](skills/exome/SKILL.md) | Exome.js state management — deeply nested stores, actions, framework integrations (React, Vue, Svelte, Solid, Lit, Angular, RxJS, vanilla) |
| [obsidian-kanban](skills/obsidian-kanban/SKILL.md) | Manage tasks on an Obsidian Kanban board — move tasks between columns, update status, track progress |
| [review-pr](skills/review-pr/SKILL.md) | Review pull requests for defects and collect supported findings in an HTML report. |
| [tech-rnd](skills/tech-rnd/SKILL.md) | Technical and product R&D — independent research, alternative comparisons, reproducible evaluations, standalone PoC demos, and concise implementation handoffs |

## Usage

List available skills:

```bash
npx skills add marcisbee/skills --list
```

Install a skill:

```bash
npx skills add marcisbee/skills --skill exome
```

Install the technical R&D skill:

```bash
npx skills add marcisbee/skills --skill tech-rnd
```

## License

MIT
