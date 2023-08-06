from enum import Enum, unique


@unique
class MainConstituentAssetClass(Enum):
    FX_FORWARD = "FxForward"
    SWAP = "Swap"
