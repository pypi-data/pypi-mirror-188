import allure
import pytest

from refinitiv.data.content.esg import full_measures
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_dataframe_column_date_for_datetime_type,
)

EXPECTED_TITLES = [
    "Instrument",
    "Period End Date",
    "TRESG Combined Score",
    "TRESG Score",
    "ESG Controversies Score",
    "Environment Pillar Score",
    "Social Pillar Score",
    "Governance Pillar Score",
    "Resource Use Score",
    "Emissions Score",
    "Accounting Controversies",
    "CSR Sustainability Committee",
    "Integrated Strategy in MD&A",
    "Global Compact Signatory",
    "Stakeholder Engagement",
    "CSR Sustainability Reporting",
    "GRI Report Guidelines",
    "CSR Sustainability Report Global Activities",
    "CSR Sustainability External Audit",
    "ESG Reporting Scope",
]


@allure.suite("Content object - ESG Full Measures")
@allure.feature("Content object - ESG Full Measures")
@allure.severity(allure.severity_level.CRITICAL)
class TestESGFullMeasures:
    @allure.title("Create ESG Full Measures definition object with valid params")
    @pytest.mark.parametrize(
        "universe,start,end",
        [("BNPP.PA", 0, -10), (["IBM.N", "VOD.L"], None, -2)],
    )
    @pytest.mark.caseid("C40232227")
    @pytest.mark.smoke
    def test_esg_full_measures_definition_object_with_valid_params_and_get_data(
        self, universe, start, end, open_platform_session
    ):
        response = full_measures.Definition(
            universe=universe, start=start, end=end
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, EXPECTED_TITLES)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
        check_non_empty_response_data(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create ESG Full Measures definition object with invalid params and get error"
    )
    @pytest.mark.caseid("C40232228")
    @pytest.mark.parametrize(
        "universe,expected_error",
        [
            (
                [],
                "Error code 400 | Validation error: Missing required parameter 'universe'",
            ),
            (
                ["INVALID"],
                "Error code 412 | Unable to resolve all requested identifiers. Requested items: ['INVALID']",
            ),
        ],
    )
    def test_esg_full_measures_definition_object_with_invalid_params_and_get_error(
        self,
        universe,
        expected_error,
        open_platform_session,
    ):
        with pytest.raises(RDError) as error:
            full_measures.Definition(universe=universe).get_data()
        assert str(error.value) == expected_error

    @allure.title(
        "Create ESG Full Measures definition object with use mix valid and invalid data - asynchronously"
    )
    @pytest.mark.caseid("C40232229")
    @pytest.mark.parametrize(
        "universe,invalid_universe", [(["BNPP.PA", "INVALID"], "INVALID")]
    )
    async def test_esg_full_measures_definition_object_with_use_mix_valid_and_invalid_data(
        self, open_platform_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            full_measures.Definition(universe=universe),
            full_measures.Definition(universe=invalid_universe),
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
