import refinitiv.data.content.ipa.financial_contracts as rdf
from tests.integration.conftest import is_open

from tests.integration.constants_list import HttpStatusCode


def option_definition_02():
    definition = rdf.option.Definition(
        instrument_code="FCHI560000L5.p",
        underlying_type=rdf.option.UnderlyingType.ETI,
        underlying_definition=rdf.option.EtiUnderlyingDefinition("FCHI560000L5.p"),
        fields=[
            "MarketValueInDealCcy",
            "DeltaPercent",
            "GammaPercent",
            "RhoPercent",
            "ThetaPercent",
            "VegaPercent",
            "ErrorCode",
            "ErrorMessage",
        ],
    )

    return definition


def check_http_status_is_success_and_df_value_not_empty(response):
    status = response.http_status
    df = response.data.df
    assert status["http_status_code"] == HttpStatusCode.TWO_HUNDRED, (
        f"Actual status code is {status['http_status_code']}, "
        f"Error: {response.http_status['error']}"
    )

    assert df is not None, f"DataFrame is {df}"
    assert not df.empty, f"DataFrame is empty: {df}"
    assert not bool(df.ErrorMessage[0]), f"{df.ErrorMessage[0]}"
    assert df.GammaPercent is not None, f"{df.GammaPercent}"


def check_stream_state_and_df_from_stream(stream):
    df = stream.get_snapshot()

    assert is_open(stream), f"Stream is not open"
    assert df is not None, f"DataFrame is {df}"
    assert not df.empty, f"DataFrame is empty: {df}"
    assert df.GammaPercent is not None, f"{df.GammaPercent}"
    assert not bool(df.ErrorMessage[0]), f"{df.ErrorMessage[0]}"


option_universe = {
    "instrumentType": "Option",
    "instrumentDefinition": {
        "InstrumentTag": "my tag",
        "tenor": "5M",
        "notionalCcy": "AUD",
        "underlyingDefinition": {"fxCrossCode": "AUDUSD"},
        "underlyingType": "Fx",
        "strike": 265,
    },
    "pricingParameters": {
        "fxSpotObject": {"bid": 0.7387, "ask": 0.7387, "mid": 0.7387},
        "priceSide": "Mid",
        "pricingModelType": "BlackScholes",
        "valuationDate": "2018-08-06",
    },
}
