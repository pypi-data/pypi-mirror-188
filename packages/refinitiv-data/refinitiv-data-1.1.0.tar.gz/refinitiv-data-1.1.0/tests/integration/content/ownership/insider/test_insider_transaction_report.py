import allure
import pytest

from refinitiv.data.content.ownership.insider import transaction_report
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
    "investorname",
    "date",
    "TR.InsiderInvestorType",
    "TR.InsiderRole",
    "TR.InsiderPrimaryRole",
    "TR.InsiderDate",
    "TR.InsiderIsNLE",
    "TR.InsiderIsNLEDate",
    "TR.InsiderInactiveDate",
    "TR.InvTrnIsNoLongerFiling",
    "TR.InvTransIsNLFDate",
    "TR.TransactionDate",
    "TR.TransactionTypeCode",
    "TR.TransactionType",
    "TR.AcquisitionType",
    "TR.AdjSharesTraded",
    "TR.AsRepSharesTraded",
    "TR.PctOfSharesOutTraded",
    "TR.TransactionPrice",
    "TR.InvTransPriceInARCurr",
    "TR.InvTransFilingType",
    "TR.TableNumber",
    "TR.IntradayTradeSeqNum",
    "TR.RoleSequenceNumber",
    "TR.RoleType",
    "TR.AmendmentId",
    "TR.InvestorTransDCN",
    "TR.TransactionCreateDate",
    "TR.TransactionUpdateDate",
    "TR.InvTransHoldingType",
    "TR.LatestHoldingType",
    "TR.AdjSharesHeld",
    "TR.AdjIndirectSharesHeld",
    "TR.AsRepSharesHeld",
    "TR.AsRepIndSharesHeld",
    "TR.InsiderRegion",
    "TR.InsAddressLine1",
    "TR.InsAddressLine2",
    "TR.InsAddressLine3",
    "TR.InsStateProv",
    "TR.InsAddressCity",
    "TR.InsCountry",
    "TR.InsPostalCode",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Equity owner name",
    "Date",
    "Investor Type",
    "Insider Role Type",
    "isPrimary InsiderRole",
    "Date Became Insider",
    "Contact NoLonger Exists",
    "Contact NoLonger Exists Date",
    "Insider Inactive Date",
    "Investment Turnsaction NoLongerFiles",
    "Date Considered NoLongerFiling",
    "Transaction Date",
    "Transaction TypeCode",
    "Transaction Type",
    "AcquisitionType",
    "Adjusted SharesTraded",
    "AsReported SharesTraded",
    "% Of SharesOutstandingTraded",
    "Transaction Price",
    "Transaction Price As Reported Curr",
    "Transaction Filing Type",
    "US Insider Form Table Num",
    "Intraday Trade SeqNumber",
    "Role SeqNum",
    "Title",
    "Amendment Indicator",
    "Filing DocControlNum",
    "Transaction CreateDate",
    "Transaction UpdateDate",
    "HoldingType",
    "Latest HoldingType",
    "Adjusted SharesHeld",
    "Adjusted Indirect SharesHeld",
    "AsReported SharesHeld",
    "AsReported Indirect SharesHeld",
    "Region",
    "AddrLine1",
    "AddrLine2",
    "AddrLine3",
    "State Province",
    "City",
    "Country",
    "PostalCode",
]


@allure.suite("Content object - Ownership Insider Transaction Report")
@allure.feature("Content object - Ownership Insider Transaction Report")
@allure.severity(allure.severity_level.CRITICAL)
class TestInsiderTransactionReport:
    @allure.title(
        "Create Insider Transaction Report definition definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37556989")
    @pytest.mark.parametrize(
        "universe,use_field_names_in_headers,extended_params",
        [
            ("AAPL.O", True, {"test_param": "test_value"}),
            (["TRI.N", "ONEX.CCP", "AAPL.O"], False, {"test_param": "test_value"}),
            (["invalid universe", "ONEX.CCP"], True, None),
        ],
    )
    def test_create_insider_transaction_report_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        use_field_names_in_headers,
        extended_params,
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = transaction_report.Definition(
            universe=universe,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        ).get_data()
        print(response.data.df.to_string())
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_dataframe_column_date_for_datetime_type(response)
        check_extended_params_were_sent_in_request(response, extended_params)
        # check_response_dataframe_instrument_contains_expected_universes(response, universe)
        #  - this check does not work yet while paging is not implemented, as all data returned
        #  for only the first universe, too many records. Uncomment with paging available.

    @allure.title(
        "Create Insider Transaction Report definition with title in headers by use_field_names_in_headers False as default"
    )
    @pytest.mark.caseid("C40219573")
    @pytest.mark.parametrize("universe", ["TRI.N"])
    def test_create_insider_transaction_report_object_with_use_field_names_in_headers_false(
        self, open_platform_session, universe
    ):
        response = transaction_report.Definition(
            universe, use_field_names_in_headers=False
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(
            response, EXPECTED_COLUMN_TITLES
        )
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create Insider Transaction Report definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556990")
    @pytest.mark.parametrize(
        "universe,invalid_universe,start,end,limit",
        [
            (
                ["ONEX.CCP", "invalid universe"],
                "invalid universe",
                "20210725",
                "20211005",
                4,
            ),
        ],
    )
    @pytest.mark.smoke
    async def test_create_insider_transaction_report_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe, start, end, limit
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            transaction_report.Definition(
                universe, start, end, limit, use_field_names_in_headers=True
            ),
            transaction_report.Definition(
                invalid_universe, start, end, limit, use_field_names_in_headers=True
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
            valid_response, universe[0]
        )
