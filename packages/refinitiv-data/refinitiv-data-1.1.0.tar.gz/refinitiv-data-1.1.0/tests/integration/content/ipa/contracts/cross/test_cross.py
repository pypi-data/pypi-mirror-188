import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.content.ipa.contracts.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
)
from tests.integration.content.ipa.contracts.cross.conftest import cross_universe
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_dataframe_column_date_for_datetime_type,
)

fields = [
    "ValuationDate",
    "InstrumentDescription",
    "EndDate",
    "FxSwapsCcy1Ccy2",
    "MarketValueInReportCcy",
    "DeltaAmountInReportCcy",
    "RhoContraCcyAmountInReportCcy",
    "RhoDealCcyAmountInReportCcy",
    "MarketDataDate",
    "ErrorCode",
    "ErrorMessage",
]


@allure.suite("Content object - Cross")
@allure.feature("Content object - Cross")
@allure.severity(allure.severity_level.CRITICAL)
class TestCross:
    @allure.title(
        "Calculate Non-Deliverable Forward Outright USD/INR and Swap Points for a Broken Date"
    )
    @pytest.mark.caseid("36597349")
    @pytest.mark.smoke
    def test_fx_no_deliverable_forward_usd_inr(self, open_session):
        response = rdf.cross.Definition(
            fx_cross_type=rdf.cross.FxCrossType.FX_NON_DELIVERABLE_FORWARD,
            fx_cross_code="USDINR",
            legs=[
                rdf.cross.LegDefinition(
                    deal_amount=1000000,
                    contra_amount=65762500,
                    deal_ccy_buy_sell=rdf.cross.BuySell.BUY,
                    tenor="4Y",
                )
            ],
            pricing_parameters=rdf.cross.PricingParameters(
                valuation_date="2017-11-15T00:00:00Z"
            ),
            fields=fields,
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Calculate a FX Forward Outright USD/EUR for a Broken Date")
    @pytest.mark.caseid("36597350")
    def test_fx_forward_usd_eur(self, open_session):
        response = rdf.cross.Definition(
            instrument_tag="00102700008910C",
            fx_cross_type=rdf.cross.FxCrossType.FX_FORWARD,
            fx_cross_code="USDEUR",
            legs=[rdf.cross.LegDefinition(end_date="2015-04-09T00:00:00Z")],
            pricing_parameters=rdf.cross.PricingParameters(
                valuation_date="2015-02-02T00:00:00Z",
                price_side=rdf.cross.PriceSide.MID,
            ),
            fields=fields,
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Calculate a FX Swap CHF/JPY Points for a Broken Date")
    @pytest.mark.caseid("36597356")
    def test_fx_swap_chf_jpy(self, open_session):
        response = rdf.cross.Definition(
            instrument_tag="1Y-CHFJPY",
            fx_cross_type=rdf.cross.FxCrossType.FX_SWAP,
            fx_cross_code="CHFJPY",
            legs=[
                rdf.cross.LegDefinition(
                    deal_ccy_buy_sell=rdf.cross.BuySell.BUY,
                    fx_leg_type=rdf.cross.FxLegType.SWAP_NEAR,
                    deal_amount=1000000,
                    contra_amount=897008.3,
                    tenor="1M",
                ),
                rdf.cross.LegDefinition(
                    deal_ccy_buy_sell=rdf.cross.BuySell.SELL,
                    fx_leg_type=rdf.cross.FxLegType.SWAP_FAR,
                    deal_amount=1000000,
                    contra_amount=900000,
                    tenor="1Y",
                ),
            ],
            pricing_parameters=rdf.cross.PricingParameters(
                valuation_date="2018-02-17T00:00:00Z",
                price_side=rdf.cross.PriceSide.ASK,
            ),
            fields=fields,
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Get a cross analytics FX Forward USD/EUR")
    @pytest.mark.caseid("36597358")
    def test_get_cross_analytics_fx_forward(self, open_session):
        response = rdf.cross.Definition(
            instrument_tag="00102700008910C",
            fx_cross_type=rdf.cross.FxCrossType.FX_FORWARD,
            fx_cross_code="USDEUR",
            traded_cross_rate=123,
            traded_swap_points=123,
            reference_spot_rate=123,
            ndf_fixing_settlement_ccy="",
            legs=[rdf.cross.LegDefinition(end_date="2015-04-09T00:00:00Z")],
            pricing_parameters=rdf.cross.PricingParameters(
                valuation_date="2015-02-02T00:00:00Z",
                price_side=rdf.cross.PriceSide.MID,
            ),
            fields=fields,
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Get cross analytics Non-Deliverable Fx Forward Outright USD/INR")
    @pytest.mark.caseid("36597373")
    def test_get_cross_analytics_fx_non_deliverable_forward(self, open_session):
        response = rdf.cross.Definition(
            instrument_tag="1Y-USDINR",
            fx_cross_type=rdf.cross.FxCrossType.FX_NON_DELIVERABLE_FORWARD,
            fx_cross_code="USDINR",
            traded_cross_rate=123,
            traded_swap_points=123,
            reference_spot_rate=123,
            ndf_fixing_settlement_ccy="",
            legs=[
                rdf.cross.LegDefinition(
                    deal_amount=1000000,
                    contra_amount=65762500,
                    deal_ccy_buy_sell=rdf.cross.BuySell.BUY,
                    tenor="4Y",
                )
            ],
            pricing_parameters=rdf.cross.PricingParameters(
                valuation_date="2017-11-15T00:00:00Z",
            ),
            fields=fields,
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title(
        "Get async cross analytics Non-Deliverable Fx Forward Outright USD/INR"
    )
    @pytest.mark.caseid("36597407")
    async def test_get_async_cross_analytics_fx_non_deliverable_forward(
        self, open_session_async
    ):
        response = await get_async_response_from_definition(
            rdf.cross.Definition(
                instrument_tag="1Y-USDINR",
                fx_cross_type=rdf.cross.FxCrossType.FX_NON_DELIVERABLE_FORWARD,
                fx_cross_code="USDINR",
                traded_cross_rate=123,
                traded_swap_points=123,
                reference_spot_rate=123,
                ndf_fixing_settlement_ccy="",
                legs=[
                    rdf.cross.LegDefinition(
                        deal_amount=1000000,
                        contra_amount=65762500,
                        deal_ccy_buy_sell=rdf.cross.BuySell.BUY,
                        tenor="4Y",
                    )
                ],
                pricing_parameters=rdf.cross.PricingParameters(
                    valuation_date="2017-11-15T00:00:00Z",
                ),
                fields=fields,
            )
        )

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create a cross analytics FX Forward USD/EUR stream")
    @pytest.mark.caseid("36598198")
    def test_create_cross_analytics_fx_forward_stream(self, open_session):
        stream = rdf.cross.Definition(
            instrument_tag="00102700008910C",
            fx_cross_type=rdf.cross.FxCrossType.FX_FORWARD,
            fx_cross_code="USDEUR",
            traded_cross_rate=123,
            traded_swap_points=123,
            reference_spot_rate=123,
            ndf_fixing_settlement_ccy="",
            legs=[rdf.cross.LegDefinition(end_date="2015-04-09T00:00:00Z")],
            pricing_parameters=rdf.cross.PricingParameters(
                valuation_date="2015-02-02T00:00:00Z",
                price_side=rdf.cross.PriceSide.MID,
            ),
            fields=fields,
            extended_params={"instrumentDefinition": {"fxCrossCode": "CHFJPY"}},
        ).get_stream(session=open_session)

        stream.open()

        check_stream_state_and_df_from_stream(stream=stream, expected_value="CHFJPY")

    @allure.title(
        "Create invalid cross analytics Non-Deliverable Fx Forward Outright USD/INR and get RDError"
    )
    @pytest.mark.caseid("38515599")
    def test_create_invalid_cross_analytics_fx_non_deliverable_forward(
        self, open_session
    ):
        with pytest.raises(RDError) as error:
            rdf.cross.Definition(
                instrument_tag="1Y-USDINR",
                fields=fields,
            ).get_data()
        assert (
            str(error.value)
            == "Error code 400 | The fxCrossType cannot be found, in the request, from the expected path instrumentDefinition.fxCrossType for 'instrumentType' FxCross"
        )

    @allure.title("Create a cross definition with extended parameters")
    @pytest.mark.caseid("C38515601")
    def test_get_cross_with_extended_params(self, open_session):
        response = rdf.cross.Definition(
            fx_cross_type=rdf.cross.FxCrossType.FX_SWAP,
            fx_cross_code="USDINR",
            legs=[
                rdf.cross.LegDefinition(
                    contra_amount=1234,
                    deal_ccy_buy_sell=rdf.cross.BuySell.SELL,
                    tenor="10Y",
                )
            ],
            fields=fields,
            extended_params={
                "instrumentDefinition": {
                    "legs": [
                        {
                            "tenor": "4Y",
                            "dealCcyBuySell": "Buy",
                            "contraAmount": 65762500,
                            "dealAmount": 1000000,
                        }
                    ],
                    "fxCrossType": "FxNonDeliverableForward",
                    "fxCrossCode": "USDINR",
                },
                "pricingParameters": {"valuationDate": "2017-11-15T00:00:00Z"},
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == cross_universe
        ), f"Extended params are applied incorrectly"
