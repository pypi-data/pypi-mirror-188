import allure
import pytest

from refinitiv.data._errors import ScopeError
from refinitiv.data.delivery import endpoint_request
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.delivery.endpoint_request.conftest import definition

from tests.integration.helpers import (
    get_async_response_from_definition,
    check_response_status,
    assert_error,
)


@allure.suite("Endpoint request")
@allure.feature("Endpoint request")
@allure.severity(allure.severity_level.CRITICAL)
class TestEndpointRequest:
    @allure.title(
        "Create endpoint request definition object with POST method, valid params - synchronously"
    )
    @pytest.mark.caseid("C37753624")
    @pytest.mark.parametrize(
        "url,body_param",
        [
            (
                "https://api.refinitiv.com/data/historical-pricing/v1/views/interday-summaries",
                {
                    "universe": ["IBM.N", "FB.O", "MSFT.O", "AAPL.O", "TSLA.O"],
                    "end": "2020-12-01",
                },
            )
        ],
    )
    @pytest.mark.smoke
    def test_endpoint_request_definition_object_with_post_method_valid_body_params_and_get_data(
        self, open_session, url, body_param
    ):
        response = endpoint_request.Definition(
            url=url,
            method=endpoint_request.RequestMethod.POST,
            body_parameters=body_param,
        ).get_data()
        assert response.data.raw, f"Empty response.data.raw received"
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)

    @allure.title(
        "Create endpoint request definition object with GET method, valid params - synchronously"
    )
    @pytest.mark.caseid("C37753623")
    @pytest.mark.parametrize(
        "url,request_method,path_param,query_param",
        [
            (
                "/data/historical-pricing/v1/views/interday-summaries/{universe}",
                "GET",
                {"universe": "VOD.L"},
                None,
            ),
            (
                "https://localhost:9000/data/news/v1/headlines",
                endpoint_request.RequestMethod.GET,
                None,
                {
                    "query": "Kyiv",
                    "count": "100",
                    "dateFrom": "2021-05-15",
                    "dateTo": "2022-03-19",
                    "sort": "newToOld",
                },
            ),
            (
                "/data/estimates/v1/view-actuals-kpi/interim",
                endpoint_request.RequestMethod.GET,
                None,
                {"universe": ["IBM", "MSFT"]},
            ),
        ],
    )
    @pytest.mark.smoke
    def test_endpoint_request_definition_object_with_get_method_valid_params_and_get_data(
        self,
        url,
        request_method,
        path_param,
        query_param,
        open_platform_session,
        open_platform_session_with_rdp_creds,
    ):
        definition = endpoint_request.Definition(
            url=url,
            method=request_method,
            path_parameters=path_param,
            query_parameters=query_param,
        )
        if "estimates" in url:
            session = open_platform_session_with_rdp_creds
            response = definition.get_data(session=session)
        else:
            response = definition.get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        assert response.data.raw, f"Empty response.data.raw received"

    @allure.title(
        "Create endpoint request definition object with GET method, universe and query params in URL"
    )
    @pytest.mark.caseid("C37753626")
    @pytest.mark.parametrize(
        "url",
        [
            "/data/historical-pricing/v1/views/events/IBM.N?eventTypes=trade&count=1",
        ],
    )
    @pytest.mark.smoke
    def test_endpoint_request_definition_object_with_get_method_universe_and_params_in_url_and_get_data(
        self, open_session, url
    ):
        response = endpoint_request.Definition(
            url=url, method=endpoint_request.RequestMethod.GET
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        assert response.data.raw, f"Empty response.data.raw received"
        assert url in str(response.request_message.url)

    @allure.title("Create endpoint request definition object using closed session")
    @pytest.mark.caseid("C37753631")
    async def test_endpoint_request_definition_object_using_closed_session(
        self, open_desktop_session_async
    ):
        await open_desktop_session_async.close_async()

        with pytest.raises(ValueError) as error:
            await get_async_response_from_definition(definition)
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title("Create endpoint request definition object using invalid scope")
    @pytest.mark.caseid("")
    async def test_endpoint_request_definition_object_using_invalid_scope(
        self, open_platform_session_async
    ):
        with pytest.raises(ScopeError) as error:
            await get_async_response_from_definition(definition)
        assert "Missing scopes" in str(error.value)

    @allure.title(
        "Create endpoint request definition object without any params and get error"
    )
    @pytest.mark.caseid("C37753628")
    def test_endpoint_request_definition_object_without_any_params_and_get_error(self):
        with pytest.raises(TypeError) as error:
            endpoint_request.Definition().get_data()
        assert_error(error, "url")

    @allure.title(
        "Create endpoint request definition object with empty params and get error"
    )
    @pytest.mark.caseid("C37753629")
    @pytest.mark.parametrize(
        "url,path_param,expected_error",
        [
            ("", None, "Requested URL is missing, please provide valid URL"),
            (
                "/data/historical-pricing/v1/views/events/{universe}",
                None,
                "Path parameter 'universe' is missing, please provide path parameter",
            ),
        ],
    )
    def test_endpoint_request_definition_object_with_empty_params_and_get_error(
        self, open_session, url, path_param, expected_error
    ):
        with pytest.raises(ValueError) as error:
            endpoint_request.Definition(
                url=url,
                path_parameters=path_param,
            ).get_data()
        assert str(error.value) == expected_error
