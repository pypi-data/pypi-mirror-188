from refinitiv.data.content._df_builder import build_empty_df
from refinitiv.data.content.search._data_provider import SearchData
from refinitiv.data.content import search

MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE = {
    "Total": 606753,
    "Hits": [
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "ICE-US FCOJ-A Futures Electronic Commodity Future Continuation 1, Commodity Future, Intercontinental Exchange US",
            "PermID": "21480992515",
            "PI": "16866",
            "RIC": "OJc1",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "ICE-US FCOJ-A Futures Electronic Commodity Future Chain Chain Contracts, Commodity Future, Intercontinental Exchange US",
            "PermID": "21481145637",
            "PI": "73603165",
            "RIC": "0#OJ:",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "ICE-US FCOJ-A Futures Electronic Commodity Future Continuation 2, Commodity Future, Intercontinental Exchange US",
            "PermID": "21480996404",
            "PI": "1095831",
            "RIC": "OJc2",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "CFTC Future and Option Commitments FRZN Concentrated Orange Juice - ICE Futures U.S. Contract Total Open Interest Contracts of 15000 Pounds 040701, Energy Statistic, Commodity Futures Trading Commission",
            "PermID": "21481534494",
            "PI": "7956248",
            "RIC": "3CFTC040701OI",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "CFTC Future and Option Commitments FRZN Concentrated Orange Juice - ICE Futures U.S. Managed Net Contracts of 15000 Pounds 040701, Energy Statistic, Commodity Futures Trading Commission",
            "PermID": "21478081931",
            "PI": "63261287",
            "RIC": "3040701MNET",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "CFTC Future and Option Commitments FRZN Concentrated Orange Juice - ICE Futures U.S. Producer Net Contracts of 15000 Pounds 040701, Energy Statistic, Commodity Futures Trading Commission",
            "PermID": "21478080548",
            "PI": "63259739",
            "RIC": "3040701PNET",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "CFTC Future and Option Commitments FRZN Concentrated Orange Juice - ICE Futures U.S. Swap Net Contracts of 15000 Pounds 040701, Energy Statistic, Commodity Futures Trading Commission",
            "PermID": "21478081878",
            "PI": "63261232",
            "RIC": "3040701SNET",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "CFTC Future and Option Commitments FRZN Concentrated Orange Juice - ICE Futures U.S. Other Net Contracts of 15000 Pounds 040701, Energy Statistic, Commodity Futures Trading Commission",
            "PermID": "21478082733",
            "PI": "63262308",
            "RIC": "3040701ONET",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "ICE-US FCOJ-A Futures Electronic Commodity Future Jan 2023, Commodity Future, Intercontinental Exchange US",
            "PermID": "21732946183",
            "PI": "413283469",
            "RIC": "OJF3",
        },
        {
            "BusinessEntity": "QUOTExCOMMODITY",
            "DocumentTitle": "ICE-US FCOJ-A Futures Electronic Commodity Future Mar 2023, Commodity Future, Intercontinental Exchange US",
            "PermID": "21744573309",
            "PI": "427951324",
            "RIC": "OJH3",
        },
    ],
    "Navigators": {
        "MaturityDate": {
            "Buckets": [
                {
                    "Label": "2020-01-01",
                    "Filter": "(MaturityDate ge 2020-01-01 and MaturityDate lt 2021-01-01)",
                    "Count": 408,
                    "BusinessEntity": {
                        "Buckets": [
                            {
                                "Label": "INSTRUMENTxFIXEDINCOMExGOVCORP",
                                "Count": 408,
                                "sum_FaceOutstandingUSD": 48138904788.0,
                            }
                        ]
                    },
                },
                {
                    "Label": "2021-01-01",
                    "Filter": "(MaturityDate ge 2021-01-01 and MaturityDate lt 2022-01-01)",
                    "Count": 561,
                    "BusinessEntity": {
                        "Buckets": [
                            {
                                "Label": "INSTRUMENTxFIXEDINCOMExGOVCORP",
                                "Count": 561,
                                "sum_FaceOutstandingUSD": 53567730098.0,
                            }
                        ]
                    },
                },
                {
                    "Label": "2022-01-01",
                    "Filter": "(MaturityDate ge 2022-01-01 and MaturityDate lt 2023-01-01)",
                    "Count": 73963,
                    "BusinessEntity": {
                        "Buckets": [
                            {
                                "Label": "INSTRUMENTxFIXEDINCOMExGOVCORP",
                                "Count": 73963,
                                "sum_FaceOutstandingUSD": 1523293417439.9312,
                            }
                        ]
                    },
                },
                {
                    "Label": "2023-01-01",
                    "Filter": "(MaturityDate ge 2023-01-01 and MaturityDate lt 2024-01-01)",
                    "Count": 309738,
                    "BusinessEntity": {
                        "Buckets": [
                            {
                                "Label": "INSTRUMENTxFIXEDINCOMExGOVCORP",
                                "Count": 309738,
                                "sum_FaceOutstandingUSD": 8394626310316.518,
                            }
                        ]
                    },
                },
                {
                    "Label": "2024-01-01",
                    "Filter": "(MaturityDate ge 2024-01-01 and MaturityDate lt 2025-01-01)",
                    "Count": 132494,
                    "BusinessEntity": {
                        "Buckets": [
                            {
                                "Label": "INSTRUMENTxFIXEDINCOMExGOVCORP",
                                "Count": 132494,
                                "sum_FaceOutstandingUSD": 5237852833418.076,
                            }
                        ]
                    },
                },
                {
                    "Label": "2025-01-01",
                    "Filter": "MaturityDate ge 2025-01-01",
                    "Count": 89589,
                    "BusinessEntity": {
                        "Buckets": [
                            {
                                "Label": "INSTRUMENTxFIXEDINCOMExGOVCORP",
                                "Count": 89589,
                                "sum_FaceOutstandingUSD": 5333550586785.237,
                            }
                        ]
                    },
                },
            ]
        }
    },
}


def test_workspace():
    assert hasattr(search, "Definition")


def test_attributes():
    # given
    excepted_attributes = [
        "_query",
        "_view",
        "_filter",
        "_order_by",
        "_boost",
        "_select",
        "_top",
        "_skip",
        "_group_by",
        "_group_count",
        "_navigators",
        "_features",
        "_scope",
        "_terms",
        "_extended_params",
        #
        "_kwargs",
        "_data_type",
        "_content_type",
        "_provider",
    ]

    # when
    definition = search.Definition()
    attributes = list(definition.__dict__.keys())

    # then
    assert len(attributes) == len(excepted_attributes)
    assert set(attributes) == set(excepted_attributes)


def test_definition_search_repr():
    # given
    definition = search.Definition()
    obj_id = hex(id(definition))
    expected_value = f"<refinitiv.data.content.search.Definition object at {obj_id} {{query='None'}}>"

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value


def test_search_navigators():
    response = SearchData(MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE, build_empty_df)

    assert (
        response.hits[0].DocumentTitle
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Hits"][0]["DocumentTitle"]
    )
    assert (
        response.hits[0].BusinessEntity
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Hits"][0]["BusinessEntity"]
    )
    assert (
        response.hits[0].PermID
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Hits"][0]["PermID"]
    )
    assert response.hits[0].PI == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Hits"][0]["PI"]
    assert (
        response.hits[0].RIC == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Hits"][0]["RIC"]
    )
    assert (
        response.navigators["MaturityDate"].buckets[0].label
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Navigators"]["MaturityDate"][
            "Buckets"
        ][0]["Label"]
    )
    assert (
        response.navigators["MaturityDate"].buckets[0].count
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Navigators"]["MaturityDate"][
            "Buckets"
        ][0]["Count"]
    )
    assert response.navigators["MaturityDate"].buckets[0].navigator.name
    assert response.navigators["MaturityDate"].name == "MaturityDate"
    assert (
        response.navigators["MaturityDate"].buckets[0].navigator.buckets[0].label
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Navigators"]["MaturityDate"][
            "Buckets"
        ][0]["BusinessEntity"]["Buckets"][0]["Label"]
    )
    assert (
        response.navigators["MaturityDate"].buckets[0]["Filter"]
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Navigators"]["MaturityDate"][
            "Buckets"
        ][0]["Filter"]
    )
    assert (
        response.navigators["MaturityDate"]
        .buckets[0]
        .navigator.buckets[0]["sum_FaceOutstandingUSD"]
        == MOCKED_SEARCH_NAVIGATORS_RAW_RESPONSE["Navigators"]["MaturityDate"][
            "Buckets"
        ][0]["BusinessEntity"]["Buckets"][0]["sum_FaceOutstandingUSD"]
    )
