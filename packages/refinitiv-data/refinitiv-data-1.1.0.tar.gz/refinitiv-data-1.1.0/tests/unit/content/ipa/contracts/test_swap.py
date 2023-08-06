from inspect import signature

import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession
from tests.unit.conftest import (
    remove_dunder_methods,
    remove_private_attributes,
    has_property_names_in_class,
    get_property_names,
)


def test_ipa_swap_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.swap.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_swap_attributes():
    expected_attributes = [
        "AdjustInterestToPaymentDate",
        "AmortizationFrequency",
        "AmortizationItem",
        "AmortizationType",
        "BusinessDayConvention",
        "DateRollingConvention",
        "DayCountBasis",
        "Definition",
        "Direction",
        "Frequency",
        "IndexAverageMethod",
        "IndexCompoundingMethod",
        "IndexConvexityAdjustmentIntegrationMethod",
        "IndexConvexityAdjustmentMethod",
        "IndexObservationMethod",
        "IndexResetType",
        "IndexSpreadCompoundingMethod",
        "InputFlow",
        "InterestCalculationConvention",
        "InterestType",
        "LegDefinition",
        "NotionalExchange",
        "PremiumSettlementType",
        "PriceSide",
        "PricingParameters",
        "StubRule",
        "SwaptionType",
        "TenorReferenceDate",
    ]
    testing_attributes = dir(rdf.swap)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=["Definition", "LegDefinition", "PricingParameters", "AmortizationItem"],
    argvalues=[
        (
            rdf.swap._swap_definition.SwapInstrumentDefinition,
            {
                "instrument_tag": "instrument_tag",
                "instrument_code": "instrument_code",
                "trade_date": "trade_date",
                "start_date": "start_date",
                "end_date": "end_date",
                "tenor": "tenor",
                "legs": [
                    rdf.swap.LegDefinition(
                        direction=rdf.swap.Direction.RECEIVED,
                        interest_type=rdf.swap.InterestType.STEPPED,
                        notional_ccy="notional_ccy",
                        interest_payment_frequency=rdf.swap.Frequency.BI_MONTHLY,
                        interest_calculation_method=rdf.swap.DayCountBasis.DCB_30_360_US,
                    )
                ],
                "is_non_deliverable": True,
                "settlement_ccy": "settlement_ccy",
                "template": "template",
                "start_tenor": "start_tenor",
            },
        ),
        (
            rdf.swap.LegDefinition,
            {
                "index_spread_compounding_method": rdf.swap.IndexSpreadCompoundingMethod.ISDA_COMPOUNDING,
                "cms_template": "cms_template",
                "floor_strike_percent": 123.123,
                "leg_tag": "leg_tag",
                "direction": rdf.swap.Direction.RECEIVED,
                "interest_type": rdf.swap.InterestType.FIXED,
                "notional_ccy": "notional_ccy",
                "notional_amount": 6.6,
                "fixed_rate_percent": 7.7,
                "index_name": "index_name",
                "index_tenor": "index_tenor",
                "spread_bp": 10.10,
                "interest_payment_frequency": rdf.swap.Frequency.EVERY14_DAYS,
                "interest_calculation_method": rdf.swap.DayCountBasis.DCB_30_360_ISDA,
                "accrued_calculation_method": rdf.swap.DayCountBasis.DCB_30_365_BRAZIL,
                "payment_business_day_convention": rdf.swap.BusinessDayConvention.NEXT_BUSINESS_DAY,
                "payment_roll_convention": rdf.swap.DateRollingConvention.LAST28,
                "index_reset_frequency": rdf.swap.Frequency.BI_MONTHLY,
                "index_reset_type": rdf.swap.IndexResetType.IN_ARREARS,
                "index_fixing_lag": 18,
                "first_regular_payment_date": "first_regular_payment_date",
                "last_regular_payment_date": "last_regular_payment_date",
                "amortization_schedule": [rdf.swap.AmortizationItem()],
                "payment_business_days": "payment_business_days",
                "notional_exchange": rdf.swap.NotionalExchange.BOTH,
                "adjust_interest_to_payment_date": rdf.swap.AdjustInterestToPaymentDate.ADJUSTED,
                "index_compounding_method": rdf.swap.IndexCompoundingMethod.COMPOUNDED,
                "interest_payment_delay": 26,
                "stub_rule": rdf.swap.StubRule.SHORT_FIRST_PRO_RATA.ISSUE,
                "index_fixing_ric": "index_fixing_ric",
                "interest_calculation_convention": rdf.swap.InterestCalculationConvention.BOND_BASIS,
                "index_observation_method": rdf.swap.IndexObservationMethod.LOOKBACK,
                "upfront_amount": 11.11,
                "index_average_method": rdf.swap.IndexAverageMethod.COMPOUNDED_ACTUAL,
                "instrument_tag": "instrument_tag",
            },
        ),
        (
            rdf.swap.PricingParameters,
            {
                "report_ccy": "report_ccy",
                "market_data_date": "market_data_date",
                "index_convexity_adjustment_integration_method": rdf.swap.IndexConvexityAdjustmentIntegrationMethod.RIEMANN_SUM,
                "index_convexity_adjustment_method": rdf.swap.IndexConvexityAdjustmentMethod.BLACK_SCHOLES,
                "discounting_ccy": "discounting_ccy",
                "discounting_tenor": "discounting_tenor",
                "market_value_in_deal_ccy": 4.4,
                "valuation_date": "valuation_date",
                "use_legs_signing": True,
                "tenor_reference_date": rdf.swap.TenorReferenceDate.SPOT_DATE,
                "price_side": rdf.swap.PriceSide.ASK,
            },
        ),
        (
            rdf.swap.AmortizationItem,
            {
                "start_date": "start_date",
                "end_date": "end_date",
                "amortization_frequency": rdf.swap.AmortizationFrequency.ONCE,
                "amortization_type": rdf.swap.AmortizationType.LINEAR,
                "remaining_notional": 1.1,
                "amount": 2.2,
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
                    "legs": [{"paymentBusinessDays": "payment_business_days"}],
                    "startDate": "start_date",
                },
                "extended_params": "extended_params",
                "instrumentType": "Swap",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.swap.Definition(
        start_date="start_date",
        fields=["1", "2"],
        legs=[rdf.swap.LegDefinition(payment_business_days="payment_business_days")],
        pricing_parameters=rdf.swap.PricingParameters(
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
