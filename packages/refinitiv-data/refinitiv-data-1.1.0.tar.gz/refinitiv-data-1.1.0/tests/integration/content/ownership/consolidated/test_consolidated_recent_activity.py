import allure
import pytest

from refinitiv.data.content.ownership._enums import SortOrder
from refinitiv.data.content.ownership.consolidated import recent_activity
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
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "investorid",
    "investorname",
    "TR.NetSharesHeldChange",
    "TR.NetSharesHeldValChg",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Investor Id",
    "Equity owner name",
    "SharesHeld Change",
    "SharesHeld Value Change",
]


@allure.suite("Content object - Ownership Consolidated Recent Activity")
@allure.feature("Content object - Ownership Consolidated Recent Activity")
@allure.severity(allure.severity_level.CRITICAL)
class TestConsolidatedRecentActivity:
    @allure.title(
        "Create Consolidated Recent Activity definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37556949")
    @pytest.mark.parametrize(
        "universe,sort_order,use_field_names_in_headers",
        [
            ("US02079K1079", "desc", False),
            (["TRI.N", "ONEX.CCP", "AAPL.O"], SortOrder.ASCENDING, True),
            (["ONEX.CCP", "invalid universe"], SortOrder.DESCENDING, False),
        ],
    )
    def test_create_consolidated_recent_activity_object_with_valid_fields_and_get_data(
        self, open_platform_session, universe, sort_order, use_field_names_in_headers
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = recent_activity.Definition(
            universe, sort_order, use_field_names_in_headers
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )

    @allure.title(
        "Create Consolidated Recent Activity definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556950")
    @pytest.mark.parametrize(
        "universe,invalid_universe,sort_order",
        [
            (
                ["ONEX.CCP", "invalid universe"],
                "invalid universe",
                SortOrder.DESCENDING,
            ),
        ],
    )
    @pytest.mark.smoke
    async def test_create_consolidated_recent_activity_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe, sort_order
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            recent_activity.Definition(
                universe, sort_order, use_field_names_in_headers=True
            ),
            recent_activity.Definition(
                invalid_universe, sort_order, use_field_names_in_headers=True
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
