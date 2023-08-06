import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from refinitiv.data.delivery._data._data_type import DataType
from tests.unit.conftest import StubSession


@pytest.mark.parametrize(
    "content_type",
    [
        DataType.ENDPOINT,
        ContentType.NEWS_STORY_RDP,
        ContentType.NEWS_STORY_UDF,
        ContentType.NEWS_IMAGES,
        ContentType.DEFAULT,
        ContentType.FILINGS_SEARCH,
    ],
)
def test_response_data_does_not_have_df_property_simple_case(content_type):
    # given
    session = StubSession(is_open=True)

    # when
    response = make_provider(content_type).get_data(session, "url")

    # then
    assert hasattr(response.data, "raw")
    assert not hasattr(response.data, "df")
