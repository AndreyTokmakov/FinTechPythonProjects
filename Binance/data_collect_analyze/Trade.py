
from typing import Dict


class Trade(Dict):

    @property
    def event_type(self) -> int:
        return self["e"]

    @event_type.setter
    def event_type(self, value: int):
        self["e"] = value

    @property
    def time(self) -> int:
        return self["E"]

    @time.setter
    def time(self, value: int):
        self["E"] = value

    @property
    def symbol(self) -> str:
        return self["s"]

    @symbol.setter
    def symbol(self, value: str):
        self["s"] = value

    @property
    def trade_id(self) -> int:
        return self["t"]

    @trade_id.setter
    def trade_id(self, value: int):
        self["t"] = value

    @property
    def price(self) -> str:
        return self["p"]

    @price.setter
    def price(self, value: str):
        self["p"] = value

    @property
    def quantity(self) -> str:
        return self["q"]

    @quantity.setter
    def quantity(self, value: str):
        self["q"] = value

    @property
    def trade_time(self) -> str:
        return self["T"]

    @trade_time.setter
    def trade_time(self, value: str):
        self["T"] = value

    @property
    def is_buyer(self) -> str:
        return self["m"]

    @is_buyer.setter
    def is_buyer(self, value: str):
        self["m"] = value

    @property
    def timestamp(self) -> str:
        return self["timestamp"]

    @timestamp.setter
    def timestamp(self, value: str):
        self["timestamp"] = value
