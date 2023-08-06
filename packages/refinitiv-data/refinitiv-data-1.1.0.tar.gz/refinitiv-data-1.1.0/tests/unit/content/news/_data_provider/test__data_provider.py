import pytest

from refinitiv.data.content._df_builder import build_empty_df
from refinitiv.data.content.news._news_data_provider import (
    NewsHeadlinesRDPData,
    NewsStoryResponseFactory,
    NewsHeadlinesUDFRequestFactory,
    NewsStoryUDFRequestFactory,
    NewsStoryRDPRequestFactory,
    NewsHeadlinesRDPRequestFactory,
    NewsUDFContentValidator,
    NewsStoryResponse,
    NewsStoryRDPData,
    NewsUDFDataProvider,
    NewsHeadlinesRDPDataProvider,
)
from refinitiv.data.delivery._data._data_factory import DataFactory
from refinitiv.data.delivery._data._data_provider import Response, ParsedData
from tests.unit.conftest import StubSession
from ...news.test_news import STORY_RAW_JSON, HEADLINE_RAW_JSON

ERROR_MESSAGE_FOR_NEWS_STORY = "Error while calling the NEP backend: Story not found"


def test_news_story_rdp_data():
    # given
    # when
    news_story_data = NewsStoryRDPData(STORY_RAW_JSON)

    # then
    assert hasattr(news_story_data, "raw")
    assert hasattr(news_story_data, "story")


def test_news_headlines_rdp_data():
    # given
    # when
    news_headlines_data = NewsHeadlinesRDPData(HEADLINE_RAW_JSON, build_empty_df)

    # then
    assert hasattr(news_headlines_data, "raw")
    assert hasattr(news_headlines_data, "headlines")


@pytest.mark.parametrize(
    ("input_error_code", "input_error_message"),
    [
        (400, ""),
        (400, "a"),
        (400, ERROR_MESSAGE_FOR_NEWS_STORY),
        (404, ""),
        (404, "a"),
        (404, ERROR_MESSAGE_FOR_NEWS_STORY),
    ],
)
def test_news_story_response_factory_create_fail_changed_data(
    input_error_code, input_error_message
):
    # given
    data = ParsedData(
        {},
        {},
        **{
            "error_codes": input_error_code,
            "error_messages": input_error_message,
        },
    )

    # when
    response_factory = NewsStoryResponseFactory()
    response_factory.create_fail(data)

    # then
    assert data.first_error_code == 404
    assert data.first_error_message == ERROR_MESSAGE_FOR_NEWS_STORY


def test_news_story_response__str_fail_data():
    # given
    input_data = ParsedData(
        {},
        {},
        **{
            "error_codes": 404,
            "error_messages": ERROR_MESSAGE_FOR_NEWS_STORY,
        },
    )
    expected_str = f"[Error(code=404, message='{ERROR_MESSAGE_FOR_NEWS_STORY}')]"

    # when
    new_story_response = NewsStoryResponse(False, input_data, DataFactory())

    # then
    assert str(new_story_response) == expected_str


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {
                "query": "test_query",
                "count": 11,
                "repository": "test_repo",
                "date_from": "11-11-2020",
                "date_to": "11-11-2020",
                "payload": "/headlines?payload=TEST",
            },
            {
                "Entity": {
                    "E": "News_Headlines",
                    "W": {
                        "query": "test_query",
                        "number": "11",
                        "repository": "test_repo",
                        "productName": "app_key",
                        "dateFrom": "2020-11-11T00:00:00",
                        "dateTo": "2020-11-11T00:00:00",
                        "payload": "TEST",
                    },
                }
            },
        )
    ],
)
def test_news_headlines_request_factory_udf_get_body_parameters(
    input_data, expected_result
):
    # given
    session = StubSession()

    # when
    result = NewsHeadlinesUDFRequestFactory().get_body_parameters(session, **input_data)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {
                "story_id": "test_story_id",
            },
            {
                "Entity": {
                    "E": "News_Story",
                    "W": {
                        "storyId": "test_story_id",
                        "productName": "app_key",
                    },
                }
            },
        )
    ],
)
def test_news_story_request_factory_udf_get_body_parameters(
    input_data, expected_result
):
    # given
    session = StubSession()

    # when
    result = NewsStoryUDFRequestFactory().get_body_parameters(session, **input_data)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {
                "story_id": "test_story_id",
            },
            {"storyId": "test_story_id"},
        )
    ],
)
def test_news_story_request_factory_rdp_get_path_parameters(
    input_data, expected_result
):
    # given
    # when
    result = NewsStoryRDPRequestFactory().get_path_parameters(**input_data)

    # then
    assert result == expected_result


def test_news_story_request_factory_rdp_get_header_parameters():
    # given
    # when
    result = NewsStoryRDPRequestFactory().get_header_parameters()

    # then
    assert result == {"accept": "application/json"}


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {
                "query": "test_query",
                "count": 10,
                "date_from": "11-11-2020",
                "date_to": "11-11-2020",
                "sort_order": "oldToNew",
                "cursor": "test",
            },
            [
                ("query", "test_query"),
                ("limit", 10),
                ("dateFrom", "2020-11-11T00:00:00"),
                ("dateTo", "2020-11-11T00:00:00"),
                ("sort", "oldToNew"),
                ("cursor", "test"),
            ],
        )
    ],
)
def test_news_headlines_request_factory_rdp_get_query_parameters(
    input_data, expected_result
):
    # given
    session = StubSession()

    # when
    result = NewsHeadlinesRDPRequestFactory().get_query_parameters(
        session, **input_data
    )

    # then
    assert result == expected_result


def test_news_headlines_request_factory_udf_extend_body_parameters():
    # given
    body_parameters = {"Entity": {"W": {"key": "value"}}}
    extended_params = {"new_key": "new_value"}

    expected_result = {"Entity": {"W": {"key": "value", "new_key": "new_value"}}}

    # when
    result = NewsHeadlinesUDFRequestFactory().extend_body_parameters(
        body_parameters, extended_params
    )

    # then
    assert result == expected_result


def test_news_headlines_request_factory_rdp_extend_query_parameters():
    # given
    query_parameters = [("key", "value"), ("number", 5)]
    extended_params = {"number": 20}

    expected_result = [("key", "value"), ("number", 20)]

    # when
    result = NewsHeadlinesRDPRequestFactory().extend_query_parameters(
        query_parameters, extended_params
    )

    # then
    assert result == expected_result


def test_news_headlines_request_factory_rdp_extend_body_parameters():
    # given
    expected_parameters = {"number": 5}
    extended_params = {"number": 20}

    # when
    result = NewsHeadlinesRDPRequestFactory().extend_body_parameters(
        expected_parameters, extended_params=extended_params
    )

    # then
    assert result == expected_parameters


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            {
                "content_data": {
                    "ErrorCode": 404,
                    "ErrorMessage": "Error code 404 | Backend error. 404 Not Found",
                }
            },
            False,
        ),
        ({"content_data": None}, False),
        ({"content_data": {"test": "data"}}, True),
    ],
)
def test_news_content_validator_udf(input_data, expected_result):
    # given
    parsed_data = ParsedData({}, {}, **input_data)
    # when
    result = NewsUDFContentValidator().validate(parsed_data)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    "input_count, limit, expected_count",
    [
        (1, 2, 1),
        (5, 10, 5),
        (15, 10, 5),
        (1, 100, 99),
        (1, 101, 0),
        (101, 100, 1),
        (100, 1000, 0),
    ],
)
def test_news_data_provider_udf_change_count(input_count, limit, expected_count):
    # given
    kwargs = {"count": 0}

    # when
    NewsUDFDataProvider().change_count(count=input_count, limit=limit, kwargs=kwargs)

    # then
    assert kwargs["count"] == expected_count


def test_news_data_provider_udf_get_data_without_count():
    # given
    session = StubSession(is_open=True)

    # when
    result = NewsUDFDataProvider().get_data(session, "")

    # then
    assert isinstance(result, Response)


def test_news_data_provider_udf_get_data_with_count_zero():
    # given
    session = StubSession(is_open=True)

    # when
    result = NewsUDFDataProvider().get_data(session, "", **{"count": 0})

    # then
    assert isinstance(result, Response)
    assert result.is_success is True
    assert result.data._dataframe is None
    assert result.errors == []


def test_news_data_provider_rdp_get_data_with_count_zero():
    # given
    session = StubSession(is_open=True)

    # when
    result = NewsHeadlinesRDPDataProvider().get_data(session, "", **{"count": 0})

    # then
    assert isinstance(result, Response)
    assert result.is_success is True
    assert result.data._dataframe is None
    assert result.errors == []
