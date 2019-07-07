# -*- coding: utf-8 -*-

class TickData:
    """
    The TickData class represents a single unit of data received from a market data source.

    """

    def __init__(self, symbol, timestamp, last_price=0, total_volume=0):
        self.symbol = symbol
        self.timestamp = timestamp
        self.open_price = 0
        self.last_price = last_price
        self.total_volume = total_volume
