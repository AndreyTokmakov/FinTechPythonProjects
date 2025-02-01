from Binance.common.BaseEvent import BaseEvent


class Trade(BaseEvent):

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
