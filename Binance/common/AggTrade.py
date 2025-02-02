
from Binance.common.BaseEvent import BaseEvent


class AggTrade(BaseEvent):

    @property
    def aggregate_trade_id(self) -> int:
        return self["a"]

    @aggregate_trade_id.setter
    def aggregate_trade_id(self, value: int):
        self["a"] = value

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
    def first_trade_id(self) -> str:
        return self["f"]

    @first_trade_id.setter
    def first_trade_id(self, value: str):
        self["f"] = value

    @property
    def flast_trade_id(self) -> str:
        return self["l"]

    @flast_trade_id.setter
    def flast_trade_id(self, value: str):
        self["l"] = value

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


'''
{
    "e"         // event_type
    "E"         // time
    "s"         // symbol
    "a"         // aggregate_trade_id
    "p"         // price
    "q"         // quantity
    "f"         // first_trade_id
    "l"         // flast_trade_id
    "T"         // trade_time
    "m"         // is_buyer
    "timestamp" // timestamp
}
'''