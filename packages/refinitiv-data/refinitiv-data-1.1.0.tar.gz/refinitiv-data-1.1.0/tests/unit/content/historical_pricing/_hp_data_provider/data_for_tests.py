from tests.unit.conftest import StubResponse

TWO_UNIVERSES_ONE_FAILED = [
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-31T11:42:58.991Z", 2.3064],
                    ["2022-10-31T11:42:58.001Z", 2.3064],
                    ["2022-10-31T11:42:48.107Z", 2.3064],
                    ["2022-10-31T11:42:47.894Z", 2.3062],
                    ["2022-10-31T11:42:47.804Z", 2.3062],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)Batman_9ccfafd6.GESG1-111923"},
            }
        ]
    ),
    StubResponse(
        {
            "state": {
                "code": 400,
                "status": "Bad Request",
                "message": "Validation Error",
            },
            "data": [
                {
                    "key": "symbol",
                    "reason": ".UUID suffix UUID-0000 not matched with userID GESG1-111923",
                }
            ],
        }
    ),
    StubResponse(
        [
            {
                "error": {
                    "code": "404",
                    "message": "CustomInstrument with symbol: S)invalid_cust_universe.GESG1-111923 for user: GESG1-111923 not found!",
                    "status": "Not Found",
                }
            }
        ]
    ),
]

ONE_UNIVERSE = [
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-31T11:42:58.991Z", 2.3064],
                    ["2022-10-31T11:42:58.001Z", 2.3064],
                    ["2022-10-31T11:42:57.557Z", 2.3066],
                    ["2022-10-31T11:42:47.894Z", 2.3062],
                    ["2022-10-31T11:42:47.804Z", 2.3062],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)Batman_9ccfafd6.GESG1-111923"},
            }
        ]
    ),
]

TWO_UNIVERSES = [
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-31T11:42:58.991Z", 2.3064],
                    ["2022-10-31T11:42:58.001Z", 2.3064],
                    ["2022-10-31T11:42:57.557Z", 2.3066],
                    ["2022-10-31T11:42:47.894Z", 2.3062],
                    ["2022-10-31T11:42:47.804Z", 2.3062],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)Batman_9ccfafd6.GESG1-111923"},
            }
        ]
    ),
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-31T12:01:49.533Z", 2.3074],
                    ["2022-10-31T12:01:49.507Z", 2.307],
                    ["2022-10-31T12:01:40.994Z", 2.3074],
                    ["2022-10-31T12:01:39.984Z", 2.307],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)Batman_3b9a8a02.GESG1-111923"},
            }
        ]
    ),
]

ONE_UNIVERSE_WITH_TWO_REQUESTS = [
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-31T11:42:58.991Z", 2.3064],
                    ["2022-10-31T11:42:58.001Z", 2.3064],
                    ["2022-10-31T11:42:57.557Z", 2.3066],
                    ["2022-10-31T11:42:54.323Z", 2.3066],
                    ["2022-10-31T11:42:52.681Z", 2.3062],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)Batman_9ccfafd6.GESG1-111923"},
            }
        ]
    ),
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-31T11:42:58.991Z", 2.3064],
                    ["2022-10-31T11:42:51.587Z", 2.3064],
                    ["2022-10-31T11:42:50.817Z", 2.3064],
                    ["2022-10-31T11:42:50.232Z", 2.3064],
                    ["2022-10-31T11:42:49.119Z", 2.306],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)Batman_9ccfafd6.GESG1-111923"},
            }
        ]
    ),
]
