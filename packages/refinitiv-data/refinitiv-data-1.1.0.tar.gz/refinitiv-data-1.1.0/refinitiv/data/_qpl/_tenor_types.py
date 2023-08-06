from enum import Enum, unique


@unique
class TenorTypes(str, Enum):
    ODD = "Odd"
    LONG = "Long"
    IMM = "IMM"
    BEGINNING_OF_MONTH = "BeginningOfMonth"
    END_OF_MONTH = "EndOfMonth"

    def __str__(self) -> str:
        return str(self.value)
