from tests.unit.conftest import StubResponse

DF_WITHOUT_NAN_RESPONSES = [
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
                "qos": {"timeliness": "delayed"},
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
                        "2022-05-25T20:01:00.000000000Z",
                        None,
                        None,
                        None,
                        None,
                        None,
                        56358,
                    ],
                    [
                        "2022-05-25T20:00:00.000000000Z",
                        92.7,
                        92.65,
                        92.7,
                        92.65,
                        2,
                        1750467,
                    ],
                    [
                        "2022-05-25T19:59:00.000000000Z",
                        92.71,
                        92.484,
                        92.55,
                        92.7099,
                        2483,
                        619187,
                    ],
                    [
                        "2022-05-25T19:58:00.000000000Z",
                        92.5714,
                        92.4722,
                        92.53,
                        92.5575,
                        1451,
                        339267,
                    ],
                    [
                        "2022-05-25T19:57:00.000000000Z",
                        92.575,
                        92.44,
                        92.55,
                        92.54,
                        1186,
                        306126,
                    ],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IMNM.O"},
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
                "qos": {"timeliness": "delayed"},
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
                        "2022-05-25T19:59:00.000000000Z",
                        None,
                        None,
                        None,
                        None,
                        None,
                        231,
                    ],
                    [
                        "2022-05-25T19:58:00.000000000Z",
                        None,
                        None,
                        None,
                        None,
                        None,
                        100,
                    ],
                    ["2022-05-25T19:57:00.000000000Z", 3, 3, 3, 3, 1, 100],
                    ["2022-05-25T19:56:00.000000000Z", 3, 3, 3, 3, 2, 224],
                    ["2022-05-25T19:54:00.000000000Z", 3, 3, 3, 3, 1, 104],
                ],
            }
        ]
    ),
]

DF_REQUIREMENT_TWO_INSTS_ONE_FIELD = [
    StubResponse(
        [
            {
                "universe": {"ric": "GBP="},
                "interval": "P1D",
                "summaryTimestampLabel": "endPeriod",
                "adjustments": [
                    "exchangeCorrection",
                    "manualCorrection",
                    "CCH",
                    "CRE",
                    "RTS",
                    "RPO",
                ],
                "defaultPricingField": "BID",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-06-22", 1.2266],
                    ["2022-06-21", 1.2272],
                    ["2022-06-20", 1.225],
                    ["2022-06-17", 1.2224],
                    ["2022-06-16", 1.2351],
                    ["2022-06-15", 1.2178],
                    ["2022-06-14", 1.1993],
                    ["2022-06-13", 1.2134],
                    ["2022-06-10", 1.2314],
                    ["2022-06-09", 1.249],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-06-23", None]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "G234BP="},
                "status": {
                    "code": "TS.Interday.UserRequestError.70005",
                    "message": "The universe is not found.",
                },
            }
        ]
    ),
]

DF_REQUIREMENT_TWO_INSTS_ONE_IS_BAD_WITHOUT_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "GBP="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
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
                    {"name": "QUALIFIERS", "type": "string"},
                ],
                "data": [
                    [
                        "2022-06-23T11:54:12.757000000Z",
                        "quote",
                        8590,
                        1.2219,
                        1.2224,
                        1.22215,
                        None,
                        "NBJX",
                        "NBJJ",
                        "NEDBANK LTD",
                        "JHB",
                        None,
                    ],
                    [
                        "2022-06-23T11:54:12.619000000Z",
                        "quote",
                        8526,
                        1.222,
                        1.2225,
                        1.22225,
                        None,
                        "RAB1",
                        "RABX",
                        "RABOBANKGFM",
                        "LON",
                        None,
                    ],
                    [
                        "2022-06-23T11:54:12.169000000Z",
                        "quote",
                        8462,
                        1.2219,
                        1.2223,
                        1.2221,
                        None,
                        "BCFX",
                        None,
                        "BARCLAYS",
                        "LON",
                        None,
                    ],
                ],
                "status": {
                    "code": "TS.Intraday.Warning.95004",
                    "message": "Trades interleaving with corrections is currently not supported. Corrections will not be returned.",
                },
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-06-23T11:54:12.757000000Z", 8590]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "G234BP="},
                "status": {
                    "code": "TS.Intraday.UserRequestError.90001",
                    "message": "The universe is not found.",
                },
            }
        ]
    ),
]


DF_WITH_EXTENDED_PARAMS = [
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "RTL", "type": "number", "decimalChar": "."},
                    {"name": "SEQNUM", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "BIDSIZE", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASKSIZE", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "IMB_SH", "type": "number", "decimalChar": "."},
                    {"name": "IMB_SIDE", "type": "string", "isEnum": True},
                    {"name": "QUALIFIERS", "type": "string"},
                ],
                "data": [
                    [
                        "2022-07-19T15:52:52.900000000Z",
                        "quote",
                        50624,
                        "9076320",
                        130.82,
                        12365,
                        131,
                        2153541,
                        130.91,
                        None,
                        None,
                        "[BID_TONE]",
                    ],
                    [
                        "2022-07-19T15:40:07.641000000Z",
                        "quote",
                        50544,
                        "9075948",
                        130.94,
                        80476,
                        131,
                        2153541,
                        130.97,
                        None,
                        None,
                        "[ASK_TONE]",
                    ],
                    [
                        "2022-07-19T15:40:00.112000000Z",
                        "quote",
                        50528,
                        "9075850",
                        130.94,
                        80476,
                        131,
                        2203541,
                        130.97,
                        None,
                        None,
                        "[ASK_TONE]",
                    ],
                    [
                        "2022-07-19T15:39:38.390000000Z",
                        "quote",
                        50496,
                        "9075694",
                        130.94,
                        80476,
                        131,
                        2503541,
                        130.97,
                        None,
                        None,
                        "[ASK_TONE]",
                    ],
                    [
                        "2022-07-19T15:39:01.320000000Z",
                        "quote",
                        50480,
                        "9075524",
                        130.94,
                        80476,
                        131,
                        2453541,
                        130.97,
                        None,
                        None,
                        "[ASK_TONE]",
                    ],
                ],
            },
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GOOG.O"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "RTL", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "BIDSIZE", "type": "number", "decimalChar": "."},
                    {"name": "BID_MMID1", "type": "string"},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASKSIZE", "type": "number", "decimalChar": "."},
                    {"name": "ASK_MMID1", "type": "string"},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "UPLIMIT", "type": "number", "decimalChar": "."},
                    {"name": "LOLIMIT", "type": "number", "decimalChar": "."},
                    {"name": "LIMIT_INDQ", "type": "string", "isEnum": True},
                    {"name": "SH_SAL_RES", "type": "string", "isEnum": True},
                    {"name": "QUALIFIERS", "type": "string"},
                ],
                "data": [
                    [
                        "2022-07-19T15:59:58.425000000Z",
                        "quote",
                        60400,
                        113.33,
                        200,
                        "DEX",
                        113.35,
                        100,
                        "NAS",
                        None,
                        118.44,
                        107.16,
                        "BOE",
                        "N",
                        "   [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]",
                    ],
                    [
                        "2022-07-19T15:59:58.424000000Z",
                        "quote",
                        60352,
                        113.33,
                        200,
                        "DEX",
                        113.35,
                        100,
                        "MMX",
                        None,
                        118.44,
                        107.16,
                        "BOE",
                        "N",
                        "   [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]",
                    ],
                    [
                        "2022-07-19T15:59:58.410000000Z",
                        "quote",
                        60336,
                        113.33,
                        200,
                        "DEX",
                        113.35,
                        200,
                        "NAS",
                        None,
                        118.44,
                        107.16,
                        "BOE",
                        "N",
                        "   [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]",
                    ],
                    [
                        "2022-07-19T15:59:58.409000000Z",
                        "quote",
                        60320,
                        113.33,
                        200,
                        "DEX",
                        113.35,
                        100,
                        "MMX",
                        None,
                        118.44,
                        107.16,
                        "BOE",
                        "N",
                        "   [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]",
                    ],
                    [
                        "2022-07-19T15:59:58.409000000Z",
                        "quote",
                        60272,
                        113.33,
                        200,
                        "DEX",
                        113.36,
                        200,
                        "NAS",
                        None,
                        118.44,
                        107.16,
                        "BOE",
                        "N",
                        "   [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]",
                    ],
                ],
            }
        ]
    ),
]

DF_EMPTY_ONE_INST = [
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
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_YLD", "type": "number", "decimalChar": "."},
                    {"name": "LOW_YLD", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_YLD", "type": "number", "decimalChar": "."},
                    {"name": "YIELD", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "BID_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "MID_HIGH", "type": "number", "decimalChar": "."},
                    {"name": "MID_LOW", "type": "number", "decimalChar": "."},
                    {"name": "MID_OPEN", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                ],
                "data": [],
            }
        ]
    )
]

DF_EMPTY_TWO_INSTS = [
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
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_YLD", "type": "number", "decimalChar": "."},
                    {"name": "LOW_YLD", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_YLD", "type": "number", "decimalChar": "."},
                    {"name": "YIELD", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "BID_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "MID_HIGH", "type": "number", "decimalChar": "."},
                    {"name": "MID_LOW", "type": "number", "decimalChar": "."},
                    {"name": "MID_OPEN", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
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
                    {"name": "HIGH_YLD", "type": "number", "decimalChar": "."},
                    {"name": "LOW_YLD", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_YLD", "type": "number", "decimalChar": "."},
                    {"name": "YIELD", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "BID_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "MID_HIGH", "type": "number", "decimalChar": "."},
                    {"name": "MID_LOW", "type": "number", "decimalChar": "."},
                    {"name": "MID_OPEN", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                ],
                "data": [],
            }
        ]
    ),
]

DF_EMPTY_ONE_INST_IS_BAD = [
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
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_YLD", "type": "number", "decimalChar": "."},
                    {"name": "LOW_YLD", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_YLD", "type": "number", "decimalChar": "."},
                    {"name": "YIELD", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "BID_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "ASK_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "MID_HIGH", "type": "number", "decimalChar": "."},
                    {"name": "MID_LOW", "type": "number", "decimalChar": "."},
                    {"name": "MID_OPEN", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                ],
                "data": [],
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

DF_EMPTY_ONE_INST_IS_BAD_OTHER_WITHOUT_HEADERS = [
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [],
                "data": [],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GBP"},
                "status": {
                    "code": "TS.Intraday.UserRequestError.90001",
                    "message": "The universe is not found.",
                },
            }
        ]
    ),
]

DF_EMPTY_WITHOUT_HEADERS = [
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [],
                "data": [],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GBP="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [],
                "data": [],
            }
        ]
    ),
]

INST_IS_BAD = [
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
