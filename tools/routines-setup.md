# Claude Code Routines Setup

This is the operating guide for turning this workspace into a scheduled Claude system without breaking the paper-first guardrails.

## What a routine is

A routine is a scheduled Claude run. It wakes up, reads files, uses available tools/APIs, does its job, writes back the result, and exits.

The important architectural fact is that the run itself is stateless. Durable memory lives in files.

## Local vs remote

### Local routine

Use local when:

- testing a prompt
- iterating on file layout
- debugging broker or research calls

Properties:

- runs on my machine
- can see local files
- stops if my computer or Claude Desktop is off

### Remote routine

Use remote when:

- I need weekday reliability
- I want runs while my machine is off
- I want the repo to act as durable memory between runs

Properties:

- runs in a temporary cloud environment
- clones the repo, works, then the environment disappears
- only persists learning if it commits and pushes updated files back to GitHub

## GitHub requirement

Remote routines should run from a **project-scoped private GitHub repo**.

This is subtle because the current git root on this machine is above the project folder. That is dangerous for remote automation and even for normal git status because unrelated desktop projects can leak into the same repository.

Recommendation:

1. Create a dedicated private GitHub repo for `Claude Trading`.
2. Make the project itself the git root.
3. Use that repo for remote routines.

Do not run remote automation from a machine-wide git repo.

## Required routine permissions

For remote routines that write state back:

- network access enabled
- the correct environment selected
- **Allow unrestricted branch pushes** enabled if the run needs to push updates back

Without branch-push permission, the routine may update files locally in the run and then fail to persist them.

## Environment variables

Remote routines should get secrets from the Claude environment, not from `.env`.

Suggested variables:

```env
ALPACA_API_KEY=
ALPACA_API_SECRET=
ALPACA_BASE_URL=https://paper-api.alpaca.markets
PERPLEXITY_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
CLICKUP_API_TOKEN=
```

## Exact-name rule

If the environment contains `ALPACA_API_SECRET`, the prompt must say `ALPACA_API_SECRET`.

Not:

- `ALPACA_SECRET`
- `ALPACA_SECRET_KEY`
- `alpaca_api_secret`

This exact-name mismatch was a real failure mode in the video notes.

## Recommended weekday schedule

- `06:00` pre-market
- `08:30` market open
- `12:00` midday
- `15:00` close
- `Friday 16:00` weekly review

These are examples. The pattern matters more than the exact clock.

## How memory persists

The routine memory path is:

1. Read `memory/` files.
2. Read the latest relevant journal entry.
3. Do the work.
4. Update memory/journal/log files.
5. Commit and push if remote.

If step 5 is missing on a remote run, the next run does not inherit the update.

## Context budget discipline

Treat each run as having a small working set.

Rules:

- read `memory/` first
- read only the latest relevant journal entry, not every journal file
- read the active strategy spec only if the routine touches that strategy
- avoid loading heavy research notes unless they are directly relevant
- do not leave unnecessary MCP servers enabled

The point is not just cost. Large context degrades run quality.

## Testing with `Run now`

Every new routine should be tested manually before trusting the schedule.

Suggested test flow:

1. Run the routine with `Run now`.
2. Watch the live execution.
3. Confirm env vars resolved correctly.
4. Confirm the routine touched only the expected files.
5. Confirm notification behavior is correct.
6. If remote, confirm the commit actually landed in GitHub.

Repeat until the run is boring.

## Suggested routine prompt contract

Each routine prompt should explicitly say:

- read memory files first
- use environment variables, not `.env`
- check kill switch before execution
- stay inside paper mode unless files explicitly allow otherwise
- update memory files and journal before exit
- commit and push if remote and files changed

## Safety defaults

- Start in paper mode
- Max 5% per position unless a strategy spec says smaller
- Stop if broker state cannot be confirmed
- Stop if the kill switch exists
- Notify only on urgent events or meaningful execution
