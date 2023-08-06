import allure
import pytest

from refinitiv.data.content.ownership.fund import shareholders_report
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "calcdate",
    "investorid",
    "investorpermid",
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
    "TR.FundPctPortfolio",
    "TR.FdAdjSharesHeldValue",
    "TR.FundHoldingsDate",
    "TR.FundFilingType",
    "TR.FdAdjShrsHeldChange",
    "TR.FdAdjShrsHeldValChg",
    "SharesOutstanding Change %",
    "TR.FdFundPctPositionChg",
    "TR.FdWeightCountry",
    "TR.FdPctCountry",
    "TR.FdWeightSector",
    "TR.FdPctSector",
    "TR.FdWeightExchange",
    "TR.FdPctExchange",
    "TR.PrevFundAdjSharesHeld",
    "TR.PrevAdjPctShrsOutHeld",
    "TR.PrevAdjSharesHeldValue",
    "TR.PrevFundHoldingsDate",
    "TR.PrevFundFilingType",
    "TR.FundContactFirstName",
    "TR.FundContactMiddleInit",
    "TR.FundContactLastName",
    "TR.FundContactTelCntry",
    "TR.FundContactTelAreaCode",
    "TR.FundContactTelNumber",
    "TR.FundContactTelExt",
    "TR.FundContactMetroArea",
    "TR.FundAddressCity",
    "TR.FundAddrCountry",
    "TR.FundParentLegacyId",
]


@allure.suite("Content object - Ownership Fund Shareholders Report")
@allure.feature("Content object - Ownership Fund Shareholders Report")
@allure.severity(allure.severity_level.CRITICAL)
class TestFundShareholdersReport:
    @allure.title(
        "Create Fund Shareholders Report definition object with valid params and get data asynchronously"
    )
    @pytest.mark.caseid("37478939")
    @pytest.mark.parametrize("universe,limit", [("TRI.N", 10)])
    async def test_create_fund_shareholders_report_async(
        self, open_platform_session_async, universe, limit
    ):
        response = await shareholders_report.Definition(
            universe, limit, use_field_names_in_headers=True
        ).get_data_async()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, EXPECTED_COLUMN_NAMES)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
