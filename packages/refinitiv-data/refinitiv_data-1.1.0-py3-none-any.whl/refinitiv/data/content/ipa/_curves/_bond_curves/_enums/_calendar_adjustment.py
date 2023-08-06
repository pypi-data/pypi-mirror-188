from enum import Enum, unique


@unique
class CalendarAdjustment(Enum):
    CALENDAR = "Calendar"
    FALSE = "False"
    WEEKEND = "Weekend"
