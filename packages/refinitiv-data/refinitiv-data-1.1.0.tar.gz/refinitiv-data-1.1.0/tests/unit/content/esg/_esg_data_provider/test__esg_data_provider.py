from unittest import mock
import pytest

from refinitiv.data.content.esg._esg_data_provider import ErrorParser
from refinitiv.data.delivery._data._data_provider import ParsedData


@pytest.mark.parametrize(
    ("input_parsed_data", "test_result"),
    [
        (
            ParsedData({}, {}),
            {
                "status": {},
                "raw_response": {},
                "content_data": None,
                "error_codes": [],
                "error_messages": [],
            },
        ),
        (
            ParsedData(
                {"error": {"errors": [{"reason": "test reason"}]}},
                {},
                error_messages=["wrong message"],
            ),
            {
                "status": {"error": {"errors": [{"reason": "test reason"}]}},
                "raw_response": {},
                "content_data": None,
                "error_codes": [0],
                "error_messages": ["wrong message: test reason"],
            },
        ),
    ],
)
def test_esg_parser_process_failed_response(input_parsed_data, test_result):
    # given
    # when
    with mock.patch(
        "refinitiv.data.delivery._data._data_provider.Parser.process_failed_response"
    ) as mock_func:
        mock_func.return_value = input_parsed_data
        result = ErrorParser().process_failed_response(...)

    # then
    assert result == test_result
