from inspect import signature

import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession
from tests.unit.conftest import remove_dunder_methods, remove_private_attributes
from tests.unit.content.ipa.contracts.conftest import (
    has_property_names_in_class,
    get_property_names,
)


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "RepoParameters",
        "PricingParameters",
        "UnderlyingContract",
        "UnderlyingPricingParameters",
    ],
    argvalues=[
        (
            rdf.repo._repo_definition.RepoInstrumentDefinition,
            {
                "instrument_tag": "instrument_tag",
                "start_date": "start_date",
                "end_date": "end_date",
                "tenor": "tenor",
                "day_count_basis": rdf.repo.DayCountBasis.DCB_30_365_BRAZIL,
                "underlying_instruments": [rdf.repo.UnderlyingContract()],
                "is_coupon_exchanged": True,
                "repo_rate_percent": 8.8,
                "buy_sell": rdf.repo.BuySell.BUY,
            },
        ),
        (
            rdf.repo.RepoParameters,
            {
                "coupon_paid_at_horizon": True,
                "haircut_rate_percent": 2.2,
                "initial_margin_percent": 3.3,
                "repurchase_price": 4.4,
                "purchase_price": 5.5,
            },
        ),
        (
            rdf.repo.PricingParameters,
            {
                "market_data_date": "market_data_date",
                "repo_curve_type": rdf.repo.RepoCurveType.LIBOR_FIXING,
                "valuation_date": "valuation_date",
                "report_ccy": "report_ccy",
            },
        ),
        (
            rdf.repo.UnderlyingContract,
            {
                "instrument_type": "instrument_type",
                "instrument_definition": rdf.bond.Definition(),
                "pricing_parameters": rdf.repo.UnderlyingPricingParameters(),
            },
        ),
        (
            rdf.repo.UnderlyingPricingParameters,
            {
                "pricing_parameters_at_end": rdf.bond.PricingParameters(),
                "pricing_parameters_at_start": rdf.bond.PricingParameters(),
                "repo_parameters": rdf.repo.RepoParameters(),
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


def test_ipa_repo_definition_attributes():
    expected_attributes = ["get_data", "get_data_async", "get_stream"]
    testing_attributes = dir(rdf.repo.Definition)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


def test_ipa_repo_attributes():
    expected_attributes = [
        "BuySell",
        "DayCountBasis",
        "Definition",
        "PricingParameters",
        "RepoCurveType",
        "RepoParameters",
        "UnderlyingContract",
        "UnderlyingPricingParameters",
    ]
    testing_attributes = dir(rdf.repo)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, testing_attributes


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
                "instrumentType": "Repo",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            }
        ],
    }
    definition = rdf.repo.Definition(
        start_date="start_date",
        fields=["1", "2"],
        pricing_parameters=rdf.repo.PricingParameters(
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
