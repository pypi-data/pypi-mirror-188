import allure
import pytest

from refinitiv.data.content.ownership.consolidated import shareholders_report
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
    get_expected_column,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "investorid",
    "TR.InvestorFullName",
    "TR.InvParentType",
    "TR.InvestorType",
    "TR.InvInvestmentStyleCode",
    "TR.InvInvmtOrientation",
    "TR.OwnTrnverRating",
    "TR.OwnTurnover",
    "TR.InvestorRegion",
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
    "TR.WeightCountry",
    "TR.PctCountry",
    "TR.WeightSector",
    "TR.PctSector",
    "TR.WeightExchange",
    "TR.PctExchange",
    "TR.PrevSharesHeld",
    "TR.PrevPctOfSharesOutHeld",
    "TR.PrevSharesHeldValue",
    "TR.PrevHoldingsDate",
    "TR.PrevFilingType",
    "TR.InvContFirstName",
    "TR.InvContMidInit",
    "TR.InvContLastName",
    "TR.InvContTelCntry",
    "TR.InvContAreaCode",
    "TR.InvContTelNumber",
    "TR.InvContTelExt",
    "TR.InvConAddrMetroArea",
    "TR.InvestorAddrCity",
    "TR.InvAddrCountry",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Calc Date",
    "Investor Id",
    "Investor Perm Id",
    "Investor Name",
    "Investor Parent Type",
    "Investor Type",
    "Investment Style",
    "Orientation",
    "Turnover Rating",
    "Turnover %",
    "Investor Region",
    "Total Equity Assets",
    "SharesHeld",
    "% of SharesOutstanding",
    "Holdings % Portfolio",
    "SharesHeld Value",
    "Holdings Date",
    "Filing Type",
    "SharesHeld Change",
    "SharesHeld Value Change",
    "% SharesOutstanding Change",
    "Weight Country",
    "% Country",
    "Weight Sector",
    "% Sector",
    "Weight Exchange",
    "% Exchange",
    "Previous SharesHeld",
    "Previous % SharesOutstanding",
    "Previous SharesHeld Value",
    "Previous Holdings Date",
    "Previous Filing Type",
    "Contact First Name",
    "Contact Middle Name",
    "Contact Last Name",
    "Contact Phone Country",
    "Contact Phone AreaCode",
    "Contact Phone TelNumber",
    "Contact PhoneExt",
    "Contact MetroArea",
    "Investor City",
    "Investor Country",
    "UltimateParentId",
]


@allure.suite("Content object - Ownership Consolidated Shareholders Report")
@allure.feature("Content object - Ownership Consolidated Shareholders Report")
@allure.severity(allure.severity_level.CRITICAL)
class TestConsolidatedShareholdersReport:
    @allure.title(
        "Create Consolidated Shareholders Report definition object with valid params and get data"
    )
    @pytest.mark.caseid("37556963")
    @pytest.mark.parametrize(
        "universe,limit,use_field_names_in_headers,extended_params,expected_universe",
        [
            ("ONEX.CCP", 5, True, {"universe": "VOD.L"}, "VOD.L"),
            (["IBM.N", "TRI.N"], 100, True, {"offset": 3560}, ["IBM.N", "TRI.N"]),
            (["ONEX.CCP", "invalid universe"], 100, False, {"offset": 50}, "ONEX.CCP"),
        ],
    )
    def test_create_consolidated_shareholders_report_object_with_valid_fields_and_get_data(
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
        response = shareholders_report.Definition(
            universe, limit, use_field_names_in_headers, extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, expected_universe
        )

    @allure.title(
        "Create Consolidated Shareholders Report definition object with valid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556964")
    @pytest.mark.parametrize(
        "universe",
        [
            ("ONEX.CCP"),
            pytest.param(
                ["TRI.N", "ONEX.CCP", "invalid"],
                marks=pytest.mark.skip(
                    reason="https://jira.refinitiv.com/browse/ADC-54133"
                ),
            ),
        ],
    )
    # this test fails due to server-side issue https://jira.refinitiv.com/browse/ADC-54133,
    # uncomment test params when issue is fixed.
    async def test_create_consolidated_shareholders_report_object_with_valid_fields_and_get_data_async(
        self, open_platform_session_async, universe
    ):
        response = await get_async_response_from_definition(
            shareholders_report.Definition(universe, use_field_names_in_headers=True)
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, EXPECTED_COLUMN_NAMES)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
