import allure
import pytest

from refinitiv.data.content.ownership import StatTypes
from refinitiv.data.content.ownership.consolidated import breakdown
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
    get_expected_column,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    get_async_response_from_definition,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_extended_params_were_sent_in_request,
)

EXPECTED_COLUMN_NAMES = [
    "instrument",
    "categoryvalue",
    "TR.CategoryInvestorCount",
    "TR.CategoryOwnershipPct",
    "TR.InstrStatCatSharesHeld",
    "TR.InstrStatCatShrsHldVal",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Category Value",
    "Category Investor Count",
    "Category Ownership %",
    "Category SharesHeld",
    "Category SharesHeld Value",
]


@allure.suite("Content object - Ownership Consolidated Breakdown")
@allure.feature("Content object - Ownership Consolidated Breakdown")
@allure.severity(allure.severity_level.CRITICAL)
class TestConsolidatedBreakdown:
    @allure.title(
        "Create Consolidated Breakdown definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37556928")
    @pytest.mark.parametrize(
        "universe,stat_type,use_field_names_in_headers,extended_params,expected_universe",
        [
            ("ONEX.CCP", 1, True, {"test_param": "test_value"}, "ONEX.CCP"),
            ("US02079K1079", 3, False, None, "US02079K1079"),
            (
                ["TRI.N", "ONEX.CCP", "AAPL.O"],
                StatTypes.REGION,
                False,
                {"universe": "ONEX.CCP,US02079K1079"},
                ["ONEX.CCP", "US02079K1079"],
            ),
            (
                ["ONEX.CCP", "invalid universe"],
                StatTypes.COUNTRY,
                True,
                None,
                ["ONEX.CCP", "invalid universe"],
            ),
        ],
    )
    def test_create_consolidated_breakdown_object_with_valid_fields_and_get_data(
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
        "Create Consolidated Breakdown definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556929")
    @pytest.mark.parametrize(
        "universe,invalid_universe,stat_type",
        [
            (["ONEX.CCP", "invalid universe"], "invalid universe", StatTypes.COUNTRY),
        ],
    )
    @pytest.mark.smoke
    async def test_create_consolidated_breakdown_object_with_mix_valid_and_invalid_params_and_get_data_async(
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

    @allure.title(
        "Create Consolidated Breakdown definition object with invalid fields and get error"
    )
    @pytest.mark.caseid("37556930")
    @pytest.mark.parametrize(
        "universe,stat_type",
        [
            ([], 2),
            ([""], 3),
        ],
    )
    def test_create_consolidated_breakdown_object_with_invalid_fields_and_get_error(
        self, open_platform_session, universe, stat_type
    ):
        with pytest.raises(RDError) as error:
            breakdown.Definition(universe, stat_type).get_data()
        assert (
            str(error.value)
            == "Error code 400 | Validation error: validation failure list:\nuniverse.0 in query should be at least 1 chars long"
        )

    @allure.title("Create Consolidated Breakdown definition object with closed session")
    @pytest.mark.caseid("37556931")
    async def test_create_consolidated_breakdown_object_with_closed_session(
        self, open_platform_session_async
    ):
        session = open_platform_session_async
        await session.close_async()
        definition = breakdown.Definition("ONEX.CCP", 1)
        with pytest.raises(ValueError) as error:
            await get_async_response_from_definition(definition)
        assert str(error.value) == "Session is not opened. Can't send any request"
