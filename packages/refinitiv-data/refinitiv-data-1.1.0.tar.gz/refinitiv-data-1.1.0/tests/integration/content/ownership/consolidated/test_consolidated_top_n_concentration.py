import re

import allure
import pytest

from refinitiv.data.content.ownership.consolidated import top_n_concentration
from refinitiv.data.errors import RDError
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
    "Instrument",
    "Total Shareholders Count",
    "% SharesOutstanding",
    "SharesHeld",
    "SharesHeld Value",
]

EXPECTED_COLUMN_TITLES = [
    "instrument",
    "Total Shareholders Count",
    "% SharesOutstanding",
    "SharesHeld",
    "SharesHeld Value",
]


@allure.suite("Content object - Ownership Consolidated Top-n-Concentration")
@allure.feature("Content object - Ownership Fund Top-n-Concentration")
@allure.severity(allure.severity_level.CRITICAL)
class TestFundTopNConcentration:
    @allure.title(
        "Create Consolidated Top-n-Concentration definition object with valid required params and get data"
    )
    @pytest.mark.caseid("37556970")
    @pytest.mark.parametrize(
        "universe,count,use_field_names_in_headers",
        [
            ("ONEX.CCP", 5, True),
            ("US02079K1079", 1, False),
            (["TRI.N", "ONEX.CCP", "AAPL.O"], 20, True),
            (["ONEX.CCP", "invalid universe"], 100, False),
        ],
    )
    def test_create_consolidated_top_n_concentration_object_with_valid_fields_and_get_data(
        self, open_platform_session, universe, count, use_field_names_in_headers
    ):
        expected_column = get_expected_column(
            use_field_names_in_headers, EXPECTED_COLUMN_TITLES, EXPECTED_COLUMN_NAMES
        )
        response = top_n_concentration.Definition(
            universe, count, use_field_names_in_headers
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )

    @allure.title(
        "Create asunc Consolidated Top-n-Concentration definition object with mix valid and invalid params"
    )
    @pytest.mark.caseid("37556971")
    @pytest.mark.parametrize(
        "universe,invalid_universe,count",
        [
            (["ONEX.CCP", "invalid universe"], "invalid universe", 15),
        ],
    )
    @pytest.mark.smoke
    async def test_async_consolidated_top_n_concentration_object_with_mix_valid_and_invalid_params(
        self, open_platform_session_async, universe, invalid_universe, count
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            top_n_concentration.Definition(
                universe, use_field_names_in_headers=True, count=count
            ),
            top_n_concentration.Definition(
                invalid_universe, use_field_names_in_headers=True, count=count
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
        "Create Consolidated Top-n-Concentration definition object with invalid params and get error"
    )
    @pytest.mark.caseid("37556972")
    @pytest.mark.parametrize(
        "universe,count", [("", 30), ("ONEX.CCP", -200), ([""], "invalid count")]
    )
    def test_create_consolidated_top_n_concentration_object_with_invalid_fields_and_get_error(
        self, open_platform_session, universe, count
    ):
        if type(count) == int and count < 1:
            with pytest.raises(RDError) as error:
                top_n_concentration.Definition(universe, count).get_data()
            assert (
                str(error.value)
                == "Error code 400 | Validation error: validation failure list:\ncount in query should be greater than or equal to 1"
            )
        elif type(count) == int and count >= 1:
            with pytest.raises(RDError) as error:
                top_n_concentration.Definition(universe, count).get_data()
            assert (
                str(error.value)
                == "Error code 400 | Validation error: validation failure list:\nuniverse.0 in query should be at least 1 chars long"
            )
        else:
            with pytest.raises(
                TypeError,
                match=re.escape(
                    "Parameter 'count' of invalid type provided: 'str', expected types: ['int']"
                ),
            ):
                top_n_concentration.Definition(universe, count).get_data()
