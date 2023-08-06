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


def test_ipa_swaption_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.swaption.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_swaption_attributes():
    expected_attributes = [
        "BermudanSwaptionDefinition",
        "BuySell",
        "CallPut",
        "Definition",
        "ExerciseScheduleType",
        "ExerciseStyle",
        "InputFlow",
        "PremiumSettlementType",
        "PriceSide",
        "PricingParameters",
        "SwaptionMarketDataRule",
        "SwaptionSettlementType",
        "SwaptionType",
    ]
    testing_attributes = dir(rdf.swaption)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "PricingParameters",
        "SwaptionMarketDataRule",
        "BermudanSwaptionDefinition",
        "InputFlow",
    ],
    argvalues=[
        (
            rdf.swaption._swaption_definition.SwaptionInstrumentDefinition,
            {
                "notional_amount": 12.321,
                "spread_vs_atm_in_bp": 123.321,
                "instrument_tag": "instrument_tag",
                "end_date": "end_date",
                "tenor": "tenor",
                "bermudan_swaption_definition": rdf.swaption.BermudanSwaptionDefinition(),
                "buy_sell": rdf.swaption.BuySell.BUY,
                "exercise_style": rdf.swaption.ExerciseStyle.EURO,
                "settlement_type": rdf.swaption.SwaptionSettlementType.CASH,
                "underlying_definition": rdf.swap.Definition(
                    tenor="5Y", template="template"
                ),
                "strike_percent": 10.10,
                "swaption_type": rdf.swaption.SwaptionType.PAYER,
                "start_date": "start_date",
                "premium_settlement_type": rdf.swaption.PremiumSettlementType.FORWARD,
                "payments": [rdf.swaption.InputFlow()],
            },
        ),
        (
            rdf.swaption.PricingParameters,
            {
                "market_data_date": "market_data_date",
                "market_value_in_deal_ccy": 3.3,
                "nb_iterations": 4,
                "valuation_date": "valuation_date",
                "price_side": rdf.swaption.PriceSide.ASK,
                "simulate_exercise": True,
                "exercise_date": "exercise_date",
                "report_ccy": "report_ccy",
            },
        ),
        (
            rdf.swaption.SwaptionMarketDataRule,
            {
                "discount": "discount",
                "forward": "forward",
            },
        ),
        (
            rdf.swaption.BermudanSwaptionDefinition,
            {
                "exercise_schedule": ["exercise_schedule"],
                "exercise_schedule_type": rdf.swaption.ExerciseScheduleType.FIXED_LEG,
                "notification_days": 3,
            },
        ),
        (
            rdf.swaption.InputFlow,
            {
                "amount": 1.1,
                "premium_settlement_type": rdf.swaption.PremiumSettlementType.SPOT,
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
                    "bermudanSwaptionDefinition": {
                        "exerciseSchedule": ["exercise_schedule"],
                        "notificationDays": 0,
                    },
                    "startDate": "start_date",
                    "underlyingDefinition": {"tradeDate": "trade_date"},
                },
                "extended_params": "extended_params",
                "instrumentType": "Swaption",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.swaption.Definition(
        bermudan_swaption_definition=rdf.swaption.BermudanSwaptionDefinition(
            exercise_schedule=["exercise_schedule"],
            notification_days=0,
        ),
        start_date="start_date",
        fields=["1", "2"],
        underlying_definition=rdf.swap.Definition(trade_date="trade_date"),
        pricing_parameters=rdf.swaption.PricingParameters(
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
