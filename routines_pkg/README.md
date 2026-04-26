# Routines Package

Python routines that read `memory/`, do a job, and write back. Designed to run
via Windows Task Scheduler (or any cron-equivalent) so they execute even when
Claude Code is closed.

## Scripts

| File | Schedule | Purpose |
|------|----------|---------|
| `premarket.py` | 06:00 Mon-Fri | Fetch latest bars for watchlist equities, write `memory/routine-state.md` |
| `eod_close.py` | 15:00 Mon-Fri | Fetch account + positions, append to `journal/YYYY-MM-DD.md`, update `memory/portfolio-state.md` |

## Wrappers

| File | Purpose |
|------|---------|
| `run_premarket.bat` | Invokes `premarket.py` with proper PYTHONPATH. Logs to `routines_pkg/logs/premarket.log` |
| `run_eod.bat` | Invokes `eod_close.py` with proper PYTHONPATH. Logs to `routines_pkg/logs/eod.log` |
| `register_tasks.ps1` | Registers both routines in Windows Task Scheduler |

## Run manually (anytime)

```bash
cd "c:/Users/rayya/Desktop/Claude Trading"
set PYTHONPATH=.
python routines_pkg/premarket.py
python routines_pkg/eod_close.py
```

## Register Windows Scheduled Tasks

**When to do this:** Only once you've started paper trading (Stage 2). Running
the routines before there's any activity just writes empty snapshots.

```powershell
cd "c:\Users\rayya\Desktop\Claude Trading"
powershell -ExecutionPolicy Bypass -File routines_pkg\register_tasks.ps1
```

Expected output:
```
Registered: ClaudeTrading-Premarket (Mon-Fri 06:00)
Registered: ClaudeTrading-EODClose (Mon-Fri 15:00)
```

### Verify

```powershell
Get-ScheduledTask ClaudeTrading-*
```

### Test a task without waiting

```powershell
Start-ScheduledTask -TaskName "ClaudeTrading-Premarket"
```

Check `routines_pkg/logs/premarket.log` for output.

### Remove

```powershell
Unregister-ScheduledTask -TaskName "ClaudeTrading-Premarket" -Confirm:$false
Unregister-ScheduledTask -TaskName "ClaudeTrading-EODClose" -Confirm:$false
```

## Non-negotiables (from PRINCIPLES.md #7)

- Every routine reads `memory/` files first.
- Every routine checks `is_halted()` before any execution.
- Every routine writes back outcomes before it exits.
- Every new routine gets tested with `Run now` before trusted.

## Troubleshooting

**Task doesn't fire:** Check `Get-ScheduledTask ClaudeTrading-Premarket | Select *`. Verify "LastRunTime" and "LastTaskResult". Code 0 = success.

**Python import errors:** The `.bat` wrappers set `PYTHONPATH=%CD%`. If you move the repo, update the scheduled task paths.

**Alpaca errors:** Routines load `.env` automatically. Verify `ALPACA_API_KEY` is set: `Get-Content .env | Select-String ALPACA`.

**Encoding errors on Windows:** All file I/O uses `encoding="utf-8"`. If you see `UnicodeDecodeError`, check you're not mixing cp1252 files.
