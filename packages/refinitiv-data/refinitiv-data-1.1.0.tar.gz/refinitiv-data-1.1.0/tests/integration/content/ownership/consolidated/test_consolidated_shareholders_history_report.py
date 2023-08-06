import re

import allure
import pytest

from refinitiv.data.content.ownership._enums import Frequency
from refinitiv.data.content.ownership.consolidated import shareholders_history_report
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import get_expected_column
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_dataframe_column_date_for_datetime_type,
)

EXPECTED_COLUMN_NAMES = [
    "calcdate",
    "investorid",
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
    "TR.SharesHeldValue",
    "TR.PctOfSharesOutHeld",
    "TR.HoldingsDate",
    "TR.FilingType",
    "TR.SharesHeldChange",
    "TR.SharesHeldValChg",
    "TR.PrevSharesHeld",
    "TR.PrevSharesHeldValue",
    "TR.PrevPctOfSharesOutHeld",
    "TR.PrevHoldingsDate",
    "TR.PrevFilingType",
]

EXPECTED_COLUMN_TITLES = [
    "Calc Date",
    "Investor Id",
    "Investor Name",
    "Investor Parent Type",
    "Investor Type",
    "Investor Region",
    "Investment Style",
    "Orientation",
    "Turnover Rating",
    "Turnover %",
    "Total Equity Assets",
    "SharesHeld",
    "SharesHeld Value",
    "% SharesOutstanding",
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


@allure.suite("Content object - Ownership Consolidated Shareholders History Report")
@allure.feature("Content object - Ownership Consolidated Shareholders History Report")
@allure.severity(allure.severity_level.CRITICAL)
class TestConsolidatedShareholdersHistoryReport:
    @allure.title(
        "Create Consolidated Shareholders History Report definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37556956")
    @pytest.mark.parametrize(
        "universe,frequency,use_field_names_in_headers",
        [("ONEX.CCP", "M", True), ("US02079K1079", Frequency.QUARTERLY, False)],
    )
    @pytest.mark.smoke
    def test_create_consolidated_shareholders_history_report_object_with_valid_fields_and_get_data(
        self, open_platform_session, universe, frequency, use_field_names_in_headers
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = shareholders_history_report.Definition(
            universe=universe,
            frequency=frequency,
            use_field_names_in_headers=use_field_names_in_headers,
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create async Consolidated Shareholders History Report definition object with valid and invalid params"
    )
    @pytest.mark.caseid("37556957")
    @pytest.mark.parametrize(
        "universe,invalid_universe,frequency,start,end,limit",
        [
            ("ONEX.CCP", "invalid universe", "M", "20210725", "20211005", 4),
        ],
    )
    @pytest.mark.smoke
    async def test_async_consolidated_shareholders_history_report_object_with_valid_and_invalid_params(
        self,
        open_platform_session,
        universe,
        invalid_universe,
        frequency,
        start,
        end,
        limit,
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            shareholders_history_report.Definition(
                universe,
                frequency,
                start,
                end,
                use_field_names_in_headers=True,
                limit=limit,
            ),
            shareholders_history_report.Definition(
                invalid_universe,
                frequency,
                start,
                end,
                use_field_names_in_headers=True,
                limit=limit,
            ),
        )
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
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

    @allure.title(
        "Create Consolidated Shareholders History Report definition object with invalid required params and get error"
    )
    @pytest.mark.caseid("37556958")
    @pytest.mark.parametrize(
        "universe,frequency",
        [("invalid", "INVALID FREQUENCY"), ("", 111)],
    )
    def test_create_consolidated_shareholders_history_report_object_with_invalid_fields_and_get_error(
        self, open_platform_session, universe, frequency
    ):
        with pytest.raises(
            AttributeError,
            match=re.escape(f"Value '{frequency}' must be in ['Q', 'M']"),
        ):
            shareholders_history_report.Definition(universe, frequency).get_data()
