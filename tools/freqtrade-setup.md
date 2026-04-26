# Freqtrade — Crypto Bot Framework

Already installed and configured. Running in dry-run mode at `docker-compose up -d`.

## What it is

Python crypto trading bot, Docker-based. Supports backtesting, dry-run (paper), and live across many exchanges. Strategies are Python classes.

## Where things live

- Container config: [../docker-compose.yml](../docker-compose.yml)
- Bot config: [../ft_userdata/config/config.json](../ft_userdata/config/config.json)
- Strategies: [../ft_userdata/strategies/](../ft_userdata/strategies/)
- Data: [../ft_userdata/data/](../ft_userdata/data/)
- UI: http://localhost:8080 (credentials in `config.json`)

## Day-to-day commands

```bash
# start
docker-compose up -d

# logs
docker-compose logs -f

# stop (see paper-trading/kill-switch.md for force-close)
docker-compose stop

# backtest a strategy
docker-compose run --rm freqtrade backtesting \
  --config //freqtrade/user_data/config/config.json \
  --strategy SimpleMA \
  --timerange 20250101-20260101

# download historical data
docker-compose run --rm freqtrade download-data \
  --config //freqtrade/user_data/config/config.json \
  --pairs BTC/USDT ETH/USDT \
  --timeframe 1h \
  --days 365
```

## Gotchas (learned the hard way)

- **Git Bash path mangling:** on Windows, paths like `/freqtrade/user_data/...` get converted to Windows paths. Use **double-slash** `//freqtrade/user_data/...` to keep them as POSIX paths inside the container.
- **Dry-run != real fills.** Dry-run assumes you get filled at the midpoint (or specified model). Paper fill on a thin pair will be much worse. Don't graduate to live just because dry-run looked good.
- **Strategy class name = file name (required).** `SimpleMA.py` must contain `class SimpleMA(IStrategy)`.
- **Interface version:** use `INTERFACE_VERSION = 3`. Older versions are deprecated.
- **Config reloads:** edit `config.json` → `docker-compose restart` (not just stop/start) → verify via FreqUI dashboard.

## First strategy lessons (baseline)

The default SimpleMA strategy lost ~16% in a window where BTC returned ~18%. That's not a freqtrade problem — it's a Stage-1 lesson: a naive MA crossover is not an edge. It's training data for learning to read a backtest report properly.

## When to pair with the multi-agent flow

Once a crypto strategy is in [../agents/](../agents/) rotation, the freqtrade bot becomes the execution layer for the Portfolio Manager role (crypto side). The Alpaca path does the same for equities.
