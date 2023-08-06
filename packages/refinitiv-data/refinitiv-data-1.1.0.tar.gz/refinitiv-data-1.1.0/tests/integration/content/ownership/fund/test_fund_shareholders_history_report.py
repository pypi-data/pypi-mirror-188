import allure
import pytest

from refinitiv.data.content.ownership._enums import Frequency
from refinitiv.data.content.ownership.fund import shareholders_history_report
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_extended_params_were_sent_in_request,
    check_dataframe_column_date_for_datetime_type,
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "TR.FundPortfolioName",
    "TR.FundParentType",
    "TR.FundClassId",
    "TR.FundInvestorType",
    "TR.FundRegion",
    "TR.FundInvtStyleCode",
    "TR.FundInvtOrientation",
    "TR.FundTurnoverRating",
    "TR.FundOwnershipTurnover",
    "TR.FundTotalEquityAssets",
    "TR.FundAdjShrsHeld",
    "TR.FdAdjPctOfShrsOutHeld",
    "TR.FdAdjSharesHeldValue",
    "TR.FundHoldingsDate",
    "TR.FundFilingType",
    "TR.FdAdjShrsHeldChange",
    "TR.FdAdjShrsHeldValChg",
    "TR.PrevFundAdjSharesHeld",
    "TR.PrevAdjSharesHeldValue",
    "TR.PrevAdjPctShrsOutHeld",
    "TR.PrevFundHoldingsDate",
    "TR.PrevFundFilingType",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Investor Perm Id",
    "Investor Name",
    "Investor Parent Type",
    "Fund ClassId",
    "Investor Type",
    "Investor Region",
    "Investment Style",
    "Orientation",
    "Turnover Rating",
    "Turnover %",
    "Total Equity Assets",
    "SharesHeld",
    "% SharesOutstanding",
    "SharesHeld Value",
    "Holdings Date",
    "Filing Type",
    "SharesHeld Change",
    "SharesHeld Value Change",
    "Previous SharesHeld",
    "Previous SharesHeld Value",
    "Previous % SharesOutstanding",
    "Previous Holdings Date",
    "Previous Filing Type",
]


@allure.suite("Content object - Ownership Fund Shareholders History Report")
@allure.feature("Content object - Ownership Fund Shareholders History Report")
@allure.severity(allure.severity_level.CRITICAL)
class TestFundShareholdersHistoryReport:
    @allure.title(
        "Create Fund Shareholders History Report definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37478943")
    @pytest.mark.parametrize(
        "universe,frequency,extended_params,",
        [
            ("ONEX.CCP", "M", {"test_param": "test_value"}),
        ],
    )
    @pytest.mark.smoke
    def test_create_fund_shareholders_history_report_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        frequency,
        extended_params,
    ):
        response = shareholders_history_report.Definition(
            universe=universe,
            frequency=frequency,
            extended_params=extended_params,
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(
            response, EXPECTED_COLUMN_TITLES
        )
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
        check_dataframe_column_date_for_datetime_type(response)
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create Fund Shareholders History Report definition object with all valid params and get data asynchronously"
    )
    @pytest.mark.caseid("37478944")
    @pytest.mark.parametrize(
        "universe,frequency,start,end, limit",
        [("ONEX.CCP", Frequency.QUARTERLY, "20210925", "20211005", 4)],
    )
    async def test_create_fund_shareholders_history_report_object_with_valid_fields_and_get_data_async(
        self, open_platform_session_async, universe, frequency, start, end, limit
    ):
        response = await get_async_response_from_definition(
            shareholders_history_report.Definition(
                universe, frequency, start, end, limit, use_field_names_in_headers=True
            )
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, EXPECTED_COLUMN_NAMES)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
