import allure
import pytest

from refinitiv.data.content.ipa.curves import forward_curves
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.curves.conftest import (
    forward_curve_definition_01,
    forward_curve_definition_02,
    forward_curve_definition_03,
    check_curves,
    check_curve_response,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    assert_error,
    check_dataframe_column_date_for_datetime_type,
)


def forward_curves_definition_01():
    definition = forward_curves.Definitions(
        [forward_curve_definition_02(), forward_curve_definition_01()]
    )

    return definition


def forward_curves_definition_02():
    definition = forward_curves.Definitions(
        [forward_curve_definition_01(), forward_curve_definition_03()]
    )

    return definition


@allure.suite("Content object - ForwardCurves")
@allure.feature("Content object - ForwardCurves")
@allure.severity(allure.severity_level.CRITICAL)
class TestForwardCurves:
    @allure.title(
        "Create a forward curves definition object with valid params and get data"
    )
    @pytest.mark.caseid("37925242")
    @pytest.mark.smoke
    def test_create_forward_curves_definition_with_valid_params(self, open_session):
        response = forward_curves_definition_01().get_data()

        check_curve_response(response, expected_currency="EUR")
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a empty forward curves definition object and get data")
    @pytest.mark.caseid("37925244")
    def test_create_empty_forward_curves_definition(self):
        with pytest.raises(TypeError) as error:
            forward_curves.Definitions().get_data()

        assert_error(error, "universe")

    @allure.title("Create an invalid forward curves definition object and get data")
    @pytest.mark.caseid("39592733")
    def test_create_invalid_forward_curves_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code QPS-Curves.6 | Invalid input: curveDefinition is missing",
        ):
            forward_curves.Definitions([forward_curves.Definition()]).get_data()

    @allure.title(
        "Create a forward curves definition object and check curve parameters"
    )
    @pytest.mark.caseid("37925245")
    def test_create_forward_curves_definition_and_check_curve_parameters(
        self, open_session
    ):
        response = forward_curves_definition_01().get_data()

        check_curves(response)

    @allure.title("Create a forward curves definition object async")
    @pytest.mark.caseid("37925246")
    async def test_create_forward_curves_definition_async(self, open_session_async):
        invalid_response, valid_response = await get_async_response_from_definitions(
            forward_curves.Definitions([forward_curves.Definition()]),
            forward_curves_definition_01(),
        )

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Curves.6",
            expected_error_message="Invalid input: curveDefinition is missing",
        )
        check_curves(valid_response)
        check_curve_response(valid_response, expected_currency="EUR")

    @allure.title(
        "Create a forward curves definition object with valid and invalid forward curve definition and get data"
    )
    @pytest.mark.caseid("39592730")
    @pytest.mark.smoke
    def test_create_forward_curves_definition_with_valid_and_invalid_forward_curve(
        self, open_session
    ):
        response = forward_curves_definition_02().get_data()

        check_curve_response(response, expected_currency="EUR")
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Curves.6",
            expected_error_message="Invalid input: curveDefinition is missing",
        )
        check_curves(response)
