from enum import Enum, unique


@unique
class RatingScaleSource(Enum):
    DBRS = "DBRS"
    FITCH = "Fitch"
    MOODYS = "Moodys"
    REFINITIV = "Refinitiv"
    S_AND_P = "SAndP"
