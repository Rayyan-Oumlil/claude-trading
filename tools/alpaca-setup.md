# Alpaca — Paper Broker + Data

Free, API-first. Used for paper trading US equities + free historical OHLCV + news.

## Why Alpaca

- Free paper account with $100k simulated buying power.
- Clean API and SDK (`alpaca-py`).
- IEX-quality historical data on the free tier is sufficient for daily bars.
- Moving from paper to live is a URL + key swap (when I decide to pay later).
- **Not** my live broker of choice (Public.com has the Claude MCP for that), but the best free paper sandbox.

## Setup

See [../paper-trading/broker-setup.md](../paper-trading/broker-setup.md) for the full setup including `.env`, smoke test, and optional MCP server.

## Limitations I should know

- IEX-only data on free tier = thin on premarket / small caps. For those, use paid SIP tier when I get there.
- Crypto on Alpaca is available but I'm using freqtrade / Binance for crypto. Don't split execution across venues for the same strategy.
- Order types supported: market, limit, stop, stop-limit, trailing. Bracket orders also supported.
- Rate limits exist. Respect them or get 429'd.

## Moving from paper to live (FUTURE — not now)

Switch the URL: `https://paper-api.alpaca.markets` -> `https://api.alpaca.markets`. Regenerate keys for the live account. Fund the account. **Only after ROADMAP stage 3 gates are met.**
