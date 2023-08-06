from refinitiv.data.content.ipa.curves._cross_currency_curves.triangulate_definitions import (
    search,
)
from refinitiv.data.content.ipa.curves._cross_currency_curves.triangulate_definitions._data_provider import (
    TriangulateDefinitionsData,
)
from tests.unit.conftest import StubResponse, StubSession


def test_search_definition():
    # given
    response = StubResponse(
        {
            "data": [
                {
                    "directCurveDefinitions": [
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
                            "id": "1146241a-e32f-45f5-9309-02c959e97b96",
                            "isFallbackForFxCurveDefinition": True,
                        }
                    ],
                    "indirectCurveDefinitions": [
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve rtf",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "fb633ff4-8c62-4c62-86e4-54637a4f11a3",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve rtf",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "fb633ff4-8c62-4c62-86e4-54637a4f11a3",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve rtfrr",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "1f7c7066-4042-407d-847f-f632cd1cf73f",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve rtfrr",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "1f7c7066-4042-407d-847f-f632cd1cf73f",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve rtf77rr",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "37eb1c0b-0bb0-4305-a4d8-2bb4a523d549",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve rtf77rr",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "37eb1c0b-0bb0-4305-a4d8-2bb4a523d549",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve223",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "02b711e1-c221-4044-b2c3-a4c2ca886a60",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve223",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "02b711e1-c221-4044-b2c3-a4c2ca886a60",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve78874",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "f02d9b4b-ec08-4cd3-9193-c325c3787079",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve78874",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "f02d9b4b-ec08-4cd3-9193-c325c3787079",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "EURIBOR",
                                    "name": "EUR USD FxCross",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "334b89f6-e272-4900-ad1e-c023b516ae13",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "EURIBOR",
                                    "name": "EUR USD FxCross",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "334b89f6-e272-4900-ad1e-c023b516ae13",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
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
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
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
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "EONIA",
                                    "name": "EUR EONIA/USD SOFR FxCross",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "4246920e-fb65-4b62-aa59-fa492ae6b1c2",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "EONIA",
                                    "name": "EUR EONIA/USD SOFR FxCross",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "4246920e-fb65-4b62-aa59-fa492ae6b1c2",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "a41be363-5709-41d7-bf6d-4233cd815070",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "a41be363-5709-41d7-bf6d-4233cd815070",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve78954",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "c0086a8a-3c3b-4adc-a217-8c95b93a4d8d",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "LIBOR",
                                    "name": "USD CHF FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "LIBOR",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "3475e008-de92-4b0c-a60c-6184d3c9afa8",
                                    "isFallbackForFxCurveDefinition": True,
                                },
                            ]
                        },
                        {
                            "crossCurrencyDefinitions": [
                                {
                                    "baseCurrency": "EUR",
                                    "baseIndexName": "ESTR",
                                    "name": "Name of the Curve78954",
                                    "quotedCurrency": "USD",
                                    "quotedIndexName": "SOFR",
                                    "source": "SourceName",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "FxForward",
                                    "riskType": "CrossCurrency",
                                    "id": "c0086a8a-3c3b-4adc-a217-8c95b93a4d8d",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                                {
                                    "baseCurrency": "USD",
                                    "baseIndexName": "SOFR",
                                    "name": "USD SOFR/CHF SARON FxCross",
                                    "quotedCurrency": "CHF",
                                    "quotedIndexName": "SARON",
                                    "source": "Refinitiv",
                                    "isNonDeliverable": False,
                                    "mainConstituentAssetClass": "Swap",
                                    "riskType": "CrossCurrency",
                                    "id": "6e07c9a4-0b99-47f1-b549-0a6e64081c9e",
                                    "isFallbackForFxCurveDefinition": False,
                                },
                            ]
                        },
                    ],
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
    assert isinstance(response.data, TriangulateDefinitionsData)
