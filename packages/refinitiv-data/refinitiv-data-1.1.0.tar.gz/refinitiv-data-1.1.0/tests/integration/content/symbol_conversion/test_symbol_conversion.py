import json

import allure
import pytest

from refinitiv.data.content import symbol_conversion
from refinitiv.data.content.symbol_conversion import SymbolTypes
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.symbol_conversion.conftest import (
    symbol_conversion_definition,
    invalid_symbol_conversion_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_extended_params_were_sent_in_request,
)


@allure.suite("Content object - Symbol Conversion")
@allure.feature("Content object - Symbol Conversion")
@allure.severity(allure.severity_level.CRITICAL)
class TestSymbolConversion:
    @allure.title("Retrieve symbol conversion with one symbol to mix symbols types")
    @pytest.mark.parametrize(
        "symbols,to_symbol_type,expected_fields",
        [
            (
                "IBM.N",
                [SymbolTypes.OA_PERM_ID, SymbolTypes.TICKER_SYMBOL],
                ["DocumentTitle", "TickerSymbol", "IssuerOAPermID"],
            )
        ],
    )
    @pytest.mark.caseid("C39748890")
    def test_symbol_conversion_ric_to_mix_of_types(
        self, open_session, symbols, to_symbol_type, expected_fields
    ):
        response = symbol_conversion.Definition(
            symbols=symbols,
            from_symbol_type=SymbolTypes.RIC,
            to_symbol_types=to_symbol_type,
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_fields)

    @allure.title("Retrieve symbol conversion with multiple rics to all symbol types")
    @pytest.mark.parametrize(
        "symbols,expected_fields",
        [
            (
                ["AAPL.O", "GOOG.O", "IBM.N"],
                [
                    "RIC",
                    "DocumentTitle",
                    "SEDOL",
                    "TickerSymbol",
                    "IssueISIN",
                    "IssuerOAPermID",
                    "CUSIP",
                ],
            ),
        ],
    )
    @pytest.mark.caseid("4170070")
    def test_symbol_conversion_with_multiple_rics_to_all_types(
        self, open_session, symbols, expected_fields
    ):
        response = symbol_conversion.Definition(
            symbols=symbols, from_symbol_type=SymbolTypes.RIC
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_fields)

    @allure.title("Retrieve symbol conversion to selected symbol types")
    @pytest.mark.parametrize(
        "symbols,to_symbol_type,expected_fields,expected_assets",
        [
            (
                ["US5949181045", "US02079K1079"],
                SymbolTypes.RIC,
                ["RIC", "DocumentTitle"],
                "'Commodities' 'Equities' 'Bond Pricing' 'Funds' 'FX & Money'",
            )
        ],
    )
    @pytest.mark.caseid("C39748891")
    def test_symbol_conversion_from_isin_to_another_two(
        self,
        open_session_async,
        symbols,
        to_symbol_type,
        expected_fields,
        expected_assets,
    ):
        response = symbol_conversion.Definition(
            symbols=symbols,
            from_symbol_type=SymbolTypes.ISIN,
            to_symbol_types=to_symbol_type,
            asset_class=[
                symbol_conversion.AssetClass.COMMODITIES,
                symbol_conversion.AssetClass.EQUITIES,
                symbol_conversion.AssetClass.BONDS,
                symbol_conversion.AssetClass.FUNDS,
                symbol_conversion.AssetClass.WARRANTS,
                symbol_conversion.AssetClass.FX_AND_MONEY,
            ],
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_fields)
        actual_assets = json.loads(response.request_message.content)
        assert expected_assets in actual_assets.get("Filter")

    @pytest.mark.skip("need to refactor")
    @allure.title(
        "Retrieve symbol conversion with valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("C39748892")
    @pytest.mark.smoke
    async def test_symbol_conversion_with_valid_and_invalid_params_and_get_data_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            symbol_conversion_definition(), invalid_symbol_conversion_definition()
        )

        check_response_status(valid_response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.FOUR_HUNDRED,
            expected_http_reason=HttpReason.BAD_REQUEST,
            expected_error_code=HttpStatusCode.FOUR_HUNDRED,
            expected_error_message="Validation error: json.Terms in body must be of type string",
        )

    @pytest.mark.skip("need to refactor")
    @allure.title("Create a invalid symbol conversion definition and get RDError")
    @pytest.mark.caseid("C39748893")
    def test_symbol_conversion_with_invalid_definition(self, open_session):
        with pytest.raises(RDError) as error:
            invalid_symbol_conversion_definition().get_data()
        assert (
            str(error.value)
            == "Error code 400 | Validation error: json.Terms in body must be of type string"
        )

    @allure.title("Retrieve symbol conversion with extended params")
    @pytest.mark.parametrize(
        "symbols,from_symbol_type,to_symbol_type,extended_params,expected_fields",
        [
            (
                ["60000008"],
                SymbolTypes.LIPPER_ID,
                [SymbolTypes.ISIN],
                {"Select": "RIC,SEDOL"},
                ["RIC", "SEDOL"],
            )
        ],
    )
    @pytest.mark.caseid("C39748894")
    def test_symbol_conversion_with_extended_params(
        self,
        open_session,
        symbols,
        from_symbol_type,
        to_symbol_type,
        extended_params,
        expected_fields,
    ):
        response = symbol_conversion.Definition(
            symbols=symbols,
            from_symbol_type=from_symbol_type,
            to_symbol_types=to_symbol_type,
            extended_params=extended_params,
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_fields)
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title("Retrieve symbol conversion with closed session")
    @pytest.mark.caseid("C39748895")
    def test_symbol_conversion_with_closed_session(self, open_session):
        session = open_session
        session.close()
        with pytest.raises(ValueError) as error:
            symbol_conversion_definition().get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"
