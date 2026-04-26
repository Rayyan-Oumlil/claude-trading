"""
Pre-market routine — runs at 06:00 weekdays.

Reads memory/watchlist.md, fetches the latest bar for each equity ticker via
Alpaca, and writes a snapshot to memory/routine-state.md.

Skips execution if the kill switch is active.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from paper_trading.kill_switch import is_halted  # noqa: E402


class _BarClient(Protocol):
    def get_stock_latest_bar(self, request): ...  # noqa: ANN001


def parse_watchlist(path: Path) -> list[str]:
    """Extract equity tickers from the watchlist markdown table.

    Ignores crypto (symbols containing '-', '/', or 'USD' suffix).
    """
    tickers: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        symbol = cells[0]
        asset_class = cells[1].lower() if len(cells) > 1 else ""
        if symbol in {"Symbol", "--------"}:
            continue
        if symbol.startswith("-") or symbol == "":
            continue
        if "crypto" in asset_class:
            continue
        if "-" in symbol or "/" in symbol:
            continue
        tickers.append(symbol)
    return tickers


def build_watchlist_snapshot(
    tickers: list[str], client: _BarClient
) -> list[dict]:
    from alpaca.data.requests import StockLatestBarRequest

    snapshot: list[dict] = []
    for ticker in tickers:
        try:
            bars = client.get_stock_latest_bar(
                StockLatestBarRequest(symbol_or_symbols=ticker)
            )
            bar = bars[ticker]
            snapshot.append({
                "symbol": ticker,
                "close": float(bar.close),
                "volume": int(bar.volume),
                "timestamp": str(bar.timestamp),
            })
        except Exception as exc:  # noqa: BLE001
            snapshot.append({
                "symbol": ticker,
                "error": str(exc),
            })
    return snapshot


def write_routine_state(
    snapshot: list[dict], state_path: Path
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Routine State",
        "",
        f"Last updated: {timestamp}",
        "",
        "## Pre-Market Snapshot",
        "",
        "| Symbol | Close | Volume | Timestamp |",
        "|--------|-------|--------|-----------|",
    ]
    for item in snapshot:
        if "error" in item:
            lines.append(f"| {item['symbol']} | ERR | ERR | {item['error']} |")
        else:
            lines.append(
                f"| {item['symbol']} | {item['close']} | "
                f"{item['volume']:,} | {item['timestamp']} |"
            )
    state_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if is_halted():
        print("HALTED -- kill switch active. Exiting.")
        return 0

    watchlist_path = PROJECT_ROOT / "memory" / "watchlist.md"
    state_path = PROJECT_ROOT / "memory" / "routine-state.md"

    tickers = parse_watchlist(watchlist_path)
    if not tickers:
        print("No equity tickers in watchlist. Exiting.")
        return 0

    from alpaca.data.historical import StockHistoricalDataClient

    client = StockHistoricalDataClient(
        api_key=os.environ["ALPACA_API_KEY"],
        secret_key=os.environ["ALPACA_API_SECRET"],
    )
    snapshot = build_watchlist_snapshot(tickers, client)
    write_routine_state(snapshot, state_path)

    ok_count = sum(1 for s in snapshot if "error" not in s)
    print(f"Pre-market snapshot: {ok_count}/{len(tickers)} tickers OK.")
    for s in snapshot:
        if "error" in s:
            print(f"  ERR {s['symbol']}: {s['error']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
