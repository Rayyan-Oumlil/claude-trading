"""Tests for EOD close routine."""
from __future__ import annotations

from pathlib import Path

from routines_pkg.eod_close import (
    format_positions,
    write_journal_entry,
    write_portfolio_state,
)


def test_format_positions_empty() -> None:
    assert format_positions([]) == "None."


def test_format_positions_single() -> None:
    out = format_positions([
        {"symbol": "SPY", "qty": 10.0, "market_value": 4500.0, "unrealized_pl": 50.0}
    ])
    assert "SPY" in out
    assert "10.00" in out
    assert "+$50.00" in out


def test_write_journal_entry_new_file(tmp_path: Path) -> None:
    account = {"equity": 100_000.0, "cash": 5000.0, "buying_power": 200_000.0,
               "status": "ACTIVE"}
    positions = [{"symbol": "SPY", "qty": 10.0, "market_value": 4500.0,
                  "unrealized_pl": 50.0}]
    path = write_journal_entry("2026-04-23", account, positions, tmp_path)
    content = path.read_text()
    assert "Automated EOD Close" in content
    assert "$100,000.00" in content
    assert "SPY" in content


def test_write_journal_entry_appends_to_existing(tmp_path: Path) -> None:
    existing = tmp_path / "2026-04-23.md"
    existing.write_text("# Existing manual content\n\nMy notes.\n")
    account = {"equity": 100_000.0, "cash": 5000.0, "buying_power": 200_000.0,
               "status": "ACTIVE"}
    path = write_journal_entry("2026-04-23", account, [], tmp_path)
    content = path.read_text()
    assert "My notes" in content
    assert "Automated EOD Close" in content


def test_write_journal_entry_replaces_old_auto_section(tmp_path: Path) -> None:
    existing = tmp_path / "2026-04-23.md"
    existing.write_text(
        "# Manual\n\n---\n\n## Automated EOD Close -- 2026-04-23T10:00:00\n\nOld equity: $99,000\n"
    )
    account = {"equity": 100_000.0, "cash": 5000.0, "buying_power": 200_000.0,
               "status": "ACTIVE"}
    path = write_journal_entry("2026-04-23", account, [], tmp_path)
    content = path.read_text()
    assert "# Manual" in content
    assert "Old equity" not in content
    assert "$100,000.00" in content


def test_write_portfolio_state(tmp_path: Path) -> None:
    state = tmp_path / "portfolio.md"
    account = {"equity": 100_000.0, "cash": 5000.0, "buying_power": 200_000.0,
               "status": "ACTIVE"}
    positions = [{"symbol": "SPY", "qty": 10.0, "market_value": 4500.0,
                  "unrealized_pl": 50.0}]
    write_portfolio_state(account, positions, state)
    content = state.read_text()
    assert "$100,000.00" in content
    assert "SPY" in content
    assert "$4,500.00" in content


def test_write_portfolio_state_empty_positions(tmp_path: Path) -> None:
    state = tmp_path / "portfolio.md"
    account = {"equity": 100_000.0, "cash": 100_000.0, "buying_power": 200_000.0,
               "status": "ACTIVE"}
    write_portfolio_state(account, [], state)
    content = state.read_text()
    assert "None." in content
