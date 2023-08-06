import allure
import pytest

from refinitiv.data.content.ownership import StatTypes
from refinitiv.data.content.ownership.fund import breakdown
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
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "categoryvalue",
    "TR.CatFundInvestorCount",
    "TR.CatFundOwnershipPct",
    "TR.InstrFdStatCatShrsHld",
    "TR.InstrFdStatCatShHldVal",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Category Value",
    "Category Investors Count",
    "Category Ownership %",
    "Category SharesHeld",
    "Category SharesHeld Value",
]


@allure.suite("Content object - Ownership Fund Breakdown")
@allure.feature("Content object - Ownership Fund Breakdown")
@allure.severity(allure.severity_level.CRITICAL)
class TestFundBreakdown:
    @allure.title(
        "Create Fund Breakdown definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37414276")
    @pytest.mark.parametrize(
        "universe,stat_type,use_field_names_in_headers,extended_params,expected_universe",
        [
            ("ONEX.CCP", 1, True, {"test_param": "test_value"}, "ONEX.CCP"),
            ("US02079K1079", 3, False, None, "US02079K1079"),
            (
                ["TRI.N", "ONEX.CCP", "AAPL.O"],
                StatTypes.REGION,
                True,
                {"universe": "TRI.N,US02079K1079"},
                ["TRI.N", "US02079K1079"],
            ),
            (
                ["ONEX.CCP", "invalid universe"],
                StatTypes.COUNTRY,
                False,
                None,
                ["ONEX.CCP", "invalid universe"],
            ),
        ],
    )
    @pytest.mark.smoke
    def test_create_fund_breakdown_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        stat_type,
        use_field_names_in_headers,
        extended_params,
        expected_universe,
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = breakdown.Definition(
            universe, stat_type, use_field_names_in_headers, extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, expected_universe
        )
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create Fund Breakdown definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37475441")
    @pytest.mark.parametrize(
        "universe,invalid_universe,stat_type",
        [
            (["AAPL.O", "invalid universe"], "invalid universe", StatTypes.REGION),
        ],
    )
    @pytest.mark.smoke
    async def test_create_fund_breakdown_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe, stat_type
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            breakdown.Definition(universe, stat_type, use_field_names_in_headers=True),
            breakdown.Definition(
                invalid_universe, stat_type, use_field_names_in_headers=True
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

    @allure.title("Create Fund Breakdown definition object with closed session")
    @pytest.mark.caseid("37478854")
    async def test_create_fund_breakdown_object_with_closed_session(
        self, open_platform_session_async
    ):
        session = open_platform_session_async
        await session.close_async()
        with pytest.raises(ValueError) as error:
            await breakdown.Definition("ONEX.CCP", 1).get_data_async()
        assert str(error.value) == "Session is not opened. Can't send any request"
