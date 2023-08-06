from enum import Enum, unique


@unique
class EconomicSector(Enum):
    ACADEMIC_AND_EDUCATIONAL_SERVICES = "AcademicAndEducationalServices"
    BASIC_MATERIALS = "BasicMaterials"
    CONSUMER_CYCLICALS = "ConsumerCyclicals"
    CONSUMER_NON_CYCLICALS = "ConsumerNonCyclicals"
    ENERGY = "Energy"
    FINANCIALS = "Financials"
    GOVERNMENT_ACTIVITY = "GovernmentActivity"
    HEALTHCARE = "Healthcare"
    INDUSTRIALS = "Industrials"
    INSTITUTIONS_ASSOCIATIONS_AND_ORGANIZATIONS = (
        "InstitutionsAssociationsAndOrganizations"
    )
    REAL_ESTATE = "RealEstate"
    TECHNOLOGY = "Technology"
    UTILITIES = "Utilities"
