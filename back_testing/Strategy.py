# -*- coding: utf-8 -*-

from abc import ABC
from back_testing.Order import Order


class Strategy(ABC):
    """
    The Strategy class is the base class for all other strategy implementations.

    The event_tick method is called when new market tick data arrives.

    The event_order method is called whenever there are order updates.

    The event_position method is called whenever there are updates to our positions.

    The send_market_order method is called when the implementing strategy sends a market order to the host
    component to be routed to the server for execution:
    """

    def __init__(self, symbol, event_sendorder):
        self.symbol = symbol
        self.event_sendorder = event_sendorder

    def event_tick(self, market_data):
        pass

    def event_order(self, order):
        pass

    def event_position(self, positions):
        pass

    def send_market_order(self, symbol, qty, is_buy, timestamp):
        if not self.event_sendorder is None:
            order = Order(timestamp, symbol, qty, is_buy, True)
            self.event_sendorder(order)
