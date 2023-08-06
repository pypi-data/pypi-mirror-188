import pytest

from refinitiv.data.content._universe_content_validator import UniverseContentValidator
from refinitiv.data.content.estimates._enums import Package
from refinitiv.data.content.estimates._data_provider import (
    EstimatesRequestFactory,
)
from refinitiv.data.delivery._data._data_provider import ParsedData


@pytest.mark.parametrize(
    ("input_value", "expected_result"),
    [
        ({"universe": "test_value"}, [("universe", "test_value")]),
        (
            {"universe": "test_value", "package": Package.BASIC},
            [("universe", "test_value"), ("package", "basic")],
        ),
        (
            {"universe": "test_value", "package": Package.STANDARD},
            [("universe", "test_value"), ("package", "standard")],
        ),
        (
            {"universe": "test_value", "package": Package.PROFESSIONAL},
            [("universe", "test_value"), ("package", "professional")],
        ),
        (
            {"universe": ["test_value1", "test_value2"]},
            [("universe", "test_value1,test_value2")],
        ),
        (
            {"universe": "test_value", "other_field": "value"},
            [("universe", "test_value")],
        ),
    ],
)
def test_estimates_request_factory_get_query_parameters(input_value, expected_result):
    # given
    request_factory = EstimatesRequestFactory()

    # when
    result = request_factory.get_query_parameters(**input_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("input_query_parameters", "input_extended_params", "expected_result"),
    [
        ([], {"universe": "test_value"}, [("universe", "test_value")]),
        (
            [("universe", "test_value")],
            {"universe": "new_value"},
            [("universe", "new_value")],
        ),
        (
            [("universe", "test_value")],
            {"universe1": "new_value"},
            [("universe", "test_value"), ("universe1", "new_value")],
        ),
    ],
)
def test_estimates_request_factory_extend_query_params(
    input_query_parameters, input_extended_params, expected_result
):
    # given
    request_factory = EstimatesRequestFactory()

    # when
    result = request_factory.extend_query_parameters(
        input_query_parameters, input_extended_params
    )

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("input_data", "expected_result", "expected_data"),
    [
        (
            {"content_data": {"data": "data"}},
            True,
            {
                "status": {},
                "raw_response": {},
                "content_data": {"data": "data"},
                "error_codes": [],
                "error_messages": [],
            },
        ),
        (
            {"content_data": None},
            False,
            {
                "status": {},
                "raw_response": {},
                "content_data": None,
                "error_codes": [1],
                "error_messages": ["Content data is None"],
            },
        ),
        (
            {"content_data": {"error": {"code": 500, "description": "error_desc"}}},
            False,
            {
                "status": {},
                "raw_response": {},
                "content_data": {"error": {"code": 500, "description": "error_desc"}},
                "error_codes": [500],
                "error_messages": ["error_desc"],
            },
        ),
        (
            {"content_data": {"error": {"message": "error_message"}}},
            False,
            {
                "status": {},
                "raw_response": {},
                "content_data": {"error": {"message": "error_message"}},
                "error_codes": [None],
                "error_messages": ["error_message"],
            },
        ),
    ],
)
def test_estimates_content_validator(input_data, expected_result, expected_data):
    # given
    content_validator = UniverseContentValidator()

    # when
    parsed_data = ParsedData({}, {}, **input_data)
    is_valid = content_validator.validate(parsed_data)

    # then
    assert is_valid == expected_result
    assert parsed_data == expected_data
