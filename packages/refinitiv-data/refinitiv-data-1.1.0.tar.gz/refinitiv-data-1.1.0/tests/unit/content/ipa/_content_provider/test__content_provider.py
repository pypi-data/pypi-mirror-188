import numpy as np
import pandas as pd
import pytest

from refinitiv.data.content.ipa._content_provider import (
    CurvesAndSurfacesRequestFactory,
    value_arg_parser,
    parse_value,
    CrossCurrencyCurvesDefinitionsRequestFactory,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._delete import (
    DeleteRequest,
)
from refinitiv.data.delivery._data._endpoint_data import RequestMethod
from .conftest import StubInstrument, StubOutputs
from ...conftest import StubDefinition


def tests_curves_and_surfaces_request_factory_get_request_method_return_post():
    # given
    expected_value = RequestMethod.POST
    factory = CurvesAndSurfacesRequestFactory()

    # when
    testing_value = factory.get_request_method()

    # then
    assert testing_value == expected_value


def tests_curves_and_surfaces_request_factory_get_body_parameters():
    # given
    factory = CurvesAndSurfacesRequestFactory()

    # when
    testing_value = factory.get_body_parameters(universe=StubDefinition())

    # then
    assert testing_value["universe"] is not None


def tests_cross_currency_curves_definitions_request_factory_get_body_parameters():
    # given
    factory = CrossCurrencyCurvesDefinitionsRequestFactory()

    # when
    testing_value = factory.get_body_parameters(request_items=DeleteRequest(id="42"))

    # then
    assert testing_value == {"id": "42"}


@pytest.mark.parametrize(
    "input_arg",
    [
        None,
        [],
        1,
        0,
        "",
        "dd",
        {},
        [4, 5],
        {"id": 45},
    ],
)
def tests_cross_currency_curves_definitions_request_factory_get_body_parameters_not_valid_arg(
    input_arg,
):
    # given
    factory = CrossCurrencyCurvesDefinitionsRequestFactory()

    # when
    testing_value = factory.get_body_parameters(request_items=input_arg)

    # then
    assert testing_value == {}


def tests_cross_currency_curves_definitions_request_factory_extend_body_parameters():
    # given
    factory = CrossCurrencyCurvesDefinitionsRequestFactory()

    # when
    testing_value = factory.extend_body_parameters(
        body_parameters={"id": 10}, extended_params={"id": 42}
    )

    # then
    assert testing_value == {"id": 42}


def tests_curves_and_surfaces_request_factory_get_body_parameters_pass_instrument():
    # given
    instrument = StubInstrument()
    factory = CurvesAndSurfacesRequestFactory()

    # when
    testing_value = factory.get_body_parameters(universe=instrument)

    # then
    assert testing_value["universe"] is not None


def tests_curves_and_surfaces_request_factory_get_body_parameters_pass_instrument_with_request_item():
    # given
    instrument = StubInstrument()
    instrument._request_item = StubInstrument()
    factory = CurvesAndSurfacesRequestFactory()

    # when
    testing_value = factory.get_body_parameters(universe=instrument)

    # then
    assert testing_value["universe"] is not None


def tests_curves_and_surfaces_request_factory_get_body_parameters_pass_outputs():
    # given
    factory = CurvesAndSurfacesRequestFactory()

    # when
    testing_value = factory.get_body_parameters(
        outputs="outputs", universe=StubDefinition()
    )

    # then
    assert testing_value["outputs"] is not None


def tests_curves_and_surfaces_request_factory_get_body_parameters_pass_outputs_as_enum():
    # given
    factory = CurvesAndSurfacesRequestFactory()

    # when
    testing_value = factory.get_body_parameters(
        outputs=StubOutputs.OUTPUTS, universe=StubDefinition()
    )

    # then
    assert testing_value["outputs"] is not None


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (1, 1),
        ("1", 1),
        (1629099184, 1629099184),
        ("1629099184", 1629099184),
        ("1.01", 1.01),
        (1.01, 1.01),
        ("2021-08-20", np.datetime64("2021-08-20")),
        (np.datetime64("2021-08-20"), np.datetime64("2021-08-20")),
    ],
)
def test_value_arg_parser_successfully(input_value, expected_value):
    # given
    value = value_arg_parser.parse(input_value)

    # then
    assert value == expected_value


def test_value_arg_parser_fail():
    # given
    value = value_arg_parser.parse("")

    # then
    assert pd.isnull(value)


@pytest.mark.parametrize("input_value", [" ", "aaa", "2021-08-20Z147"])
def test_value_arg_parser_try_except(input_value):
    # then
    with pytest.raises(ValueError):
        value_arg_parser.parse(input_value)


@pytest.mark.parametrize(
    ("test_value",),
    [
        ("2018-15-10",),
        ("2018-10-15",),
        ("2018-10-10",),
    ],
)
def test_parse_value(test_value):
    # given
    try:
        # when
        # then
        parse_value(test_value)
    except Exception as e:
        pytest.fail("Unexpected exception", str(e))
