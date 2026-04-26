# Agents — Multi-Role Workflow

Inspired by Bijit Ghosh's multi-agent trading firm architecture (from the research gathered) — but adapted to where I am. Today, these are **role prompts** I ask Claude to play. Later, they may become real orchestrated sub-agents.

## The flow

```
         ┌─────────────────────┐
         │  Market Data Agent  │
         │  (MCP data pull)    │
         └──────────┬──────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
  ┌─────────┐ ┌──────────┐ ┌──────────┐
  │Technical│ │Fundamentals│ │Sentiment│
  │ Analyst │ │  Analyst   │ │ Analyst │
  └────┬────┘ └─────┬──────┘ └────┬────┘
       │            │             │
       └────────────┼─────────────┘
                    ▼
          ┌─────────────────┐
          │  Risk Manager   │
          │  (gatekeeper)   │
          └────────┬────────┘
                   ▼
         ┌──────────────────┐
         │ Portfolio Manager│
         │  (final call)    │
         └──────────────────┘
```

## Roles

| File | Role | When to invoke |
|------|------|----------------|
| [market-data.md](market-data.md) | Pull + clean OHLCV, fundamentals, news | First step of any analysis |
| [routine-orchestrator.md](routine-orchestrator.md) | Wake-up / run / write-back contract for scheduled automation | Before trusting any routine |
| [technical.md](technical.md) | Chart patterns, indicators, regime | After market-data, in parallel with the others |
| [fundamentals.md](fundamentals.md) | Earnings, margins, balance sheet | Equities only |
| [sentiment.md](sentiment.md) | News, filings, social signal | Any asset with narrative risk |
| [risk-manager.md](risk-manager.md) | Veto + size check | Before any order |
| [portfolio-manager.md](portfolio-manager.md) | Final decision + allocation | Closes the loop |

## How I actually use this (today)

I don't need a real orchestrator yet. When I want a decision:

```
"For <ticker>, run the full agent flow:
 1. market-data pass
 2. technical + fundamentals + sentiment in parallel
 3. risk-manager veto check
 4. portfolio-manager final call with suggested size"
```

Claude reads the role files, plays each role, and produces the output for each stage before combining. Keeps the reasoning traceable — I can see where the decision came from.

## When to upgrade to real sub-agents

Once I'm in stage 3 of [../ROADMAP.md](../ROADMAP.md) (tiny live), each role can become a real Claude Code sub-agent with its own prompt and tools. That's also when I reopen `TradingAgents/`.
