# Public.com — Live Broker via Claude Desktop MCP

**Only used when ROADMAP stage 3 gates pass.** Do not configure during stages 0-2.

## Why Public.com

- First broker with an official Claude Desktop MCP — native integration.
- Zero-commission stocks, ETFs, options, crypto.
- Designed for Claude-native workflows (conversational trade entry + execution).
- Fractional shares supported (required for small-size Stage 3 trading).

## What "stage 3 ready" means (checklist)

- [ ] Active strategy has ≥2 weeks of green paper trading matching backtest expectation.
- [ ] I've tested the kill switch under real fire conditions (not just a dry run).
- [ ] I've decided the funding amount (no-pain amount).
- [ ] I've written the stage-3 entry in my journal explaining WHY I'm moving to live.

## Setup (DEFERRED)

Install when stage 3 is reached:

1. Install Claude Desktop (separate from Claude Code — MCP lives there for now).
2. Link Public.com account via the Claude Desktop MCP marketplace.
3. Grant trading scope carefully — can limit to specific accounts or symbol sets.
4. Test with a $10 order first. Always.

## Hard rules once live

- First 30 days: trade 1/4 of backtest size. Survive first, scale second.
- Weekly drift check: live P&L vs. parallel paper P&L vs. backtest expectation. Any >2-sigma divergence = halt + investigate.
- Weekly journal entry is non-negotiable.
- Monthly stage review: am I still hitting the numbers that let me advance?

## Why not Alpaca live?

Alpaca live is fine, but the Public.com MCP is the specific integration designed for Claude-driven execution. The conversational layer matters when I'm in "discretionary-on-approved-signals" mode (which is where Stage 3 lives — not full auto).
