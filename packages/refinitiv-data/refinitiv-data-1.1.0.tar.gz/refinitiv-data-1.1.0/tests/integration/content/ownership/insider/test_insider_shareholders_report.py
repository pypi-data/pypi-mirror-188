import allure
import pytest

from refinitiv.data.content.ownership.insider import shareholders_report
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
    "investorpermid",
    "TR.InvestorFullName",
    "TR.InvParentType",
    "TR.InvestorType",
    "TR.InvestorRegion",
    "TR.InvInvestmentStyleCode",
    "TR.InvInvmtOrientation",
    "TR.OwnTrnverRating",
    "TR.OwnTurnover",
    "TR.TotalEquityAssets",
    "TR.SharesHeld",
    "TR.PctOfSharesOutHeld",
    "TR.ConsHoldPctPortfolio",
    "TR.SharesHeldValue",
    "TR.HoldingsDate",
    "TR.FilingType",
    "TR.SharesHeldChange",
    "TR.SharesHeldValChg",
    "TR.PctSharesOutHeldChange",
    "TR.PctSharesHeldChangeOld",
    "TR.PrevSharesHeld",
    "TR.PrevPctOfSharesOutHeld",
    "TR.PrevSharesHeldValue",
    "TR.PrevHoldingsDate",
    "TR.PrevFilingType",
    "TR.InvAddrCountry",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Investor Perm Id",
    "Insider Full Name",
    "Investor Parent Type",
    "Investor Type",
    "Investor Region",
    "Investment Style",
    "Orientation",
    "Turnover Rating",
    "Turnover Pct",
    "Total Equity Assets",
    "SharesHeld",
    "% SharesOutstanding",
    "Holdings % Portfolio",
    "SharesHeld Value",
    "Holdings Date",
    "Filing Type",
    "SharesHeld Change",
    "SharesHeld Value Change",
    "% SharesOutstanding Change",
    "SharesHeld Change%",
    "Previous SharesHeld",
    "Previous % SharesOutstanding",
    "Previous SharesHeld Value",
    "Previous Holding sDate",
    "Previous Filing Type",
    "Country",
]


@allure.suite("Content object - Ownership Insider Shareholders Report")
@allure.feature("Content object - Ownership Insider Shareholders Report")
@allure.severity(allure.severity_level.CRITICAL)
class TestInsiderShareholdersReport:
    @allure.title(
        "Create Insider Shareholders Report definition object with valid params and get data"
    )
    @pytest.mark.caseid("37556997")
    @pytest.mark.parametrize(
        "universe,limit,use_field_names_in_headers,extended_params",
        [
            ("US02079K1079", 1, True, {"test_param": "test_value"}),
            (["TRI.N", "ONEX.CCP", "AAPL.O"], 50, False, None),
            (["ONEX.CCP", "invalid universe"], 100, True, None),
        ],
    )
    def test_create_insider_shareholders_report_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        limit,
        use_field_names_in_headers,
        extended_params,
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = shareholders_report.Definition(
            universe, limit, use_field_names_in_headers, extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
        check_dataframe_column_date_for_datetime_type(response)
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create Insider Shareholders Report definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556998")
    @pytest.mark.parametrize(
        "universe,invalid_universe,limit",
        [
            (["ONEX.CCP", "invalid universe"], "invalid universe", 100),
        ],
    )
    @pytest.mark.smoke
    async def test_create_fund_investors_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe, limit
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            shareholders_report.Definition(
                universe, limit, use_field_names_in_headers=True
            ),
            shareholders_report.Definition(
                invalid_universe, limit, use_field_names_in_headers=True
            ),
        )
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=None,
            expected_error_message="Failed to resolve identifiers ['invalid universe']",
        )
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=HttpStatusCode.FOUR_HUNDRED_TWELVE,
            expected_error_message="Unable to resolve all requested identifiers. Requested items: ['invalid universe']",
        )
        check_response_dataframe_contains_columns_names(
            valid_response, EXPECTED_COLUMN_NAMES
        )
        check_response_dataframe_instrument_contains_expected_universes(
            valid_response, universe
        )
