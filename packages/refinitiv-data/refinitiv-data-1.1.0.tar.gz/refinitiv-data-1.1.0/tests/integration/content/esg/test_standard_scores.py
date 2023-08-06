import allure
import pytest

from refinitiv.data.content.esg import standard_scores
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - ESG Standard Scores")
@allure.feature("Content object - ESG Standard Scores")
@allure.severity(allure.severity_level.CRITICAL)
class TestESGStandardScores:
    @allure.title("Create ESG Standard Scores definition object with valid params")
    @pytest.mark.parametrize(
        "universe,start,end",
        [("5000002406", 0, -2)],
    )
    @pytest.mark.caseid("C40602075")
    @pytest.mark.smoke
    def test_esg_standard_scores_definition_object_with_valid_params_and_get_data(
        self, universe, start, end, open_platform_session
    ):
        response = standard_scores.Definition(
            universe=universe, start=start, end=end
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
        check_non_empty_response_data(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create ESG Standard Scores definition object with invalid params and get error"
    )
    @pytest.mark.caseid("C40602077")
    @pytest.mark.parametrize(
        "universe,expected_error,start,end",
        [
            (
                "5000002406",
                "Error code 400 | Validation error: validation failure list:\nstart in query should be greater than or equal to -2",
                -3,
                -1,
            )
        ],
    )
    def test_esg_standard_scores_definition_object_with_invalid_params_and_get_error(
        self, universe, expected_error, start, end, open_platform_session
    ):
        with pytest.raises(RDError) as error:
            standard_scores.Definition(
                universe=universe, start=start, end=end
            ).get_data()
        assert str(error.value) == expected_error

    @allure.title(
        "Create ESG Standard Scores definition object with use mix valid and invalid data - asynchronously"
    )
    @pytest.mark.caseid("C40602078")
    @pytest.mark.parametrize(
        "universe,invalid_universe,start,end",
        [(["5000002406", "INVALID"], "INVALID", 0, -2)],
    )
    async def test_esg_standard_scores_definition_object_with_use_mix_valid_and_invalid_data(
        self, universe, invalid_universe, start, end, open_platform_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            standard_scores.Definition(universe=universe, start=start, end=end),
            standard_scores.Definition(universe=invalid_universe, start=start, end=end),
        )
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=None,
            expected_error_message="Failed to resolve identifiers ['INVALID']",
        )
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=HttpStatusCode.FOUR_HUNDRED_TWELVE,
            expected_error_message="Unable to resolve all requested identifiers. Requested items: ['INVALID']",
        )
