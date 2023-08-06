from enum import Enum, unique


@unique
class IssuerType(Enum):
    AGENCY = "Agency"
    CORPORATE = "Corporate"
    MUNIS = "Munis"
    NON_FINANCIALS = "NonFinancials"
    SOVEREIGN = "Sovereign"
    SUPRANATIONAL = "Supranational"
