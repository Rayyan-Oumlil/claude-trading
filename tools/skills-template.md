# Skills.md Template for Exchange Automation

This file is the foundation of all Claude Code automation routines. It defines how Claude connects to exchanges, executes trades, and runs multi-agent research workflows.

## Usage

1. Create `skills.md` in your Claude Code project folder (next to `.env` or via environment variables)
2. Configure the exchange credentials section
3. Use `/trade-*` commands in Claude Code or co-work prompts
4. (Optional) Use webhooks for TradingView signal automation

## Key Security Principles

- API keys are **never** sent to servers. All request signing happens locally on your machine.
- Withdrawal permissions should always be **disabled** on exchange API keys used for automation.
- Use sub-accounts to isolate automated trading from your main account.
- Test all automations on paper/sandbox before live.

---

## Section 1: Exchange Connection Setup

```markdown
# Exchange API Connection (Encrypted Locally)

## Supported Exchanges

- Binance, Bybit, Blofin, OKX, WEX (crypto futures + spot)
- Alpaca (US equities paper, via MCP)
- Public.com (US equities live, Stage 3+, via MCP)

## Setup Instructions

To configure an exchange, gather these from your broker account:

1. **API Key** — public key for authentication
2. **Secret Key** — private key (keep offline)
3. **Passphrase** (some exchanges only) — additional authentication
4. **UID** (some exchanges only) — user identifier

Store these in environment variables:
- `{EXCHANGE}_API_KEY`
- `{EXCHANGE}_API_SECRET`
- `{EXCHANGE}_PASSPHRASE` (optional)
- `{EXCHANGE}_UID` (optional)

Example for Bybit:
```
BYBIT_API_KEY=your_key
BYBIT_API_SECRET=your_secret
```

## Encryption Note

When you provide these credentials to Claude, the skill encrypts them locally. The keys never leave your machine. All trades are signed using local cryptography.
```

---

## Section 2: The 16 Trade Skills

```markdown
# /trade-* Command Reference

## Full Analysis (Stage 1+)

- `/trade-analyze {TICKER}` — Full investment thesis report (5 agents, 15+ metrics, PDF output)
  - Technical score
  - Fundamental score
  - Sentiment score
  - Risk assessment + mitigation strategies
  - Entry/exit strategy with specific price targets
  - Position sizing guidance

- `/trade-quick {TICKER}` — 60-second snapshot (4 key metrics, text)

## Dimension-Specific Analysis (Stage 0+)

- `/trade-technicals {TICKER}` — RSI, MACD, Bollinger Bands, key levels (52-week, Fibonacci), trend direction
- `/trade-fundamentals {TICKER}` — Revenue growth, net margin, P/E, analyst target vs current (equities only)
- `/trade-sentiment {TICKER}` — News sentiment, social sentiment, institutional positioning (1-10 confidence)
- `/trade-thesis {TICKER}` — Bull case, bear case, catalysts, thesis score

## Execution

- `/trade-open {TICKER} {SIDE} {SIZE} {LEVERAGE} {ENTRY} {STOP} {TAKE_PROFIT}` — Market/limit orders
- `/trade-close {TICKER} {QUANTITY|PERCENTAGE}` — Partial or full close
- `/trade-portfolio` — Current positions, P&L, correlation matrix
- `/trade-history {DAYS}` — Recent trade log + win rate

## Specialized

- `/trade-options {TICKER}` — Greeks, implied vol, contract screener (not execution)
- `/trade-compare {TICKER1} {TICKER2}` — Head-to-head analysis
- `/trade-risk {POSITION}` — Drawdown scenario, liquidation distance (if leveraged), margin health

## Scan (Crypto)

- `/trade-scan-funding` — Rank all pairs by annualized funding rate (collect passive yield)
- `/trade-scan-catalyst` — Monitor Twitter/news for event-driven moves
```

---

## Section 3: Multi-Agent Workflow

```markdown
# The 5-Agent Research System

When you run `/trade-analyze`, Claude deploys 5 agents in parallel:

### Agent 1: Technical Analyst
- Detects regime (trending vs ranging)
- Calculates indicators (MA, RSI, MACD, Bollinger Bands)
- Identifies key levels (52-week, Fibonacci, support/resistance)
- Output: technical score (0-100), trend direction, key levels table

### Agent 2: Fundamental Analyst
- Pulls latest financials (revenue, margin, earnings growth, valuation)
- Compares vs analyst consensus and historical averages
- (Equities only; crypto returns "not applicable")
- Output: fundamental score (0-100), valuation assessment, competitive mode

### Agent 3: Sentiment Analyst
- Aggregates news sentiment (last 7 days, trending vs baseline)
- Monitors social media mentions (Twitter, Reddit, TradingView)
- Checks institutional positioning if available
- Output: sentiment score (0-100), 1-10 confidence, key catalysts list

### Agent 4: Risk Manager
- Calculates position sizing using Kelly Criterion or fixed %
- Estimates max drawdown and liquidation distance
- Flags earnings dates, data gaps, low-liquidity windows
- Output: veto reasons, position size recommendation, risk matrix

### Agent 5: Thesis Synthesizer
- Aggregates all 4 scores
- Generates bull case (3-5 key reasons)
- Generates bear case (3-5 key risks)
- Produces entry/exit strategy with specific prices
- Output: trade score (0-100), thesis conviction, action recommendation

---

### Execution Flow

1. **Discovery phase** — Web search for ticker, market cap, latest news, key metrics
2. **Parallel analysis** — Launch agents 1-5 simultaneously
3. **Synthesis** — Combine outputs into structured report with PDF export
4. **Wait for user signal** — Never auto-executes. User reviews report, then triggers `/trade-open` manually
```

---

## Section 4: TradingView Webhook Integration

```markdown
# Connecting TradingView Alerts to Claude via Webhook

This allows your TradingView strategy to automatically trigger trades through Claude.

## Step 1: Generate a Webhook Endpoint

Ask Claude:
> "Create a webhook endpoint that accepts TradingView alerts. When a signal arrives with JSON like `{symbol: "BTCUSDT", side: "long", size: 100, leverage: 10, stop: -3%, profit: +8%}`, execute the trade on Bybit using my connected API."

Claude will generate a unique webhook URL.

## Step 2: Configure TradingView Alert

1. In TradingView, create your strategy/indicator
2. Click **Create Alert**
3. In **Webhook URL** field, paste the URL from Step 1
4. In **Alert Message** field, format your signal as JSON:

```json
{
  "symbol": "{{ticker}}USDT",
  "side": "long",
  "size": 100,
  "leverage": 10,
  "stop_pct": -3,
  "profit_pct": 8
}
```

5. Set **Alert Frequency** to "Once per bar" or "Every time" depending on your strategy
6. Click **Create**

## Step 3: Test

Enable the alert but do **NOT** go live with real size yet.

1. Create a small test signal on TradingView (e.g., in backtest mode, set an alert on a historical bar)
2. Watch Claude Code console to see the webhook fire
3. Confirm the trade details are correct
4. If correct, run one small live trade
5. If all goes well, enable full automation

## Step 4: Go Live (Optional)

Once tested, the webhook runs automatically. Claude will:
- Receive the signal
- Validate parameters
- Submit the trade to your exchange
- Log the execution to memory
```

---

## Section 5: Automation Patterns (Routines)

```markdown
# Common Routine Use Cases

Routines are Claude Code tasks that wake up, read memory, do a job, and write back.

### Pattern 1: Pre-Market Briefing (6:00 AM)

Trigger: Daily cron at 6:00 AM

Routine:
1. Read `memory/watchlist.md` (your tracked tickers)
2. For top 5, run `/trade-quick` and `/trade-sentiment`
3. Compile into morning briefing PDF
4. Send to Telegram or email
5. Log to `memory/briefing-log.md`

### Pattern 2: Funding Rate Scanner (Every 10 min, Crypto)

Trigger: Every 10 minutes (local or remote)

Routine:
1. Run `/trade-scan-funding` on all major pairs
2. Identify top 5 by annualized yield
3. Check `memory/funding-positions.md` for current holdings
4. If a new high-yield pair appears, alert via Telegram
5. Update `memory/funding-positions.md` with latest rates

### Pattern 3: External Signal Monitor (Every 10 min, Crypto)

Trigger: Every 10 minutes

Routine:
1. Poll Twitter/Truth Social for monitored accounts (e.g., @elonmusk, @VitalikButerin)
2. If a relevant tweet detected, run `/trade-sentiment`
3. If sentiment shifts >20 points, alert via Telegram
4. (Optional) Auto-close risky positions if signal is bearish
5. Log to `memory/signal-log.md`

### Pattern 4: Daily Performance Review (4:00 PM)

Trigger: Daily at 4:00 PM (weekdays only)

Routine:
1. Read `memory/portfolio-state.md` (current positions + entry prices)
2. Run `/trade-portfolio` for updated P&L
3. Calculate daily win rate, R-multiple average
4. Generate summary graphic (equity curve)
5. Email or Telegram to user
6. Write journal entry to `journal/2026-04-19.md`

### Pattern 5: Weekly Backtest + Paper Reconciliation (Friday 4:00 PM)

Trigger: Friday at 4:00 PM

Routine:
1. Read `strategies/active-strategy/STRATEGY.md`
2. Run backtest for the past 6 months with live historical data
3. Compare backtest Sharpe vs paper account Sharpe (should be close)
4. If divergence >10%, flag for manual review
5. Update `memory/strategy-reconciliation.md`
6. Generate weekly report PDF + email
```

---

## Important Notes

- **Start small.** Test on paper or sandbox with 1% of capital before increasing size.
- **Monitor, don't ignore.** Routines should have alert channels. A silent bot is a broken bot.
- **Kill switch.** Always have a way to halt everything (`touch .HALT` or dashboard panic button).
- **Journal every trade.** Automated or not, log the decision, entry, exit, and outcome.
- **No emotion.** Once the rules are set and tested, let the bot follow them. Second-guessing kills edge.
