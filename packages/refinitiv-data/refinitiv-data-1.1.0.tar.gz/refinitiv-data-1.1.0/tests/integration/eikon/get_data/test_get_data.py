import allure
import pytest

import refinitiv.data.eikon as ek
from refinitiv.data.errors import RDError
from tests.integration.eikon.get_data.conftest import (
    check_dataframe_contains_instruments,
    check_dataframe_contains_fields,
    check_success_response,
)


@allure.suite("Eikon Legacy module - get_data")
@allure.feature("Eikon Legacy module - get_data")
@allure.severity(allure.severity_level.NORMAL)
class TestGetData:
    @allure.title("Get snapshot with real-time pricing")
    @pytest.mark.caseid("38427361")
    @pytest.mark.parametrize("instruments,fields", [(["EUR=", "JPY="], ["BID", "ASK"])])
    @pytest.mark.smoke
    def test_get_pricing_snapshot(self, setup_app_key, instruments, fields):
        df, err = ek.get_data(instruments=instruments, fields=fields)
        check_success_response(df, err)
        check_dataframe_contains_instruments(df, instruments)
        check_dataframe_contains_fields(df, fields)

    @allure.title("Get fundamental and reference data")
    @pytest.mark.caseid("38427362")
    @pytest.mark.parametrize(
        "instruments,fields,expected_fields",
        [
            (
                ["GOOG.O", "MSFT.O", "FB.O"],
                ["TR.Revenue", "TR.GrossProfit"],
                ["Instrument", "Revenue", "Gross Profit"],
            )
        ],
    )
    def test_get_fundamental_and_reference(
        self, setup_app_key, instruments, fields, expected_fields
    ):
        df, err = ek.get_data(instruments=instruments, fields=fields)
        check_success_response(df, err)
        check_dataframe_contains_instruments(df, instruments)
        check_dataframe_contains_fields(df, expected_fields)

    @allure.title("Get fundamental and reference data with global parameters")
    @pytest.mark.caseid("38427363")
    @pytest.mark.parametrize(
        "instruments,fields,parameters,expected_fields",
        [
            (
                ["GOOG.O", "AAPL.O"],
                ["CF_BID", "CF_ASK", "TR.EV", "TR.EVToSales"],
                {"SDate": "0CY", "Curn": "CAD"},
                [
                    "Instrument",
                    "CF_BID",
                    "CF_ASK",
                    "Enterprise Value (Daily Time Series)",
                    "Enterprise Value To Sales (Daily Time Series Ratio)",
                ],
            )
        ],
    )
    def test_get_fundamental_and_reference_with_global_parameters(
        self, setup_app_key, instruments, fields, parameters, expected_fields
    ):
        df, err = ek.get_data(
            instruments=instruments,
            fields=fields,
            parameters=parameters,
        )
        check_success_response(df, err)
        check_dataframe_contains_instruments(df, instruments)
        check_dataframe_contains_fields(df, expected_fields)

    @allure.title("Get fundamental and reference data with data item parameters")
    @pytest.mark.caseid("38427364")
    @pytest.mark.parametrize(
        "instruments,fields,expected_fields",
        [
            (
                ["GOOG.O", "AAPL.O"],
                ["TR.PriceTargetMean(Source=ThomsonReuters)"],
                ["Instrument", "Price Target - Mean"],
            )
        ],
    )
    def test_get_fundamental_and_reference_with_data_item_parameters(
        self, setup_app_key, instruments, fields, expected_fields
    ):
        df, err = ek.get_data(instruments=instruments, fields=fields)
        check_success_response(df, err)
        check_dataframe_contains_instruments(df, instruments)
        check_dataframe_contains_fields(df, expected_fields)

    @allure.title("Get fundamental and reference data with invalid parameters")
    @pytest.mark.caseid("38427365")
    def test_get_data_with_invalid_parameters(self, setup_app_key):
        with pytest.raises(
            RDError,
            match="Error code 1422 | Can not process metadata for request: DataGrid_StandardAsync.requests.instruments - non-empty is required",
        ):
            ek.get_data(instruments=[""], fields=["invalid", ""])
