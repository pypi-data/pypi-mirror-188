import pytest
from refinitiv.data.content.historical_pricing import events

from refinitiv.data.content import custom_instruments
from tests.unit.conftest import StubSession, args, StubResponse
from . import data_for_tests as td


@pytest.mark.parametrize(
    "input_kwargs, mock_response",
    [
        args(
            input_kwargs={
                "universe": [
                    "S)Batman_9ccfafd6.GESG1-111923",
                ],
            },
            response=td.ONE_UNIVERSE,
        ),
        args(
            input_kwargs={
                "universe": [
                    "S)Batman_9ccfafd6.GESG1-111923",
                ],
                "count": 13000,
            },
            response=td.ONE_UNIVERSE_WITH_TWO_REQUESTS,
        ),
        args(
            input_kwargs={
                "universe": [
                    "S)Batman_9ccfafd6.GESG1-111923",
                    "S)invalid_cust_universe",
                ],
            },
            response=td.TWO_UNIVERSES_ONE_FAILED,
        ),
        args(
            input_kwargs={
                "universe": [
                    "S)Batman_9ccfafd6.GESG1-111923",
                    "S)Batman_3b9a8a02.GESG1-111923",
                ],
            },
            response=td.TWO_UNIVERSES,
        ),
    ],
)
def test_nested_attributes_type_for_response(input_kwargs, mock_response):
    # given
    session = StubSession(is_open=True, response=mock_response)
    definition = custom_instruments.events.Definition(**input_kwargs)

    # when
    testing_response = definition.get_data(session=session)

    # then
    assert isinstance(testing_response.http_status, list)
    assert isinstance(testing_response.http_headers, list)
    assert isinstance(testing_response.request_message, list)
    assert isinstance(testing_response.http_response, list)

    assert all(isinstance(i, list) for i in testing_response.http_status)
    assert all(isinstance(i, list) for i in testing_response.http_headers)
    assert all(isinstance(i, list) for i in testing_response.request_message)
    assert all(isinstance(i, list) for i in testing_response.http_response)


@pytest.mark.asyncio
async def test_get_data_async_df_return_empty_dataframe_if_universe_is_not_found():
    # given
    mock_response = StubResponse(
        [
            {
                "universe": {"ric": "INVALID"},
                "status": {
                    "code": "TS.Intraday.UserRequestError.90001",
                    "message": "The universe is not found.",
                },
            }
        ]
    )
    session = StubSession(is_open=True, response=mock_response)

    # when
    definition = events.Definition("INVALID")
    invalid_response = await definition.get_data_async(session=session)

    # then
    assert invalid_response.data.df.empty is True
