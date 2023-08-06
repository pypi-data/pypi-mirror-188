from enum import Enum, unique


@unique
class ReferenceEntityType(Enum):
    BOND_ISIN = "BondIsin"
    BOND_RIC = "BondRic"
    CHAIN_RIC = "ChainRic"
    ORGANISATION_ID = "OrganisationId"
    TICKER = "Ticker"
