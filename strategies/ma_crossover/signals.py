"""MA crossover signal generator. Returns a new DataFrame — does not mutate input."""
from __future__ import annotations

import pandas as pd


def calculate_signals(
    df: pd.DataFrame,
    fast_period: int = 10,
    slow_period: int = 50,
) -> pd.DataFrame:
    """
    Compute entry signals for the MA crossover strategy.

    Parameters
    ----------
    df : OHLCV DataFrame with columns [open, high, low, close, volume].
         Index must be a DatetimeIndex.
    fast_period : lookback for fast SMA.
    slow_period : lookback for slow SMA.

    Returns
    -------
    New DataFrame with original columns plus [sma_fast, sma_slow, signal].
    signal=True means: enter long at next-day open.
    Does NOT mutate df.
    """
    out = df.copy()
    out["sma_fast"] = out["close"].rolling(fast_period).mean()
    out["sma_slow"] = out["close"].rolling(slow_period).mean()

    fast_above = (out["sma_fast"] > out["sma_slow"]).fillna(False).astype(bool)
    prev_fast_above = fast_above.shift(1, fill_value=False)

    cross_up = fast_above & ~prev_fast_above
    volume_ok = out["volume"] > 0
    has_both_smas = out["sma_fast"].notna() & out["sma_slow"].notna()

    out["signal"] = (cross_up & volume_ok & has_both_smas).astype(bool)
    return out
