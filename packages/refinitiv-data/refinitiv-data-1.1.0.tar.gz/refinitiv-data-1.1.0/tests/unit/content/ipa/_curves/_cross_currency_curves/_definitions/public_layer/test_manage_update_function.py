from refinitiv.data.content.ipa.curves._cross_currency_curves import definitions
from refinitiv.data.content.ipa.curves._cross_currency_curves.definitions import manage
from refinitiv.data.delivery._data._response import Response
from tests.unit.conftest import StubResponse, StubSession


def test_update_function():
    # given
    response = StubResponse(
        {
            "curveDefinition": {
                "baseCurrency": "EUR",
                "baseIndexName": "ESTR",
                "name": "rename curve",
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
                "updateDateTime": "2022-12-08T03:31:56.915952Z",
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
    response = manage.update(
        session=session,
        curve_definition=definitions.CrossCurrencyCurveUpdateDefinition(
            id="7bdb00f3-0a48-40be-ace2-6d3cfd0e8e59",
            source="SourceName",
            name="rename curve",
            base_currency="EUR",
            base_index_name="ESTR",
            quoted_currency="USD",
            quoted_index_name="SOFR",
            is_non_deliverable=False,
        ),
        segments=[
            definitions.CrossCurrencyInstrumentsSegment(
                start_date="2021-01-01",
                constituents=definitions.CrossCurrencyConstituentsDescription(
                    fx_forwards=[
                        definitions.FxForwardInstrumentDescription(
                            instrument_definition=definitions.FxForwardInstrumentDefinition(
                                instrument_code="EUR1M=",
                                tenor="1M",
                                is_non_deliverable=False,
                                quotation_mode=definitions.QuotationMode.OUTRIGHT,
                            )
                        )
                    ]
                ),
            )
        ],
    )

    # then
    assert isinstance(response, Response)
