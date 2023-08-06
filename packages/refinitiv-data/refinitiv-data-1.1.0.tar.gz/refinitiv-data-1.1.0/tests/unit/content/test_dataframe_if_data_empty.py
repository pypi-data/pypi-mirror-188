import pytest

from refinitiv.data.content import (
    historical_pricing as hp,
    custom_instruments,
    ownership,
    fundamental_and_reference,
    news,
)

import refinitiv.data.content.ipa.financial_contracts as rdf
from tests.unit.conftest import StubSession, StubConfig
from tests.unit.content.data_for_test_dataframe_if_data_empty import (
    HP_EVENTS,
    CUSTOM_INSTRUMENTS_EVENTS,
    OWNERSHIP_ORG_INFO,
    FUNDAMENTAL_AND_REFERENCE_UDF,
    FUNDAMENTAL_AND_REFERENCE_RDP,
    CAP_FLOOR,
    NEWS_HEADLINES_UDF,
)


@pytest.mark.parametrize(
    "definition, mock_response",
    [
        (hp.events.Definition(universe="EUR=", end="09-09-2021T13:45"), HP_EVENTS),
        (
            custom_instruments.events.Definition(
                universe="S)Batman_9ccfafd6.ertvd-111923", end="09-09-2021T13:45"
            ),
            CUSTOM_INSTRUMENTS_EVENTS,
        ),
        (ownership.org_info.Definition("TRI.N"), OWNERSHIP_ORG_INFO),
        (
            fundamental_and_reference.Definition(["IBM"], ["TR.Volume"]),
            FUNDAMENTAL_AND_REFERENCE_UDF,
        ),
        (
            news.headlines.Definition(
                "Refinitiv", date_from="20.03.1960", date_to="20.03.1961", count=3
            ),
            NEWS_HEADLINES_UDF,
        ),
    ],
)
def test_return_empty_df_if_data_empty(definition, mock_response):
    # given
    session = StubSession(is_open=True, response=mock_response)

    # when
    response = definition.get_data(session=session)

    # then
    assert response.data.df.empty


@pytest.mark.parametrize(
    "definition, config, mock_response",
    [
        (
            fundamental_and_reference.Definition(["IBM"], ["TR.Volume"]),
            StubConfig(
                {
                    "apis.data.datagrid": {
                        "url": "/data/datagrid/beta1",
                        "underlying-platform": "rdp",
                        "endpoints.standard": "/",
                    },
                    "raise_exception_on_error": True,
                }
            ),
            FUNDAMENTAL_AND_REFERENCE_RDP,
        ),
    ],
)
def test_return_empty_df_if_data_empty_for_rdp_platform(
    definition, config, mock_response
):
    # given
    session = StubSession(response=mock_response, config=config, is_open=True)

    # when
    response = definition.get_data(session=session)

    # then
    assert response.data.df.empty


def test_return_empty_df_if_data_empty_for_financial_contracts():
    # given

    session = StubSession(is_open=True, response=CAP_FLOOR)

    # when
    definition = rdf.cap_floor.Definition(
        instrument_tag="CapOnCms",
        stub_rule=rdf.cap_floor.StubRule.MATURITY,
        notional_ccy="USD",
        start_date="2018-06-15",
        end_date="2022-06-15",
        notional_amount=1000000,
        index_name="Composite",
        index_tenor="5Y",
        interest_calculation_method="Dcb_Actual_360",
        interest_payment_frequency=rdf.cap_floor.Frequency.QUARTERLY,
        buy_sell=rdf.cap_floor.BuySell.BUY,
        cap_strike_percent=1,
        pricing_parameters=rdf.cap_floor.PricingParameters(
            skip_first_cap_floorlet=False, valuation_date="2020-02-07"
        ),
    )
    response = definition.get_data(session=session)

    # then
    assert response.data.df.empty
