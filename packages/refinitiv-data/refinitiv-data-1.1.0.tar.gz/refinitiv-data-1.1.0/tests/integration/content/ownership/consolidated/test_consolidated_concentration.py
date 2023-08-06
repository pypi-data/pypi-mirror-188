import allure
import pytest

from refinitiv.data.content.ownership.consolidated import concentration
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

EXPECTED_COLUMN_TITLES = [
    "instrument",
    "Investors Total",
    "% SharesOutstandingAll",
    "SharesHeldAll",
    "SharesHeld ValueAll",
]

EXPECTED_COLUMN_NAMES = [
    "Instrument",
    "Investors Total",
    "% SharesOutstandingAll",
    "SharesHeldAll",
    "SharesHeld ValueAll",
]


@allure.suite("Content object - Ownership Consolidated Concentration")
@allure.feature("Content object - Ownership Consolidated Concentration")
@allure.severity(allure.severity_level.CRITICAL)
class TestConsolidatedConcentration:
    @allure.title(
        "Create Consolidated Concentration definition object with valid params and get data"
    )
    @pytest.mark.caseid("37556935")
    @pytest.mark.parametrize(
        "universe,use_field_names_in_headers,extended_params,expected_universe",
        [
            ("AAPL.O", True, {"universe": "ONEX.CCP"}, "ONEX.CCP"),
            (
                ["TRI.N", "ONEX.CCP", "AAPL.O"],
                True,
                {"universe": "ONEX.CCP,US02079K1079"},
                ["ONEX.CCP", "US02079K1079"],
            ),
            (
                ["ONEX.CCP", "invalid universe"],
                False,
                None,
                ["ONEX.CCP", "invalid universe"],
            ),
        ],
    )
    @pytest.mark.smoke
    def test_create_consolidated_concentration_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        use_field_names_in_headers,
        extended_params,
        expected_universe,
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = concentration.Definition(
            universe,
            use_field_names_in_headers=True,
            extended_params=extended_params,
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, expected_universe
        )

    @allure.title(
        "Create Consolidated Concentration definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556936")
    @pytest.mark.parametrize(
        "universe,invalid_universe",
        [
            (["ONEX.CCP", "invalid universe"], "invalid universe"),
        ],
    )
    @pytest.mark.smoke
    async def test_create_consolidated_concentration_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            concentration.Definition(universe, use_field_names_in_headers=True),
            concentration.Definition(invalid_universe, use_field_names_in_headers=True),
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
