# Risk Limits

These are the system-level defaults until a strategy spec says otherwise.

## Core defaults

- Default mode: paper only
- Max position size: 5% of account equity
- Max new positions per day: 3
- Max daily realized loss before halt: 2% of account equity
- Default first live size: smallest broker-supported size only after stage gates pass
- Default action on missing data / stale broker state: no trade

## Guardrails

- If `paper-trading/.HALT` exists, veto all new trades.
- If a strategy is not at `paper` or `live` stage, it cannot route orders.
- If a routine cannot confirm current account state, it cannot trade.
- If a planned trade would exceed the per-position cap, reject it.
- If there is a same-day earnings / macro event that invalidates the strategy, reject it.

## Notification policy

- Urgent only during the trading day.
- Non-urgent summaries belong at close or weekly review.

## Review cadence

- Revisit these limits after the first real paper month, not after one emotional day.
