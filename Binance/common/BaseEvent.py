

'''
{
  "i": "5m",                // Average price interval
  "w": "25776.86000000",    // Average price
  "T": 1693907032213        // Last trade time
'''


from typing import Dict


class BaseEvent(Dict):

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
    def timestamp(self) -> str:
        return self["timestamp"]

    @timestamp.setter
    def timestamp(self, value: str):
        self["timestamp"] = value
