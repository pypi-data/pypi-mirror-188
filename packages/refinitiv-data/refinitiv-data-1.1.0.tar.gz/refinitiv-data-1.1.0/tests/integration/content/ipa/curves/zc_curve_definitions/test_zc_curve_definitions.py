import allure
import pytest

from refinitiv.data.content.ipa.curves import zc_curve_definitions
from tests.integration.content.ipa.curves.conftest import on_response
from tests.integration.content.ipa.curves.zc_curve_definition.conftest import (
    check_sc_curve_definitions_response,
    zc_curve_definition_01,
    zc_curve_definition_02,
    invalid_zc_curve_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - ZcCurveDefinitions")
@allure.feature("Content object - ZcCurveDefinitions")
@allure.severity(allure.severity_level.CRITICAL)
class TestZcCurveDefinitions:
    @allure.title(
        "Create a zc_curve_definitions object with valid definitions and get data"
    )
    @pytest.mark.caseid("39785336")
    @pytest.mark.smoke
    def test_create_zc_curve_definition_with_valid_definitions(self, open_session):
        response = zc_curve_definitions.Definitions(
            [zc_curve_definition_01(), zc_curve_definition_02()]
        ).get_data(
            on_response=lambda response, definition, session: on_response(
                response, definition, open_session
            )
        )

        check_sc_curve_definitions_response(response=response, expected_currency="EUR")
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create zc curve definitions object with invalid definition and get data"
    )
    @pytest.mark.caseid("39785337")
    def test_create_invalid_zc_curve_definitions(self, open_session):
        response = zc_curve_definitions.Definitions(
            invalid_zc_curve_definition()
        ).get_data()

        assert response.data.df.empty

    @allure.title("Create a zc curve definitions object async")
    @pytest.mark.caseid("39785338")
    async def test_create_zc_curve_definitions_async(self, open_session_async):
        response_01, response_02 = await get_async_response_from_definitions(
            zc_curve_definitions.Definitions(zc_curve_definition_01()),
            zc_curve_definitions.Definitions(invalid_zc_curve_definition()),
        )

        check_sc_curve_definitions_response(
            response=response_01, expected_currency="EUR"
        )
        assert response_02.data.df.empty
