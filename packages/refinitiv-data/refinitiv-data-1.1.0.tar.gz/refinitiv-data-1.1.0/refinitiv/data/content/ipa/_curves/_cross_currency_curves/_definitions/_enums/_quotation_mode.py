from enum import Enum, unique


@unique
class QuotationMode(Enum):
    OUTRIGHT = "Outright"
    SWAP_POINT = "SwapPoint"
