# Lessons

## 2026-04-19

- If the user changes a destructive or cleanup instruction mid-task, stop that step immediately and preserve the source material unless they restate deletion explicitly.

## 2026-04-23

- **Backtest accounting:** always track `cash` and `position` separately. On entry, `cash -= shares * fill`. On exit, `cash += shares * fill`. Mark-to-market as `cash + position * close`. Never use a single `equity` variable that doubles as both cash and position value — you will double-count. Verify with identity `starting_cash + sum(pnl) == final_cash`. Symptom: implausibly deep drawdown vs stop-loss setting.
