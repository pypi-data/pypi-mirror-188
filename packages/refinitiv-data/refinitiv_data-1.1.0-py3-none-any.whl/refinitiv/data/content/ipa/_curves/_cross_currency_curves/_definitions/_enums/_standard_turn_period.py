from enum import Enum, unique


@unique
class StandardTurnPeriod(Enum):
    NONE = "None"
    QUARTER_ENDS = "QuarterEnds"
    YEAR_ENDS = "YearEnds"
