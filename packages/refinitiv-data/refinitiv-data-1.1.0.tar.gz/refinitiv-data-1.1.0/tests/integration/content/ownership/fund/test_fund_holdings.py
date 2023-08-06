import allure
import pytest

from refinitiv.data.content.ownership.fund import holdings
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
    get_expected_column,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_extended_params_were_sent_in_request,
    check_dataframe_column_date_for_datetime_type,
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "TR.FundName",
    "Total Holdings Count",
    "TR.FdSecurityOwnedRIC",
    "TR.FdSecurityOwnedName",
    "TR.FdInvPortfolioRank",
    "TR.FdInvestorSharesHeld",
    "TR.FdPctSecuritySharesOut",
    "TR.FdInvestorPctPortfolio",
    "TR.FdInvestorValueHeld",
    "TR.FdInvestorFilingDate",
    "TR.FdInvestorFilingType",
    "TR.FdInvestorShrsHeldChg",
    "TR.FdInvestorValueHeldChg",
    "TR.FdInvestorPosPctChg",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Name",
    "Total Holdings Count",
    "RIC",
    "Security Owned Name",
    "Portfolio Rank",
    "SharesHeld",
    "% SharesOutstanding",
    "% Portfolio",
    "SharesHeld Value",
    "Holdings Date",
    "Filing Type",
    "SharesHeld Change",
    "SharesHeld Value Change",
    "SharesHeld Change %",
]


@allure.suite("Content object - Ownership Fund Holdings")
@allure.feature("Content object - Ownership Fund Holdings")
@allure.severity(allure.severity_level.CRITICAL)
class TestFundHoldings:
    @allure.title(
        "Create Fund Holdings definition object with valid params and get data"
    )
    @pytest.mark.caseid("37478861")
    @pytest.mark.parametrize(
        "universe,limit,use_field_names_in_headers,extended_params,expected_universe",
        [
            ("ONEX.CCP", 5, True, {"test_param": "test_value"}, "ONEX.CCP"),
            (
                ["TRI.N", "ONEX.CCP", "AAPL.O"],
                100,
                False,
                {"universe": "TRI.N,US02079K1079"},
                ["TRI.N", "US02079K1079"],
            ),
        ],
    )
    def test_create_fund_holdings_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        limit,
        use_field_names_in_headers,
        extended_params,
        expected_universe,
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = holdings.Definition(
            universe, limit, use_field_names_in_headers, extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, expected_universe
        )
        check_dataframe_column_date_for_datetime_type(response)
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create Fund Holdings definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37478862")
    @pytest.mark.parametrize(
        "universe,invalid_universe",
        [
            (["LP40189339", "invalid universe"], "invalid universe"),
        ],
    )
    @pytest.mark.smoke
    async def test_create_fund_holdings_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            holdings.Definition(universe, use_field_names_in_headers=True),
            holdings.Definition(invalid_universe, use_field_names_in_headers=True),
        )
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=None,
            expected_error_message="Failed to resolve identifiers ['invalid universe']",
        )
        check_non_empty_response_data(valid_response)
        check_response_dataframe_contains_columns_names(
            valid_response, EXPECTED_COLUMN_NAMES
        )
        check_response_dataframe_instrument_contains_expected_universes(
            valid_response, universe
        )
