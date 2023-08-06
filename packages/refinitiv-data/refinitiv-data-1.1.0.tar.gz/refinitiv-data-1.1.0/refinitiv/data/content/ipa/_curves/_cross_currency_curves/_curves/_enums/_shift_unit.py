from enum import Enum, unique


@unique
class ShiftUnit(Enum):
    ABSOLUTE = "Absolute"
    BP = "Bp"
    PERCENT = "Percent"
