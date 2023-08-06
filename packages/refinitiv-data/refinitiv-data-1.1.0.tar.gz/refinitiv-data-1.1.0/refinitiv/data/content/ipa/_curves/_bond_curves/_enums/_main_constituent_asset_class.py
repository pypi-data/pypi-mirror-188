from enum import Enum, unique


@unique
class MainConstituentAssetClass(Enum):
    BOND = "Bond"
    CREDIT_DEFAULT_SWAP = "CreditDefaultSwap"
