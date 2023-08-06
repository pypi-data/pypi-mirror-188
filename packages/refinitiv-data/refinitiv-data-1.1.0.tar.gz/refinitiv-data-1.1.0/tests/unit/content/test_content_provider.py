import json
from types import SimpleNamespace

import pandas as pd
import pytest
from pandas import DataFrame

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._content_data import Data
from refinitiv.data.content._df_build_type import DFBuildType
from refinitiv.data.content._df_builder_factory import get_dfbuilder
from refinitiv.data.content._historical_data_provider import (
    HistoricalDataProvider,
    copy_fields,
)
from refinitiv.data.content._join_responses import join_responses
from refinitiv.data.content._universe_content_validator import (
    UniverseContentValidator,
)
from refinitiv.data.delivery._data._data_provider import (
    ResponseFactory,
    ParsedData,
    Response,
)
from tests.unit.conftest import StubResponse


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
        (
            {
                "content_data": {
                    "error": {
                        "message": "error_message",
                        "errors": ["message1", "message2"],
                    }
                }
            },
            False,
            {
                "status": {},
                "raw_response": {},
                "content_data": {
                    "error": {
                        "message": "error_message",
                        "errors": ["message1", "message2"],
                    }
                },
                "error_codes": [None],
                "error_messages": ["error_message:\nmessage1\nmessage2"],
            },
        ),
        (
            {
                "content_data": {
                    "universe": [
                        {
                            "Instrument": "invalid",
                            "Organization PermID": "Failed to resolve identifier(s).",
                        }
                    ]
                }
            },
            True,
            {
                "status": {},
                "raw_response": {},
                "content_data": {
                    "universe": [
                        {
                            "Instrument": "invalid",
                            "Organization PermID": "Failed to resolve identifier(s).",
                        }
                    ]
                },
                "error_codes": [],
                "error_messages": ["Failed to resolve identifiers ['invalid']"],
            },
        ),
    ],
)
def test_content_validator(input_data, expected_result, expected_data):
    # given
    content_validator = UniverseContentValidator()

    # when
    parsed_data = ParsedData({}, {}, **input_data)
    is_valid = content_validator.validate(parsed_data)

    # then
    assert is_valid == expected_result
    assert parsed_data == expected_data


def test_content_validator_unable_to_resolve_all_requested_identifiers():
    # given
    content_validator = UniverseContentValidator()
    universe = '{"url":{"params": {}}}'
    universe = json.loads(universe, object_hook=lambda d: SimpleNamespace(**d))
    universe_data = {"universe": "A,B,C"}
    universe.url.params = universe_data
    data = ParsedData(
        {},
        **{
            "content_data": {
                "error": {
                    "code": 400,
                    "description": "Unable to resolve all requested identifiers.",
                }
            },
            "raw_response": universe,
        },
    )

    # when
    is_valid = content_validator.validate(data)

    # then
    assert not is_valid
    assert data.first_error_code == 400
    assert (
        data.first_error_message
        == f"Unable to resolve all requested identifiers. Requested items: {universe_data['universe'].split(',')}"
    )


@pytest.mark.parametrize(
    ("input_value", "expected_result"),
    [
        (
            {
                "raw": {
                    "headers": [{"name": "name", "title": "title"}],
                    "data": [[1], [2]],
                },
                "use_field_names_in_headers": True,
                "dfbuilder": get_dfbuilder(
                    ContentType.DATA_GRID_RDP, DFBuildType.INDEX
                ),
            },
            (["name"], 2),
        ),
        (
            {
                "raw": {
                    "headers": [{"name": "name", "title": "title"}],
                    "data": [[1], [2]],
                },
                "use_field_names_in_headers": False,
                "dfbuilder": get_dfbuilder(
                    ContentType.DATA_GRID_RDP, DFBuildType.INDEX
                ),
            },
            (["title"], 2),
        ),
        (
            {
                "raw": {
                    "headers": [{"name": "name", "title": "title"}],
                    "data": [[1], [2]],
                },
                "use_field_names_in_headers": False,
                "dfbuilder": get_dfbuilder(
                    ContentType.DATA_GRID_RDP, DFBuildType.INDEX
                ),
            },
            (["title"], 2),
        ),
    ],
)
def test_universe_data(input_value, expected_result):
    # given
    data_class = Data(**input_value)

    # when
    df = data_class.df

    # then
    # header name
    assert list(df) == expected_result[0]
    # size
    assert df.size == expected_result[1]


@pytest.mark.parametrize(
    ("input_value", "expected_result"),
    [
        (
            {
                "raw": {},
                "use_field_names_in_headers": False,
                "dfbuilder": get_dfbuilder(
                    ContentType.DATA_GRID_RDP, DFBuildType.INDEX
                ),
            },
            DataFrame(),
        ),
        (
            {
                "raw": {},
                "use_field_names_in_headers": True,
                "dfbuilder": get_dfbuilder(
                    ContentType.DATA_GRID_RDP, DFBuildType.INDEX
                ),
            },
            DataFrame(),
        ),
    ],
)
def test_universe_data_none(input_value, expected_result):
    # given
    data = Data(**input_value)

    # when
    df = data.df

    # then
    diff = df.compare(expected_result)
    assert diff.empty is True


@pytest.mark.parametrize(
    "input_value",
    [
        {
            # no headers
            "raw": {"data": []},
            "use_field_names_in_headers": True,
            "dfbuilder": get_dfbuilder(ContentType.DATA_GRID_RDP, DFBuildType.INDEX),
        },
        {
            # no data
            "raw": {"headers": []},
            "use_field_names_in_headers": True,
            "dfbuilder": get_dfbuilder(ContentType.DATA_GRID_RDP, DFBuildType.INDEX),
        },
    ],
)
def test_universe_data_empty_dataframe(input_value):
    # given
    data_class = Data(**input_value)

    # when
    df = data_class.df

    # then
    assert df.empty


def test_universe_response_factory_create_success():
    # given
    data = ParsedData({}, {}, **{"content_data": {"test": ""}})
    response_factory = ResponseFactory()

    # when
    result = response_factory.create_success(data)

    # then
    assert hasattr(result, "data")
    assert result.data.raw == data.content_data


def test_universe_response_factory_create_fail():
    # given
    data = ParsedData({}, {}, {"content_data": {"test": ""}})
    response_factory = ResponseFactory()

    # when
    result = response_factory.create_fail(data)

    # then
    assert hasattr(result, "data")
    assert result.data.raw == data.content_data


@pytest.mark.parametrize(
    "input_responses, expected_raise",
    [
        ([(1, "")], AttributeError),
        ([("1", "")], AttributeError),
        ([("1", [])], AttributeError),
    ],
)
def test_historical_data_provider_join_responses_not_valid_response(
    input_responses, expected_raise
):
    historical_data_provider = HistoricalDataProvider()
    historical_data_provider._get_axis_name = lambda **kwargs: ""
    # when
    with pytest.raises(expected_raise):
        historical_data_provider._join_responses(
            input_responses,
            data=[],
        )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ({"fields": None}, []),
        ({"fields": []}, []),
    ],
)
def test_success_without_valid_get_fields(input_value, expected_value):
    # when
    result = copy_fields(**input_value)

    # then
    assert isinstance(result, list)
    assert len(result) == 0


def test_success_with_valid_input_arg_get_fields():
    # given
    expected_value = ["IBA"]
    input_value = {"fields": expected_value}

    # when
    result = copy_fields(**input_value)

    # then
    assert isinstance(result, list)
    assert result == expected_value
    assert result is not expected_value


@pytest.mark.parametrize(
    "input_value, expected_raise",
    [
        ({"fields": ()}, AttributeError),
    ],
)
def test_failed_get_fields(input_value, expected_raise):
    # when
    with pytest.raises(expected_raise):
        copy_fields(**input_value)


def test__join_responses():
    # given
    http_statuses = [
        {"code": 200, "message": "status1"},
        {"code": 300, "message": "status2"},
    ]

    http_headers = ["header1", "header2"]
    request_messages = [0, 1]
    http_responses = [0, 1]

    response1 = StubResponse()
    response2 = StubResponse()

    response1.is_success = True
    response2.is_success = True

    response1.http_status = http_statuses[0]
    response2.http_status = http_statuses[1]

    response1.http_headers = http_headers[0]
    response2.http_headers = http_headers[1]

    response1.request_message = request_messages[0]
    response2.request_message = request_messages[1]

    response1.http_response = http_responses[0]
    response2.http_response = http_responses[1]
    response1.errors = []
    response2.errors = []

    response1.data = Data({}, pd.DataFrame({}))
    response2.data = Data({}, pd.DataFrame({}))

    responses = [response1, response2]

    # when
    result = join_responses(responses)

    # then
    assert isinstance(result, Response)
    assert result.http_response == http_responses
    assert result.http_headers == http_headers
    assert result.http_status == http_statuses
    assert result.request_message == request_messages
