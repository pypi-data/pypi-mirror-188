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


def test_ipa_cross_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.cross.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_cross_attributes():
    expected_attributes = [
        "BuySell",
        "Definition",
        "FxCrossType",
        "FxLegType",
        "FxPoint",
        "FxSwapCalculationMethod",
        "ImpliedDepositDateConvention",
        "LegDefinition",
        "PriceSide",
        "PricingParameters",
    ]
    testing_attributes = dir(rdf.cross)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=["Definition", "LegDefinition", "PricingParameters"],
    argvalues=[
        (
            rdf.cross._fx_cross_definition.FxCrossInstrumentDefinition,
            {
                "instrument_tag": "instrument_tag",
                "legs": [rdf.cross.LegDefinition()],
                "fx_cross_type": rdf.cross.FxCrossType.FX_FORWARD,
                "fx_cross_code": "fx_cross_code",
                "ndf_fixing_settlement_ccy": "ndf_fixing_settlement_ccy",
                "reference_spot_rate": 6.6,
                "traded_cross_rate": 7.7,
                "traded_swap_points": 8.8,
            },
        ),
        (
            rdf.cross.LegDefinition,
            {
                "start_date": "start_date",
                "end_date": "end_date",
                "tenor": "tenor",
                "leg_tag": "leg_tag",
                "deal_ccy_buy_sell": rdf.cross.BuySell.BUY,
                "fx_leg_type": rdf.cross.FxLegType.FX_SPOT,
                "contra_amount": 7.7,
                "contra_ccy": "contra_ccy",
                "deal_amount": 9.9,
                "deal_ccy": "deal_ccy",
                "start_tenor": "start_tenor",
            },
        ),
        (
            rdf.cross.PricingParameters,
            {
                "fx_swap_calculation_method": rdf.cross.FxSwapCalculationMethod.FX_SWAP,
                "implied_deposit_date_convention": rdf.cross.ImpliedDepositDateConvention.FX_MARKET_CONVENTION,
                "price_side": rdf.cross.PriceSide.ASK,
                "adjust_all_deposit_points_to_cross_calendars": True,
                "adjust_all_swap_points_to_cross_calendars": True,
                "ignore_ref_ccy_holidays": True,
                "market_data_date": "market_data_date",
                "report_ccy": "report_ccy",
                "use_direct_quote": True,
                "valuation_date": "valuation_date",
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

    assert has_property_names_in_class(cls, args_names), set(args_names) ^ set(
        get_property_names(cls)
    )

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        assert attr == v, k


def test_leg_definition_start_date():
    # given
    definition = rdf.cross.LegDefinition(
        tenor="1M",
        start_date="2021-01-01",
        end_date="2021-02-01",
    )

    # then
    assert definition.start_date == "2021-01-01"


def test_leg_definition_start_tenor():
    # given
    definition = rdf.cross.LegDefinition(
        start_tenor="1M",
        tenor="1M",
        end_date="2021-02-01",
    )

    # then
    assert definition.start_tenor == "1M"


def test_request_body():
    # given
    expected_body = {
        "fields": ["1", "2"],
        "universe": [
            {
                "instrumentDefinition": {
                    "fxCrossCode": "fx_cross_code",
                    "legs": [{"startDate": "start_date"}],
                },
                "extended_params": "extended_params",
                "instrumentType": "FxCross",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.cross.Definition(
        fx_cross_code="fx_cross_code",
        fields=["1", "2"],
        legs=[rdf.cross.LegDefinition(start_date="start_date")],
        pricing_parameters=rdf.cross.PricingParameters(
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
