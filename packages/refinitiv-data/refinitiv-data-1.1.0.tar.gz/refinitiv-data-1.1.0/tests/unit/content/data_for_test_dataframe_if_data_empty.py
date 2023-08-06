from tests.unit.conftest import StubResponse

HP_EVENTS = StubResponse(
    [
        {
            "universe": {"ric": "EUR="},
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
            "data": [],
            "status": {
                "code": "TS.Intraday.Warning.95004",
                "message": "Trades interleaving with corrections is currently not supported. Corrections will not be returned.",
            },
        }
    ]
)

CUSTOM_INSTRUMENTS_EVENTS = StubResponse(
    [
        {
            "universe": {"ric": "S)Batman_9ccfafd6.ertvd-111923"},
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
            "data": [],
            "status": {
                "code": "TS.Intraday.Warning.95004",
                "message": "Trades interleaving with corrections is currently not supported. Corrections will not be returned.",
            },
        }
    ]
)

OWNERSHIP_ORG_INFO = StubResponse(
    {
        "links": {"count": 1},
        "variability": "fixed",
        "universe": [
            {
                "Instrument": "TRI.N",
                "Company Common Name": "Thomson Reuters Corp",
                "Organization PermID": "4295861160",
                "Reporting Currency": "USD",
            }
        ],
        "data": [],
        "headers": [
            {
                "name": "instrument",
                "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user.",
            },
            {
                "name": "TR.CommonName",
                "title": "Company Name",
                "type": "string",
                "description": "Where available provides the name of the organization most commonly used. Provides primary share class name for funds.",
            },
            {
                "name": "TR.ExchangeName",
                "title": "ExchangeName",
                "type": "string",
                "description": "Exchange Name",
            },
            {
                "name": "TR.OrgTRBCActivity",
                "title": "TRBC Industry",
                "type": "string",
                "description": "The Refinitiv Business Classification (TRBC) Activity Description. TRBC Classifies companies with increasing granularity by Economic Sector, Business Sector, Industry Group, Industry and Activity.",
            },
            {
                "name": "TR.TRBCActivityCode",
                "title": "TRBC IndustryCode",
                "type": "string",
                "description": "The Refinitiv Business Classification (TRBC) Activity classifies companies at the most granular level and indicates the business activity. This is the fifth level in the classification, which represents the activities of the organizations.",
            },
            {
                "name": "TR.HQCountryCode",
                "title": "Country Code",
                "type": "string",
                "description": "Country Code for Organization Headquarters, ISO 3166 standard. Also known as Country of Domicile.",
            },
            {
                "name": "TR.HeadquartersCountry",
                "title": "Country Name",
                "type": "string",
                "description": "Country of Headquarters, also known as Country of Domicile.",
            },
            {
                "name": "TR.FreeFloat",
                "title": "FreeFloat",
                "type": "number",
                "decimalChar": ".",
                "description": "Shares Outstanding - Treasury Shares (if applicable) -\n(Shares held by Strategic Entities–Corporations +\n  Shares held by Strategic Entities–Holding Companies +\n  Shares held by Strategic Entities–Individuals  +\n  Shares held by Strategic Entities–Government Agencies)",
            },
            {
                "name": "TR.FreeFloatPct",
                "title": "FreeFloat %",
                "type": "number",
                "decimalChar": ".",
                "description": "Free Float as a percentage of traded shares",
            },
            {
                "name": "TR.SharesOutstanding",
                "title": "SharesOutstanding",
                "type": "number",
                "decimalChar": ".",
                "description": "The Outstanding Shares represents the issue level outstanding shares. The outstanding share is the number of shares that have been issued and are currently owned by investors. This may include shares that are publicly traded and not traded, such as restricted shares owned by Issue employees etc. Shares that have been repurchased by the Issue as treasury stock are excluded.",
            },
            {
                "name": "TR.SharesHeldByStrategicInvestors",
                "title": "SharesHeld by StrategicInvestors",
                "type": "number",
                "decimalChar": ".",
                "description": "Represents the number of shares held by strategic investors (Corporations, Holding Companies, Individuals and Government Agencies).",
            },
            {
                "name": "Strategic Entities Ownership%",
                "title": "Strategic Entities Ownership%",
                "type": "number",
                "decimalChar": ".",
                "description": None,
            },
            {
                "name": "Market Capitalization",
                "title": "Market Capitalization",
                "type": "number",
                "decimalChar": ".",
                "description": None,
            },
        ],
    }
)

FUNDAMENTAL_AND_REFERENCE_UDF = StubResponse(
    {
        "responses": [
            {
                "columnHeadersCount": 1,
                "data": [],
                "headerOrientation": "horizontal",
                "headers": [
                    [
                        {"displayName": "Instrument"},
                        {"displayName": "Volume", "field": "TR.VOLUME"},
                    ]
                ],
                "rowHeadersCount": 1,
                "totalColumnsCount": 2,
                "totalRowsCount": 2,
            }
        ]
    }
)

NEWS_HEADLINES_UDF = StubResponse({"headlines": [], "newer": "/headlines?payload=eyJ="})

FUNDAMENTAL_AND_REFERENCE_RDP = StubResponse(
    {
        "links": {"count": 1},
        "variability": "",
        "universe": [
            {
                "Instrument": "IBM",
                "Company Common Name": "International Business Machines Corp",
                "Organization PermID": "4295904307",
                "Reporting Currency": "USD",
            }
        ],
        "data": [],
        "messages": {
            "codes": [[-1, -1]],
            "descriptions": [{"code": -1, "description": "ok"}],
        },
        "headers": [
            {
                "name": "instrument",
                "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user.",
            },
            {
                "name": "TR.Volume",
                "title": "Volume",
                "type": "number",
                "decimalChar": ".",
                "description": "Volume for the latest trading day.  For stock exchanges that trade share by share, Volume is number of shares that traded on the trade date. For stock exchanges that trade in lots, Volume is divided by Lotsize, if the Lotsize is greater than one.",
            },
        ],
    }
)

CAP_FLOOR = StubResponse(
    {
        "headers": [
            {"type": "String", "name": "InstrumentTag"},
            {"type": "String", "name": "InstrumentDescription"},
            {"type": "DateTime", "name": "StartDate"},
            {"type": "DateTime", "name": "EndDate"},
            {"type": "String", "name": "InterestPaymentFrequency"},
            {"type": "String", "name": "IndexRic"},
            {"type": "Float", "name": "CapStrikePercent"},
            {"type": "Float", "name": "FloorStrikePercent"},
            {"type": "String", "name": "NotionalCcy"},
            {"type": "Float", "name": "NotionalAmount"},
            {"type": "Float", "name": "PremiumBp"},
            {"type": "Float", "name": "PremiumPercent"},
            {"type": "Float", "name": "MarketValueInDealCcy"},
            {"type": "Float", "name": "MarketValueInReportCcy"},
            {"type": "String", "name": "ErrorMessage"},
        ],
        "data": [],
    }
)
