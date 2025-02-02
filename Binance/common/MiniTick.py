from Binance.common.BaseEvent import BaseEvent


class MiniTick(BaseEvent):

    @property
    def close_price(self) -> str:
        return self["c"]

    @close_price.setter
    def close_price(self, value: str):
        self["c"] = value

    @property
    def open_price(self) -> str:
        return self["o"]

    @open_price.setter
    def open_price(self, value: str):
        self["o"] = value

    @property
    def high_price(self) -> str:
        return self["h"]

    @high_price.setter
    def high_price(self, value: str):
        self["h"] = value

    @property
    def low_price(self) -> str:
        return self["l"]

    @low_price.setter
    def low_price(self, value: str):
        self["l"] = value

    @property
    def traded_base_volume(self) -> str:
        return self["v"]

    @traded_base_volume.setter
    def traded_base_volume(self, value: str):
        self["v"] = value

    @property
    def traded_quote_volume(self) -> str:
        return self["q"]

    @traded_quote_volume.setter
    def traded_quote_volume(self, value: str):
        self["q"] = value


'''
{
    "e"         // event_type
    "E"         // time
    "s"         // symbol
    "c"         // close_price
    "o"         // open_price
    "h"         // high_price
    "l"         // low_price
    "v"         // traded_base_volume
    "q"         // traded_quote_volume    
    "timestamp" // timestamp
}
'''