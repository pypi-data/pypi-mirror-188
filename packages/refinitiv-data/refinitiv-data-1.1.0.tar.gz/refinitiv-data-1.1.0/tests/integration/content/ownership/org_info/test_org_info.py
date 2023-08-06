import allure
import pytest

from refinitiv.data.content.ownership import org_info
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
    "TR.CommonName",
    "TR.ExchangeName",
    "TR.OrgTRBCActivity",
    "TR.TRBCActivityCode",
    "TR.HQCountryCode",
    "TR.HeadquartersCountry",
    "TR.FreeFloat",
    "TR.FreeFloatPct",
    "TR.SharesOutstanding",
    "TR.SharesHeldByStrategicInvestors",
    "Strategic Entities Ownership%",
    "Market Capitalization",
]

EXPECTED_COLUMN_TITLES = [
    "Instrument",
    "Company Name",
    "ExchangeName",
    "TRBC Industry",
    "TRBC IndustryCode",
    "Country Code",
    "Country Name",
    "FreeFloat",
    "FreeFloat %",
    "SharesOutstanding",
    "SharesHeld by StrategicInvestors",
    "Strategic Entities Ownership%",
    "Market Capitalization",
]


@allure.suite("Content object - Ownership Org-info")
@allure.feature("Content object - Ownership Org-info")
@allure.severity(allure.severity_level.CRITICAL)
class TestFundOrgInfo:
    @allure.title(
        "Create Org-Info definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37556977")
    @pytest.mark.parametrize(
        "universe,use_field_names_in_headers,extended_params",
        [
            ("US02079K1079", True, {"test_param": "test_value"}),
            (["TRI.N", "ONEX.CCP", "AAPL.O"], False, None),
            (["ONEX.CCP", "invalid universe"], True, {"test_param": "test_value"}),
        ],
    )
    def test_create_fund_org_info_object_with_valid_fields_and_get_data(
        self,
        open_platform_session,
        universe,
        use_field_names_in_headers,
        extended_params,
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = org_info.Definition(
            universe, use_field_names_in_headers, extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create Org-Info definition object with mix valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37556978")
    @pytest.mark.parametrize(
        "universe,invalid_universe",
        [
            (["AAPL.O", "invalid universe"], "invalid universe"),
        ],
    )
    @pytest.mark.smoke
    async def test_create_org_info_object_with_mix_valid_and_invalid_params_and_get_data_async(
        self, open_platform_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            org_info.Definition(universe, use_field_names_in_headers=True),
            org_info.Definition(invalid_universe, use_field_names_in_headers=True),
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
