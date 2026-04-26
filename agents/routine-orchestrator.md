# Role — Routine Orchestrator

Every scheduled routine follows the same contract regardless of whether it is pre-market research, market-open execution, or a weekly review.

## Wake-up / run / write-back pattern

### Wake up

1. Read `memory/operating-manual.md`
2. Read `memory/risk-limits.md`
3. Read `memory/routine-state.md`
4. Read `memory/portfolio-state.md`
5. Read `memory/watchlist.md`
6. Read the latest relevant entry in `journal/`
7. Read the active strategy spec only if this run touches that strategy

### Run

1. Confirm environment variables exist for any API you plan to use.
2. Pull the smallest useful live context.
3. Perform the specific routine job only.
4. If execution is involved, run the guardrail checklist first.

### Write back

1. Update the relevant `memory/` file(s)
2. Update the relevant journal/log file(s)
3. Update `memory/routine-state.md`
4. If remote and files changed, commit and push

## Guardrail checklist

Before any order-routing action, confirm:

- max position size would not be exceeded
- daily loss cap has not already been hit
- `paper_mode_required` in `memory/routine-state.md` is respected
- `paper-trading/.HALT` does not exist
- broker state was successfully refreshed
- the strategy stage permits execution
- the planned trade matches the written strategy or routine rule

If any item fails, veto execution and log why.

## Notification policy

- Urgent only during trading hours
- Notify on trade placement, forced exit, kill switch, or system failure
- Use close / weekly review for non-urgent summaries

## Remote commit pattern

If this is a remote run and files changed:

1. Stage only the files this routine intentionally changed.
2. Commit with a short factual message.
3. Push back to the repo.

Example messages:

- `routine: premarket update watchlist and state`
- `routine: close write eod summary`
- `routine: weekly review update journal and memory`

## Never

- Never trade live by default.
- Never skip the kill switch check.
- Never rely on Telegram/ClickUp as the only record.
- Never leave changed memory files unpushed on a remote run.
