# -*- coding: utf-8 -*-

from back_testing.TickData import TickData


class MarketData:
    """
    An instance of this class is used throughout the system to store and retrieve prices
    by the various components.

    """

    def __init__(self):
        self.__recent_ticks__ = dict()

    def add_last_price(self, time, symbol, price, volume):
        tick_data = TickData(symbol, time, price, volume)
        self.__recent_ticks__[symbol] = tick_data

    def add_open_price(self, time, symbol, price):
        tick_data = self.get_existing_tick_data(symbol, time)
        tick_data.open_price = price

    def get_existing_tick_data(self, symbol, time):
        if not symbol in self.__recent_ticks__:
            tick_data = TickData(symbol, time)
            self.__recent_ticks__[symbol] = tick_data
        return self.__recent_ticks__[symbol]

    def get_last_price(self, symbol):
        return self.__recent_ticks__[symbol].last_price

    def get_open_price(self, symbol):
        return self.__recent_ticks__[symbol].open_price

    def get_timestamp(self, symbol):
        return self.__recent_ticks__[symbol].timestamp


class MarketDataSource:
    def __init__(self):
        self.event_tick = None
        self.ticker, self.source = None, None
        self.start, self.end = None, None
        self.md = MarketData()
