# claude-trading-skills

Skill pack cloned at [../claude-trading-skills/](../claude-trading-skills/). Provides prompt-based skills for stock screening, research, options analysis.

## What it is

A collection of Claude Code skills (prompt templates with strict spec) that I can invoke as `/skill-name` inside a session.

## Setup

1. The repo is already cloned locally.
2. To make skills available to Claude Code, symlink or copy the skill files into `~/.claude/skills/<name>/`.
3. Run `/list-skills` inside Claude Code — new skills should appear.

See the repo's own README for the exact skill-install procedure.

## Skills I want to use first (Stage 0)

| Skill | Use case |
|-------|----------|
| stock-screen | Screening the S&P 500 by custom criteria |
| ticker-research | Deep dive on a single name |
| options-chain-summary | Read an options chain, no Greeks required |

## Integration with the rest of this workspace

- Skills produce output → I save the output to `research/<ticker>.md` with today's date.
- The [../prompts/research-stock.md](../prompts/research-stock.md) prompt is my meta-wrapper that calls the skill + forces the output to land in a file.
- When I find a skill that's useful, add a line to this file so future-me knows why it's installed.

## Skill hygiene

- Don't install every skill "just in case" — each loads context per session.
- If I haven't used a skill in a month, uninstall it.
- Keep custom skills I build myself in this workspace (e.g. `skills/backtest-reporter/`) so they version-control with the rest of my trading setup.
