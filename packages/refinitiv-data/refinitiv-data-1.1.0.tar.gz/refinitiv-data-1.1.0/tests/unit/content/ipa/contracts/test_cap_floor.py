from inspect import signature
import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession
import pytest

from tests.unit.conftest import (
    remove_dunder_methods,
    remove_private_attributes,
    has_property_names_in_class,
    get_property_names,
)


def test_ipa_cap_floor_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.cap_floor.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_cap_floor_attributes():
    expected_attributes = [
        "AdjustInterestToPaymentDate",
        "AmortizationFrequency",
        "AmortizationItem",
        "AmortizationType",
        "BarrierDefinitionElement",
        "BarrierType",
        "BusinessDayConvention",
        "BuySell",
        "DateRollingConvention",
        "DayCountBasis",
        "Definition",
        "Frequency",
        "IndexConvexityAdjustmentIntegrationMethod",
        "IndexConvexityAdjustmentMethod",
        "IndexResetType",
        "InputFlow",
        "InterestCalculationConvention",
        "PremiumSettlementType",
        "PriceSide",
        "PricingParameters",
        "StubRule",
    ]
    testing_attributes = dir(rdf.cap_floor)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "PricingParameters",
        "AmortizationItem",
        "InputFlow",
        "BarrierDefinitionElement",
    ],
    argvalues=[
        (
            rdf.cap_floor._cap_floor_definition.CapFloorInstrumentDefinition,
            {
                "payment_business_days": "payment_business_days",
                "barrier_definition": rdf.cap_floor.BarrierDefinitionElement(),
                "annualized_rebate": True,
                "cap_digital_payout_percent": 123.123,
                "cms_template": "cms_template",
                "floor_digital_payout_percent": 123.123,
                "instrument_tag": "instrument_tag",
                "start_date": "start_date",
                "end_date": "end_date",
                "tenor": "tenor",
                "notional_ccy": "notional_ccy",
                "notional_amount": 6.6,
                "index_name": "index_name",
                "index_tenor": "index_tenor",
                "interest_payment_frequency": rdf.cap_floor.Frequency.ANNUAL,
                "interest_calculation_method": rdf.cap_floor.DayCountBasis.DCB_30_360,
                "payment_business_day_convention": rdf.cap_floor.BusinessDayConvention.BBSW_MODIFIED_FOLLOWING,
                "payment_roll_convention": rdf.cap_floor.DateRollingConvention.LAST,
                "index_reset_frequency": rdf.cap_floor.Frequency.ANNUAL,
                "index_reset_type": rdf.cap_floor.IndexResetType.IN_ADVANCE,
                "index_fixing_lag": 15,
                "amortization_schedule": [rdf.cap_floor.AmortizationItem()],
                "adjust_interest_to_payment_date": rdf.cap_floor.AdjustInterestToPaymentDate.ADJUSTED,
                "buy_sell": rdf.cap_floor.BuySell.BUY,
                "cap_strike_percent": 19.19,
                "floor_strike_percent": 20.20,
                "index_fixing_ric": "index_fixing_ric",
                "stub_rule": rdf.cap_floor.StubRule.MATURITY,
                "is_backward_looking_index": True,
                "payments": [rdf.cap_floor.InputFlow()],
                "is_rfr": True,
                "interest_calculation_convention": rdf.cap_floor.InterestCalculationConvention.BOND_BASIS,
                "is_term_rate": True,
            },
        ),
        (
            rdf.cap_floor.PricingParameters,
            {
                "index_convexity_adjustment_integration_method": rdf.cap_floor.IndexConvexityAdjustmentIntegrationMethod.RIEMANN_SUM,
                "index_convexity_adjustment_method": rdf.cap_floor.IndexConvexityAdjustmentMethod.BLACK_SCHOLES,
                "market_value_in_deal_ccy": 2.2,
                "report_ccy": "str",
                "skip_first_cap_floorlet": True,
                "valuation_date": "valuation_date",
                "market_data_date": "market_data_date",
                "price_side": rdf.cap_floor.PriceSide.LAST,
            },
        ),
        (
            rdf.cap_floor.AmortizationItem,
            {
                "start_date": "start_date",
                "end_date": "end_date",
                "amortization_frequency": rdf.cap_floor.AmortizationFrequency.ONCE,
                "amortization_type": rdf.cap_floor.AmortizationType.NONE,
                "remaining_notional": 1.1,
                "amount": 2.2,
            },
        ),
        (
            rdf.cap_floor.InputFlow,
            {
                "amount": 1.1,
                "premium_settlement_type": rdf.cap_floor.PremiumSettlementType.FORWARD,
                "currency": "currency",
                "date": "date",
            },
        ),
        (
            rdf.cap_floor.BarrierDefinitionElement,
            {
                "barrier_type": rdf.cap_floor.BarrierType.KNOCK_IN,
                "barrier_down_percent": 1.1,
                "barrier_up_percent": 2.2,
                "rebate_down_percent": 3.3,
                "rebate_up_percent": 4.4,
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
    ), f"csl={cls}-{str(set(get_property_names(cls)) - set(args_names))}"

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
                    "interestCalculationMethod": "Dcb_Actual_Actual",
                    "interestPaymentFrequency": "Annual",
                    "notionalCcy": "USD",
                },
                "extended_params": "extended_params",
                "instrumentType": "CapFloor",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.cap_floor.Definition(
        end_date="2032-02-28",
        notional_ccy="USD",
        interest_payment_frequency="Annual",
        interest_calculation_method=rdf.cap_floor.DayCountBasis.DCB_ACTUAL_ACTUAL,
        fields=["1", "2"],
        pricing_parameters=rdf.cap_floor.PricingParameters(
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
