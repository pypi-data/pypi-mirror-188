import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.contracts.bond.conftest import (
    bond_definition_fixed_rate,
    bond_definition_floating_rate,
    bond_definition_user_defined,
    invalid_bond_definition,
    bond_universe,
)
from tests.integration.content.ipa.contracts.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
)
from tests.integration.helpers import (
    check_response_status,
    get_async_response_from_definitions,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - Bond")
@allure.feature("Content object - Bond")
@allure.severity(allure.severity_level.CRITICAL)
class TestBond:
    # EAPI-2456 bug when async_mode True in desktop session
    @allure.title("Create a bond definition object with params and get data")
    @pytest.mark.caseid("35996161")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "bond_definition",
        [
            bond_definition_fixed_rate,
            bond_definition_floating_rate,
            bond_definition_user_defined,
        ],
    )
    def test_user_defined_bond(self, open_session, bond_definition):
        response = bond_definition().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a bond definition request asynchronously")
    @pytest.mark.caseid("35996161")
    @pytest.mark.smoke
    async def test_bond_definition_asynchronously(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            bond_definition_fixed_rate(), invalid_bond_definition()
        )

        check_http_status_is_success_and_df_value_not_empty(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )

    @allure.title("Create a bond stream")
    @pytest.mark.caseid("36597161")
    def test_bond_stream_with_default_params(self, open_session):
        stream = bond_definition_fixed_rate().get_stream()
        stream.open()

        check_stream_state_and_df_from_stream(stream)

    @allure.title("Create a bond definition object with empty pricing parameters")
    @pytest.mark.parametrize("universe", ["US10YT=RR"])
    @pytest.mark.caseid("35984974")
    def test_multiple_bond_as_definitions_empty_pricing_parameters(
        self, universe, open_session
    ):
        response = rdf.bond.Definition(
            instrument_code=universe,
            pricing_parameters=rdf.bond.PricingParameters(),
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title(
        "Create a bond definition object with different value type in universe"
    )
    @pytest.mark.parametrize("instrument_code", [2, ["1", "1"], {"1": "1"}])
    @pytest.mark.caseid("36051507")
    def test_bond_definition_with_different_value_type(
        self, instrument_code, open_platform_session
    ):
        with pytest.raises(ValueError) as error:
            rdf.bond.Definition(instrument_code=instrument_code).get_data()
        assert "Invalid type of instrument_code" in str(error.value)

    @allure.title("Create an invalid bond definition object and get RDError")
    @pytest.mark.caseid("")
    def test_invalid_bond_definition(self, open_session):
        with pytest.raises(RDError) as error:
            invalid_bond_definition().get_data()
        assert (
            str(error.value)
            == "Error code None | Market data error : There is no analytics for instrumentCode [ INVALID_INSTRUMENT_CODE ] in the data sourcing system that is used for pricing."
        )

    @allure.title("Create a bond definition with extended parameters")
    @pytest.mark.caseid("C37678339")
    def test_get_bond_with_extended_params(self, open_session):
        response = rdf.bond.Definition(
            issue_date="2002-02-28",
            end_date="2032-02-28",
            notional_ccy="USD",
            interest_payment_frequency="Annual",
            interest_calculation_method=rdf.bond.DayCountBasis.DCB_ACTUAL_ACTUAL,
            extended_params={
                "instrumentDefinition": {
                    "fixedRatePercent": 9,
                    "interestPaymentFrequency": "Annual",
                },
                "pricingParameters": {"cleanPrice": 122},
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == bond_universe
        ), f"Extended params are applied incorrectly"
