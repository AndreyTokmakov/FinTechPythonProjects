from Binance.common.BaseEvent import BaseEvent


class Tick(BaseEvent):

    @property
    def price_change(self) -> str:
        return self["p"]

    @price_change.setter
    def price_change(self, value: str):
        self["p"] = value

    @property
    def price_change_percent(self) -> str:
        return self["P"]

    @price_change_percent.setter
    def price_change_percent(self, value: str):
        self["P"] = value

    @property
    def weighted_average_price(self) -> str:
        return self["w"]

    @weighted_average_price.setter
    def weighted_average_price(self, value: str):
        self["w"] = value

    @property
    def first_trade_price(self) -> str:
        return self["x"]

    @first_trade_price.setter
    def first_trade_price(self, value: str):
        self["x"] = value

    @property
    def last_price(self) -> str:
        return self["c"]

    @last_price.setter
    def last_price(self, value: str):
        self["c"] = value

    @property
    def last_quantity(self) -> str:
        return self["Q"]

    @last_quantity.setter
    def last_quantity(self, value: str):
        self["Q"] = value

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
    def total_traded_volume(self) -> str:
        return self["v"]

    @total_traded_volume.setter
    def total_traded_volume(self, value: str):
        self["v"] = value

    @property
    def total_traded_quote_volume(self) -> str:
        return self["q"]

    @total_traded_quote_volume.setter
    def total_traded_quote_volume(self, value: str):
        self["q"] = value

    @property
    def statistics_open_time(self) -> str:
        return self["O"]

    @statistics_open_time.setter
    def statistics_open_time(self, value: str):
        self["O"] = value

    @property
    def statistics_close_time(self) -> str:
        return self["C"]

    @statistics_close_time.setter
    def statistics_close_time(self, value: str):
        self["C"] = value

    @property
    def first_trade_id(self) -> str:
        return self["F"]

    @first_trade_id.setter
    def first_trade_id(self, value: str):
        self["F"] = value

    @property
    def last_trade_id(self) -> str:
        return self["L"]

    @last_trade_id.setter
    def last_trade_id(self, value: str):
        self["L"] = value

    @property
    def number_of_trades(self) -> str:
        return self["n"]

    @number_of_trades.setter
    def number_of_trades(self, value: str):
        self["n"] = value
