from Binance.common.BaseEvent import BaseEvent

'''
{
  "u":400900217,     // order book updateId
  "s":"BNBUSDT",     // symbol
  "b":"25.35190000", // best bid price
  "B":"31.21000000", // best bid qty
  "a":"25.36520000", // best ask price
  "A":"40.66000000"  // best ask qty
}
'''


class BookTick(BaseEvent):

    @property
    def update_id(self) -> str:
        return self["u"]

    @update_id.setter
    def update_id(self, value: str):
        self["u"] = value

    @property
    def best_bid_price(self) -> str:
        return self["b"]

    @best_bid_price.setter
    def best_bid_price(self, value: str):
        self["b"] = value

    @property
    def best_bid_quantity(self) -> str:
        return self["B"]

    @best_bid_quantity.setter
    def best_bid_quantity(self, value: str):
        self["B"] = value

    @property
    def best_ask_price(self) -> str:
        return self["a"]

    @best_ask_price.setter
    def best_ask_price(self, value: str):
        self["a"] = value

    @property
    def best_ask_quantity(self) -> str:
        return self["A"]

    @best_ask_quantity.setter
    def best_ask_quantity(self, value: str):
        self["A"] = value

    '''
    @property
    def time(self) -> int:
        return self["E"]

    @time.setter
    def time(self, value: int):
        self["E"] = value
    '''
