import functools

import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession


def test_contracts_version():
    # given
    expected = "1.0.155"

    # when
    testing_version = rdf.__version__

    # then
    assert testing_version == expected, testing_version


def test_definition_repr():
    # given
    expected_value = (
        "<refinitiv.data.content.ipa.financial_contracts.Definition object at"
    )
    definition = rdf.Definitions([])

    # when
    testing_value = repr(definition)

    # then
    assert expected_value in testing_value, testing_value


def test_definition_call():
    # given
    bond_definition = rdf.bond.Definition(
        issue_date="2002-02-28",
        end_date="2032-02-28",
        notional_ccy="USD",
        interest_payment_frequency="Annual",
        fixed_rate_percent=7,
        interest_calculation_method=rdf.bond.DayCountBasis.DCB_ACTUAL_ACTUAL,
    )

    # when
    definition = rdf.Definitions([bond_definition])

    # then
    assert definition


def test_request_body():
    # given
    expected_body = {
        "fields": ["1", "2"],
        "pricingParameters": {"marketDataDate": "market_data_date"},
        "universe": [
            {
                "instrumentDefinition": {
                    "extended_params": "extended_params",
                    "legs": [{"paymentBusinessDays": "payment_business_days"}],
                    "startDate": "start_date",
                },
                "instrumentType": "Swap",
                "pricingParameters": {"marketDataDate": "market_data_date"},
            },
            {
                "instrumentDefinition": {
                    "endDate": "2032-02-28",
                    "extended_params": "extended_params",
                    "fixedRatePercent": 7,
                    "interestCalculationMethod": "Dcb_Actual_Actual",
                    "interestPaymentFrequency": "Annual",
                    "issueDate": "2002-02-28",
                    "notionalCcy": "USD",
                },
                "instrumentType": "Bond",
                "pricingParameters": {"tradeDate": "trade_date"},
            },
        ],
    }
    bond_definition = rdf.bond.Definition(
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
    swap_definition = rdf.swap.Definition(
        start_date="start_date",
        fields=["1", "2"],
        legs=[rdf.swap.LegDefinition(payment_business_days="payment_business_days")],
        pricing_parameters=rdf.swap.PricingParameters(
            market_data_date="market_data_date"
        ),
        extended_params={"extended_params": "extended_params"},
    )
    definition = rdf.Definitions(
        universe=[swap_definition, bond_definition],
        fields=["1", "2"],
        pricing_parameters=rdf.swap.PricingParameters(
            market_data_date="market_data_date"
        ),
    )

    # when
    content_type = definition._kwargs["__content_type__"]
    provider = make_provider(content_type)
    request = provider.request.create(StubSession(), "url", **definition._kwargs)

    # then
    testing_body = request.json
    assert testing_body == expected_body, expected_body


@pytest.mark.parametrize(
    "definition",
    [
        functools.partial(rdf.Definitions, None),
        functools.partial(rdf.Definitions, ""),
        functools.partial(rdf.Definitions, "None"),
        functools.partial(rdf.Definitions, 100),
        functools.partial(rdf.Definitions, ["None"]),
        functools.partial(rdf.Definitions, {None}),
        functools.partial(rdf.Definitions, [{}]),
        functools.partial(rdf.Definitions, [100]),
        functools.partial(rdf.Definitions, rdf.Definitions),
        functools.partial(
            rdf.Definitions,
            [rdf.term_deposit.Definition(), "None", rdf.bond.Definition()],
        ),
    ],
)
def test_validate_universe_raise_type_error(definition):
    with pytest.raises(TypeError):
        definition()


def test_validate_universe_type_error_message():
    err_msg = (
        "Provided type for parameter 'universe' is invalid. "
        "Expected types: [bond.Definition, cap_floor.Definition, cds.Definition, cross.Definition, "
        "option.Definition, repo.Definition, swap.Definition, swaption.Definition, "
        "term_deposit.Definition]"
    )
    try:
        rdf.Definitions(None)
    except TypeError as e:
        assert str(e) == err_msg


@pytest.mark.parametrize(
    "definition",
    [
        functools.partial(rdf.Definitions, rdf.bond.Definition()),
        functools.partial(rdf.Definitions, rdf.cap_floor.Definition()),
        functools.partial(rdf.Definitions, rdf.cds.Definition()),
        functools.partial(rdf.Definitions, rdf.cross.Definition()),
        functools.partial(rdf.Definitions, rdf.option.Definition()),
        functools.partial(rdf.Definitions, rdf.repo.Definition()),
        functools.partial(rdf.Definitions, rdf.swap.Definition()),
        functools.partial(rdf.Definitions, rdf.swaption.Definition()),
        functools.partial(rdf.Definitions, rdf.term_deposit.Definition()),
        functools.partial(rdf.Definitions, [rdf.term_deposit.Definition()]),
        functools.partial(
            rdf.Definitions,
            [
                rdf.term_deposit.Definition(),
                rdf.term_deposit.Definition(),
                rdf.bond.Definition(),
            ],
        ),
        functools.partial(rdf.Definitions, set()),
        functools.partial(rdf.Definitions, dict()),
        functools.partial(rdf.Definitions, []),
    ],
)
def test_validate_universe_do_not_raise_type_error(definition):
    try:
        definition()
    except TypeError as e:
        assert False, str(e)
    else:
        assert True
