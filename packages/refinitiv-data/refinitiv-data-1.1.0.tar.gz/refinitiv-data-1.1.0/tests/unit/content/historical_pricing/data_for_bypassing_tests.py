from tests.unit.conftest import StubResponse

# fmt: off
INTRA_WITH_DATES_0_1 = [
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-05-25T23:59:00.000000000Z",
                        90.75,
                        90.7,
                        90.75,
                        90.7,
                        17,
                        2289,
                    ],
                    [
                        "2022-05-25T23:58:00.000000000Z",
                        90.75,
                        90.7,
                        90.74,
                        90.72,
                        20,
                        1778,
                    ],
                    [
                        "2022-05-25T23:57:00.000000000Z",
                        90.75,
                        90.7,
                        90.72,
                        90.74,
                        22,
                        3790,
                    ],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-05-25T23:56:00.000000000Z",
                        90.8,
                        90.66,
                        90.7,
                        90.73,
                        19,
                        2721,
                    ],
                    [
                        "2022-05-25T23:55:00.000000000Z",
                        90.74,
                        90.68,
                        90.74,
                        90.7,
                        16,
                        1525,
                    ],
                    [
                        "2022-05-25T23:54:00.000000000Z",
                        90.77,
                        90.68,
                        90.7,
                        90.74,
                        22,
                        4193,
                    ],
                ],
            }
        ]
    ),
]


INTRA_WITH_DATES_2 = [
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-05-25T23:59:00.000000000Z",
                        90.75,
                        90.7,
                        90.75,
                        90.7,
                        17,
                        2289,
                    ],
                    [
                        "2022-05-25T23:58:00.000000000Z",
                        90.75,
                        90.7,
                        90.74,
                        90.72,
                        20,
                        1778,
                    ],
                    [
                        "2022-05-25T23:57:00.000000000Z",
                        90.75,
                        90.7,
                        90.72,
                        90.74,
                        22,
                        3790,
                    ],
                    [
                        "2022-05-25T23:56:00.000000000Z",
                        90.8,
                        90.66,
                        90.7,
                        90.73,
                        19,
                        2721,
                    ],
                    [
                        "2022-05-25T23:55:00.000000000Z",
                        90.74,
                        90.68,
                        90.74,
                        90.7,
                        16,
                        1525,
                    ],
                    [
                        "2022-05-25T23:54:00.000000000Z",
                        90.77,
                        90.68,
                        90.7,
                        90.74,
                        22,
                        4193,
                    ],
                ],
            }
        ]
    )
]


INTRA_WITH_DATES_3 = [
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-05-25T23:59:00.000000000Z",
                        90.75,
                        90.7,
                        90.75,
                        90.7,
                        17,
                        2289,
                    ],
                    [
                        "2022-05-25T23:58:00.000000000Z",
                        90.75,
                        90.7,
                        90.74,
                        90.72,
                        20,
                        1778,
                    ],
                    [
                        "2022-05-25T23:57:00.000000000Z",
                        90.75,
                        90.7,
                        90.72,
                        90.74,
                        22,
                        3790,
                    ],
                ],
            }
        ]
    )
]


INTRA_WITH_DATES_4 = [
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-05-25T23:57:00.000000000Z",
                        90.75,
                        90.7,
                        90.72,
                        90.74,
                        22,
                        3790,
                    ],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-05-25T23:56:00.000000000Z",
                        90.8,
                        90.66,
                        90.7,
                        90.73,
                        19,
                        2721,
                    ],
                    [
                        "2022-05-25T23:55:00.000000000Z",
                        90.74,
                        90.68,
                        90.74,
                        90.7,
                        16,
                        1525,
                    ],
                    [
                        "2022-05-25T23:54:00.000000000Z",
                        90.77,
                        90.68,
                        90.7,
                        90.74,
                        22,
                        4193,
                    ],
                ],
            }
        ]
    ),
]

INTRA_WITH_COUNT_0 = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-18T04:00:00.000000000Z", 6872, 9000],
                    ["2022-10-17T16:30:00.000000000Z", 6872, 9000],
                    ["2022-10-17T15:40:00.000000000Z", 7312, 7328],
                    ["2022-10-17T15:35:00.000000000Z", 7312, 7324],
                    ["2022-10-17T15:34:00.000000000Z", 8312, 6664],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                            {"name": "SEQNUM", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-10-18T04:00:09.113000000Z",
                                21920,
                                "2022-10-18T04:00:09.113000000Z",
                                "185",
                            ]
                        ],
                    }
                },
            }
        ]
    )
]

INTRA_EMPTY_DATA = [
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [],
            }
        ]
    )
]

INTRA_TWO_UNIVERSES_EMPTY_DATA = [
    StubResponse(
        [
            {
                "universe": {"ric": "AMD.O"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "interval": "PT1M",
                "summaryTimestampLabel": "startPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                ],
                "data": [],
            }
        ]
    ),
]

INST_IS_BAD = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L.ffff"},
                "status": {
                    "code": "TS.Intraday.UserRequestError.90001",
                    "message": "The universe is not found.",
                },
            }
        ]
    )
]

INSTS_ARE_BAD = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L.ffff"},
                "status": {
                    "code": "TS.Intraday.UserRequestError.90001",
                    "message": "The universe is not found.",
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.Lffff"},
                "status": {
                    "code": "TS.Intraday.UserRequestError.90001",
                    "message": "The universe is not found.",
                },
            }
        ]
    ),
]


EVENT_WITH_DATES_0_1 = [
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}], "data": [
                ["2022-10-18T09:17:04.466000000Z", "quote", 26142, 1.1319, 1.132,
                 1.13195, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
                ["2022-10-18T09:17:04.416000000Z", "quote", 26078, 1.1315, 1.132,
                 1.13175, None, "CKLU", "CKLU", "StoneX Finan", "LUX", None],
                ["2022-10-18T09:17:04.310000000Z", "quote", 26014, 1.1318, 1.132,
                 1.1319, None, None, "ZKBZ", "ZUERCHER KB", "ZUR", None],
                ["2022-10-18T09:17:04.118000000Z", "quote", 25950, 1.1318, 1.1322,
                 1.132, None, "BCFX", None, "BARCLAYS", "LON", None],
                ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321,
                 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None]], "meta": {
                "blendingEntry": {
                    "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                                {"name": "RTL", "type": "number", "decimalChar": "."}],
                    "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    )
]


EVENT_WITH_DATES_2 = [
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
                ["2022-10-18T09:17:04.466000000Z", "quote", 26142, 1.1319, 1.132, 1.13195, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
                ["2022-10-18T09:17:04.416000000Z", "quote", 26078, 1.1315, 1.132, 1.13175, None, "CKLU", "CKLU", "StoneX Finan", "LUX", None],
                ["2022-10-18T09:17:04.310000000Z", "quote", 26014, 1.1318, 1.132, 1.1319, None, None, "ZKBZ", "ZUERCHER KB", "ZUR", None],
                ["2022-10-18T09:17:04.118000000Z", "quote", 25950, 1.1318, 1.1322, 1.132, None, "BCFX", None, "BARCLAYS", "LON", None],
                ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321, 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None]
          ],
          "meta": {
                "blendingEntry": {
                    "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                                {"name": "RTL", "type": "number", "decimalChar": "."}],
                    "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    ),
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
              ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321, 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None],
              ["2022-10-18T09:17:04.270000000Z", "quote", 26142, 1.1315, 1.132, 1.13175, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
          ],
          "meta": {
              "blendingEntry": {
                  "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                              {"name": "RTL", "type": "number", "decimalChar": "."}],
                  "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    )
]

EVENT_WITH_COUNT_0 = [
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
                ["2022-10-18T09:59:59.575000000Z", "quote", 46110, 1.1271, 1.1275, 1.1273, None, "BCFX", None, "BARCLAYS", "LON", None],
                ["2022-10-18T09:59:58.574000000Z", "quote", 46046, 1.1271, 1.1275, 1.1273, None, "BCFX", None, "BARCLAYS", "LON", None],
                ["2022-10-18T09:59:57.487000000Z", "quote", 45982, 1.1271, 1.1275, 1.1273, None, "SAHK", "SAHK", "SANTANDER", "HKG", None]
          ]}]
    )
]


EVENT_WITH_COUNT_1 = [
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
                ["2022-10-18T09:17:04.466000000Z", "quote", 26142, 1.1319, 1.132, 1.13195, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
                ["2022-10-18T09:17:04.416000000Z", "quote", 26078, 1.1315, 1.132, 1.13175, None, "CKLU", "CKLU", "StoneX Finan", "LUX", None],
                ["2022-10-18T09:17:04.310000000Z", "quote", 26014, 1.1318, 1.132, 1.1319, None, None, "ZKBZ", "ZUERCHER KB", "ZUR", None],
                ["2022-10-18T09:17:04.118000000Z", "quote", 25950, 1.1318, 1.1322, 1.132, None, "BCFX", None, "BARCLAYS", "LON", None],
                ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321, 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None]
          ],
          "meta": {
                "blendingEntry": {
                    "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                                {"name": "RTL", "type": "number", "decimalChar": "."}],
                    "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    ),
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
              ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321, 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None],
              ["2022-10-18T09:17:04.270000000Z", "quote", 26142, 1.1315, 1.132, 1.13175, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
          ],
          "meta": {
              "blendingEntry": {
                  "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                              {"name": "RTL", "type": "number", "decimalChar": "."}],
                  "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    )
]


EVENT_WITH_COUNT_2 = [
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
                ["2022-10-18T09:17:04.466000000Z", "quote", 26142, 1.1319, 1.132, 1.13195, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
                ["2022-10-18T09:17:04.416000000Z", "quote", 26078, 1.1315, 1.132, 1.13175, None, "CKLU", "CKLU", "StoneX Finan", "LUX", None],
                ["2022-10-18T09:17:04.310000000Z", "quote", 26014, 1.1318, 1.132, 1.1319, None, None, "ZKBZ", "ZUERCHER KB", "ZUR", None],
                ["2022-10-18T09:17:04.118000000Z", "quote", 25950, 1.1318, 1.1322, 1.132, None, "BCFX", None, "BARCLAYS", "LON", None],
                ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321, 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None]
          ],
          "meta": {
                "blendingEntry": {
                    "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                                {"name": "RTL", "type": "number", "decimalChar": "."}],
                    "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    ),
    StubResponse(
        [{"universe": {"ric": "GBP="},
          "adjustments": ["exchangeCorrection", "manualCorrection"],
          "defaultPricingField": "BID",
          "headers": [{"name": "DATE_TIME", "type": "string"},
                      {"name": "EVENT_TYPE", "type": "string"},
                      {"name": "RTL", "type": "number", "decimalChar": "."},
                      {"name": "BID", "type": "number", "decimalChar": "."},
                      {"name": "ASK", "type": "number", "decimalChar": "."},
                      {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                      {"name": "DSPLY_NAME", "type": "string"},
                      {"name": "SRC_REF1", "type": "string"},
                      {"name": "DLG_CODE1", "type": "string"},
                      {"name": "CTBTR_1", "type": "string"},
                      {"name": "CTB_LOC1", "type": "string"},
                      {"name": "QUALIFIERS", "type": "string"}],
          "data": [
              ["2022-10-18T09:17:03.269000000Z", "quote", 25886, 1.1318, 1.1321, 1.13195, None, "COB1", "CBKF", "Commerzbank", "FFT", None],
              ["2022-10-18T09:17:04.270000000Z", "quote", 26142, 1.1315, 1.132, 1.13175, None, "SAHK", "SAHK", "SANTANDER", "HKG", None],
          ],
          "meta": {
              "blendingEntry": {
                  "headers": [{"name": "COLLECT_DATETIME", "type": "string"},
                              {"name": "RTL", "type": "number", "decimalChar": "."}],
                  "data": [["2022-10-18T09:17:04.466000000Z", 26142]]}}}]
    )
]
