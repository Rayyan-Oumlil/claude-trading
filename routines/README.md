# Routines

This folder is the schedule-facing layer for the workspace.

The exact routine prompts live in [../prompts/](../prompts/), but this folder documents how the schedule is meant to behave as a system.

## Default weekday cadence

- `06:00` pre-market research and catalyst scan
- `08:30` market-open execution and stop placement
- `12:00` midday risk check
- `15:00` close review and write-back
- `Friday 16:00` weekly review

## Local vs remote

- Local routines are for fast testing and dry runs.
- Remote routines are for dependable automation, but they only persist memory if they push changes back to GitHub.

## Non-negotiables

- Every routine reads the memory files first.
- Every routine checks the kill switch before any execution.
- Every routine writes back outcomes before it exits.
- Every new routine gets tested with `Run now`.
