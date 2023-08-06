import allure
import pytest

from refinitiv.data._errors import RDError
from refinitiv.data.content import search
from refinitiv.data.content.search import Views
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
)


@allure.suite("Content object - Search Metadata")
@allure.feature("Content object - Search Metadata")
@allure.severity(allure.severity_level.CRITICAL)
class TestMetadata:
    @allure.title("Send metadata request with valid view parameter and get data")
    @pytest.mark.caseid("36136187")
    @pytest.mark.smoke
    @pytest.mark.parametrize("view", [(Views.PEOPLE), ("People")])
    def test_send_metadata_request_with_valid_view_parameter_and_get_data(
        self, open_session, view
    ):
        response = search.metadata.Definition(view=view).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

    @allure.title("Send metadata request with invalid view parameter")
    @pytest.mark.caseid("36136196")
    @pytest.mark.parametrize(
        "view,expected_error",
        [
            (
                "invalid value",
                "Error code 400 | Validation error: validation failure list:",
            )
        ],
    )
    def test_send_metadata_request_with_invalid_view_parameter(
        self, open_session, view, expected_error
    ):
        with pytest.raises(RDError) as error:
            search.metadata.Definition(view=view).get_data()
        assert expected_error in str(error.value)

    @allure.title(
        "Send metadata request with valid view parameter and get data asynchronously"
    )
    @pytest.mark.caseid("36136243")
    @pytest.mark.parametrize("view", [Views.CMO_INSTRUMENTS])
    async def test_send_metadata_request_with_valid_view_parameter_and_get_data_asynchronously(
        self, open_session_async, view
    ):
        response = await get_async_response_from_definition(
            search.metadata.Definition(view=view)
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

    @allure.title("Send metadata request when session is not opened")
    @pytest.mark.caseid("36136244")
    @pytest.mark.parametrize("view", [Views.ORGANISATIONS])
    def test_send_metadata_request_when_session_is_not_opened(self, open_session, view):
        session = open_session
        session.close()
        definition = search.metadata.Definition(view=view)
        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            definition.get_data()
