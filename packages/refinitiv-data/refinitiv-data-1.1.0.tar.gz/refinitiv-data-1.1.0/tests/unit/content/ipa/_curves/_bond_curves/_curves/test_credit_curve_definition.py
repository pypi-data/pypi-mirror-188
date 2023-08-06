from refinitiv.data.content.ipa._curves._bond_curves._curves import (
    CreditCurveDefinition,
)
from refinitiv.data.content.ipa._curves._bond_curves._enums import (
    BusinessSector,
    CurveSubType,
    EconomicSector,
    Industry,
    IndustryGroup,
    IssuerType,
    MainConstituentAssetClass,
    Rating,
    RatingScaleSource,
    ReferenceEntityType,
    Seniority,
)


def test_credit_curve_definition():
    # given
    expected_dict = {
        "businessSector": "AcademicAndEducationalServices",
        "creditCurveTypeFallbackLogic": ["string1", "string2"],
        "curveSubType": "BondCarry",
        "curveTenors": ["string1", "string2"],
        "economicSector": "AcademicAndEducationalServices",
        "industry": "AdvancedMedicalEquipmentAndTechnology",
        "industryGroup": "AerospaceAndDefense",
        "issuerType": "Agency",
        "mainConstituentAssetClass": "Bond",
        "rating": "A",
        "ratingScaleSource": "DBRS",
        "referenceEntityType": "BondIsin",
        "seniority": "SeniorNonPreferred",
        "country": "string",
        "currency": "string",
        "id": "string",
        "name": "string",
        "referenceEntity": "string",
        "source": "string",
    }

    # when
    testing_obj = CreditCurveDefinition(
        business_sector=BusinessSector.ACADEMIC_AND_EDUCATIONAL_SERVICES,
        credit_curve_type_fallback_logic=["string1", "string2"],
        curve_sub_type=CurveSubType.BOND_CARRY,
        curve_tenors=["string1", "string2"],
        economic_sector=EconomicSector.ACADEMIC_AND_EDUCATIONAL_SERVICES,
        industry=Industry.ADVANCED_MEDICAL_EQUIPMENT_AND_TECHNOLOGY,
        industry_group=IndustryGroup.AEROSPACE_AND_DEFENSE,
        issuer_type=IssuerType.AGENCY,
        main_constituent_asset_class=MainConstituentAssetClass.BOND,
        rating=Rating.A,
        rating_scale_source=RatingScaleSource.DBRS,
        reference_entity_type=ReferenceEntityType.BOND_ISIN,
        seniority=Seniority.SENIOR_NON_PREFERRED,
        country="string",
        currency="string",
        id="string",
        name="string",
        reference_entity="string",
        source="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert (
        testing_obj.business_sector == BusinessSector.ACADEMIC_AND_EDUCATIONAL_SERVICES
    )
    assert testing_obj.credit_curve_type_fallback_logic == ["string1", "string2"]
    assert testing_obj.curve_sub_type == CurveSubType.BOND_CARRY
    assert testing_obj.curve_tenors == ["string1", "string2"]
    assert (
        testing_obj.economic_sector == EconomicSector.ACADEMIC_AND_EDUCATIONAL_SERVICES
    )
    assert testing_obj.industry == Industry.ADVANCED_MEDICAL_EQUIPMENT_AND_TECHNOLOGY
    assert testing_obj.industry_group == IndustryGroup.AEROSPACE_AND_DEFENSE
    assert testing_obj.issuer_type == IssuerType.AGENCY
    assert testing_obj.main_constituent_asset_class == MainConstituentAssetClass.BOND
    assert testing_obj.rating == Rating.A
    assert testing_obj.rating_scale_source == RatingScaleSource.DBRS
    assert testing_obj.reference_entity_type == ReferenceEntityType.BOND_ISIN
    assert testing_obj.seniority == Seniority.SENIOR_NON_PREFERRED
    assert testing_obj.country == "string"
    assert testing_obj.currency == "string"
    assert testing_obj.id == "string"
    assert testing_obj.name == "string"
    assert testing_obj.reference_entity == "string"
    assert testing_obj.source == "string"
