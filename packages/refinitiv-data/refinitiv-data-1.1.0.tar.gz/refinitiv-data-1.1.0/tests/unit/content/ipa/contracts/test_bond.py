import json
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


def test_ipa_bond_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.bond.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_bond_attributes():
    expected_attributes = [
        "AdjustInterestToPaymentDate",
        "AmortizationFrequency",
        "AmortizationItem",
        "AmortizationType",
        "BenchmarkYieldSelectionMode",
        "BondRoundingParameters",
        "BusinessDayConvention",
        "CreditSpreadType",
        "DateRollingConvention",
        "DayCountBasis",
        "Definition",
        "Direction",
        "DividendType",
        "Frequency",
        "IndexAverageMethod",
        "IndexCompoundingMethod",
        "InflationMode",
        "InterestType",
        "PriceSide",
        "PricingParameters",
        "ProjectedIndexCalculationMethod",
        "QuoteFallbackLogic",
        "RedemptionDateType",
        "Rounding",
        "RoundingType",
        "StubRule",
        "VolatilityTermStructureType",
        "VolatilityType",
        "YieldType",
    ]
    testing_attributes = dir(rdf.bond)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "PricingParameters",
        "BondRoundingParameters",
        "AmortizationItem",
    ],
    argvalues=[
        (
            rdf.bond._bond_definition.BondInstrumentDefinition,
            {
                "instrument_code": "instrument_code",
                "instrument_tag": "instrument_tag",
                "end_date": "end_date",
                "direction": rdf.bond.Direction.PAID,
                "interest_type": rdf.bond.InterestType.FIXED,
                "notional_ccy": "notional_ccy",
                "notional_amount": 7.7,
                "fixed_rate_percent": 8.8,
                "spread_bp": 9.9,
                "interest_payment_frequency": rdf.bond.Frequency.EVERY14_DAYS,
                "interest_calculation_method": rdf.bond.DayCountBasis.DCB_30_360_ISDA,
                "accrued_calculation_method": rdf.bond.DayCountBasis.DCB_30_360,
                "payment_business_day_convention": rdf.bond.BusinessDayConvention.MODIFIED_FOLLOWING,
                "payment_roll_convention": rdf.bond.DateRollingConvention.LAST28,
                "index_reset_frequency": rdf.bond.Frequency.ANNUAL,
                "index_fixing_lag": 16,
                "first_regular_payment_date": "first_regular_payment_date",
                "last_regular_payment_date": "last_regular_payment_date",
                "amortization_schedule": [rdf.bond.AmortizationItem()],
                "payment_business_days": "payment_business_days",
                "adjust_interest_to_payment_date": rdf.bond.AdjustInterestToPaymentDate.ADJUSTED,
                "index_compounding_method": rdf.bond.IndexCompoundingMethod.MEXICAN_COMPOUNDED,
                "interest_payment_delay": 23,
                "stub_rule": rdf.bond.StubRule.ISSUE,
                "issue_date": "issue_date",
                "index_average_method": rdf.bond.IndexAverageMethod.ARITHMETIC_AVERAGE,
                "first_accrual_date": "str",
                "floor_strike_percent": 10.10,
                "index_fixing_ric": "index_fixing_ric",
                "is_perpetual": True,
                "template": "str",
            },
        ),
        (
            rdf.bond.PricingParameters,
            {
                "trade_date": "trade_date",
                "benchmark_yield_selection_mode": rdf.bond.BenchmarkYieldSelectionMode.INTERPOLATE,
                "credit_spread_type": rdf.bond.CreditSpreadType.TERM_STRUCTURE,
                "dividend_type": rdf.bond.DividendType.FUTURES,
                "volatility_term_structure_type": rdf.bond.VolatilityTermStructureType.HISTORICAL,
                "volatility_type": rdf.bond.VolatilityType.FLAT,
                "bond_recovery_rate_percent": 123.123,
                "cds_recovery_rate_percent": 123.123,
                "dividend_yield_percent": 123.123,
                "flat_credit_spread_bp": 123.123,
                "flat_credit_spread_tenor": "flat_credit_spread_tenor",
                "fx_stock_correlation": 123.123,
                "fx_volatility_percent": 123.123,
                "fx_volatility_tenor": "fx_volatility_tenor",
                "stock_borrow_rate_percent": 123.123,
                "stock_flat_volatility_percent": 123.123,
                "stock_flat_volatility_tenor": "stock_flat_volatility_tenor",
                "stock_price_on_default": 123.123,
                "market_data_date": "market_data_date",
                "price_side": rdf.bond.PriceSide.MID,
                "projected_index_calculation_method": rdf.bond.ProjectedIndexCalculationMethod.CONSTANT_INDEX,
                "redemption_date_type": rdf.bond.RedemptionDateType.REDEMPTION_AT_BEST_DATE,
                "rounding_parameters": rdf.bond.BondRoundingParameters(),
                "yield_type": rdf.bond.YieldType.DISCOUNT_ACTUAL_360,
                "adjusted_clean_price": 9.9,
                "adjusted_dirty_price": 10.10,
                "adjusted_yield_percent": 11.11,
                "apply_tax_to_full_pricing": True,
                "asset_swap_spread_bp": 13.13,
                "benchmark_at_issue_price": 14.14,
                "benchmark_at_issue_ric": "benchmark_at_issue_ric",
                "benchmark_at_issue_spread_bp": 16.16,
                "benchmark_at_issue_yield_percent": 17.17,
                "benchmark_at_redemption_price": 18.18,
                "benchmark_at_redemption_spread_bp": 19.19,
                "benchmark_at_redemption_yield_percent": 20.20,
                "cash_amount": 21.21,
                "clean_price": 22.22,
                "concession_fee": 23.23,
                "current_yield_percent": 24.24,
                "dirty_price": 25.25,
                "discount_margin_bp": 26.26,
                "discount_percent": 27.27,
                "edsf_benchmark_curve_yield_percent": 28.28,
                "edsf_spread_bp": 29.29,
                "efp_benchmark_price": 30.30,
                "efp_benchmark_ric": "efp_benchmark_ric",
                "efp_benchmark_yield_percent": 32.32,
                "efp_spread_bp": 33.33,
                "gov_country_benchmark_curve_price": 34.34,
                "gov_country_benchmark_curve_yield_percent": 35.35,
                "gov_country_spread_bp": 36.36,
                "government_benchmark_curve_price": 37.37,
                "government_benchmark_curve_yield_percent": 38.38,
                "government_spread_bp": 39.39,
                "issuer_benchmark_curve_yield_percent": 40.40,
                "issuer_spread_bp": 41.41,
                "market_value_in_deal_ccy": 42.42,
                "market_value_in_report_ccy": 43.43,
                "net_price": 44.44,
                "neutral_yield_percent": 45.45,
                "option_adjusted_spread_bp": 48.48,
                "price": 49.49,
                "quoted_price": 50.50,
                "rating_benchmark_curve_yield_percent": 51.51,
                "rating_spread_bp": 52.52,
                "redemption_date": "redemption_date",
                "sector_rating_benchmark_curve_yield_percent": 54.54,
                "sector_rating_spread_bp": 55.55,
                "settlement_convention": "settlement_convention",
                "simple_margin_bp": 57.57,
                "strip_yield_percent": 58.58,
                "swap_benchmark_curve_yield_percent": 59.59,
                "swap_spread_bp": 60.60,
                "tax_on_capital_gain_percent": 61.61,
                "tax_on_coupon_percent": 62.62,
                "tax_on_price_percent": 63.63,
                "tax_on_yield_percent": 64.64,
                "user_defined_benchmark_price": 66.66,
                "user_defined_benchmark_yield_percent": 67.67,
                "user_defined_spread_bp": 68.68,
                "valuation_date": "valuation_date",
                "yield_percent": 70.70,
                "z_spread_bp": 71.71,
                "quote_fallback_logic": rdf.bond.QuoteFallbackLogic.BEST_FIELD,
                "fx_price_side": rdf.bond.PriceSide.BID,
                "ois_zc_benchmark_curve_yield_percent": 72.72,
                "ois_zc_spread_bp": 73.73,
                "use_settlement_date_from_quote": True,
                "compute_cash_flow_with_report_ccy": True,
                "inflation_mode": rdf.bond.InflationMode.DEFAULT,
                "next_coupon_rate_percent": 74.74,
                "is_coupon_payment_adjustedfor_leap_year": True,
                "report_ccy": "report_ccy",
                "compute_cash_flow_from_issue_date": True,
                "projected_index_percent": 75.75,
            },
        ),
        (
            rdf.bond.BondRoundingParameters,
            {
                "accrued_rounding": rdf.bond.Rounding.FOUR,
                "accrued_rounding_type": rdf.bond.RoundingType.FACE_NEAR,
                "price_rounding": rdf.bond.Rounding.FIVE,
                "price_rounding_type": rdf.bond.RoundingType.FACE_DOWN,
                "spread_rounding": rdf.bond.Rounding.EIGHT,
                "spread_rounding_type": rdf.bond.RoundingType.CEIL,
                "yield_rounding": rdf.bond.Rounding.DEFAULT,
                "yield_rounding_type": rdf.bond.RoundingType.FACE_UP,
            },
        ),
        (
            rdf.bond.AmortizationItem,
            {
                "start_date": "start_date",
                "end_date": "end_date",
                "amortization_frequency": rdf.bond.AmortizationFrequency.ONCE,
                "amortization_type": rdf.bond.AmortizationType.LINEAR,
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

    try:
        json_data = inst.get_dict()
        json.dumps(json_data)
    except Exception as e:
        assert False, str(e)


def test_bond_definition_will_raise_exception_if_pass_not_str():
    with pytest.raises(ValueError, match="Invalid type of instrument_code"):
        rdf.bond.Definition(["one", "two"])


def test_none_value_is_not_set_instrument_code():
    # given
    bond_definition = rdf.bond.Definition(
        issue_date="2002-02-28",
        end_date="2032-02-28",
        notional_ccy="USD",
        interest_payment_frequency="Annual",
        fixed_rate_percent=7,
        interest_calculation_method=rdf.bond.DayCountBasis.DCB_ACTUAL_ACTUAL,
    )
    definition = bond_definition._kwargs["definition"]

    # when
    testing_value = definition.instrument_code

    # then
    assert testing_value is None


def test_request_body():
    # given
    expected_body = {
        "fields": ["1", "2"],
        "universe": [
            {
                "instrumentDefinition": {
                    "endDate": "2032-02-28",
                    "fixedRatePercent": 7,
                    "interestCalculationMethod": "Dcb_Actual_Actual",
                    "interestPaymentFrequency": "Annual",
                    "issueDate": "2002-02-28",
                    "notionalCcy": "USD",
                },
                "extended_params": "extended_params",
                "instrumentType": "Bond",
                "pricingParameters": {"tradeDate": "trade_date"},
            }
        ],
    }
    definition = rdf.bond.Definition(
        issue_date="2002-02-28",
        end_date="2032-02-28",
        notional_ccy="USD",
        interest_payment_frequency="Annual",
        fixed_rate_percent=7,
        interest_calculation_method=rdf.bond.DayCountBasis.DCB_ACTUAL_ACTUAL,
        extended_params={"extended_params": "extended_params"},
        pricing_parameters=rdf.bond.PricingParameters(trade_date="trade_date"),
        fields=["1", "2"],
    )

    # when
    content_type = definition._kwargs["__content_type__"]
    provider = make_provider(content_type)
    request = provider.request.create(StubSession(), "url", **definition._kwargs)

    # then
    testing_body = request.json
    assert testing_body == expected_body, expected_body
