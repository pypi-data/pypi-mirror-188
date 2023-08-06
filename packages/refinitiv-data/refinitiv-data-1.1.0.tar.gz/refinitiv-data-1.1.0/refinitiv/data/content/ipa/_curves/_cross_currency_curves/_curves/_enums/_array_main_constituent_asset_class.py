from enum import Enum, unique


@unique
class ArrayMainConstituentAssetClass(Enum):
    DEPOSIT = "Deposit"
    FUTURES = "Futures"
    SWAP = "Swap"
