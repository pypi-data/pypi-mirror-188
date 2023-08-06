import allure
import pytest

from refinitiv.data.content import search
from refinitiv.data.content.search import Views
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    check_extended_params_were_sent_in_request,
    get_async_response_from_definition,
    check_response_dataframe_contains_columns_names,
    check_response_dataframe_contains_rows_names,
    check_empty_dataframe_in_response,
)


@allure.suite("Content object - Search Lookup")
@allure.feature("Content object - Search Lookup")
@allure.severity(allure.severity_level.CRITICAL)
class TestLookup:
    @allure.title("Send lookup request with all valid parameters and get data")
    @pytest.mark.caseid("36107140")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "view,scope,terms,select",
        [
            (
                "Instruments",
                "RIC",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
            )
        ],
    )
    def test_send_lookup_request_with_all_valid_parameters(
        self, open_session, view, scope, terms, select
    ):
        response = search.lookup.Definition(
            view=view,
            scope=scope,
            terms=terms,
            select=select,
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, select.split(","))
        check_response_dataframe_contains_rows_names(response, terms.split(","))

    @allure.title("Send lookup request with invalid parameter scope")
    @pytest.mark.caseid("36107142")
    @pytest.mark.parametrize(
        "view,scope,terms,select,error_message",
        [
            (
                Views.INSTRUMENTS,
                "invalid_scope",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
                "Invalid scope: unknown property 'invalid_scope'",
            )
        ],
    )
    def test_send_lookup_request_with_invalid_parameter_scope(
        self, open_session, view, scope, terms, select, error_message
    ):
        with pytest.raises(RDError) as error:
            search.lookup.Definition(
                view=view,
                scope=scope,
                terms=terms,
                select=select,
            ).get_data()
        assert (
            str(error.value)
            == "Error code 400 | Invalid scope: unknown property 'invalid_scope'"
        )

    @allure.title("Send lookup request with invalid parameters terms/select")
    @pytest.mark.caseid("36135835")
    @pytest.mark.parametrize(
        "view,scope,terms,select",
        [
            (
                Views.INSTRUMENTS,
                "RIC",
                "invalid_terms",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
            ),
            (
                search.Views.INSTRUMENTS,
                "RIC",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "invalid_select",
            ),
        ],
    )
    def test_send_lookup_request_with_invalid_parameters_terms_select(
        self, open_session, view, scope, terms, select
    ):
        response = search.lookup.Definition(
            view=view,
            scope=scope,
            terms=terms,
            select=select,
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_empty_dataframe_in_response(response)

    @allure.title("Send lookup request with invalid parameter view")
    @pytest.mark.caseid("36136025")
    @pytest.mark.parametrize(
        "view,scope,terms,select,expected_error",
        [
            (
                "invalid view - string",
                "RIC",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
                "Error code 400 | Validation error: json.View in body should be one of "
            )
        ],
    )
    def test_send_lookup_request_with_invalid_parameter_view(
        self, open_session, view, scope, terms, select, expected_error
    ):
        with pytest.raises(RDError) as error:
            search.lookup.Definition(
                view=view,
                scope=scope,
                terms=terms,
                select=select,
            ).get_data()
        assert expected_error in str(error.value)

    @allure.title(
        "Send lookup request with all valid parameters and get data asynchronously"
    )
    @pytest.mark.caseid("36136026")
    @pytest.mark.parametrize(
        "view,scope,valid_terms,invalid_terms,select",
        [
            (
                Views.INSTRUMENTS,
                "RIC",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "INVALID_SCOPE",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
            )
        ],
    )
    async def test_send_lookup_request_with_all_valid_parameters_and_get_data_asynchronously(
        self, open_session_async, view, scope, valid_terms, invalid_terms, select
    ):
        full_terms = valid_terms + "," + invalid_terms
        response = await get_async_response_from_definition(
            search.lookup.Definition(
                view=view,
                scope=scope,
                terms=full_terms,
                select=select,
            )
        )

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, select.split(","))
        check_response_dataframe_contains_rows_names(response, valid_terms.split(","))

    @allure.title("Send lookup request with extended parameters")
    @pytest.mark.caseid("36136031")
    @pytest.mark.parametrize(
        "view,scope,terms,select,extended_params",
        [
            (
                Views.INSTRUMENTS,
                "RIC",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
                {"param1": "value1"},
            )
        ],
    )
    def test_send_lookup_request_with_extended_parameters(
        self, open_session, view, scope, terms, select, extended_params
    ):
        response = search.lookup.Definition(
            view=view,
            scope=scope,
            terms=terms,
            select=select,
            extended_params=extended_params,
        ).get_data()
        check_extended_params_were_sent_in_request(response, extended_params)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

    @allure.title("Send lookup request when session is not opened")
    @pytest.mark.caseid("36136071")
    @pytest.mark.parametrize(
        "view,scope,terms,select",
        [
            (
                Views.INSTRUMENTS,
                "RIC",
                "MSFT.O,AAPL.O,GOOG.O,KBANK.BK,SCC.BK",
                "DocumentTitle,BusinessEntity,SEDOL,CUSIP",
            )
        ],
    )
    def test_send_lookup_request_when_session_is_not_opened(
        self, open_session, view, scope, terms, select
    ):
        session = open_session
        session.close()
        definition = search.lookup.Definition(
            view=view,
            scope=scope,
            terms=terms,
            select=select,
        )
        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            definition.get_data()
