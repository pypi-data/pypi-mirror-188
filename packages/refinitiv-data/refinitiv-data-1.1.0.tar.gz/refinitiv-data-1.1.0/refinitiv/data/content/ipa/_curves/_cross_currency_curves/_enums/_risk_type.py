from enum import Enum, unique


@unique
class RiskType(Enum):
    CROSS_CURRENCY = "CrossCurrency"
