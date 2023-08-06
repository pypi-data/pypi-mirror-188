import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.content.ipa.contracts.cds.conftest import (
    cds_definition,
    cds_universe,
)
from tests.integration.content.ipa.contracts.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
    add_call_backs,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - CDS")
@allure.feature("Content object - CDS")
@allure.severity(allure.severity_level.CRITICAL)
class TestCDS:
    @pytest.mark.xfail(
        reason="Server side problem, time to time it raise technical error"
    )
    @allure.title("Create a cds definition object with params and get data")
    @pytest.mark.caseid("36523217")
    def test_cds_definition_get_data(self, open_session):
        response = cds_definition().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create a cds definition without any parameters")
    @pytest.mark.caseid("36523223")
    def test_get_cds_analytics_without_any_parameters(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.cds.Definition().get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.1012 | Invalid input: leg definition is invalid. The Premium leg is empty."
        )

    @allure.title("Create a cds definition with empty pricing parameters")
    @pytest.mark.caseid("36523226")
    def test_get_cds_with_empty_pricing_params(self, open_session):
        response = rdf.cds.Definition(
            instrument_tag="Cds1_InstrumentCode",
            instrument_code="BNPP5YEUAM=R",
            cds_convention=rdf.cds.CdsConvention.ISDA,
            end_date_moving_convention=rdf.cds.BusinessDayConvention.NO_MOVING,
            adjust_to_isda_end_date=True,
            pricing_parameters=rdf.cds.PricingParameters(),
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a cds definition with invalid extended parameters")
    @pytest.mark.caseid("36523459")
    def test_get_cds_with_invalid_extended_params(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.cds.Definition(
                instrument_tag="Cds1_InstrumentCode",
                instrument_code="BNPP5YEUAM=R",
                cds_convention=rdf.cds.CdsConvention.ISDA,
                end_date_moving_convention=rdf.cds.BusinessDayConvention.NO_MOVING,
                adjust_to_isda_end_date=True,
                fields=[
                    "InstrumentTag",
                    "ValuationDate",
                    "InstrumentDescription",
                    "StartDate",
                    "EndDate",
                ],
                extended_params={"instrumentDefinition": "INVALID"},
            ).get_data()
        assert (
            str(error.value)
            == "Error code 400 | Invalid input: Unbindable json. Error: Could not cast or convert from System.String to TR.Qps.Calculators.BL.CdS.DataModel.CdsDefinition. Path: instrumentDefinition"
        )

    @allure.title("Create a cds definition request asynchronously")
    @pytest.mark.caseid("36523460")
    async def test_cds_definition_asynchronously(self, open_session_async):
        response = await get_async_response_from_definition(cds_definition())
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create a cds stream")
    @pytest.mark.caseid("36523463")
    def test_cds_stream(self, open_session_async):
        stream = cds_definition().get_stream()
        stream.open()

        check_stream_state_and_df_from_stream(stream)

    @allure.title(
        "Create a cds stream with callback on_response and extended parameters"
    )
    @pytest.mark.caseid("36524104")
    def test_cds_stream_with_callback_and_extended_params(self, open_session):
        events_list = []
        stream = rdf.cds.Definition(
            instrument_tag="Cds1_InstrumentCode",
            instrument_code="BNPP5YEUAM=R",
            end_date_moving_convention=rdf.cds.BusinessDayConvention.NEXT_BUSINESS_DAY,
            pricing_parameters=rdf.cds.PricingParameters(market_data_date="2020-01-01"),
            fields=[
                "InstrumentTag",
                "ValuationDate",
                "InstrumentDescription",
                "StartDate",
                "EndDate",
                "InstrumentTag",
                "ValuationDate",
                "MarketDataDate",
                "ErrorMessage",
            ],
            extended_params={
                "instrumentDefinition": {
                    "cdsConvention": "ISDA",
                    "endDateMovingConvention": "NoMoving",
                    "adjustToIsdaEndDate": True,
                },
            },
        ).get_stream(open_session)

        add_call_backs(stream, events_list)
        stream.open()

        check_stream_state_and_df_from_stream(stream)
        assert (
            stream._stream.universe == cds_universe
        ), f"Extended params are applied incorrectly"
        assert "Response received for" in events_list, f"Events list is {events_list}"
