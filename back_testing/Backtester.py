# -*- coding: utf-8 -*-

import datetime as dt

import pandas as pd

from back_testing.MarketData import MarketData
from back_testing.Position import Position


class Backtester:
    """
    A simple event-driven backtesting engine
    """

    def __init__(self, symbol, stragegy_class, data_source: pd.DataFrame):
        self.target_symbol = symbol
        self.strategy = stragegy_class(symbol, self._event_handler_order)
        self.data_source = data_source
        self.unfilled_orders = []
        self.positions = dict()
        self.current_prices = None
        self.rpnl, self.upnl = pd.DataFrame(), pd.DataFrame()

    @property
    def timestamp(self):
        return self.current_prices.get_timestamp(self.target_symbol)

    @property
    def trade_date(self):
        return self.timestamp.strftime("%Y-%m-%d")

    def get_position(self, symbol):
        if symbol not in self.positions:
            position = Position(symbol)
            self.positions[symbol] = position
        return self.positions[symbol]

    def _update_filled_position(self, symbol, qty, is_buy, price, timestamp):
        position = self.get_position(symbol)
        position.event_fill(timestamp, is_buy, qty, price)
        self.strategy.event_position(self.positions)
        self.rpnl.loc[timestamp, "rpnl"] = position.realized_pnl
        print(f"{self.trade_date}, {symbol}, Filled: {'BUY' if is_buy else 'SELL'}, Qty: {qty} at {price}")

    def _event_handler_order(self, order):
        self.unfilled_orders.append(order)
        print(
            f"{self.trade_date}, Received order: {'BUY' if order.is_buy else 'SELL'} {order.symbol}, Qty: {order.qty}")

    def _event_handler_tick(self, prices):
        self.current_prices = prices
        self.strategy.event_tick(prices)
        self._match_order_book(prices)
        self._print_position_status(self.target_symbol, prices)

    def _match_order_book(self, prices):
        if len(self.unfilled_orders) > 0:
            self.unfilled_orders = \
                [order for order in self.unfilled_orders if self._is_order_unmatched(order, prices)]

    def _is_order_unmatched(self, order, prices):
        symbol = order.symbol
        timestamp = prices.get_timestamp(symbol)

        if order.is_market_order and timestamp > order.timestamp:
            # Order is matched and filled
            order.is_filled = True
            open_price = prices.get_open_price(symbol)
            order.filled_time = timestamp
            order.filled_price = open_price
            self._update_filled_position(symbol, order.qty, order.is_buy, open_price, timestamp)
            self.strategy.event_order(order)
            return False

        return True

    def _print_position_status(self, symbol, prices):
        if symbol in self.positions:
            position = self.positions[symbol]
            close_price = prices.get_last_price(symbol)
            position.update_unrealized_pnl(close_price)
            self.upnl.loc[self.timestamp, "unpl"] = position.unrealized_pnl

            print(f"{self.trade_date}, Net: {position.net}, Value: {position.position_value}, \
                UPnL: {position.unrealized_pnl}, RPnL: {position.realized_pnl}")

    def start_backtest(self, start_date: dt.datetime, end_date: dt.datetime):
        data_view = self.data_source.loc[start_date: end_date, ["open", "close", "volume"]]
        market_data = MarketData()

        print("Backtesting started...")
        for time, row in data_view.iterrows():
            market_data.add_last_price(time, self.target_symbol, row["close"], row["volume"])
            market_data.add_open_price(time, self.target_symbol, row["open"])

            if not self._event_handler_tick is None:
                self._event_handler_tick(market_data)

        print("Backtesting completed.")
