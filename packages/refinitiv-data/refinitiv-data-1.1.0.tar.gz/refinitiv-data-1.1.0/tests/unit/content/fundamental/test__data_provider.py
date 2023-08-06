from unittest.mock import patch, MagicMock

import pytest

from refinitiv.data.content.fundamental_and_reference._data_provider import (
    DataGridRDPRequestFactory,
    DataGridUDFRequestFactory,
    DataGridRDPResponseFactory,
    DataGridUDFResponseFactory,
    DataGridRDPContentValidator,
    DataGridUDFContentValidator,
    validate_correct_format_parameters,
)
from refinitiv.data.delivery._data._data_provider import ParsedData
from refinitiv.data.delivery._data._endpoint_data import Error, RequestMethod
from tests.unit.conftest import StubSession, kwargs
from .conftest import (
    ExpectedArgs,
    side_effect_func,
    PATH_MOCK_FUNC,
)


@patch(PATH_MOCK_FUNC, return_value={})
def tests_data_grid_rdp_request_factory_get_body_parameters(mock_func):
    # given
    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_body_parameters()

    # then
    assert testing_value == {}


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_rdp_request_factory_get_body_parameters_pass_universe(mock_func):
    # given
    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_body_parameters(universe="universe")

    # then
    assert testing_value["universe"] is not None


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_rdp_request_factory_get_body_parameters_pass_fields(mock_func):
    # given
    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_body_parameters(fields="fields")

    # then
    assert testing_value["fields"] is not None


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_rdp_request_factory_get_body_parameters_pass_parameters(mock_func):
    # given
    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_body_parameters(parameters="parameters")

    # then
    assert testing_value["parameters"] is not None


@patch(PATH_MOCK_FUNC)
def tests_data_grid_rdp_request_factory_get_body_parameters_pass_output(mock_func):
    # given
    output = {"layout": {"output": ...}}
    mock_func.return_value = output

    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_body_parameters(output=output)

    # then
    assert testing_value["output"] is not None


@pytest.mark.parametrize(
    "input_layout",
    [
        {"layout": ...},
        {"layout": {"out": ...}},
        {"layout": {"output": None}},
        {"layout": {"output": ""}},
        {"layout": {"output": []}},
        {"layout": {"output": set()}},
        {"layout": {"output": {}}},
    ],
)
@patch(PATH_MOCK_FUNC)
def tests_data_grid_rdp_request_factory_get_body_parameters_fail_output(
    mock_func, input_layout
):
    # given
    mock_func.return_value = input_layout

    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_body_parameters(layout=input_layout)

    # then
    assert "output" not in testing_value


def tests_data_grid_rdp_request_factory_get_request_method():
    # given
    factory = DataGridRDPRequestFactory()

    # when
    testing_value = factory.get_request_method()

    # then
    assert testing_value == RequestMethod.POST


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_udf_request_factory_get_body_parameters_pass_instruments(mock_func):
    # given
    factory = DataGridUDFRequestFactory()

    # when
    testing_value = factory.get_body_parameters(universe="instruments")

    # then
    assert testing_value["instruments"] is not None


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_udf_request_factory_get_body_parameters_pass_fields(mock_func):
    # given
    factory = DataGridUDFRequestFactory()

    # when
    testing_value = factory.get_body_parameters(fields="fields")

    # then
    assert testing_value["fields"] is not None


@patch(PATH_MOCK_FUNC)
def tests_data_grid_udf_request_factory_get_body_parameters_pass_layout(mock_func):
    # given
    layout = {"layout": {"layout": ...}}
    mock_func.return_value = layout

    factory = DataGridUDFRequestFactory()

    # when
    testing_value = factory.get_body_parameters(layout=layout)

    # then
    assert testing_value["layout"] is not None


@pytest.mark.parametrize(
    "input_layout",
    [
        {"layout": ...},
        {"layout": {"a": ...}},
        {"layout": {"layout": None}},
        {"layout": {"layout": ""}},
        {"layout": {"layout": []}},
        {"layout": {"layout": set()}},
        {"layout": {"layout": {}}},
    ],
)
@patch(PATH_MOCK_FUNC)
def tests_data_grid_udf_request_factory_get_body_parameters_fail_layout(
    mock_func, input_layout
):
    # given
    mock_func.return_value = input_layout

    factory = DataGridUDFRequestFactory()

    # when
    testing_value = factory.get_body_parameters(layout=input_layout)

    # then
    assert "layout" not in testing_value


@patch(PATH_MOCK_FUNC)
def tests_data_grid_udf_request_factory_get_body_parameters_skip_tr_fields(mock_func):
    # given
    factory = DataGridUDFRequestFactory()
    input_fields = ["TR.PriceClose", "TR.Volume", "TR.PriceLow", "BID", "ASK"]
    expected_fields = [
        {"name": "TR.PriceClose"},
        {"name": "TR.Volume"},
        {"name": "TR.PriceLow"},
    ]
    mock_func.return_value = {
        "fields": input_fields,
        "expected_fields": expected_fields,
    }

    # when
    testing_value = factory.get_body_parameters(fields=input_fields)

    # then
    assert testing_value["fields"] == expected_fields


@patch(PATH_MOCK_FUNC)
def tests_data_grid_udf_request_factory_get_body_parameters_add_tr_and_func_fields(
    mock_func,
):
    # given
    factory = DataGridUDFRequestFactory()
    input_fields = [
        "TR.PriceClose",
        "TR.Volume",
        "tR.PriceLow",
        "BID",
        "ASK",
        "Tr.PeersRank",
        "tr.RIC",
        "AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum)/TR.TotalRevenue(Period=LTM,Methodology=InterimSum),TR.GrossProfit(Period=FY0)/TR.TotalRevenue(Period=FY0))*100",
    ]
    expected_fields = [
        {"name": "TR.PriceClose"},
        {"name": "TR.Volume"},
        {"name": "tR.PriceLow"},
        {"name": "Tr.PeersRank"},
        {"name": "tr.RIC"},
        {
            "name": "AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum)/TR.TotalRevenue(Period=LTM,Methodology=InterimSum),TR.GrossProfit(Period=FY0)/TR.TotalRevenue(Period=FY0))*100"
        },
    ]
    mock_func.return_value = {
        "fields": input_fields,
        "expected_fields": expected_fields,
    }

    # when
    testing_value = factory.get_body_parameters(fields=input_fields)

    # then
    assert testing_value["fields"] == expected_fields


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_udf_request_factory_get_body_parameters_pass_parameters(mock_func):
    # given
    factory = DataGridUDFRequestFactory()

    # when
    testing_value = factory.get_body_parameters(parameters="parameters")

    # then
    assert testing_value["parameters"] is not None


def tests_data_grid_udf_request_factory_get_request_method():
    # given
    factory = DataGridUDFRequestFactory()

    # when
    testing_value = factory.get_request_method()

    # then
    assert testing_value == RequestMethod.POST


@patch(PATH_MOCK_FUNC, return_value=MagicMock(side_effect=side_effect_func))
def tests_data_grid_udf_request_factory_create(mock_func):
    # given
    factory = DataGridUDFRequestFactory()
    session = StubSession(is_open=True)

    # when
    data = factory.create(session)

    # then
    assert data is not None


def test_data_grid_udf_response_factory_create_success():
    # given
    data = ParsedData({}, {}, **{"content_data": {"responses": [{}]}})
    response_factory = DataGridUDFResponseFactory()

    # when
    result = response_factory.create_success(data)

    # then
    assert hasattr(result, "data")
    assert result.data.raw == data.content_data["responses"][0]


@pytest.mark.parametrize(
    "data,kwargs,error_code, error_message",
    [
        (
            ({"error_codes": 412}),
            {"universe": ["INVALID"], "fields": ["TR.Volume"]},
            412,
            "Unable to resolve all requested identifiers in ['INVALID'].",
        ),
        (
            ({"error_codes": 218}),
            {"universe": "IBM.N", "fields": ["TR.Volumeee"]},
            218,
            "Unable to resolve all requested fields in ['TR.Volumeee']. "
            "The formula must contain at least one field or function.",
        ),
        (
            ({"error_codes": 101010, "error_messages": "It's error message"}),
            {"universe": ["IBM.N"], "fields": ["TR.Volume"]},
            101010,
            "It's error message Requested universes: ['IBM.N']. "
            "Requested fields: ['TR.Volume']",
        ),
    ],
)
def test_data_grid_udf_response_factory_create_fail(
    data, kwargs, error_code, error_message
):
    parsed_data = ParsedData({}, {}, **data)
    response_factory = DataGridUDFResponseFactory()
    result = response_factory.create_fail(parsed_data, **kwargs)

    assert hasattr(result, "errors")
    assert isinstance(result.errors[0], Error)
    assert result.errors[0][0] == error_code
    assert result.errors[0][1] == error_message


def test_data_grid_udf_response_factory_create_success_with_err():
    data = ParsedData(
        {},
        {},
        **{
            "content_data": {
                "responses": [
                    {
                        "error": [
                            {
                                "code": 416,
                                "col": 2,
                                "message": "Unable to collect data for the field "
                                "'TR.Volume' and some specific identifier(s).",
                                "row": 1,
                            }
                        ]
                    }
                ]
            }
        },
    )
    expected_result = [
        (
            416,
            "Unable to collect data for the field 'TR.Volume' "
            "and some specific identifier(s).",
        )
    ]
    response_factory = DataGridUDFResponseFactory()
    result = response_factory.create_success(data)
    assert result.errors == expected_result


def test_data_grid_rdp_response_factory_create_success():
    # given
    data = ParsedData({}, {}, {"messages": {"descriptions": ""}})
    response_factory = DataGridRDPResponseFactory()

    # when
    result = response_factory.create_success(data)

    # then
    assert hasattr(result, "data")
    assert result.data.raw == data.content_data


def test_data_grid_rdp_response_factory_create_success_with_err():
    data = ParsedData(
        {},
        {},
        {
            "messages": {
                "descriptions": [
                    {
                        "code": 416,
                        "description": "Unable to collect data for the field "
                        "'TR.Volume' and some specific identifier(s).",
                    }
                ]
            }
        },
    )
    expected_result = [
        (
            416,
            "Unable to collect data for the field 'TR.Volume' "
            "and some specific identifier(s).",
        )
    ]
    response_factory = DataGridRDPResponseFactory()
    result = response_factory.create_success(data)
    assert result.errors == expected_result


@pytest.mark.parametrize(
    "data,kwargs,error_code, error_message",
    [
        (
            ({"error_codes": 412}),
            {"universe": ["INVALID"], "fields": ["TR.Volume"]},
            412,
            "Unable to resolve all requested identifiers in ['INVALID'].",
        ),
        (
            ({"error_codes": 218}),
            {"universe": "IBM.N", "fields": ["TR.Volumeee"]},
            218,
            "Unable to resolve all requested fields in ['TR.Volumeee']. "
            "The formula must contain at least one field or function.",
        ),
        (
            ({"error_codes": 101010, "error_messages": "It's error message"}),
            {"universe": ["IBM.N"], "fields": ["TR.Volume"]},
            101010,
            "It's error message Requested universes: ['IBM.N']. "
            "Requested fields: ['TR.Volume']",
        ),
    ],
)
def test_data_grid_rdp_response_factory_create_fail(
    data, kwargs, error_code, error_message
):
    parsed_data = ParsedData({}, {}, **data)
    response_factory = DataGridRDPResponseFactory()
    result = response_factory.create_fail(parsed_data, **kwargs)

    assert hasattr(result, "errors")
    assert isinstance(result.errors[0], Error)
    assert result.errors[0][0] == error_code
    assert result.errors[0][1] == error_message


@pytest.mark.parametrize(
    "input_kwargs, expected_values",
    [
        (
            kwargs(universe="", fields=""),
            ExpectedArgs(universe=[""], fields=[""]),
        ),
        (
            kwargs(universe="DD", fields=""),
            ExpectedArgs(universe=["DD"], fields=[""]),
        ),
        (
            kwargs(universe="dd", fields=""),
            ExpectedArgs(universe=["DD"], fields=[""]),
        ),
        (
            kwargs(universe=["dd"], fields=""),
            ExpectedArgs(universe=["DD"], fields=[""]),
        ),
        (
            kwargs(universe=["dd"], fields="ss"),
            ExpectedArgs(universe=["DD"], fields=["ss"]),
        ),
        (
            kwargs(universe=["dd"], fields=["ss"]),
            ExpectedArgs(universe=["DD"], fields=["ss"]),
        ),
    ],
)
def test_validate_correct_format_parameters_args_universe_and_fields(
    input_kwargs, expected_values
):
    # when
    result = validate_correct_format_parameters(
        use_field_names_in_headers=False, **input_kwargs
    )

    # then
    assert result["universe"] == expected_values.universe
    assert result["fields"] == expected_values.fields


@pytest.mark.parametrize(
    "input_kwargs, expected_raise",
    [
        (kwargs(universe="", fields=""), ValueError),
        (kwargs(universe=1, fields=""), TypeError),
        (kwargs(universe={}, fields=""), TypeError),
        (kwargs(universe=[1, 2, 3], fields=""), ValueError),
        (kwargs(universe="", fields=1), TypeError),
        (kwargs(universe="", fields={}), TypeError),
        (kwargs(universe="", fields=[1, 2, 3]), ValueError),
        (kwargs(universe=["1", "2"], fields=["1", "2"]), ValueError),
        (kwargs(universe=["1"], fields=["1"], parameters=""), ValueError),
        (kwargs(universe=["1"], fields=["1"], parameters="d"), ValueError),
        (kwargs(universe=["1"], fields=["1"], parameters=[]), ValueError),
        (kwargs(universe=["1"], fields=["1"], parameters=[1]), ValueError),
        (kwargs(universe=["1"], fields=["1"], extended_params="1"), AttributeError),
        (kwargs(universe=["1"], fields=["1"], extended_params=[0]), AttributeError),
        (kwargs(universe=["1"], fields=["1"], extended_params=True), AttributeError),
        (
            kwargs(universe=["1"], fields=["1"], use_field_names_in_headers=""),
            ValueError,
        ),
        (
            kwargs(universe=["1"], fields=["1"], use_field_names_in_headers=" "),
            ValueError,
        ),
        (
            kwargs(universe=["1"], fields=["1"], use_field_names_in_headers=0),
            ValueError,
        ),
        (
            kwargs(universe=["1"], fields=["1"], use_field_names_in_headers=None),
            ValueError,
        ),
    ],
)
def test_validate_correct_format_parameters_raise_exception(
    input_kwargs, expected_raise
):
    # when
    with pytest.raises(expected_raise):
        validate_correct_format_parameters(**input_kwargs)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (None, {}),
        ("", {}),
        ([], {}),
        ({}, {}),
        ({"universe": ["1", "2"]}, {"universe": ["1", "2"]}),
    ],
)
def test_validate_correct_format_parameters_arg_extended_params(
    input_value, expected_value
):
    # when
    result = validate_correct_format_parameters(
        universe=["1"],
        fields=["1"],
        use_field_names_in_headers=False,
        extended_params=input_value,
    )

    # then
    assert result["extended_params"] == expected_value


@pytest.mark.parametrize(
    "input_value, expected_universe, expected_extended_params",
    [
        (None, ["1"], {}),
        ("", ["1"], {}),
        ({}, ["1"], {}),
        ({"universe": None}, ["1"], {"universe": None}),
        ({"universe": ""}, ["1"], {"universe": ""}),
        ({"universe": []}, ["1"], {"universe": []}),
        ({"universe": ["1", "2"]}, ["1", "2"], {"universe": ["1", "2"]}),
    ],
)
def test_validate_correct_format_parameters_swap_universe(
    input_value, expected_universe, expected_extended_params
):
    # when
    result = validate_correct_format_parameters(
        universe=["1"],
        fields=["1"],
        use_field_names_in_headers=False,
        extended_params=input_value,
    )

    # then
    assert result["universe"] == expected_universe
    assert result["extended_params"] == expected_extended_params


@pytest.mark.parametrize(
    "input_content_data",
    [
        None,
        {"error": {"a": "a"}, "data": []},
        {"error": {"description": "description"}, "data": []},
        {"error": {"code": 1, "description": "description"}, "data": []},
    ],
)
def test_data_grid_rdp_content_validator_validate_content_data_is_false(
    input_content_data,
):
    # given
    input_value = ParsedData({}, {}, **{"content_data": input_content_data})
    expected_value = False
    validator = DataGridRDPContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


def test_data_grid_rdp_content_validator_validate_content_is_false():
    # given
    input_value = ParsedData({"content": "Failed ..."}, {})
    expected_value = False
    validator = DataGridRDPContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_content_data",
    [
        {"status": {"code": "Error"}},
        {"status": {"code": "UserRequestError"}},
        {"error": {"code": 1, "description": "description"}, "data": [1, 2, 3]},
    ],
)
def test_data_grid_rdp_content_validator_validate_content_data_is_true(
    input_content_data,
):
    # given
    input_value = ParsedData({}, {}, input_content_data)
    expected_value = True
    validator = DataGridRDPContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_content_data",
    [
        {},
        {"ErrorCode": 1, "ErrorMessage": "ErrorMessage"},
        {"responses": [{"error": "error"}]},
        {"responses": [{"error": "error", "data": ""}]},
        {"responses": [{"error": "error", "data": []}]},
        {"responses": [{"error": {"code": "code"}}]},
        {"responses": [{"error": {"code": "code", "message": "message"}}]},
        {"responses": [{"error": {"code": "code", "message": "message"}, "data": ""}]},
        {"responses": [{"error": {"code": "code", "message": "message"}, "data": []}]},
    ],
)
def test_data_grid_udf_content_validator_validate_content_data_is_false(
    input_content_data,
):
    # given
    input_value = {"status": {}, "content_data": input_content_data}
    expected_value = False
    validator = DataGridUDFContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


def test_data_grid_udf_content_validator_validate_content_is_false():
    # given
    input_value = ParsedData({"content": "Failed ..."}, {})
    expected_value = False
    validator = DataGridUDFContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_content_data",
    [
        {"responses": [{"data": [1]}]},
    ],
)
def test_data_grid_udf_content_validator_validate_content_data_is_true(
    input_content_data,
):
    # given
    input_value = ParsedData({}, {}, input_content_data)
    expected_value = True
    validator = DataGridUDFContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value",
    [
        {"status": {}, "raw_response": {}},
        {"status": {"content": "Failed"}, "raw_response": {}},
        {"status": {}, "raw_response": {}, "content_data": "ErrorCode"},
        {"status": {}, "raw_response": {}, "content_data": {"ErrorCode": ...}},
        {
            "status": {},
            "raw_response": {},
            "content_data": {
                "responses": [{"error": {"code": "code", "message": "message"}}]
            },
        },
        {
            "status": {},
            "raw_response": {},
            "content_data": {
                "responses": [
                    {"error": {"code": "code", "message": "message"}, "data": None}
                ]
            },
        },
        {
            "status": {},
            "raw_response": {},
            "content_data": {
                "responses": [
                    {"error": {"code": "code", "message": "message"}, "data": ""}
                ]
            },
        },
        {
            "status": {},
            "raw_response": {},
            "content_data": {
                "responses": [
                    {"error": {"code": "code", "message": "message"}, "data": []}
                ]
            },
        },
        {
            "status": {},
            "raw_response": {},
            "content_data": {
                "responses": [
                    {
                        "error": [{"code": "code", "message": "message"}],
                        "data": [1],
                        "headers": [[{"displayName": None}]],
                    }
                ]
            },
        },
    ],
)
def test_data_grid_udf_content_validator_validate_content_data_is_false(input_value):
    # given
    expected_value = False
    validator = DataGridUDFContentValidator()

    # when
    parsed_data = ParsedData(**input_value)
    testing_value = validator.validate(parsed_data)

    # then
    assert testing_value == expected_value


def test_data_grid_udf_content_validator_validate_content_data_is_str():
    # given
    input_value = ParsedData({}, {}, **{"content_data": "some text html"})
    expected_value = False
    validator = DataGridUDFContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value
    assert input_value.first_error_message == input_value.content_data
