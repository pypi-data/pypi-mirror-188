from enum import Enum, unique


@unique
class PriceSide(Enum):
    ASK = "Ask"
    BID = "Bid"
    MID = "Mid"
