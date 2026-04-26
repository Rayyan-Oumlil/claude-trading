# Kill Switch

How to halt all paper activity in under 30 seconds, without needing to understand the code.

## Freqtrade (crypto)

```bash
docker-compose -f "C:/Users/rayya/Desktop/Claude Trading/docker-compose.yml" stop
```

Verify via the FreqUI at http://localhost:8080 — status should be "stopped". All open trades remain as-is; they don't get force-closed. To force-close first:

```bash
# inside freqtrade container
freqtrade stop_entry   # stop new entries
freqtrade forceexit all   # close all open positions at market
```

## Alpaca (equities, when configured)

Two ways:

1. **Paper dashboard:** https://paper-trading.alpaca.markets/ -> Orders -> Cancel All, Positions -> Close All.
2. **API kill-switch file:** the strategy runner checks for `paper-trading/.HALT` on every loop and exits if present.

```bash
touch "C:/Users/rayya/Desktop/Claude Trading/paper-trading/.HALT"
```

Remove the file to resume.

## Sanity checks after a kill

- Confirm no open orders in the broker UI.
- Confirm no open positions (or that remaining positions are flat by intent).
- Write a `journal/` entry before restarting. Understand WHY you killed it before you restart it.

## When to pull the plug

- Strategy behaves differently from the spec (any trade outside the rules).
- Data feed hiccup (stale bars, NaN values).
- Market event the strategy wasn't designed for (FOMC, flash crash, exchange outage).
- You are emotionally activated (stress, excitement, FOMO) — yes, that alone is a valid reason.
