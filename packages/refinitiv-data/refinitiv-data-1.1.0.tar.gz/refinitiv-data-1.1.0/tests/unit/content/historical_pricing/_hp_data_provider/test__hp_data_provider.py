import pytest
from pandas.core.dtypes.common import is_datetime64tz_dtype, is_datetime64_any_dtype

from refinitiv.data.content._historical_content_validator import (
    HistoricalContentValidator,
)
from refinitiv.data.content._historical_df_builder import HistoricalBuilder
from refinitiv.data.content._historical_response_factory import (
    HistoricalResponseFactory,
)
from refinitiv.data.content._intervals import Intervals
from refinitiv.data.content.historical_pricing import (
    EventTypes,
    Adjustments,
    MarketSession,
)
from refinitiv.data.content.historical_pricing._historical_pricing_request_factory import (
    HistoricalPricingSummariesRequestFactory,
    HistoricalPricingEventsRequestFactory,
    HistoricalPricingRequestFactory,
)

from refinitiv.data.delivery._data._data_provider import ParsedData
from refinitiv.data.delivery._data._endpoint_data import Error
from tests.unit.conftest import StubSession


def test_historical_pricing_summaries_request_factory_get_query_parameters():
    # given
    expected_value = [("interval", "P1D")]
    request_factory = HistoricalPricingSummariesRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters(interval=Intervals.DAILY)

    # then
    assert testing_value == expected_value


def test_historical_pricing_summaries_request_factory_get_query_parameters_without_pass_argument():
    # given
    expected_value = []
    request_factory = HistoricalPricingSummariesRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters()

    # then
    assert testing_value == expected_value


def test_historical_pricing_events_request_factory_get_query_parameters():
    # given
    expected_value = [("eventTypes", "quote")]
    request_factory = HistoricalPricingEventsRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters(event_types=EventTypes.QUOTE)

    # then
    assert testing_value == expected_value


def test_historical_pricing_events_request_factory_get_query_parameters_without_pass_argument():
    # given
    expected_value = []
    request_factory = HistoricalPricingEventsRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters()

    # then
    assert testing_value == expected_value


def test_historical_pricing_request_factory_get_url():
    # given
    input_value = "url"
    expected_value = "url/{universe}"
    request_factory = HistoricalPricingRequestFactory()

    # when
    testing_value = request_factory.get_url({}, input_value)

    # then
    assert testing_value == expected_value


def test_historical_pricing_request_factory_get_path_parameters():
    # given
    input_value = "universe"
    expected_value = {"universe": "universe"}
    request_factory = HistoricalPricingRequestFactory()

    # when
    session = StubSession()
    testing_value = request_factory.get_path_parameters(session, universe=input_value)

    # then
    assert testing_value == expected_value


def test_historical_pricing_summaries_request_factory_get_query_parameters_all():
    # given
    expected_value = [
        ("start", "2019-01-19T09:00:00.000000000Z"),
        ("end", "2019-01-24T17:00:00.000000000Z"),
        ("adjustments", "RPO"),
        ("sessions", "post"),
        ("count", 2),
        ("fields", "field_1,field_2,DATE"),
    ]
    request_factory = HistoricalPricingSummariesRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters(
        start="2019-01-19 09:00:00",
        end="2019-01-24 17:00:00",
        adjustments=Adjustments.RPO,
        sessions=MarketSession.POST,
        count=2,
        fields=["field_1", "field_2"],
    )

    # then
    assert testing_value == expected_value


def test_historical_pricing_events_request_factory_get_query_parameters_all():
    # given
    expected_value = [
        ("start", "2019-01-19T09:00:00.000000000Z"),
        ("end", "2019-01-24T17:00:00.000000000Z"),
        ("adjustments", "RPO"),
        ("count", 2),
        ("fields", "field_1,field_2,DATE_TIME"),
    ]
    request_factory = HistoricalPricingEventsRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters(
        start="2019-01-19 09:00:00",
        end="2019-01-24 17:00:00",
        adjustments=Adjustments.RPO,
        sessions=MarketSession.POST,
        count=2,
        fields=["field_1", "field_2"],
    )

    # then
    assert testing_value == expected_value


def test_historical_pricing_request_factory_extend_query_parameters():
    # given
    expected_value = [
        ("start", "2019-01-19T09:00:00.000000000Z"),
        ("end", "2019-01-24T17:00:00.000000000Z"),
        ("count", 2),
    ]
    request_factory = HistoricalPricingRequestFactory()

    # when
    testing_value = request_factory.extend_query_parameters(
        query_parameters=[],
        extended_params={
            "start": "2019-01-19T09:00:00",
            "end": "2019-01-24T17:00:00",
            "count": 2,
        },
    )

    # then
    assert testing_value == expected_value


def test_historical_pricing_request_factory_extend_body_parameters():
    # given
    request_factory = HistoricalPricingRequestFactory()

    # when
    testing_value = request_factory.extend_body_parameters(
        body_parameters={"a": 10}, extended_params={"count": 2}
    )

    # then
    assert testing_value is None


def test_historical_pricing_request_factory_get_query_parameters_raise_error_if_count_less_one():
    # given
    request_factory = HistoricalPricingSummariesRequestFactory()

    # then
    with pytest.raises(ValueError, match="Count minimum value is 1"):
        # when
        request_factory.get_query_parameters(count=-1)


def test_historical_pricing_request_factory_get_query_parameters_without_pass_arguments():
    # given
    expected_value = []
    request_factory = HistoricalPricingRequestFactory()

    # when
    testing_value = request_factory.get_query_parameters()

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_content_data",
    [
        [{"status": {"code": "Error"}}],
        [{"status": {"code": "UserRequestError"}}],
        [{"status": {"code": "Error"}, "universe": "IBM"}],
    ],
)
def test_historical_pricing_content_validator_validate_content_data_is_false(
    input_content_data,
):
    # given
    input_value = ParsedData({}, {}, **{"content_data": input_content_data})
    expected_value = False
    validator = HistoricalContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_content_data",
    [
        [{"status": {"code": ""}, "data": [{}]}],
        [{"status": {"code": ""}, "universe": "IBM", "data": [{}]}],
        [{"status": {"code": "UserRequestError"}, "universe": "IBM", "data": [{}]}],
    ],
)
def test_historical_pricing_content_validator_validate_content_data_is_true(
    input_content_data,
):
    # given
    input_value = ParsedData({}, {}, **{"content_data": input_content_data})
    expected_value = True
    validator = HistoricalContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "data",
    [
        (
            {
                "status": {},
                "raw_response": {},
                "content_data": [{"universe": {"ric": "IBM.N"}}],
            }
        )
    ],
)
def test_historical_pricing_response_factory_create_success(data):
    response_factory = HistoricalResponseFactory()
    parsed_data = ParsedData(**data)
    response = response_factory.create_success(parsed_data)

    assert response is not None
    assert len(response.errors) == 0


@pytest.mark.parametrize(
    "data,kwargs,error_code,error_message",
    [
        (
            {
                "content_data": [
                    {
                        "universe": {"ric": "VOD.L"},
                        "status": {
                            "code": "TS.Intraday.UserRequestError.90006",
                            "message": "The universe does not support the "
                            "following fields: [ASKee].",
                        },
                    }
                ]
            },
            {"fields": ["ASK", "ASKeee", "DATE_TIME"]},
            "TS.Intraday.UserRequestError.90006",
            "The universe does not support the following fields: [ASKee]. "
            "Requested ric: VOD.L",
        ),
        (
            {
                "content_data": [
                    {
                        "universe": {"ric": "LSEG.L"},
                        "status": {
                            "code": "TS.Intraday.Warning.95004",
                            "message": "Trades interleaving with corrections is "
                            "currently not supported. "
                            "Corrections will not be returned.",
                        },
                    }
                ]
            },
            {},
            "TS.Intraday.Warning.95004",
            "LSEG.L - Trades interleaving with corrections is currently not supported. "
            "Corrections will not be returned.",
        ),
    ],
)
def test_historical_pricing_response_factory_create_success_with_errs(
    data, kwargs, error_code, error_message
):
    response_factory = HistoricalResponseFactory()
    parsed_data = ParsedData({}, {}, **data)
    result = response_factory.create_success(parsed_data, **kwargs)
    assert isinstance(result.errors[0], Error)
    assert result.errors[0][0] == error_code
    assert result.errors[0][1] == error_message


@pytest.mark.parametrize(
    "data,kwargs,error_code,error_message",
    [
        (
            {
                "content_data": [{"universe": {"ric": "VOD.L"}}],
                "error_codes": "TS.Intraday.UserRequestError.90006",
                "error_messages": "The universe does not support the following fields: [ASKeee].",
            },
            {"fields": ["ASKeee", "DATE_TIME"]},
            "TS.Intraday.UserRequestError.90006",
            "The universe does not support the following fields: [ASKeee]. Requested ric: VOD.L",
        ),
        (
            {
                "content_data": [{"universe": {"ric": "VOD.LLL"}}],
                "error_codes": "TS.Intraday.UserRequestError.90001",
                "error_messages": "The universe is not found.",
            },
            {"fields": ["ASK"]},
            "TS.Intraday.UserRequestError.90001",
            "VOD.LLL - The universe is not found",
        ),
        (
            {"error_codes": 400, "error_messages": "Request Validation Error"},
            {"fields": ["TR.Volume", "DATE_TIME"], "universe": "IBM.N"},
            400,
            "Request Validation Error. Requested ric: IBM.N. Requested fields: ['TR.Volume', 'DATE_TIME']",
        ),
    ],
)
def test_historical_pricing_response_factory_create_fail(
    data, kwargs, error_code, error_message
):
    response_factory = HistoricalResponseFactory()
    parsed_data = ParsedData({}, {}, **data)
    result = response_factory.create_fail(parsed_data, **kwargs)
    assert hasattr(result, "errors")
    assert isinstance(result.errors[0], Error)
    assert result.errors[0][0] == error_code
    assert result.errors[0][1] == error_message


@pytest.mark.parametrize(
    "input_header_name,input_data",
    [
        ("DATE", [["2022-04-26", 130], ["2022-04-25", 129]]),
        (
            "DATE_TIME",
            [
                ["2021-07-27T16:30:00.000000000Z", 130],
                ["2021-07-27T15:50:00.000000000Z", 129],
            ],
        ),
    ],
)
def test_historical_pricing_build_df_index_type(input_header_name, input_data):
    # given
    input_raw = {
        "headers": [
            {"name": input_header_name, "type": "string"},
            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
        ],
        "data": input_data,
        "universe": {"ric": ""},
    }

    df_builder = HistoricalBuilder()

    # when
    result_df = df_builder.build_one(input_raw, [], "")

    # then
    assert is_datetime64_any_dtype(result_df.index)
    assert not is_datetime64tz_dtype(result_df.index)
