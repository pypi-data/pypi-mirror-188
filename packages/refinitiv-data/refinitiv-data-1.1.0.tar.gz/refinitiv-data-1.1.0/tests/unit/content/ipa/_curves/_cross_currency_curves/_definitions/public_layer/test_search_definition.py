from refinitiv.data.content.ipa.curves._cross_currency_curves.definitions import search
from tests.unit.conftest import StubResponse, StubSession


def test_search_definition():
    # given
    response = StubResponse(
        {
            "data": [
                {
                    "curveDefinitions": [
                        {
                            "baseCurrency": "EUR",
                            "baseIndexName": "EURIBOR",
                            "name": "EUR CHF FxCross",
                            "quotedCurrency": "CHF",
                            "quotedIndexName": "LIBOR",
                            "source": "Refinitiv",
                            "isNonDeliverable": False,
                            "mainConstituentAssetClass": "Swap",
                            "riskType": "CrossCurrency",
                            "isFallbackForFxCurveDefinition": True,
                            "firstHistoricalAvailabilityDate": "2017-01-10",
                            "id": "1146241a-e32f-45f5-9309-02c959e97b96",
                        }
                    ]
                }
            ]
        }
    )
    session = StubSession(is_open=True, response=response)
    definition = search.Definition(base_currency="EUR", quoted_currency="CHF")

    # when
    response = definition.get_data(session)

    # then
    assert response.data.raw
    assert not response.data.df.empty
