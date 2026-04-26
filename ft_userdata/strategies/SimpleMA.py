from freqtrade.strategy import IStrategy, IntParameter
from pandas import DataFrame
import talib.abstract as ta


class SimpleMA(IStrategy):
    """
    Simple Moving Average crossover strategy — starter template.
    Buy when fast MA crosses above slow MA, sell when it crosses below.
    """
    INTERFACE_VERSION = 3
    timeframe = "1h"
    minimal_roi = {"60": 0.01, "30": 0.02, "0": 0.04}
    stoploss = -0.05
    trailing_stop = False
    can_short = False

    buy_fast_period = IntParameter(5, 20, default=10, space="buy")
    buy_slow_period = IntParameter(20, 100, default=50, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for period in self.buy_fast_period.range:
            dataframe[f"ma_fast_{period}"] = ta.SMA(dataframe, timeperiod=period)
        for period in self.buy_slow_period.range:
            dataframe[f"ma_slow_{period}"] = ta.SMA(dataframe, timeperiod=period)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        fast = f"ma_fast_{self.buy_fast_period.value}"
        slow = f"ma_slow_{self.buy_slow_period.value}"
        dataframe.loc[
            (dataframe[fast] > dataframe[slow]) &
            (dataframe[fast].shift(1) <= dataframe[slow].shift(1)) &
            (dataframe["volume"] > 0),
            "enter_long"
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        fast = f"ma_fast_{self.buy_fast_period.value}"
        slow = f"ma_slow_{self.buy_slow_period.value}"
        dataframe.loc[
            (dataframe[fast] < dataframe[slow]) &
            (dataframe[fast].shift(1) >= dataframe[slow].shift(1)) &
            (dataframe["volume"] > 0),
            "exit_long"
        ] = 1
        return dataframe
