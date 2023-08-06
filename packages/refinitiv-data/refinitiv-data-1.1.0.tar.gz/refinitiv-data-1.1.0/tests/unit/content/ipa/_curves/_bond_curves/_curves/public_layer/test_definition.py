from refinitiv.data.content.ipa.curves._bond_curves import curves
from tests.unit.conftest import StubResponse, StubSession


def test_search_definition():
    # given
    response = StubResponse(
        {
            "data": [
                {
                    "curveParameters": {
                        "calculateParYield": False,
                        "priceSide": "Mid",
                        "calendarAdjustment": "Calendar",
                        "calendars": ["EMU_FI"],
                        "calibrationModel": "BasisSpline",
                        "useDurationWeightedMinimization": False,
                        "returnCalibratedParameters": False,
                        "valuationDate": "2022-12-08",
                        "useDelayedDataIfDenied": False,
                    },
                    "curveDefinition": {
                        "name": "Eurozone GOV Par Benchmark Curve",
                        "issuerType": "Sovereign",
                        "country": "EP",
                        "source": "Refinitiv",
                        "currency": "EUR",
                        "curveSubType": "GovernmentBenchmark",
                        "id": "b302758b-1049-49b5-ba3b-da726712e133",
                    },
                    "curvePoints": [
                        {
                            "endDate": "2023-03-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.9954433125749454,
                            "ratePercent": 1.8694729555234435,
                            "tenor": "3M",
                        },
                        {
                            "endDate": "2023-06-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.9908068253445579,
                            "ratePercent": 1.8694729555234213,
                            "tenor": "6M",
                        },
                        {
                            "endDate": "2023-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.981648349586145,
                            "ratePercent": 1.8694729555234213,
                            "tenor": "1Y",
                        },
                        {
                            "endDate": "2024-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.9636822499969483,
                            "ratePercent": 1.8668953382534603,
                            "tenor": "2Y",
                        },
                        {
                            "endDate": "2025-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.9459012159432262,
                            "ratePercent": 1.8711961113877074,
                            "tenor": "3Y",
                        },
                        {
                            "endDate": "2026-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.9285423675021957,
                            "ratePercent": 1.8707653196890606,
                            "tenor": "4Y",
                        },
                        {
                            "endDate": "2027-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.9115020825793422,
                            "ratePercent": 1.8705068455443064,
                            "tenor": "5Y",
                        },
                        {
                            "endDate": "2028-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.8950010766357648,
                            "ratePercent": 1.866036146990635,
                            "tenor": "6Y",
                        },
                        {
                            "endDate": "2029-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.8783093544751289,
                            "ratePercent": 1.870949944479694,
                            "tenor": "7Y",
                        },
                        {
                            "endDate": "2030-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.8621909282465827,
                            "ratePercent": 1.8707653196890606,
                            "tenor": "8Y",
                        },
                        {
                            "endDate": "2031-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.8463683017414042,
                            "ratePercent": 1.87062172286101,
                            "tenor": "9Y",
                        },
                        {
                            "endDate": "2032-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.8312147776735689,
                            "ratePercent": 1.86586430960769,
                            "tenor": "10Y",
                        },
                        {
                            "endDate": "2034-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.8005808057529976,
                            "ratePercent": 1.8707653196890606,
                            "tenor": "12Y",
                        },
                        {
                            "endDate": "2037-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.7572703576225682,
                            "ratePercent": 1.870851477883062,
                            "tenor": "15Y",
                        },
                        {
                            "endDate": "2042-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.6902535080485741,
                            "ratePercent": 1.8707653196890606,
                            "tenor": "20Y",
                        },
                        {
                            "endDate": "2047-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.629167510093972,
                            "ratePercent": 1.8707136248076406,
                            "tenor": "25Y",
                        },
                        {
                            "endDate": "2052-12-12",
                            "startDate": "2022-12-12",
                            "discountFactor": 0.5743303216160913,
                            "ratePercent": 1.8656924725146018,
                            "tenor": "30Y",
                        },
                    ],
                    "constituents": {
                        "creditInstruments": {
                            "EUR": {
                                "bonds": [
                                    {
                                        "fields": {
                                            "bid": {"value": 99.407},
                                            "ask": {"value": 99.507},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU10YT=RR",
                                            "fixedRatePercent": 1.7,
                                            "endDate": "2032-08-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:08JUL2022 DMC:F EMC:S FRCD:15AUG2023 FRQ:1 ISSUE:08JUL2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 88.906},
                                            "ask": {"value": 89.065},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU15YT=RR",
                                            "fixedRatePercent": 1.0,
                                            "endDate": "2038-05-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:29APR2022 DMC:F EMC:S FRCD:15MAY2023 FRQ:1 ISSUE:29APR2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 99.983},
                                            "ask": {"value": 99.985},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU1MT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2022-12-14",
                                            "template": "ACC:A0 CFADJ:NO CLDR:EMU_FI DMC:F EMC:S ISSUE:15DEC2021 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 97.951},
                                            "ask": {"value": 98.001},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU1YT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2023-11-22",
                                            "template": "ACC:A0 CFADJ:NO CLDR:EMU_FI DMC:F EMC:S ISSUE:23NOV2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 124.449},
                                            "ask": {"value": 124.811},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU20YT=RR",
                                            "fixedRatePercent": 3.25,
                                            "endDate": "2042-07-04",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:04JUL2010 DMC:F EMC:S FRCD:04JUL2011 FRQ:1 ISSUE:23JUL2010 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 116.551},
                                            "ask": {"value": 116.754},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU25YT=RR",
                                            "fixedRatePercent": 2.5,
                                            "endDate": "2046-08-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:28FEB2014 DMC:F EMC:S FRCD:15AUG2015 FRQ:1 ISSUE:28FEB2014 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 100.401},
                                            "ask": {"value": 100.521},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU2YT=RR",
                                            "fixedRatePercent": 2.2,
                                            "endDate": "2024-12-12",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:10NOV2022 DMC:F EMC:S FRCD:12DEC2023 FRQ:1 ISSUE:10NOV2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 63.304},
                                            "ask": {"value": 63.468},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU30YT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2052-08-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:15AUG2021 DMC:F EMC:S FRCD:15AUG2022 FRQ:1 ISSUE:08SEP2021 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 99.431},
                                            "ask": {"value": 99.461},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU3MT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2023-04-13",
                                            "template": "ACC:A0 CFADJ:NO CLDR:EMU_FI DMC:F EMC:S ISSUE:13APR2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 97.084},
                                            "ask": {"value": 97.204},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU3YT=RR",
                                            "fixedRatePercent": 0.5,
                                            "endDate": "2025-02-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:16JAN2015 DMC:F EMC:S FRCD:15FEB2016 FRQ:1 ISSUE:16JAN2015 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 96.014},
                                            "ask": {"value": 96.134},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU4YT=RR",
                                            "fixedRatePercent": 0.5,
                                            "endDate": "2026-02-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:15JAN2016 DMC:F EMC:S FRCD:15FEB2017 FRQ:1 ISSUE:15JAN2016 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 97.875},
                                            "ask": {"value": 97.967},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU5YT=RR",
                                            "fixedRatePercent": 1.3,
                                            "endDate": "2027-10-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:30JUN2022 DMC:F EMC:S FRCD:15OCT2023 FRQ:1 ISSUE:30JUN2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 98.969},
                                            "ask": {"value": 99.014},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU6MT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2023-06-21",
                                            "template": "ACC:A0 CFADJ:NO CLDR:EMU_FI DMC:F EMC:S ISSUE:22JUN2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 93.944},
                                            "ask": {"value": 94.019},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU6YT=RR",
                                            "fixedRatePercent": 0.5,
                                            "endDate": "2028-02-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:12JAN2018 DMC:F EMC:S FRCD:15FEB2019 FRQ:1 ISSUE:12JAN2018 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 102.046},
                                            "ask": {"value": 102.306},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU7YT=RR",
                                            "fixedRatePercent": 2.1,
                                            "endDate": "2029-11-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:20OCT2022 DMC:F EMC:S FRCD:15NOV2023 FRQ:1 ISSUE:20OCT2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 88.543},
                                            "ask": {"value": 88.663},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU8YT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2030-02-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:10JAN2020 DMC:F EMC:S FRCD:15FEB2021 FRQ:1 ISSUE:10JAN2020 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 98.381},
                                            "ask": {"value": 98.444},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU9MT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2023-09-20",
                                            "template": "ACC:A0 CFADJ:NO CLDR:EMU_FI DMC:F EMC:S ISSUE:21SEP2022 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                    {
                                        "fields": {
                                            "bid": {"value": 86.954},
                                            "ask": {"value": 87.104},
                                        },
                                        "instrumentDefinition": {
                                            "instrumentCode": "EU9YT=RR",
                                            "fixedRatePercent": 0.0,
                                            "endDate": "2031-02-15",
                                            "template": "ACC:AA CCM:BBAA CFADJ:NO CLDR:EMU_FI DATED:08JAN2021 DMC:F EMC:S FRCD:15FEB2022 FRQ:1 ISSUE:08JAN2021 NOTIONAL:1 PX:C PXRND:1E-5:NEAR REFDATE:MATURITY RP:1 SETTLE:2WD XD:NO",
                                            "quotationMode": "PercentCleanPrice",
                                        },
                                    },
                                ]
                            }
                        }
                    },
                }
            ]
        }
    )
    session = StubSession(is_open=True, response=response)
    definition = curves.Definition(
        curve_definition=curves.CreditCurveDefinition(
            reference_entity="0#EUGOVPBMK=R",
            reference_entity_type=curves.ReferenceEntityType.CHAIN_RIC,
        )
    )

    # when
    response = definition.get_data(session)

    # then
    assert response.data.raw
    assert not response.data.df.empty
