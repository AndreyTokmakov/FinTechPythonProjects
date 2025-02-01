
from Binance.common.BaseEvent import BaseEvent


class AvgPrice(BaseEvent):

    @property
    def price_interval(self) -> str:
        return self["i"]

    @price_interval.setter
    def price_interval(self, value: str):
        self["i"] = value

    @property
    def average_price(self) -> str:
        return self["w"]

    @average_price.setter
    def average_price(self, value: str):
        self["w"] = value

    @property
    def last_trade_time(self) -> str:
        return self["T"]

    @last_trade_time.setter
    def last_trade_time(self, value: str):
        self["T"] = value


