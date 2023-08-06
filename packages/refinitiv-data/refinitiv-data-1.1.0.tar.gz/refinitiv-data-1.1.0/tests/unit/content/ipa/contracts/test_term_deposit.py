from inspect import signature

import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession
from tests.unit.conftest import (
    remove_private_attributes,
    remove_dunder_methods,
    has_property_names_in_class,
    get_property_names,
)


def test_ipa_term_deposit_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.term_deposit.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_term_deposit_attributes():
    expected_attributes = [
        "BusinessDayConvention",
        "DateRollingConvention",
        "DayCountBasis",
        "Definition",
        "PriceSide",
        "PricingParameters",
    ]
    testing_attributes = dir(rdf.term_deposit)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=["Definition", "PricingParameters"],
    argvalues=[
        (
            rdf.term_deposit._term_deposit_definition.TermDepositInstrumentDefinition,
            {
                "instrument_tag": "instrument_tag",
                "instrument_code": "instrument_code",
                "start_date": "start_date",
                "end_date": "end_date",
                "tenor": "tenor",
                "notional_ccy": "notional_ccy",
                "notional_amount": 7.7,
                "fixed_rate_percent": 8.8,
                "payment_business_day_convention": rdf.term_deposit.BusinessDayConvention.NO_MOVING,
                "payment_roll_convention": rdf.term_deposit.DateRollingConvention.LAST28,
                "year_basis": rdf.term_deposit.DayCountBasis.DCB_30_360_ISDA,
                "calendar": "calendar",
            },
        ),
        (
            rdf.term_deposit.PricingParameters,
            {
                "price_side": rdf.term_deposit.PriceSide.LAST,
                "income_tax_percent": 2.2,
                "valuation_date": "valuation_date",
                "market_data_date": "market_data_date",
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
                    "startDate": "start_date",
                },
                "extended_params": "extended_params",
                "instrumentType": "TermDeposit",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.term_deposit.Definition(
        start_date="start_date",
        fields=["1", "2"],
        pricing_parameters=rdf.term_deposit.PricingParameters(
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
