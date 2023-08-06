from inspect import signature

import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession
from tests.unit.conftest import has_property_names_in_class, get_property_names


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "FxBarrierDefinition",
        "FxForwardStart",
        "FxDoubleBarrierInfo",
        "EtiUnderlyingDefinition",
        "FxDoubleBarrierDefinition",
        "FxAverageInfo",
        "BidAskMid",
        "FxUnderlyingDefinition",
        "EtiCbbcDefinition",
        "PricingParameters",
        "EtiDoubleBarriersDefinition",
        "FxDualCurrencyDefinition",
        "EtiBinaryDefinition",
        "EtiFixingInfo",
        "EtiBarrierDefinition",
        "FxBinaryDefinition",
        "FxDoubleBinaryDefinition",
        "InterpolationWeight",
        "PayoutScaling",
        "OptionDefinition",
        "FxDefinition",
        "EtiDefinition",
        "InputFlow",
    ],
    argvalues=[
        (
            rdf.option.FxBarrierDefinition,
            {
                "barrier_mode": rdf.option.BarrierMode.EUROPEAN,
                "in_or_out": rdf.option.InOrOut.OUT,
                "up_or_down": rdf.option.UpOrDown.UP,
                "level": 4.4,
                "rebate_amount": 5.5,
                "window_end_date": "window_end_date",
                "window_start_date": "window_start_date",
            },
        ),
        (
            rdf.option.FxForwardStart,
            {
                "forward_start_date": "forward_start_date",
                "forward_start_tenor": "forward_start_tenor",
                "strike_percent": 123.123,
            },
        ),
        (
            rdf.option.FxDoubleBarrierInfo,
            {
                "in_or_out": rdf.option.InOrOut.IN,
                "level": 2.2,
                "rebate_amount": 3.3,
            },
        ),
        (
            rdf.option.EtiUnderlyingDefinition,
            {
                "instrument_code": "instrument_code",
            },
        ),
        (
            rdf.option.FxDoubleBarrierDefinition,
            {
                "barrier_down": rdf.option.FxDoubleBarrierInfo(),
                "barrier_mode": rdf.option.BarrierMode.EARLY_END_WINDOW,
                "barrier_up": rdf.option.FxDoubleBarrierInfo(),
            },
        ),
        (
            rdf.option.FxAverageInfo,
            {
                "average_type": rdf.option.AverageType.GEOMETRIC_STRIKE,
                "fixing_frequency": rdf.option.FixingFrequency.ANNUAL,
                "average_so_far": 3.3,
                "fixing_ric": "fixing_ric",
                "fixing_start_date": "str",
                "include_holidays": True,
                "include_week_ends": True,
            },
        ),
        (
            rdf.option.BidAskMid,
            {
                "bid": 123.123,
                "ask": 123.123,
                "mid": 123.123,
            },
        ),
        (
            rdf.option.FxUnderlyingDefinition,
            {"fx_cross_code": "fx_cross_code"},
        ),
        (
            rdf.option.EtiCbbcDefinition,
            {
                "conversion_ratio": 1.1,
                "level": 2.2,
            },
        ),
        (
            rdf.option.PricingParameters,
            {
                "butterfly10_d_object": rdf.option.BidAskMid(),
                "butterfly25_d_object": rdf.option.BidAskMid(),
                "payout_custom_dates": ["payout_custom_dates"],
                "payout_scaling_interval": rdf.option.PayoutScaling(),
                "risk_reversal10_d_object": rdf.option.BidAskMid(),
                "risk_reversal25_d_object": rdf.option.BidAskMid(),
                "compute_payout_chart": True,
                "compute_volatility_payout": True,
                "report_ccy_rate": True,
                "atm_volatility_object": rdf.option.BidAskMid(),
                "domestic_deposit_rate_percent_object": rdf.option.BidAskMid(),
                "foreign_deposit_rate_percent_object": rdf.option.BidAskMid(),
                "forward_points_object": rdf.option.BidAskMid(),
                "fx_spot_object": rdf.option.BidAskMid(),
                "fx_swap_calculation_method": rdf.option.FxSwapCalculationMethod.FX_SWAP,
                "implied_volatility_object": rdf.option.BidAskMid(),
                "interpolation_weight": rdf.option.InterpolationWeight(),
                "option_price_side": rdf.option.PriceSide.BID,
                "option_time_stamp": rdf.option.TimeStamp.DEFAULT,
                "price_side": rdf.option.PriceSide.MID,
                "pricing_model_type": rdf.option.PricingModelType.BINOMIAL,
                "underlying_price_side": rdf.option.PriceSide.ASK,
                "underlying_time_stamp": rdf.option.TimeStamp.OPEN,
                "volatility_model": rdf.option.VolatilityModel.CUBIC_SPLINE,
                "volatility_type": rdf.option.OptionVolatilityType.IMPLIED,
                "cutoff_time": "cutoff_time",
                "cutoff_time_zone": "cutoff_time_zone",
                "market_value_in_deal_ccy": 23.23,
                "risk_free_rate_percent": 24.24,
                "underlying_price": 25.25,
                "valuation_date": "valuation_date",
                "volatility_percent": 27.27,
                "market_data_date": "market_data_date",
                "market_value_in_report_ccy": 28.28,
                "volatility": 29.29,
                "report_ccy": "report_ccy",
                "simulate_exercise": True,
            },
        ),
        (
            rdf.option.EtiDoubleBarriersDefinition,
            {
                "barriers_definition": [rdf.option.EtiBarrierDefinition()],
            },
        ),
        (
            rdf.option.FxDualCurrencyDefinition,
            {
                "deposit_start_date": "deposit_start_date",
                "margin_percent": 123.123,
            },
        ),
        (
            rdf.option.EtiBinaryDefinition,
            {
                "notional_amount": 1.1,
                "binary_type": rdf.option.BinaryType.DIGITAL,
                "up_or_down": rdf.option.UpOrDown.DOWN,
                "level": 4.4,
            },
        ),
        (
            rdf.option.EtiFixingInfo,
            {
                "average_so_far": 123,
                "average_type": rdf.option.AverageType.GEOMETRIC_STRIKE,
                "fixing_frequency": rdf.option.FixingFrequency.WEEKLY,
                "fixing_calendar": "fixing_calendar",
                "fixing_end_date": "fixing_end_date",
                "fixing_start_date": "fixing_start_date",
                "include_holidays": True,
                "include_week_ends": True,
            },
        ),
        (
            rdf.option.EtiBarrierDefinition,
            {
                "barrier_style": rdf.option.BarrierStyle.AMERICAN,
                "in_or_out": rdf.option.InOrOut.IN,
                "up_or_down": rdf.option.UpOrDown.DOWN,
                "level": 3.3,
            },
        ),
        (
            rdf.option.FxBinaryDefinition,
            {
                "binary_type": rdf.option.FxBinaryType.ONE_TOUCH_DEFERRED,
                "payout_amount": 3.3,
                "payout_ccy": "payout_ccy",
                "trigger": 5.5,
            },
        ),
        (
            rdf.option.FxDoubleBinaryDefinition,
            {
                "double_binary_type": rdf.option.DoubleBinaryType.DOUBLE_NO_TOUCH,
                "payout_amount": 3.3,
                "payout_ccy": "payout_ccy",
                "trigger_down": 5.5,
                "trigger_up": 6.6,
            },
        ),
        (
            rdf.option.InterpolationWeight,
            {
                "days_list": [rdf.option.DayWeight()],
                "holidays": 123.123,
                "week_days": 123.123,
                "week_ends": 123.123,
            },
        ),
        (
            rdf.option.PayoutScaling,
            {
                "maximum": 123.123,
                "minimum": 123.123,
            },
        ),
        (
            rdf.option._option_definition.OptionDefinition,
            {
                "instrument_tag": "instrument_tag",
                "end_date": "end_date",
                "buy_sell": rdf.option.BuySell.BUY,
                "call_put": rdf.option.CallPut.CALL,
                "exercise_style": rdf.option.ExerciseStyle.AMER,
                "underlying_type": rdf.option.UnderlyingType.ETI,
                "strike": 123.123,
                "start_date": "start_date",
            },
        ),
        (
            rdf.option._fx._fx_definition.FxDefinition,
            {
                "instrument_tag": "instrument_tag",
                "end_date": "end_date",
                "tenor": "tenor",
                "notional_ccy": "notional_ccy",
                "notional_amount": 123.123,
                "asian_definition": rdf.option.FxAverageInfo(),
                "barrier_definition": rdf.option.FxBarrierDefinition(),
                "binary_definition": rdf.option.FxBinaryDefinition(),
                "buy_sell": rdf.option.BuySell.BUY,
                "call_put": rdf.option.CallPut.CALL,
                "double_barrier_definition": rdf.option.FxDoubleBarrierDefinition(),
                "double_binary_definition": rdf.option.FxDoubleBinaryDefinition(),
                "dual_currency_definition": rdf.option.FxDualCurrencyDefinition(),
                "exercise_style": rdf.option.ExerciseStyle.AMER,
                "forward_start_definition": rdf.option.FxForwardStart(),
                "underlying_definition": rdf.option.FxUnderlyingDefinition(),
                "underlying_type": rdf.option.UnderlyingType.ETI,
                "delivery_date": "delivery_date",
                "strike": 123.123,
                "settlement_type": rdf.option.SettlementType.CASH,
                "settlement_ccy": "settlement_ccy",
                "payments": [rdf.option.InputFlow()],
                "start_date": "start_date",
            },
        ),
        (
            rdf.option._eti._eti_definition.EtiDefinition,
            {
                "instrument_tag": "instrument_tag",
                "instrument_code": "instrument_code",
                "end_date": "end_date",
                "asian_definition": rdf.option.EtiFixingInfo(),
                "barrier_definition": rdf.option.EtiBarrierDefinition(),
                "binary_definition": rdf.option.EtiBinaryDefinition(),
                "buy_sell": rdf.option.BuySell.SELL,
                "call_put": rdf.option.CallPut.PUT,
                "cbbc_definition": rdf.option.EtiCbbcDefinition(),
                "double_barriers_definition": rdf.option.EtiDoubleBarriersDefinition(),
                "exercise_style": rdf.option.ExerciseStyle.EURO,
                "underlying_definition": rdf.option.EtiUnderlyingDefinition(),
                "underlying_type": rdf.option.UnderlyingType.FX,
                "deal_contract": 123,
                "end_date_time": "end_date_time",
                "lot_size": 123.123,
                "strike": 123.123,
                "time_zone_offset": 123,
                "start_date": "start_date",
            },
        ),
        (
            rdf.option.InputFlow,
            {
                "amount": 1.1,
                "premium_settlement_type": rdf.option.PremiumSettlementType.SPOT,
                "currency": "currency",
                "date": "date",
            },
        ),
    ],
)
def test_parameter(input_data):
    cls, kwargs = input_data
    args_names = list(kwargs.keys())
    inst = cls(**kwargs)

    s = signature(cls.__init__)
    testing_len = len(s.parameters)
    expected_len = len(args_names) + 1  # +1 for (self)

    if s.parameters.get("kwargs"):
        expected_len += 1  # +1 for kwargs

    assert (
        testing_len == expected_len
    ), f"csl={cls}{str(set(get_property_names(cls)) - set(args_names))}"
    assert has_property_names_in_class(cls, args_names), set(args_names) - set(
        get_property_names(cls)
    )

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        if hasattr(v, "value") and attr == "Eti":
            assert attr == v.value, k
        else:
            assert attr == v, k


def test_request_body():
    # given
    expected_body = {
        "fields": ["1", "2"],
        "universe": [
            {
                "instrumentDefinition": {
                    "asianDefinition": {"averageSoFar": 1.1},
                },
                "extended_params": "extended_params",
                "instrumentType": "Option",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.option.Definition(
        asian_definition=rdf.option.EtiFixingInfo(average_so_far=1.1),
        fields=["1", "2"],
        pricing_parameters=rdf.option.PricingParameters(
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
