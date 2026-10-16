# swag

My personal agent skills, packaged as an [Agent Plugin](https://agent-plugins.org) for Cursor, Claude Code and anything else that reads `SKILL.md`.

| Skill | What it does |
| --- | --- |
| [reply-like-me](skills/reply-like-me/README.md) | Learns how you write from your chat, email and docs, then drafts your replies in your voice. |

## Install

**Cursor (as a plugin):** clone into `~/.cursor/plugins/local/swag`, then run **Developer: Reload Window**.

```sh
git clone https://github.com/mjward/swag ~/.cursor/plugins/local/swag
```

**Just the skills:** copy a folder from `skills/` into `~/.cursor/skills/` or `~/.claude/skills/`.

## Adding a skill

Add a folder under `skills/` with a `SKILL.md` (frontmatter `name` and `description`), then add a row to the table above.
