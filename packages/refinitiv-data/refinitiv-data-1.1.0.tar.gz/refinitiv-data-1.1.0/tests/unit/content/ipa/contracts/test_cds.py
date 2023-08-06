from inspect import signature
import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession
import pytest

from tests.unit.conftest import (
    remove_dunder_methods,
    has_property_names_in_class,
    get_property_names,
    remove_private_attributes,
)


def test_ipa_cds_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.cds.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_cds_attributes():
    expected_attributes = [
        "BusinessDayConvention",
        "CdsConvention",
        "DayCountBasis",
        "Definition",
        "Direction",
        "DocClause",
        "Frequency",
        "PremiumLegDefinition",
        "PricingParameters",
        "ProtectionLegDefinition",
        "Seniority",
        "StubRule",
    ]
    testing_attributes = dir(rdf.cds)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "PremiumLegDefinition",
        "ProtectionLegDefinition",
        "PricingParameters",
    ],
    argvalues=[
        (
            rdf.cds._cds_definition.CdsInstrumentDefinition,
            {
                "instrument_tag": "instrument_tag",
                "instrument_code": "instrument_code",
                "cds_convention": rdf.cds.CdsConvention.ISDA,
                "trade_date": "trade_date",
                "step_in_date": "step_in_date",
                "start_date": "start_date",
                "end_date": "end_date",
                "tenor": "tenor",
                "start_date_moving_convention": rdf.cds.BusinessDayConvention.MODIFIED_FOLLOWING,
                "end_date_moving_convention": rdf.cds.BusinessDayConvention.NO_MOVING,
                "adjust_to_isda_end_date": True,
                "protection_leg": rdf.cds.ProtectionLegDefinition(
                    index_factor=1,
                    index_series=1,
                    notional_amount=1,
                    recovery_rate=1,
                    seniority=rdf.cds.Seniority.PREFERENCE,
                    settlement_convention="settlement_convention",
                ),
                "premium_leg": rdf.cds.PremiumLegDefinition(
                    direction=rdf.cds.Direction.PAID,
                    interest_payment_ccy="interest_payment_ccy",
                    interest_payment_frequency=rdf.cds.Frequency.SEMI_ANNUAL,
                    interest_calculation_method=rdf.cds.DayCountBasis.DCB_ACTUAL_360,
                ),
                "accrued_begin_date": "accrued_begin_date",
            },
        ),
        (
            rdf.cds.PremiumLegDefinition,
            {
                "direction": rdf.cds.Direction.PAID,
                "notional_ccy": "notional_ccy",
                "notional_amount": 3.3,
                "fixed_rate_percent": 4.4,
                "interest_payment_frequency": rdf.cds.Frequency.ANNUAL,
                "interest_calculation_method": rdf.cds.DayCountBasis.DCB_30_360,
                "accrued_calculation_method": rdf.cds.DayCountBasis.DCB_30_ACTUAL,
                "payment_business_day_convention": rdf.cds.BusinessDayConvention.NO_MOVING,
                "first_regular_payment_date": "first_regular_payment_date",
                "last_regular_payment_date": "last_regular_payment_date",
                "payment_business_days": "payment_business_days",
                "stub_rule": rdf.cds.StubRule.MATURITY,
                "accrued_paid_on_default": True,
                "interest_payment_ccy": "interest_payment_ccy",
            },
        ),
        (
            rdf.cds.ProtectionLegDefinition,
            {
                "direction": rdf.cds.Direction.RECEIVED,
                "notional_ccy": "notional_ccy",
                "notional_amount": 3.3,
                "doc_clause": rdf.cds.DocClause.EX_RESTRUCT14,
                "seniority": rdf.cds.Seniority.SENIOR_UNSECURED,
                "index_factor": 6.6,
                "index_series": 7,
                "recovery_rate": 8.8,
                "recovery_rate_percent": 9.9,
                "reference_entity": "reference_entity",
                "settlement_convention": "settlement_convention",
            },
        ),
        (
            rdf.cds.PricingParameters,
            {
                "market_data_date": "market_data_date",
                "cash_amount_in_deal_ccy": 1.1,
                "clean_price_percent": 2.2,
                "conventional_spread_bp": 3.3,
                "upfront_amount_in_deal_ccy": 4.4,
                "upfront_percent": 5.5,
                "valuation_date": "valuation_date",
                "report_ccy": "report_ccy",
            },
        ),
    ],
)
def test_parameter(input_data):
    cls, kwargs = input_data
    args_names = list(kwargs.keys())
    inst = cls(**kwargs)

    s = signature(cls.__init__)
    # +1 for (self)
    assert len(s.parameters) == (
        len(args_names) + 1
    ), f"csl={cls}{str(set(get_property_names(cls)) - set(args_names))}"

    assert has_property_names_in_class(cls, args_names), set(args_names) - set(
        get_property_names(cls)
    )

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        assert attr == v, k


def test_request_body():
    # given
    expected_body = {
        "fields": ["1", "2"],
        "universe": [
            {
                "instrumentDefinition": {
                    "endDate": "2032-02-28",
                },
                "instrumentType": "Cds",
                "pricingParameters": {"marketDataDate": "market_data_date"},
                "extended_params": "extended_params",
            }
        ],
    }
    definition = rdf.cds.Definition(
        end_date="2032-02-28",
        fields=["1", "2"],
        pricing_parameters=rdf.cds.PricingParameters(
            market_data_date="market_data_date"
        ),
        extended_params={"extended_params": "extended_params"},
    )

    # when
    content_type = definition._kwargs["__content_type__"]
    provider = make_provider(content_type)
    request = provider.request.create(StubSession(), "url", **definition._kwargs)

    # then
    testing_body = request.json
    assert testing_body == expected_body, expected_body
