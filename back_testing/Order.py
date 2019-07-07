# -*- coding: utf-8 -*-

class Order:
    """
    The Order class represents a single order sent by the strategy to the server.
    Once an order is filled, the order is further updated with the filled time, quantity, and price.
    """

    def __init__(self, timestamp, symbol, qty, is_buy, is_market_order, price=0):
        self.timestamp = timestamp
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.is_buy = is_buy
        self.is_market_order = is_market_order
        self.is_fulled = False
        self.filled_price = 0
        self.filled_time = None
        self.fill_qty = 0
