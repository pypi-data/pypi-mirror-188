import mock
import pytest

from refinitiv.data.content._universe_content_validator import UniverseContentValidator
from refinitiv.data.content.ownership._enums import (
    StatTypes,
    Frequency,
    SortOrder,
)
from refinitiv.data.content.ownership._ownership_data_provider import (
    OwnershipRequestFactory,
)
from refinitiv.data.delivery._data._data_provider import ParsedData


@pytest.mark.parametrize(
    ("input_value", "test_result"),
    [
        ({"universe": "test_value"}, [("universe", "test_value")]),
        (
            {"universe": "test_value", "stat_type": 1},
            [("universe", "test_value"), ("statType", "1")],
        ),
        (
            {"universe": "test_value", "stat_type": StatTypes.INVESTOR_TYPE},
            [("universe", "test_value"), ("statType", "1")],
        ),
        (
            {"universe": "test_value", "offset": "test_value"},
            [("universe", "test_value"), ("offset", "test_value")],
        ),
        (
            {"universe": "test_value", "limit": "test_value"},
            [("universe", "test_value"), ("limit", "test_value")],
        ),
        (
            {"universe": "test_value", "sort_order": "asc"},
            [("universe", "test_value"), ("sortOrder", "asc")],
        ),
        (
            {"universe": "test_value", "sort_order": SortOrder.ASCENDING},
            [("universe", "test_value"), ("sortOrder", "asc")],
        ),
        (
            {"universe": "test_value", "frequency": "M"},
            [("universe", "test_value"), ("frequency", "M")],
        ),
        (
            {"universe": "test_value", "frequency": Frequency.MONTHLY},
            [("universe", "test_value"), ("frequency", "M")],
        ),
        (
            {"universe": "test_value", "count": "test_value"},
            [("universe", "test_value"), ("count", "test_value")],
        ),
        (
            {"universe": "test_value", "start": "1Q"},
            [("universe", "test_value"), ("start", "1Q")],
        ),
        (
            {"universe": "test_value", "end": "1Q"},
            [("universe", "test_value"), ("end", "1Q")],
        ),
        (
            {"universe": "test_value", "end": None},
            [
                ("universe", "test_value"),
            ],
        ),
        (
            {"universe": "test_value", "start": "12.10.2021"},
            [("universe", "test_value"), ("start", "20211210")],
        ),
        (
            {"universe": "test_value", "end": "12/11/2020"},
            [("universe", "test_value"), ("end", "20201211")],
        ),
    ],
)
def test_ownership_request_factory_get_query_params(input_value, test_result):
    # given
    request_factory = OwnershipRequestFactory()

    # when
    result = request_factory.get_query_parameters(**input_value)

    # then
    assert result == test_result


def test_ownership_request_factory_get_query_params_with_duplicate_universe():
    # given
    request_factory = OwnershipRequestFactory()
    input_universe = ["test_value", "testt_value", "test_value"]
    expected_results = ["test_value,testt_value", "testt_value,test_value"]

    # when
    result = request_factory.get_query_parameters(universe=input_universe)

    # then
    assert dict(result)["universe"] in expected_results, result


@pytest.mark.parametrize(
    ("input_query_parameters", "input_extended_params", "test_result"),
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
def test_ownership_request_factory_extend_query_params(
    input_query_parameters, input_extended_params, test_result
):
    # given
    request_factory = OwnershipRequestFactory()

    # when
    result = request_factory.extend_query_parameters(
        input_query_parameters, input_extended_params
    )

    # then
    assert result == test_result


@pytest.mark.parametrize(
    ("input_data", "test_result"),
    [
        ({"content_data": {}}, True),
        ({"content_data": {"error": {"code": "", "description": ""}}}, False),
    ],
)
def test_ownership_validator(input_data, test_result):
    # given
    # when
    validator = UniverseContentValidator()
    result = validator.validate(ParsedData({}, {}, **input_data))

    # then
    assert result == test_result
