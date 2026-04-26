"""Tests for pre-market routine."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from routines_pkg.premarket import (
    build_watchlist_snapshot,
    parse_watchlist,
    write_routine_state,
)


def test_parse_watchlist_extracts_equity_tickers(tmp_path: Path) -> None:
    wl = tmp_path / "watchlist.md"
    wl.write_text(
        "# Watchlist\n\n"
        "| Symbol | Class | Status | Thesis |\n"
        "|--------|-------|--------|--------|\n"
        "| SPY | ETF | benchmark | anchor |\n"
        "| QQQ | ETF | benchmark | growth |\n"
        "| BTC-USD | crypto | monitor | weekend |\n"
    )
    result = parse_watchlist(wl)
    assert result == ["SPY", "QQQ"]


def test_parse_watchlist_empty_returns_empty(tmp_path: Path) -> None:
    wl = tmp_path / "watchlist.md"
    wl.write_text("# Empty\n")
    assert parse_watchlist(wl) == []


def test_build_snapshot_returns_list_of_dicts() -> None:
    mock_bar = MagicMock()
    mock_bar.close = 450.0
    mock_bar.volume = 1_000_000
    mock_bar.timestamp = "2026-04-23T13:30:00Z"
    mock_client = MagicMock()
    mock_client.get_stock_latest_bar.return_value = {"SPY": mock_bar}
    result = build_watchlist_snapshot(["SPY"], mock_client)
    assert len(result) == 1
    assert result[0]["symbol"] == "SPY"
    assert result[0]["close"] == 450.0
    assert result[0]["volume"] == 1_000_000


def test_build_snapshot_captures_errors() -> None:
    mock_client = MagicMock()
    mock_client.get_stock_latest_bar.side_effect = RuntimeError("Not found")
    result = build_watchlist_snapshot(["INVALID"], mock_client)
    assert len(result) == 1
    assert "error" in result[0]
    assert result[0]["symbol"] == "INVALID"


def test_write_routine_state_creates_file(tmp_path: Path) -> None:
    state_file = tmp_path / "routine-state.md"
    write_routine_state(
        [{"symbol": "SPY", "close": 450.0, "volume": 1_000_000,
          "timestamp": "2026-04-23"}],
        state_file,
    )
    content = state_file.read_text()
    assert "SPY" in content
    assert "450.0" in content
    assert "Pre-Market Snapshot" in content


def test_write_routine_state_includes_errors(tmp_path: Path) -> None:
    state_file = tmp_path / "routine-state.md"
    write_routine_state(
        [{"symbol": "BAD", "error": "something broke"}],
        state_file,
    )
    content = state_file.read_text()
    assert "BAD" in content
    assert "something broke" in content
