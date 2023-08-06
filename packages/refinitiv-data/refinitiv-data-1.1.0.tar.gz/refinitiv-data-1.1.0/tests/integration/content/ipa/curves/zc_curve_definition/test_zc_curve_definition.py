import json

import allure
import pytest

from refinitiv.data.content.ipa.curves import zc_curve_definitions
from tests.integration.content.ipa.curves.conftest import on_response
from tests.integration.content.ipa.curves.zc_curve_definition.conftest import (
    check_sc_curve_definitions_response,
    zc_curve_definition_01,
    zc_curve_definition_02, zc_curve_definition_universe,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - ZcCurveDefinition")
@allure.feature("Content object - ZcCurveDefinition")
@allure.severity(allure.severity_level.CRITICAL)
class TestZcCurveDefinition:
    @allure.title("Create a zc_curve_definition object with valid params and get data")
    @pytest.mark.caseid("39597176")
    @pytest.mark.smoke
    def test_create_zc_curve_definition_with_valid_params(self, open_session):
        response = zc_curve_definition_01().get_data(
            on_response=lambda response, definition, session: on_response(
                response, definition, open_session
            )
        )

        check_sc_curve_definitions_response(response=response, expected_currency="EUR")
        check_dataframe_column_date_for_datetime_type(response)


    @allure.title("Create zc curve definition object with invalid source and get data")
    @pytest.mark.caseid("39597177")
    def test_create_empty_zc_curve_definition(self, open_session):
        response = zc_curve_definitions.Definition(source="INVALID_SOURCE").get_data()

        assert response.data.df.empty

    @allure.title("Create a zc curve definition object async")
    @pytest.mark.caseid("39597178")
    async def test_create_zc_curve_definition_async(self, open_session_async):
        response_01, response_02 = await get_async_response_from_definitions(
            zc_curve_definition_01(), zc_curve_definition_02()
        )

        check_sc_curve_definitions_response(
            response=response_01, expected_currency="EUR"
        )

    @allure.title("Create a zc_curve definition with extended parameters")
    @pytest.mark.caseid("C40214933")
    def test_get_zc_curve_definition_with_extended_params(self, open_session):
        response = zc_curve_definitions.Definition(
            source="Refinitiv",
            extended_params={
                "indexName": "EURIBOR",
                "source": "Refinitiv",
                "valuationDate": "2020-07-01",
            },
        ).get_data()

        check_sc_curve_definitions_response(response=response, expected_currency="EUR")

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == zc_curve_definition_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.df.indexName[0] == "EURIBOR"



