from enum import Enum, unique


@unique
class Seniority(Enum):
    SENIOR_NON_PREFERRED = "SeniorNonPreferred"
    SENIOR_PREFERRED = "SeniorPreferred"
    SUBORDINATE_UNSECURED = "SubordinateUnsecured"
