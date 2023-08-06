from enum import Enum, unique


@unique
class ShiftType(Enum):
    ADDITIVE = "Additive"
    RELATIVE = "Relative"
    RELATIVE_PERCENT = "RelativePercent"
    SCALED = "Scaled"
