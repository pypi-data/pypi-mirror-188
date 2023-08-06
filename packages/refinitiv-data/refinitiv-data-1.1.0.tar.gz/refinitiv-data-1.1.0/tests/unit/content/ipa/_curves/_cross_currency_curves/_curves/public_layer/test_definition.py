from refinitiv.data.content.ipa.curves._cross_currency_curves import curves
from tests.unit.conftest import StubResponse, StubSession


def test_definition():
    # given
    response = StubResponse(
        {
            "data": [
                {
                    "curveDefinition": {
                        "baseCurrency": "EUR",
                        "baseIndexName": "ESTR",
                        "quotedCurrency": "USD",
                        "quotedIndexName": "SOFR",
                        "crossCurrencyDefinitions": [
                            {
                                "baseCurrency": "EUR",
                                "baseIndexName": "ESTR",
                                "name": "EUR ESTR/USD SOFR FxCross",
                                "quotedCurrency": "USD",
                                "quotedIndexName": "SOFR",
                                "source": "Refinitiv",
                                "isNonDeliverable": False,
                                "mainConstituentAssetClass": "Swap",
                                "riskType": "CrossCurrency",
                                "id": "c9f2e9fb-b04b-4140-8377-8b7e47391486",
                                "ignoreExistingDefinition": False,
                            }
                        ],
                    },
                    "curveParameters": {
                        "valuationDate": "2021-10-06",
                        "interpolationMode": "Linear",
                        "extrapolationMode": "Constant",
                        "turnAdjustments": {},
                        "ignorePivotCurrencyHolidays": False,
                        "useDelayedDataIfDenied": False,
                        "ignoreInvalidInstrument": True,
                        "marketDataLookBack": {"value": 10, "unit": "CalendarDay"},
                    },
                    "curve": {
                        "fxCrossScalingFactor": 1.0,
                        "fxSwapPointScalingFactor": 10000.0,
                        "curvePoints": [
                            {
                                "tenor": "SPOT",
                                "startDate": "2021-10-08",
                                "endDate": "2021-10-08",
                                "swapPoint": {"bid": 0.0, "ask": 0.0, "mid": 0.0},
                                "outright": {
                                    "bid": 1.1556,
                                    "ask": 1.156,
                                    "mid": 1.1558,
                                },
                            },
                            {
                                "tenor": "9M",
                                "startDate": "2021-10-08",
                                "endDate": "2022-07-08",
                                "instruments": [{"instrumentCode": "EUR9M="}],
                                "swapPoint": {
                                    "bid": 66.25000000000102,
                                    "ask": 69.42999999999921,
                                    "mid": 67.84000000000012,
                                },
                                "outright": {
                                    "bid": 1.162225,
                                    "ask": 1.1629429999999998,
                                    "mid": 1.1625839999999998,
                                },
                            },
                        ],
                    },
                }
            ]
        }
    )
    session = StubSession(is_open=True, response=response)
    definition = curves.Definition(
        curve_definition=curves.FxForwardCurveDefinition(
            base_currency="EUR",
            base_index_name="ESTR",
            quoted_currency="USD",
            quoted_index_name="SOFR",
        ),
        curve_parameters=curves.FxForwardCurveParameters(valuation_date="2021-10-06"),
    )

    # when
    response = definition.get_data(session)

    # then
    assert response.data.raw
    assert not response.data.df.empty
