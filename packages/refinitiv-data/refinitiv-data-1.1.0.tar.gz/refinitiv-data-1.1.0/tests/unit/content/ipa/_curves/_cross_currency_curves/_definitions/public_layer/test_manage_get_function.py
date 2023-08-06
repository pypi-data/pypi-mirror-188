from refinitiv.data.content.ipa.curves._cross_currency_curves.definitions import manage
from refinitiv.data.delivery._data._response import Response
from tests.unit.conftest import StubResponse, StubSession


def test_get_function():
    # given
    response = StubResponse(
        {
            "curveDefinition": {
                "baseCurrency": "EUR",
                "baseIndexName": "ESTR",
                "name": "Name of the Curve854",
                "quotedCurrency": "USD",
                "quotedIndexName": "SOFR",
                "source": "SourceName",
                "isNonDeliverable": False,
                "mainConstituentAssetClass": "FxForward",
                "riskType": "CrossCurrency",
                "isFallbackForFxCurveDefinition": False,
                "firstHistoricalAvailabilityDate": "2021-01-01",
                "id": "7bdb00f3-0a48-40be-ace2-6d3cfd0e8e59",
            },
            "curveInfo": {
                "creationDateTime": "2022-12-08T03:19:00.011739Z",
                "creationUserId": "GESG1-111923",
                "updateDateTime": "2022-12-08T03:19:00.011739Z",
                "updateUserId": "GESG1-111923",
            },
            "segments": [
                {
                    "constituents": {
                        "fxForwards": [
                            {
                                "instrumentDefinition": {
                                    "instrumentCode": "EUR1M=",
                                    "tenor": "1M",
                                    "isNonDeliverable": False,
                                    "quotationMode": "Outright",
                                }
                            }
                        ]
                    },
                    "startDate": "2021-01-01",
                }
            ],
        }
    )
    session = StubSession(is_open=True, response=response)
    response = manage.get(
        session=session,
        id="7bdb00f3-0a48-40be-ace2-6d3cfd0e8e59",
    )

    # then
    assert isinstance(response, Response)
