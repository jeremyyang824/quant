# -*- coding: utf-8 -*-

import datetime as dt

import pandas as pd

from back_testing.Backtester import Backtester
from back_testing.Strategy import Strategy


class MeanRevertingStrategy(Strategy):
    """
    Implementation of a mean-reverting strategy
    """

    def __init__(self, symbol, event_sendorder,
                 lookback_intervals=3,
                 buy_threshold=-0.5,
                 sell_threshold=0.5):
        super().__init__(symbol, event_sendorder)
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.prices = pd.DataFrame()
        self.is_long, self.is_short = False, False

    def event_position(self, positions):
        "updates the state of the strategy to indicate a long or a short on every change in position"
        if self.symbol in positions:
            position = positions[self.symbol]
            self.is_long = True if position.net > 0 else False
            self.is_short = True if position.net < 0 else False

    def event_tick(self, market_data):
        """perform the trade logic decision on every incoming tick data,
        which is stored as a pandas DataFrame object, to calculate the strategy parameters"""
        self._store_prices(market_data)

        if len(self.prices) < self.lookback_intervals:
            return

        signal_value = self._calculate_z_score()
        timestamp = market_data.get_timestamp(self.symbol)

        if signal_value < self.buy_threshold:
            self._on_buy_signal(timestamp)
        elif signal_value > self.sell_threshold:
            self._on_sell_signal(timestamp)

    def _store_prices(self, market_data):
        timestamp = market_data.get_timestamp(self.symbol)
        self.prices.loc[timestamp, "close"] = \
            market_data.get_last_price(self.symbol)
        self.prices.loc[timestamp, "open"] = \
            market_data.get_open_price(self.symbol)

    def _calculate_z_score(self):
        "z_score = (x - μ) / sigma"
        self.prices = self.prices[-self.lookback_intervals:]
        returns = self.prices["close"].pct_change().dropna()
        z_score = ((returns - returns.mean()) / returns.std())[-1]
        return z_score

    def _on_buy_signal(self, timestamp):
        if not self.is_long:
            self.send_market_order(self.symbol, 100, True, timestamp)

    def _on_sell_signal(self, timestamp):
        if not self.is_short:
            self.send_market_order(self.symbol, 100, False, timestamp)


if __name__ == "__main__":
    data_source = pd.DataFrame({
        "date": ['2018-03-01', '2018-03-02', '2018-03-05', '2018-03-06', '2018-03-07'],
        "open": [21.1, 21.5, 26.23, 24.6, 23.23],
        "close": [21.3, 22.6, 26.1, 21.5, 21.2],
        "volume": [100, 200, 300, 200, 200]
    })
    data_source.set_index("date", inplace=True)
    data_source.index = pd.DatetimeIndex(data_source.index)

    backtester = Backtester("#603833.SH#", MeanRevertingStrategy, data_source)

    backtester.start_backtest(dt.datetime(2018, 1, 1), dt.datetime(2018, 12, 31))
