from pandas import DataFrame

from tests.unit.conftest import StubResponse

# fmt: off
SEARCH_QUERY_CFO_RESPONSE = StubResponse({"Total": 114035, "Hits": [
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Amy E. Hood - Microsoft Corp - Chief Financial Officer, Executive Vice President",
     "PermID": "34415553383", "PI": "34415553383"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Luca Maestri - Apple Inc - Chief Financial Officer, Senior Vice President",
     "PermID": "34414554748", "PI": "34414554748"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Brian T. Olsavsky - Amazon.com Inc - Chief Financial Officer, Senior Vice President",
     "PermID": "34417610894", "PI": "34417610894"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Ruth M. Porat - Alphabet Inc - Chief Financial Officer, Senior Vice President",
     "PermID": "34413960665", "PI": "34413960665"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "David M. Wehner - Meta Platforms Inc - Chief Financial Officer",
     "PermID": "34414804241", "PI": "34414804241"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Marc D. Hamburg - Berkshire Hathaway Inc - Chief Financial Officer, Senior Vice President",
     "PermID": "34413152672", "PI": "34413152672"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Andrew K. Klatt - Berkshire Hathaway Inc - CFO & COO",
     "PermID": "34414966250", "PI": "34414966250"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Xu Hong - Alibaba Group Holding Ltd - Chief Financial Officer",
     "PermID": "34425652371", "PI": "34425652371"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "John Lo - Tencent Holdings Ltd - Chief Financial Officer, Senior Vice President",
     "PermID": "34414907131", "PI": "34414907131"},
    {"BusinessEntity": "PERSON",
     "DocumentTitle": "Vasant M. Prabhu - Visa Inc - Vice Chairman of the Board, Chief Financial Officer",
     "PermID": "34413340523", "PI": "34413340523"}]})
SEARCH_QUERY_IBM_RESPONSE = StubResponse({"Total": 44696, "Hits": [
    {"BusinessEntity": "ORGANISATION", "DocumentTitle": "International Business Machines Corp, Public Company",
     "PI": "37036"},
    {"BusinessEntity": "ORGANISATION", "DocumentTitle": "Banco IBM SA, Private Company", "PI": "76208"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "International Business Machines Corp, Ordinary Share, NYSE Consolidated",
     "PermID": "55839165994", "PI": "1097326", "RIC": "IBM"},
    {"BusinessEntity": "ORGANISATION",
     "DocumentTitle": "Tiers Corporate Bond Backed Certificates Trust Series Ibm 1997 4, Private Company",
     "PI": "18062670"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "Eurex International Business Machines Equity Future Chain Contract , Equity Future, USD, Eurex",
     "PermID": "21481052421",
     "PI": "48924732", "RIC": "0#IBMF:"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "Euronext Amsterdam IBM Dividend Future Chain Contracts, Equity Future, USD, Euronext Amsterdam",
     "PermID": "21612423771", "PI": "259118763", "RIC": "0#IBMDF:"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "Eurex International Business Machines Equity Future Continuation 1, Equity Future, USD, Eurex",
     "PermID": "21481052892", "PI": "49450681",
     "RIC": "IBMFc1"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "Eurex International Business Machines Equity Future Continuation 2, Equity Future, USD, Eurex",
     "PermID": "21481053949", "PI": "50092347", "RIC": "IBMFc2"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "Euronext Amsterdam IBM Single Stock Dividend Future Continuation 1, Equity Future, USD, Euronext Amsterdam",
     "PermID": "21613372305", "PI": "260213021",
     "RIC": "IBMDFc1"},
    {"BusinessEntity": "QUOTExEQUITY",
     "DocumentTitle": "Eurex International Business Machines Equity Future Continuation 3, Equity Future, USD, Eurex",
     "PermID": "21481053950",
     "PI": "50092348",
     "RIC": "IBMFc3"}]})

# tests get_data

# ONE VALID PRICING UNIVERSE
GET_DATA_PARAMS_1 = {"universe": "EUR="}
GET_DATA_RAW_RESPONSE_1 = {
    "links": {"count": 1},
    "variability": "",
    "universe": [
        {
            "Instrument": "EUR=",
            "Company Common Name": "Vodafone Group PLC",
            "Organization PermID": "4295896661",
            "Reporting Currency": "EUR",
        }
    ],
    "data": [["EUR=", "EUR="]],
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
            "name": "RIC",
            "title": "RIC",
            "type": "string",
            "description": "Refinitiv Identification Code consolidated with RICCode",
        },
    ],
}
GET_DATA_STREAM_MESSAGES_1 = [{
    "ID": 5,
    "Type": "Refresh",
    "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
    "State": {"Stream": "NonStreaming", "Data": "Ok"},
    "Qos": {"Timeliness": "Realtime", "Rate": "JitConflated"},
    "PermData": "AwEBUmw=",
    "SeqNumber": 19854,
    "Fields": {
        "PROD_PERM": 526,
        "RDNDISPLAY": 153,
        "DSPLY_NAME": "SANTANDER    HKG",
    },
}]
GET_DATA_RESULT_1 = """  Instrument  PROD_PERM  RDNDISPLAY        DSPLY_NAME
0       EUR=        526         153  SANTANDER    HKG"""

# ONE INVALID UNIVERSE
GET_DATA_PARAMS_2 = {"universe": "INVAL"}
GET_DATA_RAW_RESPONSE_2 = {"links": {"count": 1}, "variability": "", "universe": [
    {"Instrument": "INVAL", "Company Common Name": "Failed to resolve identifier(s).",
     "Organization PermID": "Failed to resolve identifier(s).",
     "Reporting Currency": "Failed to resolve identifier(s)."}], "data": [["INVAL", None]],
                           "messages": {"codes": [[-1, -2]], "descriptions": [{"code": -2, "description": "empty"},
                                                                              {"code": -1, "description": "ok"}]},
                           "headers": [{"name": "instrument", "title": "Instrument", "type": "string",
                                        "description": "The requested Instrument as defined by the user."},
                                       {"name": "RIC", "title": "RIC", "type": "string",
                                        "description": "Refinitiv Identification Code consolidated with RICCode"}]}
GET_DATA_STREAM_MESSAGES_2 = [
    {'ID': 5, 'Type': 'Status', 'Key': {'Service': 'ELEKTRON_DD', 'Name': 'INVAL'},
     'State': {'Stream': 'Closed', 'Data': 'Suspect', 'Code': 'NotFound', 'Text': '**The record could not be found'}}
]
GET_DATA_RESULT_2 = DataFrame().to_string()

# VALID PRICING UNIVERSE AND INVALID UNIVERSE
GET_DATA_PARAMS_3 = {"universe": ["INVAL", "EUR="]}

GET_DATA_RAW_RESPONSE_3 = {
    "links": {"count": 2}, "variability": "", "universe": [
        {
            "Instrument": "INVAL",
            "Company Common Name": "Failed to resolve identifier(s).",
            "Organization PermID": "Failed to resolve identifier(s).",
            "Reporting Currency": "Failed to resolve identifier(s)."
        },
        {
            "Instrument": "EUR=",
            "Company Common Name": "Failed to resolve identifier(s).",
            "Organization PermID": "Failed to resolve identifier(s).",
            "Reporting Currency": "Failed to resolve identifier(s)."
        }], "data": [["INVAL", None], ["EUR=", "EUR="]],
    "messages": {
        "codes": [[-1, -2], [-1, -1]],
        "descriptions": [{"code": -2, "description": "empty"},
                         {"code": -1, "description": "ok"}]
    }, "headers": [
        {
            "name": "instrument", "title": "Instrument", "type": "string",
            "description": "The requested Instrument as defined by the user."
        },
        {
            "name": "RIC", "title": "RIC", "type": "string",
            "description": "Refinitiv Identification Code consolidated with RICCode"
        }]
}

GET_DATA_STREAM_MESSAGES_3 = [
    {
        'ID': 5, 'Type': 'Status',
        'Key': {'Service': 'ELEKTRON_DD', 'Name': 'INVAL'},
        'State': {
            'Stream': 'Closed', 'Data': 'Suspect', 'Code': 'NotFound',
            'Text': '**The record could not be found'
        }
    },
    {
        'ID': 6,
        'Type': 'Refresh',
        'Key': {'Service': 'ELEKTRON_DD', 'Name': 'EUR='},
        'State': {'Stream': 'NonStreaming', 'Data': 'Ok'},
        'Qos': {'Timeliness': 'Realtime', 'Rate': 'JitConflated'},
        'PermData': 'AwEBUmw=',
        'SeqNumber': 1566,

        'Fields': {
            'PROD_PERM': 526,
            'RDNDISPLAY': 153,
            'DSPLY_NAME': 'ZUERCHER KB  ZUR'
        }
    },
]
GET_DATA_RESULT_3 = """  Instrument  PROD_PERM  RDNDISPLAY        DSPLY_NAME
0      INVAL       <NA>        <NA>              <NA>
1       EUR=        526         153  ZUERCHER KB  ZUR"""

# VALID AND INVALID UNIVERSE WITH PRICING AND ADC FIELDS
GET_DATA_PARAMS_4 = {"universe": ["INVAL", "EUR="], "fields": ["PROD_PERM", "TR.RIC", "BID"]}
GET_DATA_RAW_RESPONSE_4 = {"links": {"count": 2}, "variability": "",
                           "universe": [{"Instrument": "INVAL",
                                         "Company Common Name": "Failed to resolve identifier(s).",
                                         "Organization PermID": "Failed to resolve identifier(s).",
                                         "Reporting Currency": "Failed to resolve identifier(s)."},
                                        {"Instrument": "EUR=",
                                         "Company Common Name": "Failed to resolve identifier(s).",
                                         "Organization PermID": "Failed to resolve identifier(s).",
                                         "Reporting Currency": "Failed to resolve identifier(s)."}],
                           "data": [["INVAL", None], ["EUR=", "EUR="]],
                           "messages": {"codes": [[-1, -2], [-1, -1]],
                                        "descriptions": [
                                            {"code": -2, "description": "empty"},
                                            {"code": -1, "description": "ok"}]},
                           "headers": [
                               {"name": "instrument", "title": "Instrument",
                                "type": "string",
                                "description": "The requested Instrument as defined by the user."},
                               {"name": "RIC", "title": "RIC", "type": "string",
                                "description": "Refinitiv Identification Code consolidated with RICCode"}]}
GET_DATA_STREAM_MESSAGES_4 = [
    {'ID': 5, 'Type': 'Status', 'Key': {'Service': 'ELEKTRON_DD', 'Name': 'INVAL'},
     'State': {'Stream': 'Closed', 'Data': 'Suspect', 'Code': 'NotFound', 'Text': '**The record could not be found'}},
    {'ID': 6, 'Type': 'Refresh', 'Key': {'Service': 'ELEKTRON_DD', 'Name': 'EUR='},
     'State': {'Stream': 'NonStreaming', 'Data': 'Ok'}, 'Qos': {'Timeliness': 'Realtime', 'Rate': 'JitConflated'},
     'PermData': 'AwEBUmw=', 'SeqNumber': 3166,
     'Fields': {'PROD_PERM': 526, 'BID': 1.0051}}

]
GET_DATA_RESULT_4 = """  Instrument   RIC  PROD_PERM     BID
0      INVAL  <NA>       <NA>    <NA>
1       EUR=  EUR=        526  1.0051"""

# CI universe
GET_DATA_PARAMS_5 = {"universe": "S)TR12"}
GET_DATA_RAW_RESPONSE_5 = {"services": [
    {"provider": "AWS", "endpoint": "custom-instruments.refinitiv.com/websocket", "transport": "websocket", "port": 443,
     "dataFormat": ["tr_json2"], "location": ["us-east-1", "eu-west-1"]}]}
GET_DATA_STREAM_MESSAGES_5 = [{'Domain': 'MarketPrice', 'ID': 5, 'Type': 'Refresh',
                               'Key': {'Name': 'S)TR12.GESG1-106493', 'Service': 'CUSTOM_BASKETS'},
                               'State': {'Data': 'Ok', 'Stream': 'NonStreaming'},
                               'Fields': {'TRDPRC_1': 3.0156, 'TRADE_DATE': '2022-08-19', 'SALTIM_NS': '12:15:34.777'},
                               'Qos': {'Timeliness': 'Realtime', 'Rate': 'TimeConflated', 'RateInfo': 300}}]
GET_DATA_RESULT_5 = """  Instrument  TRDPRC_1 TRADE_DATE     SALTIM_NS
0     S)TR12    3.0156 2022-08-19  12:15:34.777"""

# adc
GET_DATA_PARAMS_6 = {'universe': "VOD.L", "fields": ["TR.RIC"]}
GET_DATA_RAW_RESPONSE_6 = {"responses": [
    {"columnHeadersCount": 1, "data": [["VOD.L", "VOD.L"]], "headerOrientation": "horizontal",
     "headers": [[{"displayName": "Instrument"}, {"displayName": "RIC", "field": "TR.RIC"}]], "rowHeadersCount": 1,
     "totalColumnsCount": 2, "totalRowsCount": 2}]}
GET_DATA_STREAM_MESSAGES_6 = None
GET_DATA_RESULT_6 = """  Instrument    RIC
0      VOD.L  VOD.L"""

# update universe
GET_DATA_PARAMS_7 = {"universe": 'peers("VOD.L")', "fields": ["TR.RIC", "TRADE_DATE"]}
GET_DATA_RAW_RESPONSE_7 = {"responses": [{"columnHeadersCount": 1,
                                          "data": [["BT.L", "BT.L"], ["DTEGn.DE", "DTEGn.DE"], ["TEF.MC", "TEF.MC"],
                                                   ["ORAN.PA", "ORAN.PA"]],
                                          "headerOrientation": "horizontal", "headers": [
        [{"displayName": "Instrument"}, {"displayName": "RIC", "field": "TR.RIC"}]], "rowHeadersCount": 1,
                                          "totalColumnsCount": 2, "totalRowsCount": 5}]}
GET_DATA_STREAM_MESSAGES_7 = [
    {'ID': 5, 'Type': 'Status', 'Key': {'Service': 'IDN_FD3', 'Name': 'BT.L'},
     'State': {'Stream': 'Closed', 'Data': 'Suspect', 'Code': 'NotEntitled',
               'Text': 'Access Denied: User req to PE(5625)'}},
    *[{'ID': i, 'Type': 'Refresh', 'Key': {'Service': 'IDN_FD3', 'Name': 'DTEGn.DE'},
       'State': {'Stream': 'NonStreaming', 'Data': 'Ok', 'Text': 'All is well'},
       'Qos': {'Timeliness': 'Realtime', 'Rate': 'JitConflated'}, 'PermData': 'AwECWSbA', 'SeqNumber': 52000,
       'Fields': {'TRADE_DATE': '2022-08-19'}} for i in range(6, 9)]
]
GET_DATA_RESULT_7 = """  Instrument       RIC TRADE_DATE
0       BT.L      BT.L        NaT
1   DTEGn.DE  DTEGn.DE 2022-08-19
2     TEF.MC    TEF.MC 2022-08-19
3    ORAN.PA   ORAN.PA 2022-08-19"""

# invalid universe, ivalid fields(pricing and adc)
GET_DATA_PARAMS_8 = {"universe": 'INVAL', "fields": ["INVAL", "TR.INVAL"]}
GET_DATA_RAW_RESPONSE_8 = {"responses": [{"columnHeadersCount": 1, "data": [["INVAL", None]], "error": [
    {"code": 218, "col": 1, "message": "The formula must contain at least one field or function.", "row": 0}],
                                          "headerOrientation": "horizontal", "headers": [
        [{"displayName": None}, {"displayName": "TR.INVAL", "field": "TR.INVAL"}]], "rowHeadersCount": 1,
                                          "totalColumnsCount": 2, "totalRowsCount": 2}]}
GET_DATA_STREAM_MESSAGES_8 = [{'ID': 5, 'Type': 'Status', 'Key': {'Service': 'IDN_FD3', 'Name': 'INVAL'}, 'State': {'Stream': 'Closed', 'Data': 'Suspect', 'Code': 'NotFound', 'Text': 'The record could not be found'}}]
GET_DATA_RESULT_8 = DataFrame().to_string()

GET_DATA_DUPLICATE_DATE_HTTP = {
    "responses": [{
                      "columnHeadersCount": 1,
                      "data": [["IBM.N", 63.3953136510557, "2021-12-31T00:00:00Z",
                                63.3953136510557, "2020-12-31T00:00:00Z", 57350000000],
                               ["IBM.N", "", "2020-12-31T00:00:00Z", 61.5449669904257,
                                "2019-12-31T00:00:00Z", ""],
                               ["IBM.N", "", "2019-12-31T00:00:00Z", 64.6428487200443,
                                "2018-12-31T00:00:00Z", ""],
                               ["VOD.L", 1.56583874403106, "2022-03-31T00:00:00Z",
                                1.56583874403106, "2021-03-31T00:00:00Z", 45580000000],
                               ["VOD.L", "", "2021-03-31T00:00:00Z", 1.4758952936024,
                                "2020-03-31T00:00:00Z", ""],
                               ["VOD.L", "", "2020-03-31T00:00:00Z", 1.52858405274964,
                                "2019-03-31T00:00:00Z", ""]],
                      "headerOrientation": "horizontal",
                      "headers": [[{"displayName": "Instrument"}, {
                          "displayName": "Total Revenue per Share",
                          "field": "TR.F.TOTREVPERSHR"
                      }, {
                                       "displayName": "Date",
                                       "field": "TR.F.TOTREVPERSHR(SDATE=0,EDATE=-2,"
                                                "PERIOD=FY0,FRQ=FY).DATE"
                                   }, {
                                       "displayName": "Total Revenue per Share",
                                       "field": "TR.F.TOTREVPERSHR(SDATE=0,EDATE=-2,"
                                                "PERIOD=FY0,FRQ=FY)"
                                   }, {
                                       "displayName": "Date",
                                       "field": "TR.F.TOTREVENUE(SDATE=-1,EDATE=-3,"
                                                "PERIOD=FY0,FRQ=FY).DATE"
                                   }, {
                                       "displayName": "Revenue from Business "
                                                      "Activities - Total",
                                       "field": "TR.F.TOTREVENUE"
                                   }]],
                      "rowHeadersCount": 1,
                      "totalColumnsCount": 6,
                      "totalRowsCount": 7
                  }]
}
GET_DATA_DUPLICATE_DATE_STREAM = [
    {
        'ID': 6,
        'Type': 'Refresh',
        'Key': {'Service': 'IDN_FD3', 'Name': 'VOD.L'},
        'State': {
            'Stream': 'NonStreaming',
            'Data': 'Ok',
            'Text': 'New Session Mounted'
        },
        'Qos': {'Timeliness': 'Realtime', 'Rate': 'JitConflated'},
        'PermData': 'AwECViXA',
        'SeqNumber': 10112,
        'Fields': {
            'PROD_PERM': 5625,
            'RDNDISPLAY': 115,
            'DSPLY_NAME': 'VODAFONE GROUP',
            'RDN_EXCHID': 64,
            'TRDPRC_1': 106.36,
            'TRDPRC_2': 106.36,
            'TRDPRC_3': 106.36,
            'TRDPRC_4': 106.32,
            'TRDPRC_5': 106.34,
            'NETCHNG_1': 1.64,
            'HIGH_1': 106.62,
            'LOW_1': 104.6,
            'PRCTCK_1': 1,
            'CURRENCY': 2008,
            'TRADE_DATE': '2022-11-08',
            'TRDTIM_1': '10:55:30',
            'OPEN_PRC': 104.78,
            'HST_CLOSE': 104.72,
            'BID': 106.36,
            'ASK': 106.38,
            'NEWS': 'YYYY',
            'NEWS_TIME': '07:53:03',
            'BIDSIZE': 5000,
            'ASKSIZE': 17667,
            'ACVOL_1': 10002800,
            'EARNINGS': 6.07,
            'YIELD': 7.2002,
            'PERATIO': 17.2521,
            'DIVPAYDATE': '2022-08-05',
            'EXDIVDATE': '2022-06-01',
            'BLKCOUNT': None,
            'BLKVOLUM': None,
            'TRD_UNITS': 20,
            'LOT_SIZE': 1,
            'PCTCHNG': 1.566,
            'CLOSE_BID': 104.72,
            'CLOSE_ASK': 104.76,
            'DIVIDEND': 7.54,
            'NUM_MOVES': 2709,
            'OFFCL_CODE': 'BH4HKS3',
            'HSTCLSDATE': '2022-11-07',
            'YRHIGH': 141.6,
            'YRLOW': 97.4,
            'LIFE_HIGH': 141.6,
            'LIFE_LOW': 97.4,
            'TURNOVER': 1054.5832,
            'BOND_TYPE': 186,
            'YCHIGH_IND': None,
            'YCLOW_IND': None,
            'CUM_EX_MKR': 0,
            'PRC_QL_CD': None,
            'PRC_QL2': 0,
            'MID_PRICE': 106.37,
            'MID_NET_CH': 1.63,
            'MID_CLOSE': 104.74,
            'TRDVOL_1': 5000,
            'TOT_MOVES': 2742,
            'LOT_SIZE_A': 1,
            'RECORDTYPE': 113,
            'ACT_TP_1': 63,
            'SEC_ACT_1': 106.37,
            'SEC_ACT_2': 106.37,
            'SEC_ACT_3': 106.37,
            'SEC_ACT_4': 106.37,
            'SEC_ACT_5': 106.33,
            'OPEN_TONE': 'A',
            'BID_TONE': None,
            'ASK_TONE': None,
            'CLOSE_TONE': None,
            'IRGPRC': 104.892,
            'IRGVOL': 3049,
            'IRGCOND': 39,
            'TIMCOR': '09:00:19',
            'INSPRC': 104.892,
            'INSVOL': 2939,
            'SALTIM': '10:55:30',
            'TNOVER_SC': 5,
            'PRIMACT_1': 104.78,
            'BCAST_REF': 'VOD.L',
            'LONGLINK1': '0#.SET1',
            'OFF_CD_IND': 27,
            'VALUE_DT1': '2022-11-07',
            'QTE_CNT1': 15000,
            'QTE_CNT2': 105.429,
            'ACT_FLAG1': 'A',
            'ACT_FLAG2': 'S',
            'ACT_FLAG3': 'A',
            'ACT_FLAG4': 'A',
            'ACT_FLAG5': 'A',
            'SEC_VOL1': 8353623,
            'GEN_TEXT16': '651349586894058',
            'GEN_VAL1': 106.36,
            'GEN_VAL2': 106.62,
            'GEN_VAL3': 104.6,
            'GV1_TEXT': 'OBLast',
            'GV4_TEXT': 'SET1',
            'QCNT1_IND': 20,
            'SEQNUM': 2490541,
            'QUOTIM': '10:55:35',
            'GV1_DATE': '2022-11-08',
            'GEN_VAL6': 104.78,
            'GEN_VAL7': 630748,
            'GEN_VAL8': 105.417,
            'GEN_VAL9': 1649177,
            'GEN_VAL10': 83.51,
            'GV5_TEXT': 'FE10',
            'GV6_TEXT': 'XLON',
            'GV7_TEXT': 'Auc',
            'GV2_DATE': '2022-11-08',
            'GN_TXT16_2': None,
            'GN_TXT16_4': 'Crest',
            'OFF_CD_IN2': 25,
            'OFFC_CODE2': 'GB00BH4HKS39',
            'EXCHTIM': '10:55:30',
            'CONDCODE_1': 'A',
            'CONDCODE_2': None,
            'COLID_2': 15,
            'COLID_3': 15,
            'COLID_4': 15,
            'COLID_5': 14,
            'YRHI_IND': 1,
            'YRLO_IND': 1,
            'PREF_DISP': 8374,
            'HST_CLOSE3': None,
            'COLID_6': 15,
            'ADJUST_CLS': 104.72,
            'RDN_EXCHD2': 64,
            'LIST_DATE': '2014-02-24',
            'GV1_CURRCY': 2008,
            'GV2_CURRCY': 2008,
            'LIST_MKT': 'SETS',
            'DELIST_DAT': None,
            'PREV_DISP': 1852,
            'PRC_QL3': 105,
            '52WK_HIGH': 141.6,
            '52WK_LOW': 97.4,
            'MPV': None,
            'OFF_CLOSE': None,
            'QUOTE_DATE': '2022-11-08',
            'TRDVOL_2': 2719,
            'TRDVOL_3': 1726,
            'TRDVOL_4': 709,
            'TRDVOL_5': 5882,
            'VWAP': 105.4288,
            'PROV_SYMB': '133215',
            'MULTIPLIER': 1,
            '52W_HDAT': '2022-02-10',
            '52W_HIND': None,
            '52W_LDAT': '2022-10-12',
            '52W_LIND': None,
            'BID_ASK_DT': '2022-11-07',
            'CRSTRD_PRC': None,
            'ISIN_CODE': 'GB00BH4HKS39',
            'MNEMONIC': 'VOD',
            'SEC_CHN': None,
            'SEDOL': 'BH4HKS3',
            'VOL_DEC': 5000,
            'MKOASK_VOL': None,
            'MKOBID_VOL': None,
            'MKT_SECTOR': 'FE10',
            'MKT_SEGMNT': 'SET1',
            'PERIOD_CDE': 'T',
            'TRDTIM_MS': 39330846,
            'SALTIM_MS': 39330846,
            'QUOTIM_MS': 39335161,
            'TIMCOR_MS': 32419453,
            'SEQ_NO': 115616,
            'BLK_PRC1': None,
            'OPN_AUC': 104.78,
            'INT_AUC': None,
            'CLS_AUC': None,
            'OPN_AUCVOL': 630748,
            'INT_AUCVOL': None,
            'CLS_AUCVOL': None,
            'ORDBK_VWAP': 105.417,
            'ORDBK_VOL': 8353623,
            'OFFBK_VOL': 1649177,
            'MKT_OPEN': 104.78,
            'MKT_LOW': 104.6,
            'MKT_HIGH': 106.62,
            'PDTRDPRC': None,
            'PREDAYVOL': None,
            'PDTRDDATE': None,
            'ORDBK_TRD': 106.36,
            'TRADE_ID': '651349586894058',
            'IND_AUC': 104.78,
            'IND_AUCVOL': 630748,
            'CLR_HOUSE': None,
            'NML_MKT_SZ': 1000,
            'TRD_TYPE': None,
            'OFFBK_PRC': 106.36,
            'ASK_TIM_MS': 39335161,
            'BID_TIM_MS': 39330847,
            'AVTURNOVER': 16966929727,
            'IPO_PRC': None,
            'RCS_AS_CLA': 'ORD',
            'IMB_ACT_TP': 1,
            'IMB_SH': 22683,
            'IMB_SIDE': 3,
            'IRGDATE': '2022-11-08',
            'PRICE_METH': 28,
            'TURN_BLOCK': None,
            'TRD_IND_1': 'A',
            'TRD_IND_2': 'S',
            'TRD_IND_3': 'A',
            'TRD_IND_4': 'A',
            'TRD_IND_5': 'A',
            'LSTSALCOND': '0',
            'IRGSALCOND': None,
            'INSSALCOND': None,
            'MID_PRICE1': 106.37,
            'PCT_OB_VOL': 83.513,
            'OFFBK_DATE': '2022-11-08',
            'CONTEXT_ID': 1885,
            'CF_ASK': 106.38,
            'CF_BID': 106.36,
            'CF_CLOSE': 104.72,
            'CF_DATE': '2022-11-08',
            'CF_EXCHNG': 64,
            'CF_HIGH': 106.62,
            'CF_LAST': 106.36,
            'CF_LOTSIZE': 1,
            'CF_LOW': 104.6,
            'CF_NETCHNG': 1.64,
            'CF_SOURCE': 'LSE',
            'CF_TICK': 1,
            'CF_TIME': '10:55:30',
            'CF_VOLUME': 10002800,
            'CF_YIELD': 7.2002,
            'IRG_TRDID': '886364908541386864',
            'PRC_TICK': None,
            'SUS_DATE': None,
            'OPEN_T_MS': 28800834,
            'HIGH_T_MS': 39193296,
            'LOW_T_MS': 28893100,
            'CF_NAME': 'VODAFONE GROUP',
            'IRG_SEQNO': 135803,
            'INS_SEQNO': 135807,
            'PREV_RIC': None,
            'MBP_RIC': 'VOD.LO',
            'OFF_CL_TIM': None,
            'DDS_DSO_ID': 12477,
            'BR_LINK5': 'VODl.TRE',
            'CF_CURR': 2008,
            'SPS_SP_RIC': '.[SPSLSEGTP01L1',
            'HALT_REASN': None,
            'ORD_ENT_ST': 1,
            'TRVOL_ONBK': 5000,
            'TRVOLOFFBK': 2719,
            'CAN_PRC': 104.892,
            'CAN_VOL': 3049,
            'CAN_COND': 39,
            'CAN_COND_N': None,
            'CAN_TRD_ID': '886364908541386864',
            'MIC_CODE': 'XLON',
            'TRD_STATUS': 1,
            'HALT_RSN': 1,
            'TRG_RSM_TM': None,
            'HALT_DATE': '2019-08-16',
            'HALT_TIME': '08:16:33',
            'ADJ_ENDTIM': None,
            'OFF_CLS_DT': None,
            'OB_TRD_DT': '2022-11-08',
            'CAN_DATE': '2022-11-08',
            'INSTRD_DT': '2022-11-08',
            'IND_AUCDT': '2022-11-08',
            'DELBY_DT': None,
            'OFFBKSEQNO': 192501,
            'PD_SEQNO': None,
            'SMS_MKT_SZ': 10000,
            'BLKTRDVOL': None,
            'PDACVOL': None,
            'OF_NUM_MOV': 467,
            'EXC_MKT_SZ': 15000,
            'AC_VOL_CRS': None,
            'MIN_ORD_SZ': 1,
            'CAN_SEQNO': 93316,
            'ELG_NUMMOV': 2242,
            'BLK_SEQNO': None,
            'CRS_SEQNO': None,
            'CRS_TRDVOL': None,
            'CRS_NUMOV': None,
            'AC_TRN_CRS': None,
            'OFFBK_TNOV': 173.97032,
            'OFFBK_HIGH': 106.6,
            'OFFBK_LOW': 104.6,
            'CB_REFPRC': None,
            'BAS_THRES': 5,
            'SEE_RIC': None,
            'BCASTREF32': 'VOD.L',
            'TRDAUCTP_N': 'O',
            'ASK_TONE1': None,
            'BID_TONE1': None,
            'XMIC_CODE': 'XLON',
            'CRSSALCOND': None,
            'TICK_SZIDX': 'TM_48',
            'CAN_CCY': 'GBp',
            'CAN_XID': 'XLON',
            'TRD_P_XID': 'XLON',
            'OFFBK_CD_N': None,
            'PD_SALCOND': None,
            'MKT_TIER': 'SET1',
            'MMT_CLASS': '12-------PH---',
            'INST_CLA_N': 'DE',
            'RCS_AS_CL2': None,
            'OFFBKTRDID': '897177108336025712',
            'PD_TRDID': None,
            'PERIOD_CD2': 'T',
            'INS_TRDID': '589092012129198192',
            'BLK_TRDID': None,
            'CRS_TRDID': None,
            'SRC_SYMB': '72057594038061151',
            'INST_PHASE': 3,
            'LIST_STAT': 1,
            'INSTIM_MS': 29997515,
            'IRGTIM_MS': 32419453,
            'OFBKTIM_MS': 39326126,
            'BLK_DATE': None,
            'CRS_DATE': None,
            'HLT_RSM_DT': '2019-08-16',
            'SRC_ES_DT': '2022-11-08',
            'CB_REFPRC2': None,
            'CB_INST_T1': 8,
            'CB_INST_T2': 3,
            'PRETRD_LIS': 54618200,
            'CANVOL_DEC': 3049,
            'BLKSALCOND': None,
            'IND_AUC_TP': 'O',
            'ADMIN_COND': '1',
            'MMT_VER': '3.04',
            'MIFIR_ID': 'SHRS',
            'MIFIR_U_AS': None,
            'PDTRDP_XID': None,
            'OFBK_P_XID': 'SINT',
            'FISN': 'VODE GROU/PAR VTG FPD 0.2095238',
            'PRC_TCK_TP': 2,
            'CLR_FLAG': 1,
            'QTE_ENT_ST': 0,
            'PHASE_RSN': 1,
            'ELIGBL_TRD': 1,
            'LIQIND_INS': 2,
            'DVC_IND': 1,
            'LOTSZUNIT2': 53,
            'TR_TRD_FLG': 1,
            'CB_TYPE': 1,
            'CAN_TRTFLG': 5,
            'CB_TYPE2': 2,
            'PD_P_CCY': None,
            'CAN_P_CCY': 2008,
            'BLKTIM_MS': None,
            'PDTRDTM_MS': None,
            'INDAUC_MS': '08:00:00.736',
            'OFFBKHI_MS': '10:53:16.046',
            'OFFBKLO_MS': '08:02:13.127',
            'CRSTIM_MS': None,
            'HLT_RSM_MS': '08:20:00.012',
            'HALT_TM_MS': '08:16:33.336',
            'OFF_CLS_MS': None,
            'ASK_TIM_NS': '10:55:35.161017',
            'BID_TIM_NS': '10:55:30.847954',
            'QUOTIM_NS': '10:55:35.161017',
            'SALTIM_NS': '10:55:30.846483',
            'TRD_TYP_NS': '08:00:00.82673',
            'IRGTIM_NS': '09:00:19.453239',
            'OFBKTIM_NS': '10:55:26.126787',
            'BLKTIM_NS': None,
            'INSTIM_NS': '08:19:57.515',
            'CAN_TIM_NS': '08:19:57.515',
            'CRSTIM_NS': None,
            'PDTRDTM_NS': None,
            'HIGH_T_NS': '10:53:13.296985',
            'LOW_T_NS': '08:01:33.10022',
            'SRC_ES_NS': '10:55:30.846803',
            'IMB_TIM_NS': '08:00:00.736152',
            'HALT_TM_NS': '08:16:33.336062',
            'HLT_RSM_NS': '08:20:00.0121',
            'OFF_CLS_NS': None,
            'PHA_STM_NS': '08:00:00.82673',
            'TRG_RSM_NS': None,
            'ELG_ACVOL': 8353623,
            'VEH_PERMID': None,
            'ELG_TNOV': 880612878.46,
            'EX_VOL_UNS': 10067408,
            'LTNOV_UNS': 531800,
            'TRNOVR_UNS': 1054583201.5320158,
            'ACVOL_UNS': 10002800
        }
    },
    {
        'ID': 5,
        'Type': 'Status',
        'Key': {'Service': 'IDN_FD3', 'Name': 'IBM.N'},
        'State': {
            'Stream': 'Closed',
            'Data': 'Suspect',
            'Code': 'NotEntitled',
            'Text': 'Access Denied: User req to PE(62)'
        }
    },
]

# get history test data
UDF_GET_HISTORY_ONE_INSTRUMENT_NO_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "MKT_HIGH", "type": "number", "decimalChar": "."},
                    {"name": "MKT_LOW", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "MKT_OPEN", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "TRNOVR_UNS", "type": "number", "decimalChar": "."},
                    {"name": "VWAP", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "PERATIO", "type": "number", "decimalChar": "."},
                    {"name": "ORDBK_VOL", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "IND_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "OFFBK_VOL", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ORDBK_VWAP", "type": "number", "decimalChar": "."},
                    {"name": "IND_AUC", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OFF_CLOSE", "type": "number", "decimalChar": "."},
                    {"name": "CLS_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "OPN_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "OPN_AUC", "type": "number", "decimalChar": "."},
                    {"name": "CLS_AUC", "type": "number", "decimalChar": "."},
                    {"name": "INT_AUC", "type": "number", "decimalChar": "."},
                    {"name": "INT_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "EX_VOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "ALL_C_MOVE", "type": "number", "decimalChar": "."},
                    {"name": "ELG_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "NAVALUE", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-09-27",
                        7652,
                        7694,
                        7548,
                        669293,
                        7606,
                        7622,
                        7624,
                        5102433530.01501,
                        7623.6154,
                        7623,
                        47.4103,
                        569638,
                        6502,
                        282974,
                        99655,
                        7694,
                        7630.916,
                        7622,
                        7606,
                        7548,
                        7622,
                        282974,
                        16892,
                        7606,
                        7622,
                        None,
                        None,
                        789364,
                        6613,
                        6164,
                        None,
                    ],
                    [
                        "2022-09-26",
                        7489.15237,
                        7660,
                        7480,
                        627075,
                        7494,
                        7632,
                        7634,
                        4773442156.7861,
                        7612.2345,
                        7633,
                        46.3793,
                        533163,
                        7984,
                        192701,
                        93912,
                        7660,
                        7611.826,
                        7634,
                        7494,
                        7482,
                        7634,
                        192701,
                        4644,
                        7494,
                        7634,
                        None,
                        None,
                        677187,
                        8209,
                        7673,
                        None,
                    ],
                    [
                        "2022-09-23",
                        7461.98718,
                        7528,
                        7300,
                        525502,
                        7446,
                        7468,
                        7470,
                        3914411797.42,
                        7449.43887,
                        7469,
                        46.3793,
                        495162,
                        7688,
                        201094,
                        27640,
                        7528,
                        7449.858,
                        7468,
                        7446,
                        7300,
                        7468,
                        201094,
                        4947,
                        7446,
                        7468,
                        None,
                        None,
                        638640,
                        8116,
                        7424,
                        None,
                    ],
                    [
                        "2022-09-22",
                        7563.56,
                        7706,
                        7416,
                        759195,
                        7620,
                        7468,
                        7470,
                        5729651816.67,
                        7547.00074,
                        7469,
                        47.994,
                        480791,
                        5866,
                        244543,
                        278361,
                        7706,
                        7508.555,
                        7468,
                        7620,
                        7416,
                        7468,
                        244543,
                        3711,
                        7620,
                        7468,
                        None,
                        None,
                        910761,
                        6009,
                        5666,
                        None,
                    ],
                    [
                        "2022-09-21",
                        7663.44985,
                        7730,
                        7518,
                        1001952,
                        7552,
                        7728,
                        7730,
                        7631392654.3177,
                        7616.5246,
                        7729,
                        46.8762,
                        471364,
                        6981,
                        144538,
                        530588,
                        7730,
                        7678.82,
                        7728,
                        7552,
                        7518,
                        7728,
                        144538,
                        4575,
                        7552,
                        7728,
                        None,
                        None,
                        1151781,
                        7092,
                        6807,
                        None,
                    ],
                    [
                        "2022-09-20",
                        7763.06667,
                        7768,
                        7460,
                        513033,
                        7732,
                        7542,
                        7548,
                        3878593615.79,
                        7559.7715,
                        7545,
                        48.3542,
                        473450,
                        6890,
                        186298,
                        36986,
                        7768,
                        7559.729,
                        7548,
                        7732,
                        7460,
                        7548,
                        186298,
                        27764,
                        7732,
                        7548,
                        None,
                        None,
                        663257,
                        6999,
                        6407,
                        None,
                    ],
                    [
                        "2022-09-19",
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        7778,
                        48.3542,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        "2022-09-16",
                        7760,
                        7824,
                        7720,
                        2168875,
                        7760,
                        7770,
                        7786,
                        16851819857.53,
                        7769.846,
                        7778,
                        48.4536,
                        1015294,
                        7430,
                        619678,
                        1152524,
                        7824,
                        7778.599,
                        7786,
                        7760,
                        7720,
                        7786,
                        619678,
                        3973,
                        7760,
                        7786,
                        7748,
                        103606,
                        2577171,
                        7929,
                        7276,
                        None,
                    ],
                    [
                        "2022-09-15",
                        7895.55636,
                        7908,
                        7766,
                        422663,
                        7900,
                        7800,
                        7802,
                        3299449612.11,
                        7806.3314,
                        7801,
                        49.0622,
                        399733,
                        5081,
                        232161,
                        22606,
                        7908,
                        7806.016,
                        7802,
                        7900,
                        7766,
                        7802,
                        232161,
                        5668,
                        7900,
                        7802,
                        None,
                        None,
                        507673,
                        5324,
                        4851,
                        None,
                    ],
                    [
                        "2022-09-14",
                        7972.1,
                        8070,
                        7892,
                        521577,
                        7962,
                        7900,
                        7902,
                        4134076455.03,
                        7925.89236,
                        7901,
                        49.7081,
                        499343,
                        6976,
                        235608,
                        21464,
                        8070,
                        7924.937,
                        7900,
                        7962,
                        7892,
                        7900,
                        235608,
                        3225,
                        7962,
                        7900,
                        None,
                        None,
                        640027,
                        7101,
                        6746,
                        None,
                    ],
                    [
                        "2022-09-13",
                        8023.8095,
                        8162,
                        7942,
                        534518,
                        8134,
                        8004,
                        8006,
                        4285291504.4,
                        8016.4881,
                        8005,
                        50.2919,
                        454096,
                        6799,
                        199046,
                        76775,
                        8162,
                        8016.292,
                        8004,
                        8134,
                        7942,
                        8004,
                        199046,
                        5863,
                        8134,
                        8004,
                        None,
                        None,
                        683751,
                        6853,
                        6609,
                        None,
                    ],
                    [
                        "2022-09-12",
                        8028.12,
                        8098,
                        7954,
                        393139,
                        7998,
                        8094,
                        8098,
                        3165188290.65,
                        8051.06695,
                        8096,
                        49.7081,
                        374415,
                        5142,
                        163090,
                        18685,
                        8098,
                        8053.243,
                        8098,
                        7998,
                        7954,
                        8098,
                        163090,
                        7468,
                        7998,
                        8098,
                        None,
                        None,
                        508848,
                        5196,
                        4919,
                        None,
                    ],
                    [
                        "2022-09-09",
                        8024,
                        8090,
                        7956,
                        479583,
                        7956,
                        8004,
                        8010,
                        3848903522.51,
                        8025.5082,
                        8007,
                        49.7081,
                        381305,
                        5416,
                        182620,
                        98135,
                        8090,
                        8021.854,
                        8004,
                        7956,
                        7956,
                        8004,
                        182620,
                        1606,
                        7956,
                        8004,
                        None,
                        None,
                        602315,
                        5471,
                        5306,
                        None,
                    ],
                    [
                        "2022-09-08",
                        8044,
                        8060,
                        7688,
                        611208,
                        7964,
                        8004,
                        8006,
                        4847453609.7,
                        7930.94,
                        8005,
                        49.3355,
                        587774,
                        7217,
                        240248,
                        23394,
                        8060,
                        7932.403,
                        8004,
                        7964,
                        7688,
                        8004,
                        240248,
                        6609,
                        7964,
                        8004,
                        None,
                        None,
                        754372,
                        7318,
                        7011,
                        None,
                    ],
                    [
                        "2022-09-07",
                        7897.33333,
                        8000,
                        7838,
                        1050642,
                        7918,
                        7944,
                        7946,
                        8288071402.15,
                        7888.567,
                        7945,
                        49.4845,
                        412145,
                        7695,
                        167471,
                        638292,
                        8000,
                        7934.95,
                        7944,
                        7918,
                        7838,
                        7944,
                        167471,
                        5849,
                        7918,
                        7944,
                        None,
                        None,
                        1154149,
                        7753,
                        7199,
                        None,
                    ],
                    [
                        "2022-09-06",
                        7950,
                        7974,
                        7862,
                        362104,
                        7924,
                        7966,
                        7968,
                        2874146953.91,
                        7937.36362,
                        7967,
                        49.41,
                        347868,
                        5115,
                        125206,
                        13993,
                        7974,
                        7938.464,
                        7968,
                        7924,
                        7862,
                        7968,
                        125206,
                        3068,
                        7924,
                        7968,
                        None,
                        None,
                        486599,
                        5274,
                        5019,
                        None,
                    ],
                    [
                        "2022-09-05",
                        7859.75,
                        7962,
                        7778,
                        592614,
                        7930,
                        7954,
                        7956,
                        4683013244.54,
                        7911.6287,
                        7955,
                        49.7205,
                        309648,
                        4132,
                        140236,
                        582572,
                        7962,
                        7917.55,
                        7956,
                        7930,
                        7778,
                        7956,
                        140236,
                        6933,
                        7930,
                        7956,
                        None,
                        None,
                        640688,
                        4289,
                        3995,
                        None,
                    ],
                    [
                        "2022-09-02",
                        8000,
                        8010,
                        7868,
                        678603,
                        7978,
                        8006,
                        8008,
                        5404213577.17,
                        7963.77182,
                        8007,
                        49.2361,
                        389146,
                        6002,
                        121309,
                        288541,
                        8010,
                        7954.941,
                        8006,
                        7978,
                        7868,
                        8006,
                        121309,
                        10480,
                        7978,
                        8006,
                        None,
                        None,
                        697004,
                        6090,
                        5803,
                        None,
                    ],
                    [
                        "2022-09-01",
                        7922,
                        8120,
                        7904,
                        399309,
                        8052,
                        7926,
                        7928,
                        3176528830.76,
                        7955.032,
                        7927,
                        50.3167,
                        378100,
                        5453,
                        121772,
                        21041,
                        8120,
                        7953.505,
                        7928,
                        8052,
                        7904,
                        7928,
                        121772,
                        4371,
                        8052,
                        7928,
                        None,
                        None,
                        464271,
                        5622,
                        5214,
                        None,
                    ],
                    [
                        "2022-08-31",
                        8184.4,
                        8234,
                        8060,
                        648268,
                        8204,
                        8102,
                        8106,
                        5260572719,
                        8114.8267,
                        8104,
                        50.7763,
                        618395,
                        5212,
                        398190,
                        27712,
                        8234,
                        8114.731,
                        8102,
                        8204,
                        8060,
                        8102,
                        398190,
                        3770,
                        8204,
                        8102,
                        None,
                        None,
                        816294,
                        5710,
                        5056,
                        None,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                            {"name": "MKT_HIGH", "type": "number", "decimalChar": "."},
                            {"name": "MKT_LOW", "type": "number", "decimalChar": "."},
                            {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                            {"name": "MKT_OPEN", "type": "number", "decimalChar": "."},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRNOVR_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "VWAP", "type": "number", "decimalChar": "."},
                            {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                            {"name": "PERATIO", "type": "number", "decimalChar": "."},
                            {"name": "ORDBK_VOL", "type": "number", "decimalChar": "."},
                            {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                            {
                                "name": "IND_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OFFBK_VOL", "type": "number", "decimalChar": "."},
                            {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                            {
                                "name": "ORDBK_VWAP",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "IND_AUC", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                            {"name": "LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "OFF_CLOSE", "type": "number", "decimalChar": "."},
                            {
                                "name": "CLS_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "OPN_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OPN_AUC", "type": "number", "decimalChar": "."},
                            {"name": "CLS_AUC", "type": "number", "decimalChar": "."},
                            {"name": "INT_AUC", "type": "number", "decimalChar": "."},
                            {
                                "name": "INT_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "EX_VOL_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ALL_C_MOVE",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ELG_NUMMOV",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "NAVALUE", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-09-27",
                                7652,
                                7694,
                                7548,
                                669293,
                                7606,
                                7622,
                                7624,
                                5102433530.01501,
                                7623.6154,
                                7623,
                                47.4103,
                                569638,
                                6502,
                                282974,
                                99655,
                                7694,
                                7630.916,
                                7622,
                                7606,
                                7548,
                                7622,
                                282974,
                                16892,
                                7606,
                                7622,
                                None,
                                None,
                                789364,
                                6613,
                                6164,
                                None,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [["LSEG.L", "2021-12-31T00:00:00Z", 6740000000]],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {"displayName": "Revenue", "field": "TR.REVENUE"},
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 2,
                }
            ]
        }
    )
]

UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_FIELD_NAMES_IN_HEADERS = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [["LSEG.L", "2021-12-31T00:00:00Z", 6740000000]],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {"displayName": "Revenue", "field": "TR.REVENUE"},
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 2,
                }
            ]
        }
    )
]

UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_PRICING_FIELD = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 7622],
                    ["2022-09-26", 7632],
                    ["2022-09-23", 7468],
                    ["2022-09-22", 7468],
                    ["2022-09-21", 7728],
                    ["2022-09-20", 7542],
                    ["2022-09-16", 7770],
                    ["2022-09-15", 7800],
                    ["2022-09-14", 7900],
                    ["2022-09-13", 8004],
                    ["2022-09-12", 8094],
                    ["2022-09-09", 8004],
                    ["2022-09-08", 8004],
                    ["2022-09-07", 7944],
                    ["2022-09-06", 7966],
                    ["2022-09-05", 7954],
                    ["2022-09-02", 8006],
                    ["2022-09-01", 7926],
                    ["2022-08-31", 8102],
                    ["2022-08-30", 8176],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 7622]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_AND_ONE_PRICING_FIELD = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [["LSEG.L", "2022-08-18T00:00:00Z", "GBP"]],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Currency",
                                "field": "TR.REVENUEMEAN.currency",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 2,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 7622],
                    ["2022-09-26", 7632],
                    ["2022-09-23", 7468],
                    ["2022-09-22", 7468],
                    ["2022-09-21", 7728],
                    ["2022-09-20", 7542],
                    ["2022-09-16", 7770],
                    ["2022-09-15", 7800],
                    ["2022-09-14", 7900],
                    ["2022-09-13", 8004],
                    ["2022-09-12", 8094],
                    ["2022-09-09", 8004],
                    ["2022-09-08", 8004],
                    ["2022-09-07", 7944],
                    ["2022-09-06", 7966],
                    ["2022-09-05", 7954],
                    ["2022-09-02", 8006],
                    ["2022-09-01", 7926],
                    ["2022-08-31", 8102],
                    ["2022-08-30", 8176],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 7622]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_ADC_FIELDS = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [["LSEG.L", "2022-08-18T00:00:00Z", 7284197000, "GBP"]],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Revenue - Mean",
                                "field": "TR.REVENUEMEAN",
                            },
                            {
                                "displayName": "Currency",
                                "field": "TR.REVENUEMEAN.currency",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 4,
                    "totalRowsCount": 2,
                }
            ]
        }
    )
]

UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_WITH_INTRADAY_INTERVAL = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [["LSEG.L", "2021-12-31T00:00:00Z", 6740000000]],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {"displayName": "Revenue", "field": "TR.REVENUE"},
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 2,
                }
            ]
        }
    )
]

UDF_GET_HISTORY_ONE_INST_ONE_PRICING_FIELD_WITH_INTRADAY_INTERVAL = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
                "interval": "PT10M",
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
                ],
                "data": [
                    ["2022-09-28T10:10:00.000000000Z", 7562],
                    ["2022-09-28T10:00:00.000000000Z", 7526],
                    ["2022-09-28T09:50:00.000000000Z", 7450],
                    ["2022-09-28T09:40:00.000000000Z", 7482],
                    ["2022-09-28T09:30:00.000000000Z", 7488],
                    ["2022-09-28T09:20:00.000000000Z", 7488],
                    ["2022-09-28T09:10:00.000000000Z", 7512],
                    ["2022-09-28T09:00:00.000000000Z", 7534],
                    ["2022-09-28T08:50:00.000000000Z", 7562],
                    ["2022-09-28T08:40:00.000000000Z", 7562],
                    ["2022-09-28T08:30:00.000000000Z", 7542],
                    ["2022-09-28T08:20:00.000000000Z", 7552],
                    ["2022-09-28T08:10:00.000000000Z", 7526],
                    ["2022-09-28T08:00:00.000000000Z", 7522],
                    ["2022-09-28T07:50:00.000000000Z", 7520],
                    ["2022-09-28T07:40:00.000000000Z", 7506],
                    ["2022-09-28T07:30:00.000000000Z", 7498],
                    ["2022-09-28T07:20:00.000000000Z", 7486],
                    ["2022-09-28T07:10:00.000000000Z", 7480],
                    ["2022-09-28T07:00:00.000000000Z", 7538],
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
                                "2022-09-28T10:19:01.738000000Z",
                                60752,
                                "2022-09-28T10:19:01.738000000Z",
                                "8132295",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_ONE_INST_ONE_ADC_WITH_NON_INTRADAY_INTERVAL = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [["LSEG.L", "2022-08-18T00:00:00Z", 7284197000]],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Revenue - Mean",
                                "field": "TR.REVENUEMEAN",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 2,
                }
            ]
        }
    )
]

UDF_GET_HISTORY_ONE_INST_ONE_PRICING_WITH_NON_INTRADAY_INTERVAL = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 7622],
                    ["2022-09-26", 7632],
                    ["2022-09-23", 7468],
                    ["2022-09-22", 7468],
                    ["2022-09-21", 7728],
                    ["2022-09-20", 7542],
                    ["2022-09-16", 7770],
                    ["2022-09-15", 7800],
                    ["2022-09-14", 7900],
                    ["2022-09-13", 8004],
                    ["2022-09-12", 8094],
                    ["2022-09-09", 8004],
                    ["2022-09-08", 8004],
                    ["2022-09-07", 7944],
                    ["2022-09-06", 7966],
                    ["2022-09-05", 7954],
                    ["2022-09-02", 8006],
                    ["2022-09-01", 7926],
                    ["2022-08-31", 8102],
                    ["2022-08-30", 8176],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 7622]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_ONE_INS_TWO_ADC_TWO_HP_NON_INTRADAY_START_END_DATE = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2019-12-31T00:00:00Z", 7292000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-31T00:00:00Z", 4042000000, ""],
                        ["IBM", "2020-12-16T00:00:00Z", "", 73950729070],
                        ["IBM", "2020-12-16T00:00:00Z", "", 73950729070],
                        ["IBM", "2020-12-16T00:00:00Z", "", 73950729070],
                        ["IBM", "2020-12-16T00:00:00Z", "", 73950729070],
                        ["IBM", "2020-12-16T00:00:00Z", "", 73950729070],
                        ["IBM", "2020-12-16T00:00:00Z", "", 73950729070],
                        ["IBM", "2021-01-12T00:00:00Z", "", 73959395730],
                        ["IBM", "2021-01-12T00:00:00Z", "", 73959395730],
                        ["IBM", "2021-01-14T00:00:00Z", "", 73965995730],
                        ["IBM", "2021-01-14T00:00:00Z", "", 73965995730],
                        ["IBM", "2021-01-18T00:00:00Z", "", 73987395730],
                        ["IBM", "2021-01-18T00:00:00Z", "", 73987395730],
                        ["IBM", "2021-01-21T00:00:00Z", "", 74726080400],
                        ["IBM", "2021-01-22T00:00:00Z", "", 74238533200],
                        ["IBM", "2021-01-25T00:00:00Z", "", 74191285570],
                        ["IBM", "2021-01-25T00:00:00Z", "", 74191285570],
                        ["IBM", "2021-01-27T00:00:00Z", "", 74195199870],
                        ["IBM", "2021-01-27T00:00:00Z", "", 74195199870],
                        ["IBM", "2021-01-27T00:00:00Z", "", 74195199870],
                        ["IBM", "2021-01-27T00:00:00Z", "", 74195199870],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Net Income after Tax",
                                "field": "TR.F.NETINCAFTERTAX",
                            },
                            {
                                "displayName": "Revenue - Mean",
                                "field": "TR.REVENUEMEAN",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 4,
                    "totalRowsCount": 41,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
]

UDF_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_PRICING_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 7622, 7624],
                    ["2022-09-26", 7632, 7634],
                    ["2022-09-23", 7468, 7470],
                    ["2022-09-22", 7468, 7470],
                    ["2022-09-21", 7728, 7730],
                    ["2022-09-20", 7542, 7548],
                    ["2022-09-16", 7770, 7786],
                    ["2022-09-15", 7800, 7802],
                    ["2022-09-14", 7900, 7902],
                    ["2022-09-13", 8004, 8006],
                    ["2022-09-12", 8094, 8098],
                    ["2022-09-09", 8004, 8010],
                    ["2022-09-08", 8004, 8006],
                    ["2022-09-07", 7944, 7946],
                    ["2022-09-06", 7966, 7968],
                    ["2022-09-05", 7954, 7956],
                    ["2022-09-02", 8006, 8008],
                    ["2022-09-01", 7926, 7928],
                    ["2022-08-31", 8102, 8106],
                    ["2022-08-30", 8176, 8178],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 7622, 7624]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_TWO_INSTRUMENTS_WITHOUT_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "TRNOVR_UNS", "type": "number", "decimalChar": "."},
                    {"name": "VWAP", "type": "number", "decimalChar": "."},
                    {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                    {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "TRD_STATUS", "type": "number", "decimalChar": "."},
                    {"name": "SALTIM", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-09-27",
                        121.74,
                        123.95,
                        121.09,
                        1335006,
                        122.6,
                        121.76,
                        121.77,
                        162900375,
                        122.0222,
                        2,
                        559187,
                        10219,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-26",
                        122.01,
                        124.25,
                        121.76,
                        1287055,
                        122.3,
                        122,
                        122.01,
                        157505074,
                        122.3763,
                        2,
                        593148,
                        9160,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-23",
                        122.71,
                        124.57,
                        121.75,
                        1555461,
                        124.53,
                        122.75,
                        122.76,
                        191160601,
                        122.8964,
                        2,
                        684185,
                        11039,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-22",
                        125.31,
                        126.49,
                        124.45,
                        1152042,
                        124.76,
                        125.31,
                        125.32,
                        144521845,
                        125.4484,
                        2,
                        450245,
                        9169,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-21",
                        124.93,
                        127.77,
                        124.92,
                        1096128,
                        126.89,
                        124.94,
                        124.95,
                        137967478,
                        125.868,
                        2,
                        477129,
                        8477,
                        1,
                        72600,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                            {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                            {"name": "LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRNOVR_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "VWAP", "type": "number", "decimalChar": "."},
                            {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                            {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                            {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRD_STATUS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "SALTIM", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-09-27",
                                121.74,
                                123.95,
                                121.09,
                                1335006,
                                122.6,
                                121.76,
                                121.77,
                                162900375,
                                122.0222,
                                2,
                                559187,
                                10219,
                                1,
                                72600,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASIAOP_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIAHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIALO_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIACL_BID", "type": "number", "decimalChar": "."},
                    {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMEROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-09-28",
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        0.9592,
                        0.96,
                        0.9534,
                        0.9577,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        "2022-09-27",
                        0.9592,
                        0.9596,
                        0.967,
                        0.9567,
                        0.9609,
                        0.9594,
                        104222,
                        0.957,
                        0.9673,
                        0.9609,
                        0.967,
                        0.9583,
                        0.9645,
                        0.9635,
                        0.967,
                        0.9592,
                        0.9612,
                        0.9627,
                        0.9652,
                        0.9567,
                        0.9592,
                        0.9611,
                    ],
                    [
                        "2022-09-26",
                        0.9606,
                        0.9609,
                        0.9709,
                        0.9565,
                        0.9678,
                        0.96075,
                        109840,
                        0.9569,
                        0.9712,
                        0.9684,
                        0.9709,
                        0.9565,
                        0.9676,
                        0.9627,
                        0.9701,
                        0.9608,
                        0.9621,
                        0.9641,
                        0.9689,
                        0.9598,
                        0.9606,
                        0.968,
                    ],
                    [
                        "2022-09-23",
                        0.969,
                        0.9694,
                        0.9851,
                        0.9666,
                        0.9835,
                        0.9692,
                        90975,
                        0.9669,
                        0.9854,
                        0.9835,
                        0.9851,
                        0.9765,
                        0.9774,
                        0.9821,
                        0.9838,
                        0.97,
                        0.9716,
                        0.9751,
                        0.9774,
                        0.9666,
                        0.969,
                        0.9839,
                    ],
                    [
                        "2022-09-22",
                        0.9836,
                        0.984,
                        0.9907,
                        0.9807,
                        0.9836,
                        0.9838,
                        103843,
                        0.981,
                        0.9909,
                        0.9836,
                        0.9853,
                        0.9807,
                        0.9843,
                        0.9828,
                        0.9907,
                        0.981,
                        0.9838,
                        0.9874,
                        0.9887,
                        0.981,
                        0.9836,
                        0.9838,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "BID_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                            {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                            {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                            {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                            {
                                "name": "ASK_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAOP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIALO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIACL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                            {
                                "name": "AMEROP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERLO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERCL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-09-28",
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                0.9592,
                                0.96,
                                0.9534,
                                0.9577,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_TWO_INST_ONE_ADC_QUARTERLY_INTERVAL_START_DATE = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["IBM", "2018-12-31T00:00:00Z", 10760000000],
                        ["MSFT.O", "2019-06-30T00:00:00Z", 39397000000],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Net Income after Tax",
                                "field": "TR.F.NETINCAFTERTAX",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 3,
                }
            ]
        }
    )
]

UDF_GET_HISTORY_TWO_INSTRUMENTS_TWO_HP_DAILY_INTERVAL_START_DATE = [
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 0.9592, 0.9596],
                    ["2022-09-26", 0.9606, 0.9609],
                    ["2022-09-23", 0.969, 0.9694],
                    ["2022-09-22", 0.9836, 0.984],
                    ["2022-09-21", 0.9837, 0.9839],
                    ["2022-09-20", 0.997, 0.9974],
                    ["2022-09-19", 1.0022, 1.0026],
                    ["2022-09-16", 1.0015, 1.0019],
                    ["2022-09-15", 0.9999, 1.0003],
                    ["2022-09-14", 0.9977, 0.9981],
                    ["2022-09-13", 0.997, 0.9974],
                    ["2022-09-12", 1.0119, 1.0122],
                    ["2022-09-09", 1.0039, 1.0043],
                    ["2022-09-08", 0.9994, 0.9998],
                    ["2022-09-07", 0.9999, 1.0003],
                    ["2022-09-06", 0.9902, 0.9906],
                    ["2022-09-05", 0.9926, 0.993],
                    ["2022-09-02", 0.9951, 0.9955],
                    ["2022-09-01", 0.9944, 0.9947],
                    ["2022-08-31", 1.0057, 1.0061],
                ],
            }
        ]
    ),
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 1.0731, 1.0734],
                    ["2022-09-26", 1.0684, 1.0688],
                    ["2022-09-23", 1.0856, 1.086],
                    ["2022-09-22", 1.1257, 1.1261],
                    ["2022-09-21", 1.1266, 1.127],
                    ["2022-09-20", 1.1379, 1.1383],
                    ["2022-09-19", 1.1429, 1.1435],
                    ["2022-09-16", 1.1412, 1.1416],
                    ["2022-09-15", 1.1463, 1.1469],
                    ["2022-09-14", 1.1535, 1.1539],
                    ["2022-09-13", 1.1491, 1.1495],
                    ["2022-09-12", 1.1679, 1.1688],
                    ["2022-09-09", 1.1587, 1.1591],
                    ["2022-09-08", 1.15, 1.1504],
                    ["2022-09-07", 1.1525, 1.1529],
                    ["2022-09-06", 1.1516, 1.1524],
                    ["2022-09-05", 1.1513, 1.1517],
                    ["2022-09-02", 1.1507, 1.1511],
                    ["2022-09-01", 1.1542, 1.1546],
                    ["2022-08-31", 1.1622, 1.1625],
                ],
            }
        ]
    ),
]

UDF_GET_HISTORY_TWO_INSTRUMENTS_ADC_AND_HP_1H_INTERVAL_FIELD_NAMES = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["VOD.L", "2022-03-31T00:00:00Z", 2624000000, ""],
                        ["VOD.L", "2022-09-22T00:00:00Z", "", "EUR"],
                        ["MSFT.O", "2022-06-30T00:00:00Z", 72738000000, ""],
                        ["MSFT.O", "2022-09-26T00:00:00Z", "", "USD"],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Net Income after Tax",
                                "field": "TR.F.NETINCAFTERTAX",
                            },
                            {
                                "displayName": "Currency",
                                "field": "TR.REVENUEMEAN.currency",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 4,
                    "totalRowsCount": 5,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "interval": "PT60M",
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
                    ["2022-09-28T12:00:00.000000000Z", 103.98, 104.04],
                    ["2022-09-28T11:00:00.000000000Z", 104.2, 104.24],
                    ["2022-09-28T10:00:00.000000000Z", 104.5, 104.56],
                    ["2022-09-28T09:00:00.000000000Z", 102.68, 102.72],
                    ["2022-09-28T08:00:00.000000000Z", 103.18, 103.22],
                    ["2022-09-28T07:00:00.000000000Z", 103.58, 103.62],
                    ["2022-09-28T06:00:00.000000000Z", 121.38, 89.73],
                    ["2022-09-28T04:00:00.000000000Z", 105.02, 107.2],
                    ["2022-09-27T16:00:00.000000000Z", 105.02, 107.2],
                    ["2022-09-27T15:00:00.000000000Z", 105.54, 105.64],
                    ["2022-09-27T14:00:00.000000000Z", 106.84, 106.88],
                    ["2022-09-27T13:00:00.000000000Z", 106.66, 106.72],
                    ["2022-09-27T12:00:00.000000000Z", 106.7, 106.74],
                    ["2022-09-27T11:00:00.000000000Z", 106.54, 106.58],
                    ["2022-09-27T10:00:00.000000000Z", 106.06, 106.12],
                    ["2022-09-27T09:00:00.000000000Z", 105.82, 105.86],
                    ["2022-09-27T08:00:00.000000000Z", 106.38, 106.44],
                    ["2022-09-27T07:00:00.000000000Z", 106.72, 106.76],
                    ["2022-09-27T06:00:00.000000000Z", 111.14, 92.8],
                    ["2022-09-27T04:00:00.000000000Z", 105.02, 110],
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
                                "2022-09-28T12:33:38.430000000Z",
                                15808,
                                "2022-09-28T12:33:38.430000000Z",
                                "12664891",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "interval": "PT60M",
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
                    ["2022-09-28T12:00:00.000000000Z", 103.98, 104.04],
                    ["2022-09-28T11:00:00.000000000Z", 104.2, 104.24],
                    ["2022-09-28T10:00:00.000000000Z", 104.5, 104.56],
                    ["2022-09-28T09:00:00.000000000Z", 102.68, 102.72],
                    ["2022-09-28T08:00:00.000000000Z", 103.18, 103.22],
                    ["2022-09-28T07:00:00.000000000Z", 103.58, 103.62],
                    ["2022-09-28T06:00:00.000000000Z", 121.38, 89.73],
                    ["2022-09-28T04:00:00.000000000Z", 105.02, 107.2],
                    ["2022-09-27T16:00:00.000000000Z", 105.02, 107.2],
                    ["2022-09-27T15:00:00.000000000Z", 105.54, 105.64],
                    ["2022-09-27T14:00:00.000000000Z", 106.84, 106.88],
                    ["2022-09-27T13:00:00.000000000Z", 106.66, 106.72],
                    ["2022-09-27T12:00:00.000000000Z", 106.7, 106.74],
                    ["2022-09-27T11:00:00.000000000Z", 106.54, 106.58],
                    ["2022-09-27T10:00:00.000000000Z", 106.06, 106.12],
                    ["2022-09-27T09:00:00.000000000Z", 105.82, 105.86],
                    ["2022-09-27T08:00:00.000000000Z", 106.38, 106.44],
                    ["2022-09-27T07:00:00.000000000Z", 106.72, 106.76],
                    ["2022-09-27T06:00:00.000000000Z", 111.14, 92.8],
                    ["2022-09-27T04:00:00.000000000Z", 105.02, 110],
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
                                "2022-09-28T12:33:38.430000000Z",
                                15808,
                                "2022-09-28T12:33:38.430000000Z",
                                "12664891",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.O"},
                "interval": "PT60M",
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
                    ["2022-09-28T12:00:00.000000000Z", 235.7, 236.33],
                    ["2022-09-28T11:00:00.000000000Z", 234.38, 234.84],
                    ["2022-09-28T10:00:00.000000000Z", 234.99, 235.55],
                    ["2022-09-28T09:00:00.000000000Z", 233, 233.27],
                    ["2022-09-28T08:00:00.000000000Z", 234, 234.5],
                    ["2022-09-27T23:00:00.000000000Z", 236.31, 236.45],
                    ["2022-09-27T22:00:00.000000000Z", 236.41, 236.6],
                    ["2022-09-27T21:00:00.000000000Z", 236.39, 236.48],
                    ["2022-09-27T20:00:00.000000000Z", 236.26, 236.6],
                    ["2022-09-27T19:00:00.000000000Z", 236.41, 236.49],
                    ["2022-09-27T18:00:00.000000000Z", 236.41, 236.43],
                    ["2022-09-27T17:00:00.000000000Z", 235.2, 235.22],
                    ["2022-09-27T16:00:00.000000000Z", 235.65, 235.67],
                    ["2022-09-27T15:00:00.000000000Z", 236.74, 236.77],
                    ["2022-09-27T14:00:00.000000000Z", 239.56, 239.58],
                    ["2022-09-27T13:00:00.000000000Z", 240.07, 240.11],
                    ["2022-09-27T12:00:00.000000000Z", 239.82, 240.07],
                    ["2022-09-27T11:00:00.000000000Z", 240.38, 240.49],
                    ["2022-09-27T10:00:00.000000000Z", 239.9, 240.21],
                    ["2022-09-27T09:00:00.000000000Z", 239.09, 239.65],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-09-28T12:33:42.679000000Z",
                                8720,
                                "2022-09-28T12:33:42.679000000Z",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.O"},
                "interval": "PT60M",
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
                    ["2022-09-28T12:00:00.000000000Z", 235.7, 236.33],
                    ["2022-09-28T11:00:00.000000000Z", 234.38, 234.84],
                    ["2022-09-28T10:00:00.000000000Z", 234.99, 235.55],
                    ["2022-09-28T09:00:00.000000000Z", 233, 233.27],
                    ["2022-09-28T08:00:00.000000000Z", 234, 234.5],
                    ["2022-09-27T23:00:00.000000000Z", 236.31, 236.45],
                    ["2022-09-27T22:00:00.000000000Z", 236.41, 236.6],
                    ["2022-09-27T21:00:00.000000000Z", 236.39, 236.48],
                    ["2022-09-27T20:00:00.000000000Z", 236.26, 236.6],
                    ["2022-09-27T19:00:00.000000000Z", 236.41, 236.49],
                    ["2022-09-27T18:00:00.000000000Z", 236.41, 236.43],
                    ["2022-09-27T17:00:00.000000000Z", 235.2, 235.22],
                    ["2022-09-27T16:00:00.000000000Z", 235.65, 235.67],
                    ["2022-09-27T15:00:00.000000000Z", 236.74, 236.77],
                    ["2022-09-27T14:00:00.000000000Z", 239.56, 239.58],
                    ["2022-09-27T13:00:00.000000000Z", 240.07, 240.11],
                    ["2022-09-27T12:00:00.000000000Z", 239.82, 240.07],
                    ["2022-09-27T11:00:00.000000000Z", 240.38, 240.49],
                    ["2022-09-27T10:00:00.000000000Z", 239.9, 240.21],
                    ["2022-09-27T09:00:00.000000000Z", 239.09, 239.65],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-09-28T12:33:42.679000000Z",
                                8720,
                                "2022-09-28T12:33:42.679000000Z",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_TWO_INSTS_ONE_ADC_FIELD_TWO_HP_TICK_START_DATE = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["IBM.N", "2021-04-25T00:00:00Z", 74397055190],
                        ["LSEG.L", "2021-05-10T00:00:00Z", 6935640740],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {
                                "displayName": "Revenue - Mean",
                                "field": "TR.REVENUEMEAN",
                            },
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 3,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27T20:00:02.001000000Z", "trade", 0, 0],
                    ["2022-09-27T20:00:00.163000000Z", "quote", 0, 0],
                    ["2022-09-27T19:59:59.998000000Z", "quote", 121.76, 121.77],
                    ["2022-09-27T19:59:59.998000000Z", "quote", 121.76, 121.77],
                    ["2022-09-27T19:59:59.997000000Z", "quote", 121.76, 121.77],
                    ["2022-09-27T19:59:59.997000000Z", "quote", 121.76, 121.77],
                    ["2022-09-27T19:59:59.982000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.962000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.958000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.901000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.900000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.855000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.855000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.855000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.855000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.784000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.713000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.630000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.608000000Z", "quote", 121.74, 121.77],
                    ["2022-09-27T19:59:59.533000000Z", "quote", 121.74, 121.77],
                ],
                "status": {
                    "code": "TS.Intraday.Warning.95004",
                    "message": "Trades interleaving with corrections is currently not "
                               "supported. Corrections will not be returned.",
                },
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-09-28T13:34:15.725000000Z",
                                60400,
                                "2022-09-28T13:34:15.725000000Z",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28T13:34:15.400000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.963000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.963000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.963000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.962000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.953000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.952000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.952000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.952000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.923000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.563000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.200000000Z", "quote", 7616, 7620],
                    ["2022-09-28T13:34:14.139000000Z", "quote", 7616, 7620],
                ],
                "status": {
                    "code": "TS.Intraday.Warning.95004",
                    "message": "Trades interleaving with corrections is currently not "
                               "supported. Corrections will not be returned.",
                },
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
                                "2022-09-28T13:34:15.400000000Z",
                                41376,
                                "2022-09-28T13:34:15.400000000Z",
                                "14561261",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_THREE_INSTRUMENTS_WITHOUT_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "TRNOVR_UNS", "type": "number", "decimalChar": "."},
                    {"name": "VWAP", "type": "number", "decimalChar": "."},
                    {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                    {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "TRD_STATUS", "type": "number", "decimalChar": "."},
                    {"name": "SALTIM", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-09-27",
                        121.74,
                        123.95,
                        121.09,
                        1335006,
                        122.6,
                        121.76,
                        121.77,
                        162900375,
                        122.0222,
                        2,
                        559187,
                        10219,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-26",
                        122.01,
                        124.25,
                        121.76,
                        1287055,
                        122.3,
                        122,
                        122.01,
                        157505074,
                        122.3763,
                        2,
                        593148,
                        9160,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-23",
                        122.71,
                        124.57,
                        121.75,
                        1555461,
                        124.53,
                        122.75,
                        122.76,
                        191160601,
                        122.8964,
                        2,
                        684185,
                        11039,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-22",
                        125.31,
                        126.49,
                        124.45,
                        1152042,
                        124.76,
                        125.31,
                        125.32,
                        144521845,
                        125.4484,
                        2,
                        450245,
                        9169,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-21",
                        124.93,
                        127.77,
                        124.92,
                        1096128,
                        126.89,
                        124.94,
                        124.95,
                        137967478,
                        125.868,
                        2,
                        477129,
                        8477,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-20",
                        126.3,
                        126.9,
                        125.53,
                        799630,
                        126.9,
                        126.3,
                        126.31,
                        100914959,
                        126.2021,
                        2,
                        357706,
                        7375,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-19",
                        127.73,
                        128.06,
                        126.28,
                        1320203,
                        126.5,
                        127.69,
                        127.73,
                        168291147,
                        127.4737,
                        2,
                        725956,
                        7910,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-16",
                        127.27,
                        127.49,
                        124.01,
                        5408858,
                        124.36,
                        127.23,
                        127.27,
                        685427466,
                        126.7231,
                        2,
                        4463300,
                        10894,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-15",
                        125.49,
                        127.39,
                        124.9,
                        1474804,
                        127.39,
                        125.49,
                        125.5,
                        185269243,
                        125.623,
                        3,
                        705660,
                        10066,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-14",
                        127.69,
                        129,
                        126.85,
                        1286648,
                        127.5,
                        127.66,
                        127.67,
                        164386719,
                        127.7636,
                        3,
                        725522,
                        8149,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-13",
                        127.25,
                        129.82,
                        126.8,
                        1603709,
                        129.14,
                        127.23,
                        127.25,
                        205136259,
                        127.9136,
                        2,
                        752373,
                        9835,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-12",
                        130.66,
                        130.99,
                        129.91,
                        1245309,
                        130.33,
                        130.7,
                        130.71,
                        162528528,
                        130.5126,
                        2,
                        628490,
                        6975,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-09",
                        129.19,
                        129.49,
                        128.07,
                        1069094,
                        128.9,
                        129.21,
                        129.22,
                        138041202,
                        129.1198,
                        2,
                        520062,
                        6216,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-08",
                        128.47,
                        128.51,
                        126.59,
                        911647,
                        127.12,
                        128.42,
                        128.43,
                        116797276,
                        128.1168,
                        2,
                        465537,
                        5751,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-07",
                        127.71,
                        127.855,
                        126.28,
                        771510,
                        126.69,
                        127.72,
                        127.73,
                        98346699,
                        127.473,
                        2,
                        420909,
                        4878,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-06",
                        126.72,
                        127.9,
                        126.3,
                        1071382,
                        127.8,
                        126.76,
                        126.77,
                        135947360,
                        126.8897,
                        2,
                        447271,
                        8029,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-02",
                        127.79,
                        130.56,
                        127.25,
                        886927,
                        130.3,
                        127.83,
                        127.84,
                        113943414,
                        128.4699,
                        2,
                        450566,
                        6472,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-01",
                        129.66,
                        129.79,
                        127.74,
                        1060391,
                        128.7,
                        129.66,
                        129.67,
                        137059053,
                        129.2533,
                        2,
                        522811,
                        7331,
                        1,
                        72600,
                    ],
                    [
                        "2022-08-31",
                        128.45,
                        130,
                        128.4,
                        1137678,
                        129.92,
                        128.46,
                        128.48,
                        146465933,
                        128.7411,
                        2,
                        709588,
                        6077,
                        1,
                        72600,
                    ],
                    [
                        "2022-08-30",
                        129.58,
                        130.77,
                        129.3,
                        735905,
                        130.55,
                        129.58,
                        129.59,
                        95531452,
                        129.8149,
                        2,
                        350014,
                        6041,
                        1,
                        72600,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                            {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                            {"name": "LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRNOVR_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "VWAP", "type": "number", "decimalChar": "."},
                            {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                            {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                            {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRD_STATUS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "SALTIM", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-09-27",
                                121.74,
                                123.95,
                                121.09,
                                1335006,
                                122.6,
                                121.76,
                                121.77,
                                162900375,
                                122.0222,
                                2,
                                559187,
                                10219,
                                1,
                                72600,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASIAOP_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIAHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIALO_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIACL_BID", "type": "number", "decimalChar": "."},
                    {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMEROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-09-28",
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        0.9592,
                        0.96,
                        0.9534,
                        0.9577,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        "2022-09-27",
                        0.9592,
                        0.9596,
                        0.967,
                        0.9567,
                        0.9609,
                        0.9594,
                        104222,
                        0.957,
                        0.9673,
                        0.9609,
                        0.967,
                        0.9583,
                        0.9645,
                        0.9635,
                        0.967,
                        0.9592,
                        0.9612,
                        0.9627,
                        0.9652,
                        0.9567,
                        0.9592,
                        0.9611,
                    ],
                    [
                        "2022-09-26",
                        0.9606,
                        0.9609,
                        0.9709,
                        0.9565,
                        0.9678,
                        0.96075,
                        109840,
                        0.9569,
                        0.9712,
                        0.9684,
                        0.9709,
                        0.9565,
                        0.9676,
                        0.9627,
                        0.9701,
                        0.9608,
                        0.9621,
                        0.9641,
                        0.9689,
                        0.9598,
                        0.9606,
                        0.968,
                    ],
                    [
                        "2022-09-23",
                        0.969,
                        0.9694,
                        0.9851,
                        0.9666,
                        0.9835,
                        0.9692,
                        90975,
                        0.9669,
                        0.9854,
                        0.9835,
                        0.9851,
                        0.9765,
                        0.9774,
                        0.9821,
                        0.9838,
                        0.97,
                        0.9716,
                        0.9751,
                        0.9774,
                        0.9666,
                        0.969,
                        0.9839,
                    ],
                    [
                        "2022-09-22",
                        0.9836,
                        0.984,
                        0.9907,
                        0.9807,
                        0.9836,
                        0.9838,
                        103843,
                        0.981,
                        0.9909,
                        0.9836,
                        0.9853,
                        0.9807,
                        0.9843,
                        0.9828,
                        0.9907,
                        0.981,
                        0.9838,
                        0.9874,
                        0.9887,
                        0.981,
                        0.9836,
                        0.9838,
                    ],
                    [
                        "2022-09-21",
                        0.9837,
                        0.9839,
                        0.9976,
                        0.9812,
                        0.997,
                        0.9838,
                        87445,
                        0.9814,
                        0.998,
                        0.997,
                        0.9976,
                        0.9883,
                        0.9909,
                        0.9959,
                        0.9968,
                        0.9865,
                        0.9878,
                        0.9921,
                        0.9925,
                        0.9812,
                        0.9837,
                        0.9974,
                    ],
                    [
                        "2022-09-20",
                        0.997,
                        0.9974,
                        1.005,
                        0.9953,
                        1.0021,
                        0.9972,
                        72943,
                        0.9956,
                        1.0053,
                        1.0021,
                        1.005,
                        1.0011,
                        1.0034,
                        1.0021,
                        1.0041,
                        0.9953,
                        0.9992,
                        1.0006,
                        1.0013,
                        0.9953,
                        0.997,
                        1.0025,
                    ],
                    [
                        "2022-09-19",
                        1.0022,
                        1.0026,
                        1.0029,
                        0.9964,
                        1.001,
                        1.0024,
                        63178,
                        0.9967,
                        1.0031,
                        1.001,
                        1.0029,
                        0.9964,
                        0.9978,
                        0.9992,
                        1.0017,
                        0.9964,
                        1.0002,
                        0.9992,
                        1.0027,
                        0.9974,
                        1.0022,
                        1.0014,
                    ],
                    [
                        "2022-09-16",
                        1.0015,
                        1.0019,
                        1.0036,
                        0.9943,
                        0.9999,
                        1.0017,
                        72842,
                        0.9946,
                        1.0038,
                        0.9999,
                        1.0012,
                        0.9943,
                        0.9956,
                        0.9995,
                        1.0036,
                        0.9943,
                        1.001,
                        0.9983,
                        1.0036,
                        0.9951,
                        1.0015,
                        1.0003,
                    ],
                    [
                        "2022-09-15",
                        0.9999,
                        1.0003,
                        1.0017,
                        0.9954,
                        0.9979,
                        1.0001,
                        69080,
                        0.9957,
                        1.002,
                        0.9979,
                        0.9984,
                        0.9954,
                        0.9977,
                        0.9967,
                        1.0017,
                        0.9954,
                        0.999,
                        0.9977,
                        1.0017,
                        0.997,
                        0.9999,
                        0.9982,
                    ],
                    [
                        "2022-09-14",
                        0.9977,
                        0.9981,
                        1.0023,
                        0.9954,
                        0.9967,
                        0.9979,
                        87677,
                        0.9957,
                        1.0026,
                        0.9967,
                        1.0002,
                        0.9954,
                        0.9986,
                        0.9994,
                        1.0023,
                        0.9958,
                        0.9992,
                        1.0006,
                        1.0009,
                        0.9967,
                        0.9977,
                        0.9971,
                    ],
                    [
                        "2022-09-13",
                        0.997,
                        0.9974,
                        1.0187,
                        0.9964,
                        1.0121,
                        0.9972,
                        77655,
                        0.9968,
                        1.0189,
                        1.0121,
                        1.0155,
                        1.0116,
                        1.0145,
                        1.0126,
                        1.0187,
                        0.9994,
                        0.9996,
                        1.0179,
                        1.0187,
                        0.9964,
                        0.997,
                        1.0125,
                    ],
                    [
                        "2022-09-12",
                        1.0119,
                        1.0122,
                        1.0197,
                        1.0058,
                        1.0078,
                        1.01205,
                        62347,
                        1.0061,
                        1.02,
                        1.0078,
                        1.0197,
                        1.0058,
                        1.0174,
                        1.0076,
                        1.0197,
                        1.0076,
                        1.0124,
                        1.0135,
                        1.0162,
                        1.0103,
                        1.0119,
                        1.0082,
                    ],
                    [
                        "2022-09-09",
                        1.0039,
                        1.0043,
                        1.0112,
                        0.9993,
                        0.9993,
                        1.0041,
                        76399,
                        0.9997,
                        1.0115,
                        0.9993,
                        1.011,
                        0.9993,
                        1.0096,
                        1.0071,
                        1.0112,
                        1.003,
                        1.0044,
                        1.0073,
                        1.0075,
                        1.003,
                        1.0039,
                        0.9997,
                    ],
                    [
                        "2022-09-08",
                        0.9994,
                        0.9998,
                        1.0029,
                        0.9929,
                        1.0001,
                        0.9996,
                        86338,
                        0.9932,
                        1.0032,
                        1.0001,
                        1.0014,
                        0.9975,
                        0.998,
                        0.9988,
                        1.0029,
                        0.9929,
                        0.9952,
                        1.0008,
                        1.0029,
                        0.9929,
                        0.9994,
                        1.0003,
                    ],
                    [
                        "2022-09-07",
                        0.9999,
                        1.0003,
                        1.001,
                        0.9874,
                        0.9902,
                        1.0001,
                        82606,
                        0.9876,
                        1.0013,
                        0.9902,
                        0.9928,
                        0.9875,
                        0.9922,
                        0.9891,
                        0.9954,
                        0.9874,
                        0.9937,
                        0.9896,
                        1.001,
                        0.9874,
                        0.9999,
                        0.9906,
                    ],
                    [
                        "2022-09-06",
                        0.9902,
                        0.9906,
                        0.9986,
                        0.9862,
                        0.9925,
                        0.9904,
                        101494,
                        0.9865,
                        0.9988,
                        0.9925,
                        0.9986,
                        0.9923,
                        0.9975,
                        0.9946,
                        0.9986,
                        0.9862,
                        0.991,
                        0.9924,
                        0.9937,
                        0.9862,
                        0.9902,
                        0.9929,
                    ],
                    [
                        "2022-09-05",
                        0.9926,
                        0.993,
                        0.9948,
                        0.9875,
                        0.9948,
                        0.9928,
                        67114,
                        0.9879,
                        0.9952,
                        0.9948,
                        0.9948,
                        0.9875,
                        0.991,
                        0.9904,
                        0.9943,
                        0.9875,
                        0.9927,
                        0.9932,
                        0.9936,
                        0.9911,
                        0.9926,
                        0.9952,
                    ],
                    [
                        "2022-09-02",
                        0.9951,
                        0.9955,
                        1.0033,
                        0.9941,
                        0.9944,
                        0.9953,
                        68962,
                        0.9944,
                        1.0036,
                        0.9944,
                        0.9997,
                        0.9941,
                        0.9987,
                        0.9965,
                        1.0033,
                        0.9962,
                        1.0028,
                        0.9996,
                        1.0033,
                        0.9943,
                        0.9951,
                        0.9947,
                    ],
                    [
                        "2022-09-01",
                        0.9944,
                        0.9947,
                        1.0055,
                        0.9909,
                        1.0053,
                        0.99455,
                        85854,
                        0.9912,
                        1.0059,
                        1.0053,
                        1.0055,
                        1.0006,
                        1.0028,
                        1.0012,
                        1.0048,
                        0.9909,
                        0.9947,
                        1.0017,
                        1.0021,
                        0.9909,
                        0.9944,
                        1.0057,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "BID_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                            {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                            {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                            {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                            {
                                "name": "ASK_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAOP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIALO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIACL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                            {
                                "name": "AMEROP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERLO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERCL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-09-28",
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                0.9592,
                                0.96,
                                0.9534,
                                0.9577,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "data": [
                    ["2022-09-28", 3],
                    ["2022-09-27", 3],
                    ["2022-09-26", 3],
                    ["2022-09-23", 3],
                    ["2022-09-22", 3],
                    ["2022-09-21", 3],
                    ["2022-09-20", 3],
                    ["2022-09-19", 3],
                    ["2022-09-16", 3],
                    ["2022-09-15", 3],
                    ["2022-09-14", 3],
                    ["2022-09-13", 3],
                    ["2022-09-12", 3],
                    ["2022-09-09", 3],
                    ["2022-09-08", 3],
                    ["2022-09-07", 3],
                    ["2022-09-06", 3],
                    ["2022-09-05", 3],
                    ["2022-09-02", 3],
                    ["2022-09-01", 3],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": "P1D",
                "summaryTimestampLabel": "endPeriod",
                "universe": {"ric": "S)MyUSD.GESG1-150112"},
            }
        ]
    ),
]

UDF_GET_HISTORY_EUR_GPB_TICK_INTERVAL = [
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28T17:00:19.794000000Z", "quote", 0.97, 0.9704],
                    ["2022-09-28T17:00:18.790000000Z", "quote", 0.97, 0.9704],
                    ["2022-09-28T17:00:16.765000000Z", "quote", 0.97, 0.9704],
                    ["2022-09-28T17:00:15.770000000Z", "quote", 0.97, 0.9704],
                    ["2022-09-28T17:00:14.906000000Z", "quote", 0.9701, 0.9703],
                ],
                "status": {
                    "code": "TS.Intraday.Warning.95004",
                    "message": "Trades interleaving with corrections is currently not "
                               "supported. Corrections will not be returned.",
                },
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28T17:00:19.794000000Z", 51966]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GBP="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28T17:00:19.785000000Z", "quote", 1.0854, 1.0858],
                    ["2022-09-28T17:00:19.283000000Z", "quote", 1.0855, 1.0858],
                    ["2022-09-28T17:00:19.061000000Z", "quote", 1.0854, 1.0857],
                    ["2022-09-28T17:00:18.794000000Z", "quote", 1.0853, 1.0857],
                    ["2022-09-28T17:00:18.051000000Z", "quote", 1.0855, 1.0858],
                ],
                "status": {
                    "code": "TS.Intraday.Warning.95004",
                    "message": "Trades interleaving with corrections is currently not "
                               "supported. Corrections will not be returned.",
                },
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28T17:00:19.785000000Z", 62222]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_CHAIN_ONE_ADC_FIELD_ONE_HP_FIELD = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["BMA.BA", "", ""],
                        ["BBAR.BA", "", ""],
                        ["BHIP.BA", "", ""],
                        ["GGAL.BA", "", ""],
                        ["BPAT.BA", "", ""],
                        ["SUPV.BA", "", ""],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {"displayName": "Revenue", "field": "TR.REVENUE"},
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 7,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BMA.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 444.3],
                    ["2022-09-26", 462],
                    ["2022-09-23", 488.6],
                    ["2022-09-22", 510],
                    ["2022-09-21", 502],
                    ["2022-09-20", 503],
                    ["2022-09-19", 520.9],
                    ["2022-09-16", 489.9],
                    ["2022-09-15", 480],
                    ["2022-09-14", 477],
                    ["2022-09-13", 455],
                    ["2022-09-12", 468],
                    ["2022-09-09", 472.2],
                    ["2022-09-08", 441],
                    ["2022-09-07", 443.5],
                    ["2022-09-06", 419],
                    ["2022-09-05", 418.6],
                    ["2022-09-01", 407.46538],
                    ["2022-08-31", 408.459198],
                    ["2022-08-30", 430.323194],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 444.3]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BBAR.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 304.5],
                    ["2022-09-26", 305.15],
                    ["2022-09-23", 319.2],
                    ["2022-09-22", 345.5],
                    ["2022-09-21", 340.45],
                    ["2022-09-20", 342.6],
                    ["2022-09-19", 339.2],
                    ["2022-09-16", 315.5],
                    ["2022-09-15", 310],
                    ["2022-09-14", 315],
                    ["2022-09-13", 306],
                    ["2022-09-12", 315.5],
                    ["2022-09-09", 321],
                    ["2022-09-08", 311.2],
                    ["2022-09-07", 311],
                    ["2022-09-06", 298],
                    ["2022-09-05", 302.1],
                    ["2022-09-01", 289.205112],
                    ["2022-08-31", 296.658852],
                    ["2022-08-30", 313.05708],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 304.5]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BHIP.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 10.45],
                    ["2022-09-26", 10.65],
                    ["2022-09-23", 11],
                    ["2022-09-22", 11.65],
                    ["2022-09-21", 11.6],
                    ["2022-09-20", 11.75],
                    ["2022-09-19", 12],
                    ["2022-09-16", 11.85],
                    ["2022-09-15", 11.9],
                    ["2022-09-14", 12.2],
                    ["2022-09-13", 12.1],
                    ["2022-09-12", 12.35],
                    ["2022-09-09", 12.55],
                    ["2022-09-08", 12.5],
                    ["2022-09-07", 12.7],
                    ["2022-09-06", 12],
                    ["2022-09-05", 12.2],
                    ["2022-09-01", 11.65],
                    ["2022-08-31", 11.5],
                    ["2022-08-30", 12.2],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 10.45]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GGAL.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 228.9],
                    ["2022-09-26", 242.35],
                    ["2022-09-23", 257.3],
                    ["2022-09-22", 269.5],
                    ["2022-09-21", 267.6],
                    ["2022-09-20", 268.3],
                    ["2022-09-19", 270.7],
                    ["2022-09-16", 259.2],
                    ["2022-09-15", 258],
                    ["2022-09-14", 256.1],
                    ["2022-09-13", 250.1],
                    ["2022-09-12", 259.6],
                    ["2022-09-09", 264.3],
                    ["2022-09-08", 252.5],
                    ["2022-09-07", 251.293376],
                    ["2022-09-06", 243.27969],
                    ["2022-09-05", 241.004198],
                    ["2022-09-01", 237.343626],
                    ["2022-08-31", 236.997355],
                    ["2022-08-30", 247.632803],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 228.9]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BPAT.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 100.5],
                    ["2022-09-26", 107],
                    ["2022-09-23", 104.25],
                    ["2022-09-22", 108.25],
                    ["2022-09-21", 106],
                    ["2022-09-20", 108.5],
                    ["2022-09-19", 105],
                    ["2022-09-16", 108.816611],
                    ["2022-09-15", 106.332213],
                    ["2022-09-14", 109.31349],
                    ["2022-09-13", 104.344695],
                    ["2022-09-12", 109.31349],
                    ["2022-09-09", 107.822852],
                    ["2022-09-08", 108.319731],
                    ["2022-09-07", 108.319731],
                    ["2022-09-06", 105.338454],
                    ["2022-09-05", 106.829093],
                    ["2022-09-01", 103.350936],
                    ["2022-08-31", 104.344695],
                    ["2022-08-30", 108.071291],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 100.5]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "SUPV.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-27", 106.55],
                    ["2022-09-26", 107.6],
                    ["2022-09-23", 112],
                    ["2022-09-22", 113.1],
                    ["2022-09-21", 114],
                    ["2022-09-20", 113.5],
                    ["2022-09-19", 114],
                    ["2022-09-16", 113],
                    ["2022-09-15", 113.05],
                    ["2022-09-14", 113],
                    ["2022-09-13", 109.5],
                    ["2022-09-12", 110.5],
                    ["2022-09-09", 111.4],
                    ["2022-09-08", 108],
                    ["2022-09-07", 107],
                    ["2022-09-06", 104],
                    ["2022-09-05", 104.6],
                    ["2022-09-01", 106.5],
                    ["2022-08-31", 106.05],
                    ["2022-08-30", 112.4],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-27", 106.55]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_CHAINS_PRICING_FIELDS = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["GS.N", "1999-05-04T00:00:00Z", "GS.N"],
                        ["NKE.N", "1990-10-19T00:00:00Z", "NKE.N"],
                        ["CSCO.OQ", "2002-06-27T00:00:00Z", "CSCO.OQ"],
                        ["JPM.N", "2001-01-02T00:00:00Z", "JPM.N"],
                        ["DIS.N", "1990-03-23T00:00:00Z", "DIS.N"],
                        ["INTC.OQ", "2002-06-27T00:00:00Z", "INTC.OQ"],
                        ["DOW.N", "2019-04-02T00:00:00Z", "DOW.N"],
                        ["MRK.N", "1990-03-23T00:00:00Z", "MRK.N"],
                        ["CVX.N", "2001-10-10T00:00:00Z", "CVX.N"],
                        ["AXP.N", "1990-03-23T00:00:00Z", "AXP.N"],
                        ["VZ.N", "2000-07-01T00:00:00Z", "VZ.N"],
                        ["HD.N", "1990-03-23T00:00:00Z", "HD.N"],
                        ["WBA.OQ", "2014-12-31T00:00:00Z", "WBA.OQ"],
                        ["MCD.N", "1990-03-23T00:00:00Z", "MCD.N"],
                        ["UNH.N", "1991-10-09T00:00:00Z", "UNH.N"],
                        ["KO.N", "1990-03-23T00:00:00Z", "KO.N"],
                        ["JNJ.N", "1990-03-23T00:00:00Z", "JNJ.N"],
                        ["MSFT.OQ", "2002-06-28T00:00:00Z", "MSFT.OQ"],
                        ["HON.OQ", "2021-05-11T00:00:00Z", "HON.OQ"],
                        ["CRM.N", "2004-06-21T00:00:00Z", "CRM.N"],
                        ["PG.N", "1990-03-23T00:00:00Z", "PG.N"],
                        ["IBM.N", "1990-03-23T00:00:00Z", "IBM.N"],
                        ["MMM.N", "1990-03-23T00:00:00Z", "MMM.N"],
                        ["AAPL.OQ", "2002-06-27T00:00:00Z", "AAPL.OQ"],
                        ["WMT.N", "1990-03-23T00:00:00Z", "WMT.N"],
                        ["CAT.N", "1990-03-23T00:00:00Z", "CAT.N"],
                        ["AMGN.OQ", "2002-06-27T00:00:00Z", "AMGN.OQ"],
                        ["V.N", "2007-12-26T00:00:00Z", "V.N"],
                        ["TRV.N", "2007-02-27T00:00:00Z", "TRV.N"],
                        ["BA.N", "1990-03-23T00:00:00Z", "BA.N"],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {"displayName": "RIC", "field": "TR.RIC"},
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 31,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GS.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 300.71, 300.72],
                    ["2022-08-31", 332.63, 332.69],
                    ["2022-07-31", 333.52, 333.61],
                    ["2022-06-30", 297.56, 297.91],
                    ["2022-05-31", 327.1, 327.24],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 300.71, 300.72]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CSCO.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 41.32, 41.33],
                    ["2022-08-31", 44.69, 44.71],
                    ["2022-07-31", 45.37, 45.38],
                    ["2022-06-30", 42.65, 42.67],
                    ["2022-05-31", 45.03, 45.06],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 41.32, 41.33]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DIS.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 99.36, 99.4],
                    ["2022-08-31", 112.08, 112.09],
                    ["2022-07-31", 106.1, 106.12],
                    ["2022-06-30", 94.47, 94.5],
                    ["2022-05-31", 110.51, 110.53],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 99.36, 99.4]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "INTC.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 27.11, 27.12],
                    ["2022-08-31", 31.9, 31.92],
                    ["2022-07-31", 36.29, 36.3],
                    ["2022-06-30", 37.44, 37.45],
                    ["2022-05-31", 44.41, 44.42],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 27.11, 27.12]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "NKE.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 98.66, 98.67],
                    ["2022-08-31", 106.44, 106.45],
                    ["2022-07-31", 114.92, 114.94],
                    ["2022-06-30", 102.2, 102.25],
                    ["2022-05-31", 118.96, 118.97],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 98.66, 98.67]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DOW.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 45.05, 45.06],
                    ["2022-08-31", 50.99, 51],
                    ["2022-07-31", 53.23, 53.24],
                    ["2022-06-30", 51.61, 51.62],
                    ["2022-05-31", 67.99, 68],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 45.05, 45.06]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JPM.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 108.04, 108.05],
                    ["2022-08-31", 113.72, 113.73],
                    ["2022-07-31", 115.36, 115.4],
                    ["2022-06-30", 112.63, 112.67],
                    ["2022-05-31", 132.29, 132.33],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 108.04, 108.05]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AXP.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 140.46, 140.49],
                    ["2022-08-31", 151.99, 152],
                    ["2022-07-31", 154, 154.01],
                    ["2022-06-30", 138.7, 138.76],
                    ["2022-05-31", 168.95, 169.02],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 140.46, 140.49]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CVX.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 145.62, 145.63],
                    ["2022-08-31", 158.07, 158.08],
                    ["2022-07-31", 163.73, 163.76],
                    ["2022-06-30", 144.78, 144.79],
                    ["2022-05-31", 174.57, 174.63],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 145.62, 145.63]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MRK.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 86.78, 86.79],
                    ["2022-08-31", 85.4, 85.41],
                    ["2022-07-31", 89.38, 89.39],
                    ["2022-06-30", 91.36, 91.39],
                    ["2022-05-31", 92.19, 92.2],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 86.78, 86.79]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WBA.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 33.18, 33.19],
                    ["2022-08-31", 35.05, 35.06],
                    ["2022-07-31", 39.61, 39.63],
                    ["2022-06-30", 37.9, 37.91],
                    ["2022-05-31", 43.81, 43.82],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 33.18, 33.19]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "UNH.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 513.45, 513.75],
                    ["2022-08-31", 519.33, 519.44],
                    ["2022-07-31", 542.75, 542.77],
                    ["2022-06-30", 515.2, 515.38],
                    ["2022-05-31", 496.87, 497.06],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 513.45, 513.75]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MCD.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 236.89, 236.94],
                    ["2022-08-31", 252.27, 252.28],
                    ["2022-07-31", 263.4, 263.59],
                    ["2022-06-30", 246.91, 246.97],
                    ["2022-05-31", 252.44, 252.45],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 236.89, 236.94]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HD.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 282.19, 282.2],
                    ["2022-08-31", 288.35, 288.42],
                    ["2022-07-31", 300.95, 301.02],
                    ["2022-06-30", 274.5, 274.61],
                    ["2022-05-31", 302.75, 303.01],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 282.19, 282.2]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VZ.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 39.35, 39.36],
                    ["2022-08-31", 41.81, 41.82],
                    ["2022-07-31", 46.19, 46.2],
                    ["2022-06-30", 50.76, 50.77],
                    ["2022-05-31", 51.31, 51.33],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 39.35, 39.36]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 241.02, 241.03],
                    ["2022-08-31", 261.44, 261.48],
                    ["2022-07-31", 280.74, 280.81],
                    ["2022-06-30", 256.86, 256.99],
                    ["2022-05-31", 271.82, 272.01],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 241.02, 241.03]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JNJ.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 166.47, 166.53],
                    ["2022-08-31", 161.34, 161.36],
                    ["2022-07-31", 174.48, 174.53],
                    ["2022-06-30", 177.85, 177.87],
                    ["2022-05-31", 179.4, 179.52],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 166.47, 166.53]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "KO.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 56.97, 56.98],
                    ["2022-08-31", 61.7, 61.71],
                    ["2022-07-31", 64.2, 64.21],
                    ["2022-06-30", 62.94, 62.95],
                    ["2022-05-31", 63.41, 63.42],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 56.97, 56.98]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HON.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 173.8, 173.83],
                    ["2022-08-31", 189.31, 189.32],
                    ["2022-07-31", 192.46, 192.53],
                    ["2022-06-30", 173.81, 173.86],
                    ["2022-05-31", 193.58, 193.6],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 173.8, 173.83]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CRM.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 150.17, 150.18],
                    ["2022-08-31", 156.12, 156.14],
                    ["2022-07-31", 184.17, 184.31],
                    ["2022-06-30", 165.11, 165.12],
                    ["2022-05-31", 160.95, 160.97],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 150.17, 150.18]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MMM.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 114.25, 114.26],
                    ["2022-08-31", 124.35, 124.38],
                    ["2022-07-31", 143.26, 143.28],
                    ["2022-06-30", 129.46, 129.52],
                    ["2022-05-31", 149.22, 149.29],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 114.25, 114.26]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 122.71, 122.72],
                    ["2022-08-31", 128.46, 128.48],
                    ["2022-07-31", 130.69, 130.72],
                    ["2022-06-30", 141.33, 141.37],
                    ["2022-05-31", 138.87, 138.88],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 122.71, 122.72]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WMT.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 133.07, 133.11],
                    ["2022-08-31", 132.64, 132.7],
                    ["2022-07-31", 132.03, 132.04],
                    ["2022-06-30", 121.59, 121.61],
                    ["2022-05-31", 128.72, 128.8],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 133.07, 133.11]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AAPL.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 149.79, 149.8],
                    ["2022-08-31", 157.17, 157.18],
                    ["2022-07-31", 162.57, 162.58],
                    ["2022-06-30", 136.76, 136.82],
                    ["2022-05-31", 148.74, 148.84],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 149.79, 149.8]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "PG.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 131.93, 131.98],
                    ["2022-08-31", 137.97, 137.98],
                    ["2022-07-31", 138.97, 138.98],
                    ["2022-06-30", 144.02, 144.09],
                    ["2022-05-31", 148, 148.01],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 131.93, 131.98]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "TRV.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 152.98, 152.99],
                    ["2022-08-31", 161.61, 161.63],
                    ["2022-07-31", 158.6, 158.7],
                    ["2022-06-30", 169.21, 169.35],
                    ["2022-05-31", 179.04, 179.16],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 152.98, 152.99]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BA.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 133.36, 133.37],
                    ["2022-08-31", 160.25, 160.26],
                    ["2022-07-31", 159.35, 159.43],
                    ["2022-06-30", 136.88, 136.91],
                    ["2022-05-31", 131.4, 131.46],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 133.36, 133.37]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CAT.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 167.69, 167.74],
                    ["2022-08-31", 184.69, 184.71],
                    ["2022-07-31", 198.38, 198.45],
                    ["2022-06-30", 178.76, 178.83],
                    ["2022-05-31", 215.75, 215.85],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 167.69, 167.74]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AMGN.OQ"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 230.91, 230.98],
                    ["2022-08-31", 240.07, 240.24],
                    ["2022-07-31", 247.41, 247.47],
                    ["2022-06-30", 243.34, 243.35],
                    ["2022-05-31", 256.61, 256.73],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 230.91, 230.98]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "V.N"},
                "interval": "P1M",
                "summaryTimestampLabel": "endPeriod",
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
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-30", 179.1, 179.24],
                    ["2022-08-31", 198.71, 198.72],
                    ["2022-07-31", 212.14, 212.25],
                    ["2022-06-30", 196.89, 197.07],
                    ["2022-05-31", 212.04, 212.05],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 179.1, 179.24]],
                    }
                },
            }
        ]
    ),
]

UDF_GET_HISTORY_CHAINS_ADC_PRICING_FIELDS = [
    StubResponse(
        {
            "responses": [
                {
                    "columnHeadersCount": 1,
                    "data": [
                        ["GS.N", "2021-12-31T00:00:00Z", 64989000000],
                        ["NKE.N", "2022-05-31T00:00:00Z", 46710000000],
                        ["CSCO.OQ", "2022-07-30T00:00:00Z", 51557000000],
                        ["JPM.N", "", ""],
                        ["DIS.N", "2021-10-02T00:00:00Z", 67418000000],
                        ["INTC.OQ", "2021-12-25T00:00:00Z", 79024000000],
                        ["DOW.N", "2021-12-31T00:00:00Z", 54968000000],
                        ["MRK.N", "2021-12-31T00:00:00Z", 48704000000],
                        ["CVX.N", "2021-12-31T00:00:00Z", 155606000000],
                        ["AXP.N", "2021-12-31T00:00:00Z", 42838000000],
                        ["VZ.N", "2021-12-31T00:00:00Z", 133613000000],
                        ["HD.N", "2022-01-30T00:00:00Z", 151157000000],
                        ["WBA.OQ", "2021-08-31T00:00:00Z", 132509000000],
                        ["MCD.N", "2021-12-31T00:00:00Z", 23222900000],
                        ["UNH.N", "", ""],
                        ["KO.N", "2021-12-31T00:00:00Z", 38655000000],
                        ["JNJ.N", "2022-01-02T00:00:00Z", 93775000000],
                        ["MSFT.OQ", "2022-06-30T00:00:00Z", 198270000000],
                        ["HON.OQ", "2021-12-31T00:00:00Z", 34392000000],
                        ["CRM.N", "2022-01-31T00:00:00Z", 26492000000],
                        ["PG.N", "2022-06-30T00:00:00Z", 80187000000],
                        ["IBM.N", "2021-12-31T00:00:00Z", 57350000000],
                        ["MMM.N", "2021-12-31T00:00:00Z", 35355000000],
                        ["AAPL.OQ", "2021-09-25T00:00:00Z", 365817000000],
                        ["WMT.N", "2022-01-31T00:00:00Z", 572754000000],
                        ["CAT.N", "2021-12-31T00:00:00Z", 50971000000],
                        ["AMGN.OQ", "2021-12-31T00:00:00Z", 25979000000],
                        ["V.N", "2021-09-30T00:00:00Z", 24105000000],
                        ["TRV.N", "", ""],
                        ["BA.N", "2021-12-31T00:00:00Z", 62286000000],
                    ],
                    "headerOrientation": "horizontal",
                    "headers": [
                        [
                            {"displayName": "Instrument"},
                            {"displayName": "Date"},
                            {"displayName": "Revenue", "field": "TR.REVENUE"},
                        ]
                    ],
                    "rowHeadersCount": 2,
                    "totalColumnsCount": 3,
                    "totalRowsCount": 31,
                }
            ]
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GS.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 300.71, 300.72],
                    ["2022-09-27", 291.64, 291.66],
                    ["2022-09-26", 294.72, 294.86],
                    ["2022-09-23", 302.19, 302.26],
                    ["2022-09-22", 312.49, 312.73],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 300.71, 300.72]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "NKE.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 98.66, 98.67],
                    ["2022-09-27", 96.29, 96.3],
                    ["2022-09-26", 96.16, 96.18],
                    ["2022-09-23", 97.04, 97.06],
                    ["2022-09-22", 98.54, 98.55],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 98.66, 98.67]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CSCO.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 41.32, 41.33],
                    ["2022-09-27", 40.54, 40.55],
                    ["2022-09-26", 40.58, 40.6],
                    ["2022-09-23", 40.67, 40.68],
                    ["2022-09-22", 41.14, 41.15],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 41.32, 41.33]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JPM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 108.04, 108.05],
                    ["2022-09-27", 105.87, 105.88],
                    ["2022-09-26", 106.79, 106.8],
                    ["2022-09-23", 109.21, 109.22],
                    ["2022-09-22", 111.19, 111.2],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 108.04, 108.05]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "INTC.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 27.11, 27.12],
                    ["2022-09-27", 26.88, 26.89],
                    ["2022-09-26", 26.94, 26.95],
                    ["2022-09-23", 27.52, 27.54],
                    ["2022-09-22", 28.06, 28.07],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 27.11, 27.12]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DOW.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 45.05, 45.06],
                    ["2022-09-27", 43.8, 43.81],
                    ["2022-09-26", 43.37, 43.38],
                    ["2022-09-23", 43.9, 43.91],
                    ["2022-09-22", 44.76, 44.77],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 45.05, 45.06]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MRK.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 86.78, 86.79],
                    ["2022-09-27", 85.87, 85.88],
                    ["2022-09-26", 86.35, 86.36],
                    ["2022-09-23", 86.79, 86.8],
                    ["2022-09-22", 87.5, 87.51],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 86.78, 86.79]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AXP.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 140.46, 140.49],
                    ["2022-09-27", 137.53, 137.59],
                    ["2022-09-26", 137.5, 137.53],
                    ["2022-09-23", 140.34, 140.37],
                    ["2022-09-22", 143.01, 143.03],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 140.46, 140.49]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DIS.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 99.36, 99.4],
                    ["2022-09-27", 95.91, 95.93],
                    ["2022-09-26", 98.18, 98.19],
                    ["2022-09-23", 99.55, 99.59],
                    ["2022-09-22", 102.15, 102.16],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 99.36, 99.4]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CVX.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 145.62, 145.63],
                    ["2022-09-27", 141.07, 141.12],
                    ["2022-09-26", 141.1, 141.11],
                    ["2022-09-23", 144.81, 144.82],
                    ["2022-09-22", 154.83, 154.84],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 145.62, 145.63]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MCD.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 236.89, 236.94],
                    ["2022-09-27", 236.71, 236.87],
                    ["2022-09-26", 243.69, 243.78],
                    ["2022-09-23", 245.95, 245.96],
                    ["2022-09-22", 247.91, 247.92],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 236.89, 236.94]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HD.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 282.19, 282.2],
                    ["2022-09-27", 268.8, 268.87],
                    ["2022-09-26", 266.87, 266.93],
                    ["2022-09-23", 271.08, 271.25],
                    ["2022-09-22", 268.97, 269.15],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 282.19, 282.2]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VZ.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 39.35, 39.36],
                    ["2022-09-27", 38.89, 38.9],
                    ["2022-09-26", 38.92, 38.94],
                    ["2022-09-23", 39.55, 39.56],
                    ["2022-09-22", 39.93, 39.94],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 39.35, 39.36]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WBA.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 33.18, 33.19],
                    ["2022-09-27", 32.43, 32.44],
                    ["2022-09-26", 32.7, 32.71],
                    ["2022-09-23", 32.83, 32.84],
                    ["2022-09-22", 33.29, 33.31],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 33.18, 33.19]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "UNH.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 513.45, 513.75],
                    ["2022-09-27", 508.76, 508.89],
                    ["2022-09-26", 508.69, 508.81],
                    ["2022-09-23", 513.98, 514.07],
                    ["2022-09-22", 517.22, 517.45],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 513.45, 513.75]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HON.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 173.8, 173.83],
                    ["2022-09-27", 170.07, 170.1],
                    ["2022-09-26", 170.07, 170.12],
                    ["2022-09-23", 171.4, 171.49],
                    ["2022-09-22", 173.21, 173.25],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 173.8, 173.83]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 241.02, 241.03],
                    ["2022-09-27", 236.41, 236.49],
                    ["2022-09-26", 237.46, 237.52],
                    ["2022-09-23", 237.96, 237.97],
                    ["2022-09-22", 240.78, 240.8],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 241.02, 241.03]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JNJ.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 166.47, 166.53],
                    ["2022-09-27", 164.95, 164.96],
                    ["2022-09-26", 165.8, 165.82],
                    ["2022-09-23", 166.87, 166.93],
                    ["2022-09-22", 166.12, 166.13],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 166.47, 166.53]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "KO.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 56.97, 56.98],
                    ["2022-09-27", 56.39, 56.4],
                    ["2022-09-26", 57.86, 57.87],
                    ["2022-09-23", 58.6, 58.61],
                    ["2022-09-22", 59.24, 59.25],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 56.97, 56.98]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CRM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 150.17, 150.18],
                    ["2022-09-27", 148.86, 148.89],
                    ["2022-09-26", 146.32, 146.39],
                    ["2022-09-23", 147.08, 147.09],
                    ["2022-09-22", 150.1, 150.11],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 150.17, 150.18]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 122.71, 122.72],
                    ["2022-09-27", 121.76, 121.77],
                    ["2022-09-26", 122, 122.01],
                    ["2022-09-23", 122.75, 122.76],
                    ["2022-09-22", 125.31, 125.32],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 122.71, 122.72]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "PG.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 131.93, 131.98],
                    ["2022-09-27", 132.04, 132.05],
                    ["2022-09-26", 135.78, 135.79],
                    ["2022-09-23", 135.63, 135.64],
                    ["2022-09-22", 136.19, 136.2],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 131.93, 131.98]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MMM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 114.25, 114.26],
                    ["2022-09-27", 112.46, 112.49],
                    ["2022-09-26", 113.04, 113.06],
                    ["2022-09-23", 113.11, 113.16],
                    ["2022-09-22", 114.1, 114.11],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 114.25, 114.26]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AAPL.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 149.79, 149.8],
                    ["2022-09-27", 151.75, 151.76],
                    ["2022-09-26", 150.73, 150.89],
                    ["2022-09-23", 150.51, 150.53],
                    ["2022-09-22", 152.69, 152.71],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 149.79, 149.8]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WMT.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 133.07, 133.11],
                    ["2022-09-27", 130.98, 131.04],
                    ["2022-09-26", 131.47, 131.48],
                    ["2022-09-23", 130.15, 130.16],
                    ["2022-09-22", 133.35, 133.37],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 133.07, 133.11]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "V.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 179.1, 179.24],
                    ["2022-09-27", 178.03, 178.06],
                    ["2022-09-26", 180.61, 180.71],
                    ["2022-09-23", 184.1, 184.18],
                    ["2022-09-22", 185.7, 185.75],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 179.1, 179.24]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "TRV.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 152.98, 152.99],
                    ["2022-09-27", 151.28, 151.29],
                    ["2022-09-26", 150.51, 150.6],
                    ["2022-09-23", 155.5, 155.57],
                    ["2022-09-22", 156.99, 157],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 152.98, 152.99]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AMGN.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 230.91, 230.98],
                    ["2022-09-27", 225.99, 226.07],
                    ["2022-09-26", 226.83, 226.87],
                    ["2022-09-23", 226.98, 227],
                    ["2022-09-22", 227.68, 227.75],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 230.91, 230.98]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CAT.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 167.69, 167.74],
                    ["2022-09-27", 162.47, 162.48],
                    ["2022-09-26", 162.65, 162.76],
                    ["2022-09-23", 164.24, 164.29],
                    ["2022-09-22", 170.49, 170.54],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 167.69, 167.74]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BA.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-09-28", 133.36, 133.37],
                    ["2022-09-27", 127.57, 127.58],
                    ["2022-09-26", 127.47, 127.48],
                    ["2022-09-23", 131.28, 131.29],
                    ["2022-09-22", 138.66, 138.67],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-09-28", 133.36, 133.37]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_NO_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "MKT_HIGH", "type": "number", "decimalChar": "."},
                    {"name": "MKT_LOW", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "MKT_OPEN", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "TRNOVR_UNS", "type": "number", "decimalChar": "."},
                    {"name": "VWAP", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "PERATIO", "type": "number", "decimalChar": "."},
                    {"name": "ORDBK_VOL", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "IND_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "OFFBK_VOL", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ORDBK_VWAP", "type": "number", "decimalChar": "."},
                    {"name": "IND_AUC", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OFF_CLOSE", "type": "number", "decimalChar": "."},
                    {"name": "CLS_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "OPN_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "OPN_AUC", "type": "number", "decimalChar": "."},
                    {"name": "CLS_AUC", "type": "number", "decimalChar": "."},
                    {"name": "INT_AUC", "type": "number", "decimalChar": "."},
                    {"name": "INT_AUCVOL", "type": "number", "decimalChar": "."},
                    {"name": "EX_VOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "ALL_C_MOVE", "type": "number", "decimalChar": "."},
                    {"name": "ELG_NUMMOV", "type": "number", "decimalChar": "."},
                    {"name": "NAVALUE", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-10-04",
                        7574.02425,
                        8023.4566,
                        7378,
                        578779,
                        7658,
                        7716,
                        7718,
                        4443587354.43106,
                        7677.5139,
                        7717,
                        47.4475,
                        519805,
                        6738,
                        207398,
                        58974,
                        7742,
                        7662.27,
                        7718,
                        7658,
                        7378,
                        7718,
                        207398,
                        9203,
                        7658,
                        7718,
                        None,
                        None,
                        666728,
                        6868,
                        6544,
                        None,
                    ],
                    [
                        "2022-10-03",
                        7617.6667,
                        7681.7377,
                        7460,
                        427138,
                        7514,
                        7638,
                        7640,
                        3251555544.02803,
                        7612.4188,
                        7639,
                        47.373,
                        410624,
                        5480,
                        174454,
                        16514,
                        7680,
                        7613.227,
                        7640,
                        7514,
                        7460,
                        7640,
                        174454,
                        11143,
                        7514,
                        7640,
                        None,
                        None,
                        526075,
                        5612,
                        5234,
                        None,
                    ],
                    [
                        "2022-09-30",
                        7582.51632,
                        7674,
                        7560,
                        551922,
                        7566,
                        7628,
                        7630,
                        4207910038.42096,
                        7624.1024,
                        7629,
                        47.1867,
                        517852,
                        5225,
                        326104,
                        34070,
                        7674,
                        7624.07,
                        7628,
                        7566,
                        7560,
                        7628,
                        326104,
                        6842,
                        7566,
                        7628,
                        None,
                        None,
                        703665,
                        5282,
                        5019,
                        None,
                    ],
                    [
                        "2022-09-29",
                        7594,
                        7676.75664,
                        7524,
                        844879,
                        7630,
                        7596,
                        7598,
                        6437374217.61,
                        7619.29235,
                        7597,
                        47.7953,
                        571898,
                        8832,
                        224749,
                        272681,
                        7662,
                        7595.53,
                        7598,
                        7630,
                        7524,
                        7598,
                        224749,
                        10588,
                        7630,
                        7598,
                        None,
                        None,
                        1049100,
                        9064,
                        8646,
                        None,
                    ],
                    [
                        "2022-09-28",
                        7564.1,
                        7704,
                        7454,
                        601494,
                        7560,
                        7692,
                        7696,
                        4588771149.55,
                        7628.9668,
                        7694,
                        47.3357,
                        528526,
                        8427,
                        190944,
                        72768,
                        7704,
                        7636.925,
                        7696,
                        7560,
                        7454,
                        7696,
                        190944,
                        9332,
                        7560,
                        7696,
                        None,
                        None,
                        657801,
                        8502,
                        8182,
                        None,
                    ],
                    [
                        "2022-09-27",
                        7652,
                        7694,
                        7548,
                        669659,
                        7606,
                        7622,
                        7624,
                        5105228152.01,
                        7623.6154,
                        7623,
                        47.4103,
                        569638,
                        6502,
                        282974,
                        99655,
                        7694,
                        7630.916,
                        7622,
                        7606,
                        7548,
                        7622,
                        282974,
                        16892,
                        7606,
                        7622,
                        None,
                        None,
                        789730,
                        6613,
                        6164,
                        None,
                    ],
                    [
                        "2022-09-26",
                        7489.15237,
                        7660,
                        7480,
                        627346,
                        7494,
                        7632,
                        7634,
                        4775494706.78,
                        7612.2345,
                        7633,
                        46.3793,
                        533163,
                        7984,
                        192701,
                        93912,
                        7660,
                        7611.826,
                        7634,
                        7494,
                        7482,
                        7634,
                        192701,
                        4644,
                        7494,
                        7634,
                        None,
                        None,
                        677458,
                        8209,
                        7673,
                        None,
                    ],
                    [
                        "2022-09-23",
                        7461.98718,
                        7528,
                        7300,
                        525502,
                        7446,
                        7468,
                        7470,
                        3914411797.42,
                        7449.43887,
                        7469,
                        46.3793,
                        495162,
                        7688,
                        201094,
                        27640,
                        7528,
                        7449.858,
                        7468,
                        7446,
                        7300,
                        7468,
                        201094,
                        4947,
                        7446,
                        7468,
                        None,
                        None,
                        638640,
                        8116,
                        7424,
                        None,
                    ],
                    [
                        "2022-09-22",
                        7563.56,
                        7706,
                        7416,
                        759195,
                        7620,
                        7468,
                        7470,
                        5729651816.67,
                        7547.00074,
                        7469,
                        47.994,
                        480791,
                        5866,
                        244543,
                        278361,
                        7706,
                        7508.555,
                        7468,
                        7620,
                        7416,
                        7468,
                        244543,
                        3711,
                        7620,
                        7468,
                        None,
                        None,
                        910761,
                        6009,
                        5666,
                        None,
                    ],
                    [
                        "2022-09-21",
                        7663.44985,
                        7730,
                        7518,
                        1001952,
                        7552,
                        7728,
                        7730,
                        7631392654.3177,
                        7616.5246,
                        7729,
                        46.8762,
                        471364,
                        6981,
                        144538,
                        530588,
                        7730,
                        7678.82,
                        7728,
                        7552,
                        7518,
                        7728,
                        144538,
                        4575,
                        7552,
                        7728,
                        None,
                        None,
                        1151781,
                        7092,
                        6807,
                        None,
                    ],
                    [
                        "2022-09-20",
                        7763.06667,
                        7768,
                        7460,
                        513033,
                        7732,
                        7542,
                        7548,
                        3878593615.79,
                        7559.7715,
                        7545,
                        48.3542,
                        473450,
                        6890,
                        186298,
                        36986,
                        7768,
                        7559.729,
                        7548,
                        7732,
                        7460,
                        7548,
                        186298,
                        27764,
                        7732,
                        7548,
                        None,
                        None,
                        663257,
                        6999,
                        6407,
                        None,
                    ],
                    [
                        "2022-09-19",
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        7778,
                        48.3542,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        "2022-09-16",
                        7760,
                        7824,
                        7720,
                        2168875,
                        7760,
                        7770,
                        7786,
                        16851819857.53,
                        7769.846,
                        7778,
                        48.4536,
                        1015294,
                        7430,
                        619678,
                        1152524,
                        7824,
                        7778.599,
                        7786,
                        7760,
                        7720,
                        7786,
                        619678,
                        3973,
                        7760,
                        7786,
                        7748,
                        103606,
                        2577171,
                        7929,
                        7276,
                        None,
                    ],
                    [
                        "2022-09-15",
                        7895.55636,
                        7908,
                        7766,
                        422663,
                        7900,
                        7800,
                        7802,
                        3299449612.11,
                        7806.3314,
                        7801,
                        49.0622,
                        399733,
                        5081,
                        232161,
                        22606,
                        7908,
                        7806.016,
                        7802,
                        7900,
                        7766,
                        7802,
                        232161,
                        5668,
                        7900,
                        7802,
                        None,
                        None,
                        507673,
                        5324,
                        4851,
                        None,
                    ],
                    [
                        "2022-09-14",
                        7972.1,
                        8070,
                        7892,
                        521577,
                        7962,
                        7900,
                        7902,
                        4134076455.03,
                        7925.89236,
                        7901,
                        49.7081,
                        499343,
                        6976,
                        235608,
                        21464,
                        8070,
                        7924.937,
                        7900,
                        7962,
                        7892,
                        7900,
                        235608,
                        3225,
                        7962,
                        7900,
                        None,
                        None,
                        640027,
                        7101,
                        6746,
                        None,
                    ],
                    [
                        "2022-09-13",
                        8023.8095,
                        8162,
                        7942,
                        534518,
                        8134,
                        8004,
                        8006,
                        4285291504.4,
                        8016.4881,
                        8005,
                        50.2919,
                        454096,
                        6799,
                        199046,
                        76775,
                        8162,
                        8016.292,
                        8004,
                        8134,
                        7942,
                        8004,
                        199046,
                        5863,
                        8134,
                        8004,
                        None,
                        None,
                        683751,
                        6853,
                        6609,
                        None,
                    ],
                    [
                        "2022-09-12",
                        8028.12,
                        8098,
                        7954,
                        393139,
                        7998,
                        8094,
                        8098,
                        3165188290.65,
                        8051.06695,
                        8096,
                        49.7081,
                        374415,
                        5142,
                        163090,
                        18685,
                        8098,
                        8053.243,
                        8098,
                        7998,
                        7954,
                        8098,
                        163090,
                        7468,
                        7998,
                        8098,
                        None,
                        None,
                        508848,
                        5196,
                        4919,
                        None,
                    ],
                    [
                        "2022-09-09",
                        8024,
                        8090,
                        7956,
                        479583,
                        7956,
                        8004,
                        8010,
                        3848903522.51,
                        8025.5082,
                        8007,
                        49.7081,
                        381305,
                        5416,
                        182620,
                        98135,
                        8090,
                        8021.854,
                        8004,
                        7956,
                        7956,
                        8004,
                        182620,
                        1606,
                        7956,
                        8004,
                        None,
                        None,
                        602315,
                        5471,
                        5306,
                        None,
                    ],
                    [
                        "2022-09-08",
                        8044,
                        8060,
                        7688,
                        611208,
                        7964,
                        8004,
                        8006,
                        4847453609.7,
                        7930.94,
                        8005,
                        49.3355,
                        587774,
                        7217,
                        240248,
                        23394,
                        8060,
                        7932.403,
                        8004,
                        7964,
                        7688,
                        8004,
                        240248,
                        6609,
                        7964,
                        8004,
                        None,
                        None,
                        754372,
                        7318,
                        7011,
                        None,
                    ],
                    [
                        "2022-09-07",
                        7897.33333,
                        8000,
                        7838,
                        1050642,
                        7918,
                        7944,
                        7946,
                        8288071402.15,
                        7888.567,
                        7945,
                        49.4845,
                        412145,
                        7695,
                        167471,
                        638292,
                        8000,
                        7934.95,
                        7944,
                        7918,
                        7838,
                        7944,
                        167471,
                        5849,
                        7918,
                        7944,
                        None,
                        None,
                        1154149,
                        7753,
                        7199,
                        None,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                            {"name": "MKT_HIGH", "type": "number", "decimalChar": "."},
                            {"name": "MKT_LOW", "type": "number", "decimalChar": "."},
                            {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                            {"name": "MKT_OPEN", "type": "number", "decimalChar": "."},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRNOVR_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "VWAP", "type": "number", "decimalChar": "."},
                            {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                            {"name": "PERATIO", "type": "number", "decimalChar": "."},
                            {"name": "ORDBK_VOL", "type": "number", "decimalChar": "."},
                            {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                            {
                                "name": "IND_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OFFBK_VOL", "type": "number", "decimalChar": "."},
                            {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                            {
                                "name": "ORDBK_VWAP",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "IND_AUC", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                            {"name": "LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "OFF_CLOSE", "type": "number", "decimalChar": "."},
                            {
                                "name": "CLS_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "OPN_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OPN_AUC", "type": "number", "decimalChar": "."},
                            {"name": "CLS_AUC", "type": "number", "decimalChar": "."},
                            {"name": "INT_AUC", "type": "number", "decimalChar": "."},
                            {
                                "name": "INT_AUCVOL",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "EX_VOL_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ALL_C_MOVE",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ELG_NUMMOV",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "NAVALUE", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-10-04",
                                7574.02425,
                                8023.4566,
                                7378,
                                578779,
                                7658,
                                7716,
                                7718,
                                4443587354.43106,
                                7677.5139,
                                7717,
                                47.4475,
                                519805,
                                6738,
                                207398,
                                58974,
                                7742,
                                7662.27,
                                7718,
                                7658,
                                7378,
                                7718,
                                207398,
                                9203,
                                7658,
                                7718,
                                None,
                                None,
                                666728,
                                6868,
                                6544,
                                None,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD = [
    StubResponse(
        {
            "links": {"count": 1},
            "variability": "",
            "universe": [
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                }
            ],
            "data": [["LSEG.L", "2021-12-31T00:00:00", 6740000000]],
            "messages": {
                "codes": [[-1, -1, -1]],
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
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.Revenue",
                    "title": "Revenue",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Is used for industrial and utility companies. It "
                                   "consists of revenue from the sale of merchandise, "
                                   "manufactured goods and services, and the distribution "
                                   "of regulated energy resources, depending on a "
                                   "specific company's industry.",
                },
            ],
        }
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_FIELD_NAMES_IN_HEADERS = [
    StubResponse(
        {
            "links": {"count": 1},
            "variability": "",
            "universe": [
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                }
            ],
            "data": [["LSEG.L", "2021-12-31T00:00:00", 6740000000]],
            "messages": {
                "codes": [[-1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by "
                                   "the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.Revenue",
                    "title": "Revenue",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Is used for industrial and utility "
                                   "companies. It consists of revenue from "
                                   "the sale of merchandise, manufactured "
                                   "goods and services, and the distribution "
                                   "of regulated energy resources, depending "
                                   "on a specific company's industry.",
                },
            ],
        }
    )
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_PRICING_FIELD = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 7716],
                    ["2022-10-03", 7638],
                    ["2022-09-30", 7628],
                    ["2022-09-29", 7596],
                    ["2022-09-28", 7692],
                    ["2022-09-27", 7622],
                    ["2022-09-26", 7632],
                    ["2022-09-23", 7468],
                    ["2022-09-22", 7468],
                    ["2022-09-21", 7728],
                    ["2022-09-20", 7542],
                    ["2022-09-16", 7770],
                    ["2022-09-15", 7800],
                    ["2022-09-14", 7900],
                    ["2022-09-13", 8004],
                    ["2022-09-12", 8094],
                    ["2022-09-09", 8004],
                    ["2022-09-08", 8004],
                    ["2022-09-07", 7944],
                    ["2022-09-06", 7966],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 7716]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_AND_ONE_PRICING_FIELD = [
    StubResponse(
        {
            "links": {"count": 1},
            "variability": "",
            "universe": [
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                }
            ],
            "data": [["LSEG.L", "2022-08-18T00:00:00", "GBP"]],
            "messages": {
                "codes": [[-1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by "
                                   "the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Currency",
                    "type": "string",
                    "description": "The statistical average of all broker "
                                   "estimates determined to be on the "
                                   "majority accounting basis. Revenue (or "
                                   "Sales) is a corporation's net revenue, "
                                   "generally derived from core business "
                                   "activities. For non-financial companies, "
                                   "the calculation of net revenue (or net "
                                   "turnover) in most markets generally "
                                   "involves subtracting transportation and "
                                   "related operational costs from gross "
                                   "revenue/sales. Revenue recognition "
                                   "practices vary significantly from market "
                                   "to market, though generally the recording "
                                   "of revenue is based upon sales invoices "
                                   "issued (or anticipated for forecast "
                                   "purposes) during the accounting period.",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 7716],
                    ["2022-10-03", 7638],
                    ["2022-09-30", 7628],
                    ["2022-09-29", 7596],
                    ["2022-09-28", 7692],
                    ["2022-09-27", 7622],
                    ["2022-09-26", 7632],
                    ["2022-09-23", 7468],
                    ["2022-09-22", 7468],
                    ["2022-09-21", 7728],
                    ["2022-09-20", 7542],
                    ["2022-09-16", 7770],
                    ["2022-09-15", 7800],
                    ["2022-09-14", 7900],
                    ["2022-09-13", 8004],
                    ["2022-09-12", 8094],
                    ["2022-09-09", 8004],
                    ["2022-09-08", 8004],
                    ["2022-09-07", 7944],
                    ["2022-09-06", 7966],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 7716]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_ADC_FIELDS = [
    StubResponse(
        {
            "links": {"count": 1},
            "variability": "",
            "universe": [
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                }
            ],
            "data": [["LSEG.L", "2022-08-18T00:00:00", 7284197000, "GBP"]],
            "messages": {
                "codes": [[-1, -1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by "
                                   "the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Revenue - Mean",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "The statistical average of all broker "
                                   "estimates determined to be on the "
                                   "majority accounting basis. Revenue (or "
                                   "Sales) is a corporation's net revenue, "
                                   "generally derived from core business "
                                   "activities. For non-financial companies, "
                                   "the calculation of net revenue (or net "
                                   "turnover) in most markets generally "
                                   "involves subtracting transportation and "
                                   "related operational costs from gross "
                                   "revenue/sales. Revenue recognition "
                                   "practices vary significantly from market "
                                   "to market, though generally the recording "
                                   "of revenue is based upon sales invoices "
                                   "issued (or anticipated for forecast "
                                   "purposes) during the accounting period.",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Currency",
                    "type": "string",
                    "description": "The statistical average of all broker "
                                   "estimates determined to be on the "
                                   "majority accounting basis. Revenue (or "
                                   "Sales) is a corporation's net revenue, "
                                   "generally derived from core business "
                                   "activities. For non-financial companies, "
                                   "the calculation of net revenue (or net "
                                   "turnover) in most markets generally "
                                   "involves subtracting transportation and "
                                   "related operational costs from gross "
                                   "revenue/sales. Revenue recognition "
                                   "practices vary significantly from market "
                                   "to market, though generally the recording "
                                   "of revenue is based upon sales invoices "
                                   "issued (or anticipated for forecast "
                                   "purposes) during the accounting period.",
                },
            ],
        }
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_WITH_INTRADAY_INTERVAL = [
    StubResponse(
        {
            "links": {"count": 1},
            "variability": "",
            "universe": [
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                }
            ],
            "data": [["LSEG.L", "2021-12-31T00:00:00", 6740000000]],
            "messages": {
                "codes": [[-1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by "
                                   "the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.Revenue",
                    "title": "Revenue",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Is used for industrial and utility "
                                   "companies. It consists of revenue from "
                                   "the sale of merchandise, manufactured "
                                   "goods and services, and the distribution "
                                   "of regulated energy resources, depending "
                                   "on a specific company's industry.",
                },
            ],
        }
    )
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_PRICING_FIELD_WITH_INTRADAY_INT = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
                "interval": "PT10M",
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
                ],
                "data": [
                    ["2022-10-05T15:40:00.000000000Z", 7790],
                    ["2022-10-05T15:30:00.000000000Z", 7790],
                    ["2022-10-05T15:20:00.000000000Z", 7764],
                    ["2022-10-05T15:10:00.000000000Z", 7758],
                    ["2022-10-05T15:00:00.000000000Z", 7734],
                    ["2022-10-05T14:50:00.000000000Z", 7722],
                    ["2022-10-05T14:40:00.000000000Z", 7728],
                    ["2022-10-05T14:30:00.000000000Z", 7718],
                    ["2022-10-05T14:20:00.000000000Z", 7720],
                    ["2022-10-05T14:10:00.000000000Z", 7712],
                    ["2022-10-05T14:00:00.000000000Z", 7710],
                    ["2022-10-05T13:50:00.000000000Z", 7708],
                    ["2022-10-05T13:40:00.000000000Z", 7710],
                    ["2022-10-05T13:30:00.000000000Z", 7714],
                    ["2022-10-05T13:20:00.000000000Z", 7714],
                    ["2022-10-05T13:10:00.000000000Z", 7688],
                    ["2022-10-05T13:00:00.000000000Z", 7690],
                    ["2022-10-05T12:50:00.000000000Z", 7704],
                    ["2022-10-05T12:40:00.000000000Z", 7710],
                    ["2022-10-05T12:30:00.000000000Z", 7706],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                            {"name": "SEQNUM", "type": "string"},
                        ],
                        "data": [[2656, "2022-10-05T16:15:00.023000000Z", "11622949"]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_WITH_NON_INTRADAY_INT = [
    StubResponse(
        {
            "links": {"count": 1},
            "variability": "",
            "universe": [
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                }
            ],
            "data": [["LSEG.L", "2022-08-18T00:00:00", 7284197000]],
            "messages": {
                "codes": [[-1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by "
                                   "the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Revenue - Mean",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "The statistical average of all broker "
                                   "estimates determined to be on the "
                                   "majority accounting basis. Revenue (or "
                                   "Sales) is a corporation's net revenue, "
                                   "generally derived from core business "
                                   "activities. For non-financial companies, "
                                   "the calculation of net revenue (or net "
                                   "turnover) in most markets generally "
                                   "involves subtracting transportation and "
                                   "related operational costs from gross "
                                   "revenue/sales. Revenue recognition "
                                   "practices vary significantly from market "
                                   "to market, though generally the recording "
                                   "of revenue is based upon sales invoices "
                                   "issued (or anticipated for forecast "
                                   "purposes) during the accounting period.",
                },
            ],
        }
    )
]

RDP_GET_HISTORY_ONE_INST_ONE_PRICING_FIELD_WITH_NON_INTRADAY_INT = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-05", 7788],
                    ["2022-10-04", 7716],
                    ["2022-10-03", 7638],
                    ["2022-09-30", 7628],
                    ["2022-09-29", 7596],
                    ["2022-09-28", 7692],
                    ["2022-09-27", 7622],
                    ["2022-09-26", 7632],
                    ["2022-09-23", 7468],
                    ["2022-09-22", 7468],
                    ["2022-09-21", 7728],
                    ["2022-09-20", 7542],
                    ["2022-09-16", 7770],
                    ["2022-09-15", 7800],
                    ["2022-09-14", 7900],
                    ["2022-09-13", 8004],
                    ["2022-09-12", 8094],
                    ["2022-09-09", 8004],
                    ["2022-09-08", 8004],
                    ["2022-09-07", 7944],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-05", 7788]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HIST_ONE_INS_TWO_ADC_TWO_HP_NON_INTRADAY_INT_START_END_DATE = [
    StubResponse(
        {
            "links": {"count": 40},
            "variability": "",
            "universe": [
                {
                    "Instrument": "IBM",
                    "Company Common Name": "International Business Machines " "Corp",
                    "Organization PermID": "4295904307",
                    "Reporting Currency": "USD",
                }
            ],
            "data": [
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2019-12-31T00:00:00", 7292000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-31T00:00:00", 4042000000, None],
                ["IBM", "2020-12-16T00:00:00", None, 73950729070],
                ["IBM", "2020-12-16T00:00:00", None, 73950729070],
                ["IBM", "2020-12-16T00:00:00", None, 73950729070],
                ["IBM", "2020-12-16T00:00:00", None, 73950729070],
                ["IBM", "2020-12-16T00:00:00", None, 73950729070],
                ["IBM", "2020-12-16T00:00:00", None, 73950729070],
                ["IBM", "2021-01-12T00:00:00", None, 73959395730],
                ["IBM", "2021-01-12T00:00:00", None, 73959395730],
                ["IBM", "2021-01-14T00:00:00", None, 73965995730],
                ["IBM", "2021-01-14T00:00:00", None, 73965995730],
                ["IBM", "2021-01-18T00:00:00", None, 73987395730],
                ["IBM", "2021-01-18T00:00:00", None, 73987395730],
                ["IBM", "2021-01-21T00:00:00", None, 74726080400],
                ["IBM", "2021-01-22T00:00:00", None, 74238533200],
                ["IBM", "2021-01-25T00:00:00", None, 74191285570],
                ["IBM", "2021-01-25T00:00:00", None, 74191285570],
                ["IBM", "2021-01-27T00:00:00", None, 74195199870],
                ["IBM", "2021-01-27T00:00:00", None, 74195199870],
                ["IBM", "2021-01-27T00:00:00", None, 74195199870],
                ["IBM", "2021-01-27T00:00:00", None, 74195199870],
            ],
            "messages": {
                "codes": [
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -1, -2],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                    [-1, -1, -2, -1],
                ],
                "descriptions": [
                    {"code": -2, "description": "empty"},
                    {"code": -1, "description": "ok"},
                ],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by "
                                   "the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.F.NetIncAfterTax",
                    "title": "Net Income after Tax",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Net Income after Tax [SIAT] represents "
                                   "the income/expense after all operating "
                                   "and non-operating income and expense, "
                                   "reserves, income taxes, but before equity "
                                   "in earnings, minority interest, "
                                   "extraordinary items, after-tax "
                                   "adjustments, discontinued operations and "
                                   "preferred dividends. Applicable to all "
                                   "Industries.\nNet Income after Tax [SIAT] "
                                   "includes:\n• Net Income after Tax [XIAT]",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Revenue - Mean",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "The statistical average of all broker "
                                   "estimates determined to be on the "
                                   "majority accounting basis. Revenue (or "
                                   "Sales) is a corporation's net revenue, "
                                   "generally derived from core business "
                                   "activities. For non-financial companies, "
                                   "the calculation of net revenue (or net "
                                   "turnover) in most markets generally "
                                   "involves subtracting transportation and "
                                   "related operational costs from gross "
                                   "revenue/sales. Revenue recognition "
                                   "practices vary significantly from market "
                                   "to market, though generally the recording "
                                   "of revenue is based upon sales invoices "
                                   "issued (or anticipated for forecast "
                                   "purposes) during the accounting period.",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2021-02-01", 115.078159, 115.135469],
                    ["2021-01-29", 113.693171, 113.702723],
                    ["2021-01-28", 114.686541, 114.696093],
                    ["2021-01-27", 116.978935, 117.103106],
                    ["2021-01-26", 116.969383, 116.988487],
                    ["2021-01-25", 113.253795, 113.263347],
                    ["2021-01-22", 113.28245, 113.292002],
                    ["2021-01-21", 125.909718, 125.91927],
                    ["2021-01-20", 124.190423, 124.247733],
                    ["2021-01-19", 123.206604, 123.235259],
                    ["2021-01-15", 122.623954, 122.662161],
                    ["2021-01-14", 123.177949, 123.187501],
                    ["2021-01-13", 121.219863, 121.229415],
                    ["2021-01-12", 123.397637, 123.407189],
                    ["2021-01-11", 122.824539, 122.862745],
                    ["2021-01-08", 122.767229, 122.805435],
                    ["2021-01-07", 123.206604, 123.244811],
                    ["2021-01-06", 123.493154, 123.512257],
                    ["2021-01-05", 120.513042, 120.5608],
                    ["2021-01-04", 118.449888, 118.459439],
                ],
            }
        ]
    ),
]

RDP_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_PRICING_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-05", 7788, 7790],
                    ["2022-10-04", 7716, 7718],
                    ["2022-10-03", 7638, 7640],
                    ["2022-09-30", 7628, 7630],
                    ["2022-09-29", 7596, 7598],
                    ["2022-09-28", 7692, 7696],
                    ["2022-09-27", 7622, 7624],
                    ["2022-09-26", 7632, 7634],
                    ["2022-09-23", 7468, 7470],
                    ["2022-09-22", 7468, 7470],
                    ["2022-09-21", 7728, 7730],
                    ["2022-09-20", 7542, 7548],
                    ["2022-09-16", 7770, 7786],
                    ["2022-09-15", 7800, 7802],
                    ["2022-09-14", 7900, 7902],
                    ["2022-09-13", 8004, 8006],
                    ["2022-09-12", 8094, 8098],
                    ["2022-09-09", 8004, 8010],
                    ["2022-09-08", 8004, 8006],
                    ["2022-09-07", 7944, 7946],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-05", 7788, 7790]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_TWO_INSTRUMENTS_WITHOUT_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "TRNOVR_UNS", "type": "number", "decimalChar": "."},
                    {"name": "VWAP", "type": "number", "decimalChar": "."},
                    {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                    {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "TRD_STATUS", "type": "number", "decimalChar": "."},
                    {"name": "SALTIM", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-10-04",
                        125.5,
                        125.62,
                        122.53,
                        1444246,
                        122.8,
                        125.47,
                        125.5,
                        180658926,
                        125.0887,
                        2,
                        681369,
                        10240,
                        1,
                        72600,
                    ],
                    [
                        "2022-10-03",
                        121.51,
                        122.21,
                        119.63,
                        1396140,
                        120.2,
                        121.51,
                        121.56,
                        169501789,
                        121.4074,
                        3,
                        689575,
                        9004,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-30",
                        118.81,
                        122.43,
                        118.61,
                        2029911,
                        121.66,
                        118.83,
                        118.92,
                        242494240,
                        119.4605,
                        2,
                        1133279,
                        11289,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-29",
                        121.63,
                        122.56,
                        120.58,
                        1048410,
                        122.26,
                        121.68,
                        121.71,
                        127412543,
                        121.5293,
                        2,
                        525500,
                        7993,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-28",
                        122.76,
                        123.22,
                        119.81,
                        1820304,
                        121.65,
                        122.71,
                        122.72,
                        222716495,
                        122.3513,
                        3,
                        998710,
                        10524,
                        1,
                        72600,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                            {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                            {"name": "LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRNOVR_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "VWAP", "type": "number", "decimalChar": "."},
                            {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                            {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                            {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRD_STATUS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "SALTIM", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-10-04",
                                125.5,
                                125.62,
                                122.53,
                                1444246,
                                122.8,
                                125.47,
                                125.5,
                                180658926,
                                125.0887,
                                2,
                                681369,
                                10240,
                                1,
                                72600,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASIAOP_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIAHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIALO_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIACL_BID", "type": "number", "decimalChar": "."},
                    {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMEROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-10-05",
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        0.9984,
                        0.9994,
                        0.9934,
                        0.9939,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        "2022-10-04",
                        0.9983,
                        0.9987,
                        0.9999,
                        0.9804,
                        0.9825,
                        0.9985,
                        86112,
                        0.9807,
                        1.0002,
                        0.9825,
                        0.9895,
                        0.9804,
                        0.9873,
                        0.9831,
                        0.9979,
                        0.9824,
                        0.9974,
                        0.989,
                        0.9999,
                        0.9875,
                        0.9983,
                        0.9827,
                    ],
                    [
                        "2022-10-03",
                        0.9824,
                        0.9827,
                        0.9844,
                        0.9751,
                        0.9798,
                        0.98255,
                        97658,
                        0.9754,
                        0.9847,
                        0.9798,
                        0.9834,
                        0.9782,
                        0.981,
                        0.9783,
                        0.9844,
                        0.9751,
                        0.9806,
                        0.9776,
                        0.9844,
                        0.9752,
                        0.9824,
                        0.9802,
                    ],
                    [
                        "2022-09-30",
                        0.9799,
                        0.9803,
                        0.9853,
                        0.9733,
                        0.9815,
                        0.9801,
                        94060,
                        0.9736,
                        0.9856,
                        0.9815,
                        0.9844,
                        0.9789,
                        0.9832,
                        0.9798,
                        0.9853,
                        0.9733,
                        0.9781,
                        0.976,
                        0.9817,
                        0.9733,
                        0.9799,
                        0.9818,
                    ],
                    [
                        "2022-09-29",
                        0.9814,
                        0.9818,
                        0.9815,
                        0.9634,
                        0.9733,
                        0.9816,
                        96257,
                        0.9636,
                        0.9818,
                        0.9733,
                        0.9738,
                        0.9634,
                        0.9655,
                        0.9684,
                        0.9789,
                        0.9634,
                        0.9771,
                        0.9713,
                        0.9815,
                        0.9682,
                        0.9814,
                        0.9737,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "BID_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                            {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                            {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                            {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                            {
                                "name": "ASK_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAOP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIALO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIACL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                            {
                                "name": "AMEROP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERLO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERCL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-10-05",
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                0.9984,
                                0.9994,
                                0.9934,
                                0.9939,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_TWO_INST_ONE_ADC_FIELDS_QUARTERLY_INT_START_DATE = [
    StubResponse(
        {
            "links": {"count": 2},
            "variability": "",
            "universe": [
                {
                    "Instrument": "IBM",
                    "Company Common Name": "International Business Machines Corp",
                    "Organization PermID": "4295904307",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MSFT.O",
                    "Company Common Name": "Microsoft Corp",
                    "Organization PermID": "4295907168",
                    "Reporting Currency": "USD",
                },
            ],
            "data": [
                ["IBM", "2018-12-31T00:00:00", 10760000000],
                ["MSFT.O", "2019-06-30T00:00:00", 39397000000],
            ],
            "messages": {
                "codes": [[-1, -1, -1], [-1, -1, -1]],
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
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.F.NetIncAfterTax",
                    "title": "Net Income after Tax",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Net Income after Tax [SIAT] represents the income/expense after all operating and non-operating income and expense, reserves, income taxes, but before equity in earnings, minority interest, extraordinary items, after-tax adjustments, discontinued operations and preferred dividends. Applicable to all Industries.\nNet Income after Tax [SIAT] includes:\n• Net Income after Tax [XIAT]",
                },
            ],
        }
    )
]

RDP_GET_HISTORY_TWO_INS_TWO_HP_FIELDS_DAILY_INT_START_DATE = [
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 0.9983, 0.9987],
                    ["2022-10-03", 0.9824, 0.9827],
                    ["2022-09-30", 0.9799, 0.9803],
                    ["2022-09-29", 0.9814, 0.9818],
                    ["2022-09-28", 0.9734, 0.9737],
                    ["2022-09-27", 0.9592, 0.9596],
                    ["2022-09-26", 0.9606, 0.9609],
                    ["2022-09-23", 0.969, 0.9694],
                    ["2022-09-22", 0.9836, 0.984],
                    ["2022-09-21", 0.9837, 0.9839],
                    ["2022-09-20", 0.997, 0.9974],
                    ["2022-09-19", 1.0022, 1.0026],
                    ["2022-09-16", 1.0015, 1.0019],
                    ["2022-09-15", 0.9999, 1.0003],
                    ["2022-09-14", 0.9977, 0.9981],
                    ["2022-09-13", 0.997, 0.9974],
                    ["2022-09-12", 1.0119, 1.0122],
                    ["2022-09-09", 1.0039, 1.0043],
                    ["2022-09-08", 0.9994, 0.9998],
                    ["2022-09-07", 0.9999, 1.0003],
                ],
            }
        ]
    ),
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 1.1473, 1.1477],
                    ["2022-10-03", 1.1322, 1.1326],
                    ["2022-09-30", 1.116, 1.1164],
                    ["2022-09-29", 1.1115, 1.1119],
                    ["2022-09-28", 1.0888, 1.0892],
                    ["2022-09-27", 1.0731, 1.0734],
                    ["2022-09-26", 1.0684, 1.0688],
                    ["2022-09-23", 1.0856, 1.086],
                    ["2022-09-22", 1.1257, 1.1261],
                    ["2022-09-21", 1.1266, 1.127],
                    ["2022-09-20", 1.1379, 1.1383],
                    ["2022-09-19", 1.1429, 1.1435],
                    ["2022-09-16", 1.1412, 1.1416],
                    ["2022-09-15", 1.1463, 1.1469],
                    ["2022-09-14", 1.1535, 1.1539],
                    ["2022-09-13", 1.1491, 1.1495],
                    ["2022-09-12", 1.1679, 1.1688],
                    ["2022-09-09", 1.1587, 1.1591],
                    ["2022-09-08", 1.15, 1.1504],
                    ["2022-09-07", 1.1525, 1.1529],
                ],
            }
        ]
    ),
]

RDP_GET_HISTORY_TWO_INST_ADC_AND_PRICING_FIELDS_1H_INT_FIELD_NAMES = [
    StubResponse(
        {
            "links": {"count": 4},
            "variability": "",
            "universe": [
                {
                    "Instrument": "VOD.L",
                    "Company Common Name": "Vodafone Group PLC",
                    "Organization PermID": "4295896661",
                    "Reporting Currency": "EUR",
                },
                {
                    "Instrument": "MSFT.O",
                    "Company Common Name": "Microsoft Corp",
                    "Organization PermID": "4295907168",
                    "Reporting Currency": "USD",
                },
            ],
            "data": [
                ["VOD.L", "2022-03-31T00:00:00", 2624000000, None],
                ["VOD.L", "2022-10-04T00:00:00", None, "EUR"],
                ["MSFT.O", "2022-06-30T00:00:00", 72738000000, None],
                ["MSFT.O", "2022-10-04T00:00:00", None, "USD"],
            ],
            "messages": {
                "codes": [
                    [-1, -1, -1, -2],
                    [-1, -1, -2, -1],
                    [-1, -1, -1, -2],
                    [-1, -1, -2, -1],
                ],
                "descriptions": [
                    {"code": -2, "description": "empty"},
                    {"code": -1, "description": "ok"},
                ],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.F.NetIncAfterTax",
                    "title": "Net Income after Tax",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Net Income after Tax [SIAT] represents the income/expense after all operating and non-operating income and expense, reserves, income taxes, but before equity in earnings, minority interest, extraordinary items, after-tax adjustments, discontinued operations and preferred dividends. Applicable to all Industries.\nNet Income after Tax [SIAT] includes:\n• Net Income after Tax [XIAT]",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Currency",
                    "type": "string",
                    "description": "The statistical average of all broker estimates determined to be on the majority accounting basis. Revenue (or Sales) is a corporation's net revenue, generally derived from core business activities. For non-financial companies, the calculation of net revenue (or net turnover) in most markets generally involves subtracting transportation and related operational costs from gross revenue/sales. Revenue recognition practices vary significantly from market to market, though generally the recording of revenue is based upon sales invoices issued (or anticipated for forecast purposes) during the accounting period.",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "interval": "PT60M",
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
                    ["2022-10-05T16:00:00.000000000Z", 102.02, 105],
                    ["2022-10-05T15:00:00.000000000Z", 102.54, 102.72],
                    ["2022-10-05T14:00:00.000000000Z", 102.16, 102.2],
                    ["2022-10-05T13:00:00.000000000Z", 102.64, 102.7],
                    ["2022-10-05T12:00:00.000000000Z", 103.12, 103.14],
                    ["2022-10-05T11:00:00.000000000Z", 102.8, 102.82],
                    ["2022-10-05T10:00:00.000000000Z", 102.76, 102.8],
                    ["2022-10-05T09:00:00.000000000Z", 102.08, 102.1],
                    ["2022-10-05T08:00:00.000000000Z", 102.08, 102.12],
                    ["2022-10-05T07:00:00.000000000Z", 102.7, 102.74],
                    ["2022-10-05T06:00:00.000000000Z", 120.72, 89.24],
                    ["2022-10-05T04:00:00.000000000Z", 103, 110],
                    ["2022-10-04T16:00:00.000000000Z", 103, 110],
                    ["2022-10-04T15:00:00.000000000Z", 104.94, 105.02],
                    ["2022-10-04T14:00:00.000000000Z", 104.94, 104.96],
                    ["2022-10-04T13:00:00.000000000Z", 105.26, 105.3],
                    ["2022-10-04T12:00:00.000000000Z", 105.62, 105.66],
                    ["2022-10-04T11:00:00.000000000Z", 105.56, 105.6],
                    ["2022-10-04T10:00:00.000000000Z", 106.24, 106.3],
                    ["2022-10-04T09:00:00.000000000Z", 106.1, 106.16],
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
                                "2022-10-05T17:05:02.017000000Z",
                                12142,
                                "2022-10-05T17:05:02.409000000Z",
                                "371077",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "interval": "PT60M",
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
                    ["2022-10-05T16:00:00.000000000Z", 102.02, 105],
                    ["2022-10-05T15:00:00.000000000Z", 102.54, 102.72],
                    ["2022-10-05T14:00:00.000000000Z", 102.16, 102.2],
                    ["2022-10-05T13:00:00.000000000Z", 102.64, 102.7],
                    ["2022-10-05T12:00:00.000000000Z", 103.12, 103.14],
                    ["2022-10-05T11:00:00.000000000Z", 102.8, 102.82],
                    ["2022-10-05T10:00:00.000000000Z", 102.76, 102.8],
                    ["2022-10-05T09:00:00.000000000Z", 102.08, 102.1],
                    ["2022-10-05T08:00:00.000000000Z", 102.08, 102.12],
                    ["2022-10-05T07:00:00.000000000Z", 102.7, 102.74],
                    ["2022-10-05T06:00:00.000000000Z", 120.72, 89.24],
                    ["2022-10-05T04:00:00.000000000Z", 103, 110],
                    ["2022-10-04T16:00:00.000000000Z", 103, 110],
                    ["2022-10-04T15:00:00.000000000Z", 104.94, 105.02],
                    ["2022-10-04T14:00:00.000000000Z", 104.94, 104.96],
                    ["2022-10-04T13:00:00.000000000Z", 105.26, 105.3],
                    ["2022-10-04T12:00:00.000000000Z", 105.62, 105.66],
                    ["2022-10-04T11:00:00.000000000Z", 105.56, 105.6],
                    ["2022-10-04T10:00:00.000000000Z", 106.24, 106.3],
                    ["2022-10-04T09:00:00.000000000Z", 106.1, 106.16],
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
                                "2022-10-05T17:05:02.017000000Z",
                                12142,
                                "2022-10-05T17:05:02.409000000Z",
                                "371077",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.O"},
                "interval": "PT60M",
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
                    ["2022-10-05T17:00:00.000000000Z", 247.7, 247.72],
                    ["2022-10-05T16:00:00.000000000Z", 247.63, 247.66],
                    ["2022-10-05T15:00:00.000000000Z", 245.62, 245.64],
                    ["2022-10-05T14:00:00.000000000Z", 244.34, 244.37],
                    ["2022-10-05T13:00:00.000000000Z", 246.13, 246.18],
                    ["2022-10-05T12:00:00.000000000Z", 245.84, 246.35],
                    ["2022-10-05T11:00:00.000000000Z", 246.62, 247.05],
                    ["2022-10-05T10:00:00.000000000Z", 246.99, 247.51],
                    ["2022-10-05T09:00:00.000000000Z", 245.96, 246.5],
                    ["2022-10-05T08:00:00.000000000Z", 246.8, 247.25],
                    ["2022-10-04T23:00:00.000000000Z", 248.15, 248.25],
                    ["2022-10-04T22:00:00.000000000Z", 248.41, 248.6],
                    ["2022-10-04T21:00:00.000000000Z", 248.8, 249],
                    ["2022-10-04T20:00:00.000000000Z", 248.9, 248.98],
                    ["2022-10-04T19:00:00.000000000Z", 248.89, 248.9],
                    ["2022-10-04T18:00:00.000000000Z", 248.84, 248.87],
                    ["2022-10-04T17:00:00.000000000Z", 248.08, 248.1],
                    ["2022-10-04T16:00:00.000000000Z", 248.03, 248.04],
                    ["2022-10-04T15:00:00.000000000Z", 248.52, 248.54],
                    ["2022-10-04T14:00:00.000000000Z", 249.57, 249.6],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-10-05T17:09:50.423000000Z",
                                7984,
                                "2022-10-05T17:09:50.423000000Z",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.O"},
                "interval": "PT60M",
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
                    ["2022-10-05T17:00:00.000000000Z", 247.7, 247.72],
                    ["2022-10-05T16:00:00.000000000Z", 247.63, 247.66],
                    ["2022-10-05T15:00:00.000000000Z", 245.62, 245.64],
                    ["2022-10-05T14:00:00.000000000Z", 244.34, 244.37],
                    ["2022-10-05T13:00:00.000000000Z", 246.13, 246.18],
                    ["2022-10-05T12:00:00.000000000Z", 245.84, 246.35],
                    ["2022-10-05T11:00:00.000000000Z", 246.62, 247.05],
                    ["2022-10-05T10:00:00.000000000Z", 246.99, 247.51],
                    ["2022-10-05T09:00:00.000000000Z", 245.96, 246.5],
                    ["2022-10-05T08:00:00.000000000Z", 246.8, 247.25],
                    ["2022-10-04T23:00:00.000000000Z", 248.15, 248.25],
                    ["2022-10-04T22:00:00.000000000Z", 248.41, 248.6],
                    ["2022-10-04T21:00:00.000000000Z", 248.8, 249],
                    ["2022-10-04T20:00:00.000000000Z", 248.9, 248.98],
                    ["2022-10-04T19:00:00.000000000Z", 248.89, 248.9],
                    ["2022-10-04T18:00:00.000000000Z", 248.84, 248.87],
                    ["2022-10-04T17:00:00.000000000Z", 248.08, 248.1],
                    ["2022-10-04T16:00:00.000000000Z", 248.03, 248.04],
                    ["2022-10-04T15:00:00.000000000Z", 248.52, 248.54],
                    ["2022-10-04T14:00:00.000000000Z", 249.57, 249.6],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "COLLECT_DATETIME", "type": "string"},
                            {"name": "RTL", "type": "number", "decimalChar": "."},
                            {"name": "SOURCE_DATETIME", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-10-05T17:09:50.906000000Z",
                                8112,
                                "2022-10-05T17:09:50.906000000Z",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_TWO_INSTS_ONE_ADC_TWO_HP_FIELDS_INT_TICK_START_DATE = [
    StubResponse(
        {
            "links": {"count": 2},
            "variability": "",
            "universe": [
                {
                    "Instrument": "IBM.N",
                    "Company Common Name": "International Business Machines Corp",
                    "Organization PermID": "4295904307",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "LSEG.L",
                    "Company Common Name": "London Stock Exchange Group PLC",
                    "Organization PermID": "4298007752",
                    "Reporting Currency": "GBP",
                },
            ],
            "data": [
                ["IBM.N", "2021-04-25T00:00:00", 74397055190],
                ["LSEG.L", "2021-05-10T00:00:00", 6935640740],
            ],
            "messages": {
                "codes": [[-1, -1, -1], [-1, -1, -1]],
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
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.RevenueMean",
                    "title": "Revenue - Mean",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "The statistical average of all broker estimates determined to be on the majority accounting basis. Revenue (or Sales) is a corporation's net revenue, generally derived from core business activities. For non-financial companies, the calculation of net revenue (or net turnover) in most markets generally involves subtracting transportation and related operational costs from gross revenue/sales. Revenue recognition practices vary significantly from market to market, though generally the recording of revenue is based upon sales invoices issued (or anticipated for forecast purposes) during the accounting period.",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-05T17:05:25.430000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:25.196000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:25.196000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:25.196000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:25.174000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:25.174000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:25.081000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.985000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.925000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.925000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.925000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.925000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.881000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.881000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.881000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.881000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.397000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.373000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.372000000Z", "quote", 125.35, 125.38],
                    ["2022-10-05T17:05:24.257000000Z", "quote", 125.35, 125.38],
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
                            {"name": "SOURCE_DATETIME", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-10-05T17:20:22.551000000Z",
                                54656,
                                "2022-10-05T17:20:22.551000000Z",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "LSEG.L"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 9000],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8746],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8634],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8580],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8490],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8470],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8200],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 8030],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 7998],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 7886],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 7834],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 7830],
                    ["2022-10-05T16:30:00.285000000Z", "quote", 7170, 7824],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7170, 7820],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7170, 7816],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7170, 7810],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7704, 7810],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7710, 7810],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7714, 7810],
                    ["2022-10-05T16:30:00.284000000Z", "quote", 7720, 7810],
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
                            {"name": "SOURCE_DATETIME", "type": "string"},
                            {"name": "SEQNUM", "type": "string"},
                        ],
                        "data": [
                            [
                                "2022-10-05T17:17:40.000000000Z",
                                3662,
                                "2022-10-05T17:18:09.619000000Z",
                                "384855",
                            ]
                        ],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_THREE_INSTRUMENTS_WITHOUT_FIELDS = [
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                    {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "TRNOVR_UNS", "type": "number", "decimalChar": "."},
                    {"name": "VWAP", "type": "number", "decimalChar": "."},
                    {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                    {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                    {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                    {"name": "TRD_STATUS", "type": "number", "decimalChar": "."},
                    {"name": "SALTIM", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-10-04",
                        125.5,
                        125.62,
                        122.53,
                        1444246,
                        122.8,
                        125.47,
                        125.5,
                        180658926,
                        125.0887,
                        2,
                        681369,
                        10240,
                        1,
                        72600,
                    ],
                    [
                        "2022-10-03",
                        121.51,
                        122.21,
                        119.63,
                        1396140,
                        120.2,
                        121.51,
                        121.56,
                        169501789,
                        121.4074,
                        3,
                        689575,
                        9004,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-30",
                        118.81,
                        122.43,
                        118.61,
                        2029911,
                        121.66,
                        118.83,
                        118.92,
                        242494240,
                        119.4605,
                        2,
                        1133279,
                        11289,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-29",
                        121.63,
                        122.56,
                        120.58,
                        1048410,
                        122.26,
                        121.68,
                        121.71,
                        127412543,
                        121.5293,
                        2,
                        525500,
                        7993,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-28",
                        122.76,
                        123.22,
                        119.81,
                        1820304,
                        121.65,
                        122.71,
                        122.72,
                        222716495,
                        122.3513,
                        3,
                        998710,
                        10524,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-27",
                        121.74,
                        123.95,
                        121.09,
                        1335006,
                        122.6,
                        121.76,
                        121.77,
                        162900375,
                        122.0222,
                        2,
                        559187,
                        10219,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-26",
                        122.01,
                        124.25,
                        121.76,
                        1287055,
                        122.3,
                        122,
                        122.01,
                        157505074,
                        122.3763,
                        2,
                        593148,
                        9160,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-23",
                        122.71,
                        124.57,
                        121.75,
                        1555461,
                        124.53,
                        122.75,
                        122.76,
                        191160601,
                        122.8964,
                        2,
                        684185,
                        11039,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-22",
                        125.31,
                        126.49,
                        124.45,
                        1152042,
                        124.76,
                        125.31,
                        125.32,
                        144521845,
                        125.4484,
                        2,
                        450245,
                        9169,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-21",
                        124.93,
                        127.77,
                        124.92,
                        1096128,
                        126.89,
                        124.94,
                        124.95,
                        137967478,
                        125.868,
                        2,
                        477129,
                        8477,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-20",
                        126.3,
                        126.9,
                        125.53,
                        799630,
                        126.9,
                        126.3,
                        126.31,
                        100914959,
                        126.2021,
                        2,
                        357706,
                        7375,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-19",
                        127.73,
                        128.06,
                        126.28,
                        1320203,
                        126.5,
                        127.69,
                        127.73,
                        168291147,
                        127.4737,
                        2,
                        725956,
                        7910,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-16",
                        127.27,
                        127.49,
                        124.01,
                        5408858,
                        124.36,
                        127.23,
                        127.27,
                        685427466,
                        126.7231,
                        2,
                        4463300,
                        10894,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-15",
                        125.49,
                        127.39,
                        124.9,
                        1474804,
                        127.39,
                        125.49,
                        125.5,
                        185269243,
                        125.623,
                        3,
                        705660,
                        10066,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-14",
                        127.69,
                        129,
                        126.85,
                        1286648,
                        127.5,
                        127.66,
                        127.67,
                        164386719,
                        127.7636,
                        3,
                        725522,
                        8149,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-13",
                        127.25,
                        129.82,
                        126.8,
                        1603709,
                        129.14,
                        127.23,
                        127.25,
                        205136259,
                        127.9136,
                        2,
                        752373,
                        9835,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-12",
                        130.66,
                        130.99,
                        129.91,
                        1245309,
                        130.33,
                        130.7,
                        130.71,
                        162528528,
                        130.5126,
                        2,
                        628490,
                        6975,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-09",
                        129.19,
                        129.49,
                        128.07,
                        1069094,
                        128.9,
                        129.21,
                        129.22,
                        138041202,
                        129.1198,
                        2,
                        520062,
                        6216,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-08",
                        128.47,
                        128.51,
                        126.59,
                        911647,
                        127.12,
                        128.42,
                        128.43,
                        116797276,
                        128.1168,
                        2,
                        465537,
                        5751,
                        1,
                        72600,
                    ],
                    [
                        "2022-09-07",
                        127.71,
                        127.855,
                        126.28,
                        771510,
                        126.69,
                        127.72,
                        127.73,
                        98346699,
                        127.473,
                        2,
                        420909,
                        4878,
                        1,
                        72600,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "TRDPRC_1", "type": "number", "decimalChar": "."},
                            {"name": "HIGH_1", "type": "number", "decimalChar": "."},
                            {"name": "LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "ACVOL_UNS", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_PRC", "type": "number", "decimalChar": "."},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRNOVR_UNS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "VWAP", "type": "number", "decimalChar": "."},
                            {"name": "BLKCOUNT", "type": "number", "decimalChar": "."},
                            {"name": "BLKVOLUM", "type": "number", "decimalChar": "."},
                            {"name": "NUM_MOVES", "type": "number", "decimalChar": "."},
                            {
                                "name": "TRD_STATUS",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "SALTIM", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-10-04",
                                125.5,
                                125.62,
                                122.53,
                                1444246,
                                122.8,
                                125.47,
                                125.5,
                                180658926,
                                125.0887,
                                2,
                                681369,
                                10240,
                                1,
                                72600,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
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
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                    {"name": "BID_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                    {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                    {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                    {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                    {"name": "ASK_HIGH_1", "type": "number", "decimalChar": "."},
                    {"name": "ASIAOP_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIAHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIALO_BID", "type": "number", "decimalChar": "."},
                    {"name": "ASIACL_BID", "type": "number", "decimalChar": "."},
                    {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMEROP_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERHI_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERLO_BID", "type": "number", "decimalChar": "."},
                    {"name": "AMERCL_BID", "type": "number", "decimalChar": "."},
                    {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    [
                        "2022-10-05",
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        0.9984,
                        0.9994,
                        0.9934,
                        0.9939,
                        0.9965,
                        0.9994,
                        0.9833,
                        0.9864,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ],
                    [
                        "2022-10-04",
                        0.9983,
                        0.9987,
                        0.9999,
                        0.9804,
                        0.9825,
                        0.9985,
                        86112,
                        0.9807,
                        1.0002,
                        0.9825,
                        0.9895,
                        0.9804,
                        0.9873,
                        0.9831,
                        0.9979,
                        0.9824,
                        0.9974,
                        0.989,
                        0.9999,
                        0.9875,
                        0.9983,
                        0.9827,
                    ],
                    [
                        "2022-10-03",
                        0.9824,
                        0.9827,
                        0.9844,
                        0.9751,
                        0.9798,
                        0.98255,
                        97658,
                        0.9754,
                        0.9847,
                        0.9798,
                        0.9834,
                        0.9782,
                        0.981,
                        0.9783,
                        0.9844,
                        0.9751,
                        0.9806,
                        0.9776,
                        0.9844,
                        0.9752,
                        0.9824,
                        0.9802,
                    ],
                    [
                        "2022-09-30",
                        0.9799,
                        0.9803,
                        0.9853,
                        0.9733,
                        0.9815,
                        0.9801,
                        94060,
                        0.9736,
                        0.9856,
                        0.9815,
                        0.9844,
                        0.9789,
                        0.9832,
                        0.9798,
                        0.9853,
                        0.9733,
                        0.9781,
                        0.976,
                        0.9817,
                        0.9733,
                        0.9799,
                        0.9818,
                    ],
                    [
                        "2022-09-29",
                        0.9814,
                        0.9818,
                        0.9815,
                        0.9634,
                        0.9733,
                        0.9816,
                        96257,
                        0.9636,
                        0.9818,
                        0.9733,
                        0.9738,
                        0.9634,
                        0.9655,
                        0.9684,
                        0.9789,
                        0.9634,
                        0.9771,
                        0.9713,
                        0.9815,
                        0.9682,
                        0.9814,
                        0.9737,
                    ],
                    [
                        "2022-09-28",
                        0.9734,
                        0.9737,
                        0.975,
                        0.9534,
                        0.9592,
                        0.97355,
                        104438,
                        0.9537,
                        0.9753,
                        0.9592,
                        0.96,
                        0.9534,
                        0.9577,
                        0.9549,
                        0.9688,
                        0.9534,
                        0.9678,
                        0.9574,
                        0.975,
                        0.9548,
                        0.9734,
                        0.9596,
                    ],
                    [
                        "2022-09-27",
                        0.9592,
                        0.9596,
                        0.967,
                        0.9567,
                        0.9609,
                        0.9594,
                        104222,
                        0.957,
                        0.9673,
                        0.9609,
                        0.967,
                        0.9583,
                        0.9645,
                        0.9635,
                        0.967,
                        0.9592,
                        0.9612,
                        0.9627,
                        0.9652,
                        0.9567,
                        0.9592,
                        0.9611,
                    ],
                    [
                        "2022-09-26",
                        0.9606,
                        0.9609,
                        0.9709,
                        0.9565,
                        0.9678,
                        0.96075,
                        109840,
                        0.9569,
                        0.9712,
                        0.9684,
                        0.9709,
                        0.9565,
                        0.9676,
                        0.9627,
                        0.9701,
                        0.9608,
                        0.9621,
                        0.9641,
                        0.9689,
                        0.9598,
                        0.9606,
                        0.968,
                    ],
                    [
                        "2022-09-23",
                        0.969,
                        0.9694,
                        0.9851,
                        0.9666,
                        0.9835,
                        0.9692,
                        90975,
                        0.9669,
                        0.9854,
                        0.9835,
                        0.9851,
                        0.9765,
                        0.9774,
                        0.9821,
                        0.9838,
                        0.97,
                        0.9716,
                        0.9751,
                        0.9774,
                        0.9666,
                        0.969,
                        0.9839,
                    ],
                    [
                        "2022-09-22",
                        0.9836,
                        0.984,
                        0.9907,
                        0.9807,
                        0.9836,
                        0.9838,
                        103843,
                        0.981,
                        0.9909,
                        0.9836,
                        0.9853,
                        0.9807,
                        0.9843,
                        0.9828,
                        0.9907,
                        0.981,
                        0.9838,
                        0.9874,
                        0.9887,
                        0.981,
                        0.9836,
                        0.9838,
                    ],
                    [
                        "2022-09-21",
                        0.9837,
                        0.9839,
                        0.9976,
                        0.9812,
                        0.997,
                        0.9838,
                        87445,
                        0.9814,
                        0.998,
                        0.997,
                        0.9976,
                        0.9883,
                        0.9909,
                        0.9959,
                        0.9968,
                        0.9865,
                        0.9878,
                        0.9921,
                        0.9925,
                        0.9812,
                        0.9837,
                        0.9974,
                    ],
                    [
                        "2022-09-20",
                        0.997,
                        0.9974,
                        1.005,
                        0.9953,
                        1.0021,
                        0.9972,
                        72943,
                        0.9956,
                        1.0053,
                        1.0021,
                        1.005,
                        1.0011,
                        1.0034,
                        1.0021,
                        1.0041,
                        0.9953,
                        0.9992,
                        1.0006,
                        1.0013,
                        0.9953,
                        0.997,
                        1.0025,
                    ],
                    [
                        "2022-09-19",
                        1.0022,
                        1.0026,
                        1.0029,
                        0.9964,
                        1.001,
                        1.0024,
                        63178,
                        0.9967,
                        1.0031,
                        1.001,
                        1.0029,
                        0.9964,
                        0.9978,
                        0.9992,
                        1.0017,
                        0.9964,
                        1.0002,
                        0.9992,
                        1.0027,
                        0.9974,
                        1.0022,
                        1.0014,
                    ],
                    [
                        "2022-09-16",
                        1.0015,
                        1.0019,
                        1.0036,
                        0.9943,
                        0.9999,
                        1.0017,
                        72842,
                        0.9946,
                        1.0038,
                        0.9999,
                        1.0012,
                        0.9943,
                        0.9956,
                        0.9995,
                        1.0036,
                        0.9943,
                        1.001,
                        0.9983,
                        1.0036,
                        0.9951,
                        1.0015,
                        1.0003,
                    ],
                    [
                        "2022-09-15",
                        0.9999,
                        1.0003,
                        1.0017,
                        0.9954,
                        0.9979,
                        1.0001,
                        69080,
                        0.9957,
                        1.002,
                        0.9979,
                        0.9984,
                        0.9954,
                        0.9977,
                        0.9967,
                        1.0017,
                        0.9954,
                        0.999,
                        0.9977,
                        1.0017,
                        0.997,
                        0.9999,
                        0.9982,
                    ],
                    [
                        "2022-09-14",
                        0.9977,
                        0.9981,
                        1.0023,
                        0.9954,
                        0.9967,
                        0.9979,
                        87677,
                        0.9957,
                        1.0026,
                        0.9967,
                        1.0002,
                        0.9954,
                        0.9986,
                        0.9994,
                        1.0023,
                        0.9958,
                        0.9992,
                        1.0006,
                        1.0009,
                        0.9967,
                        0.9977,
                        0.9971,
                    ],
                    [
                        "2022-09-13",
                        0.997,
                        0.9974,
                        1.0187,
                        0.9964,
                        1.0121,
                        0.9972,
                        77655,
                        0.9968,
                        1.0189,
                        1.0121,
                        1.0155,
                        1.0116,
                        1.0145,
                        1.0126,
                        1.0187,
                        0.9994,
                        0.9996,
                        1.0179,
                        1.0187,
                        0.9964,
                        0.997,
                        1.0125,
                    ],
                    [
                        "2022-09-12",
                        1.0119,
                        1.0122,
                        1.0197,
                        1.0058,
                        1.0078,
                        1.01205,
                        62347,
                        1.0061,
                        1.02,
                        1.0078,
                        1.0197,
                        1.0058,
                        1.0174,
                        1.0076,
                        1.0197,
                        1.0076,
                        1.0124,
                        1.0135,
                        1.0162,
                        1.0103,
                        1.0119,
                        1.0082,
                    ],
                    [
                        "2022-09-09",
                        1.0039,
                        1.0043,
                        1.0112,
                        0.9993,
                        0.9993,
                        1.0041,
                        76399,
                        0.9997,
                        1.0115,
                        0.9993,
                        1.011,
                        0.9993,
                        1.0096,
                        1.0071,
                        1.0112,
                        1.003,
                        1.0044,
                        1.0073,
                        1.0075,
                        1.003,
                        1.0039,
                        0.9997,
                    ],
                    [
                        "2022-09-08",
                        0.9994,
                        0.9998,
                        1.0029,
                        0.9929,
                        1.0001,
                        0.9996,
                        86338,
                        0.9932,
                        1.0032,
                        1.0001,
                        1.0014,
                        0.9975,
                        0.998,
                        0.9988,
                        1.0029,
                        0.9929,
                        0.9952,
                        1.0008,
                        1.0029,
                        0.9929,
                        0.9994,
                        1.0003,
                    ],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                            {
                                "name": "BID_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "BID_LOW_1", "type": "number", "decimalChar": "."},
                            {"name": "OPEN_BID", "type": "number", "decimalChar": "."},
                            {"name": "MID_PRICE", "type": "number", "decimalChar": "."},
                            {"name": "NUM_BIDS", "type": "number", "decimalChar": "."},
                            {"name": "ASK_LOW_1", "type": "number", "decimalChar": "."},
                            {
                                "name": "ASK_HIGH_1",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAOP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIAHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIALO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "ASIACL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "EUROP_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURHI_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURLO_BID", "type": "number", "decimalChar": "."},
                            {"name": "EURCL_BID", "type": "number", "decimalChar": "."},
                            {
                                "name": "AMEROP_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERHI_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERLO_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {
                                "name": "AMERCL_BID",
                                "type": "number",
                                "decimalChar": ".",
                            },
                            {"name": "OPEN_ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [
                            [
                                "2022-10-05",
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                0.9984,
                                0.9994,
                                0.9934,
                                0.9939,
                                0.9965,
                                0.9994,
                                0.9833,
                                0.9864,
                                None,
                                None,
                                None,
                                None,
                                None,
                            ]
                        ],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "data": [
                    ["2022-10-06", 3],
                    ["2022-10-05", 3],
                    ["2022-10-04", 3],
                    ["2022-10-03", 3],
                    ["2022-09-30", 3],
                    ["2022-09-29", 3],
                    ["2022-09-28", 3],
                    ["2022-09-27", 3],
                    ["2022-09-26", 3],
                    ["2022-09-23", 3],
                    ["2022-09-22", 3],
                    ["2022-09-21", 3],
                    ["2022-09-20", 3],
                    ["2022-09-19", 3],
                    ["2022-09-16", 3],
                    ["2022-09-15", 3],
                    ["2022-09-14", 3],
                    ["2022-09-13", 3],
                    ["2022-09-12", 3],
                    ["2022-09-09", 3],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": "P1D",
                "summaryTimestampLabel": "endPeriod",
                "universe": {"ric": "S)MyUSD.GESG1-150112"},
            }
        ]
    ),
]

RDP_GET_HISTORY_EUR_GPB_TICK_INTERVAL = [
    StubResponse(
        [
            {
                "universe": {"ric": "EUR="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-05T19:22:56.533000000Z", "quote", 0.9892, 0.9896],
                    ["2022-10-05T19:22:56.215000000Z", "quote", 0.9894, 0.9895],
                    ["2022-10-05T19:22:55.520000000Z", "quote", 0.9892, 0.9896],
                    ["2022-10-05T19:22:51.650000000Z", "quote", 0.9894, 0.9898],
                    ["2022-10-05T19:22:49.503000000Z", "quote", 0.9894, 0.9898],
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
                        "data": [["2022-10-05T19:22:56.533000000Z", 31566]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GBP="},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "BID",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"name": "EVENT_TYPE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-05T19:22:57.138000000Z", "quote", 1.135, 1.1351],
                    ["2022-10-05T19:22:56.539000000Z", "quote", 1.1347, 1.1351],
                    ["2022-10-05T19:22:56.204000000Z", "quote", 1.1348, 1.135],
                    ["2022-10-05T19:22:55.533000000Z", "quote", 1.1347, 1.1351],
                    ["2022-10-05T19:22:55.501000000Z", "quote", 1.1347, 1.1354],
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
                        "data": [["2022-10-05T19:22:57.138000000Z", 41502]],
                    }
                },
            }
        ]
    ),
]
RDP_GET_HISTORY_CHAIN_ONE_ADC_FIELD_ONE_HP_FIELD = [
    StubResponse(
        {
            "links": {"count": 6},
            "variability": "",
            "universe": [
                {
                    "Instrument": "BMA.BA",
                    "Company Common Name": "Banco Macro SA",
                    "Organization PermID": "4295856087",
                    "Reporting Currency": "ARS",
                },
                {
                    "Instrument": "BBAR.BA",
                    "Company Common Name": "Banco Bbva Argentina SA",
                    "Organization PermID": "4295856044",
                    "Reporting Currency": "ARS",
                },
                {
                    "Instrument": "BHIP.BA",
                    "Company Common Name": "Banco Hipotecario SA",
                    "Organization PermID": "4295856086",
                    "Reporting Currency": "ARS",
                },
                {
                    "Instrument": "GGAL.BA",
                    "Company Common Name": "Grupo Financiero Galicia SA",
                    "Organization PermID": "4295856094",
                    "Reporting Currency": "ARS",
                },
                {
                    "Instrument": "BPAT.BA",
                    "Company Common Name": "Banco Patagonia SA",
                    "Organization PermID": "4295856058",
                    "Reporting Currency": "ARS",
                },
                {
                    "Instrument": "SUPV.BA",
                    "Company Common Name": "Grupo Supervielle SA",
                    "Organization PermID": "5000698780",
                    "Reporting Currency": "ARS",
                },
            ],
            "data": [
                ["BMA.BA", None, None],
                ["BBAR.BA", None, None],
                ["BHIP.BA", None, None],
                ["GGAL.BA", None, None],
                ["BPAT.BA", None, None],
                ["SUPV.BA", None, None],
            ],
            "messages": {
                "codes": [
                    [-1, -2, -2],
                    [-1, -2, -2],
                    [-1, -2, -2],
                    [-1, -2, -2],
                    [-1, -2, -2],
                    [-1, -2, -2],
                ],
                "descriptions": [
                    {"code": -2, "description": "empty"},
                    {"code": -1, "description": "ok"},
                ],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.Revenue",
                    "title": "Revenue",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Is used for industrial and utility companies. It consists of revenue from the sale of merchandise, manufactured goods and services, and the distribution of regulated energy resources, depending on a specific company's industry.",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BMA.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 479],
                    ["2022-10-03", 475.5],
                    ["2022-09-30", 434],
                    ["2022-09-29", 437.43964],
                    ["2022-09-28", 438.930912],
                    ["2022-09-27", 441.714618],
                    ["2022-09-26", 459.311622],
                    ["2022-09-23", 485.756837],
                    ["2022-09-22", 507.03231],
                    ["2022-09-21", 499.078862],
                    ["2022-09-20", 500.073043],
                    ["2022-09-19", 517.868883],
                    ["2022-09-16", 487.049272],
                    ["2022-09-15", 477.20688],
                    ["2022-09-14", 474.224337],
                    ["2022-09-13", 452.352355],
                    ["2022-09-12", 465.276708],
                    ["2022-09-09", 469.452268],
                    ["2022-09-08", 438.433821],
                    ["2022-09-07", 440.919274],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 479]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BBAR.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 328],
                    ["2022-10-03", 325.1],
                    ["2022-09-30", 312.219934],
                    ["2022-09-29", 309.236941],
                    ["2022-09-28", 312.219934],
                    ["2022-09-27", 302.77379],
                    ["2022-09-26", 303.420105],
                    ["2022-09-23", 317.390455],
                    ["2022-09-22", 343.541361],
                    ["2022-09-21", 338.519989],
                    ["2022-09-20", 340.657801],
                    ["2022-09-19", 337.277075],
                    ["2022-09-16", 313.711431],
                    ["2022-09-15", 308.24261],
                    ["2022-09-14", 313.214265],
                    ["2022-09-13", 304.265286],
                    ["2022-09-12", 313.711431],
                    ["2022-09-09", 319.180251],
                    ["2022-09-08", 309.435807],
                    ["2022-09-07", 309.236941],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 328]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BHIP.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 11.1],
                    ["2022-10-03", 11],
                    ["2022-09-30", 10.6],
                    ["2022-09-29", 10.35],
                    ["2022-09-28", 10.5],
                    ["2022-09-27", 10.45],
                    ["2022-09-26", 10.65],
                    ["2022-09-23", 11],
                    ["2022-09-22", 11.65],
                    ["2022-09-21", 11.6],
                    ["2022-09-20", 11.75],
                    ["2022-09-19", 12],
                    ["2022-09-16", 11.85],
                    ["2022-09-15", 11.9],
                    ["2022-09-14", 12.2],
                    ["2022-09-13", 12.1],
                    ["2022-09-12", 12.35],
                    ["2022-09-09", 12.55],
                    ["2022-09-08", 12.5],
                    ["2022-09-07", 12.7],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 11.1]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GGAL.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 250],
                    ["2022-10-03", 250],
                    ["2022-09-30", 234],
                    ["2022-09-29", 230.55],
                    ["2022-09-28", 233.4],
                    ["2022-09-27", 228.9],
                    ["2022-09-26", 242.35],
                    ["2022-09-23", 257.3],
                    ["2022-09-22", 269.5],
                    ["2022-09-21", 267.6],
                    ["2022-09-20", 268.3],
                    ["2022-09-19", 270.7],
                    ["2022-09-16", 259.2],
                    ["2022-09-15", 258],
                    ["2022-09-14", 256.1],
                    ["2022-09-13", 250.1],
                    ["2022-09-12", 259.6],
                    ["2022-09-09", 264.3],
                    ["2022-09-08", 252.5],
                    ["2022-09-07", 251.293376],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 250]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BPAT.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 108.5],
                    ["2022-10-03", 107.5],
                    ["2022-09-30", 105.5],
                    ["2022-09-29", 103],
                    ["2022-09-28", 103.5],
                    ["2022-09-27", 100.5],
                    ["2022-09-26", 107],
                    ["2022-09-23", 104.25],
                    ["2022-09-22", 108.25],
                    ["2022-09-21", 106],
                    ["2022-09-20", 108.5],
                    ["2022-09-19", 105],
                    ["2022-09-16", 108.816611],
                    ["2022-09-15", 106.332213],
                    ["2022-09-14", 109.31349],
                    ["2022-09-13", 104.344695],
                    ["2022-09-12", 109.31349],
                    ["2022-09-09", 107.822852],
                    ["2022-09-08", 108.319731],
                    ["2022-09-07", 108.319731],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 108.5]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "SUPV.BA"},
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
                "defaultPricingField": "OFF_CLOSE",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 116.6],
                    ["2022-10-03", 115],
                    ["2022-09-30", 105.55],
                    ["2022-09-29", 105.4],
                    ["2022-09-28", 107],
                    ["2022-09-27", 106.55],
                    ["2022-09-26", 107.6],
                    ["2022-09-23", 112],
                    ["2022-09-22", 113.1],
                    ["2022-09-21", 114],
                    ["2022-09-20", 113.5],
                    ["2022-09-19", 114],
                    ["2022-09-16", 113],
                    ["2022-09-15", 113.05],
                    ["2022-09-14", 113],
                    ["2022-09-13", 109.5],
                    ["2022-09-12", 110.5],
                    ["2022-09-09", 111.4],
                    ["2022-09-08", 108],
                    ["2022-09-07", 107],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 116.6]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_CHAINS_PRICING_FIELDS = [
    StubResponse(
        {
            "links": {"count": 30},
            "variability": "",
            "universe": [
                {
                    "Instrument": "GS.N",
                    "Company Common Name": "Goldman Sachs Group Inc",
                    "Organization PermID": "4295911963",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "NKE.N",
                    "Company Common Name": "Nike Inc",
                    "Organization PermID": "4295904620",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CSCO.OQ",
                    "Company Common Name": "Cisco Systems Inc",
                    "Organization PermID": "5080018615",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "JPM.N",
                    "Company Common Name": "JPMorgan Chase & Co",
                    "Organization PermID": "5000021791",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "DIS.N",
                    "Company Common Name": "Walt Disney Co",
                    "Organization PermID": "5064610769",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "INTC.OQ",
                    "Company Common Name": "Intel Corp",
                    "Organization PermID": "4295906830",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "DOW.N",
                    "Company Common Name": "Dow Inc",
                    "Organization PermID": "5000296881",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MRK.N",
                    "Company Common Name": "Merck & Co Inc",
                    "Organization PermID": "4295904886",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CVX.N",
                    "Company Common Name": "Chevron Corp",
                    "Organization PermID": "4295903744",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "AXP.N",
                    "Company Common Name": "American Express Co",
                    "Organization PermID": "4295903329",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "VZ.N",
                    "Company Common Name": "Verizon Communications Inc",
                    "Organization PermID": "4295911976",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "HD.N",
                    "Company Common Name": "Home Depot Inc",
                    "Organization PermID": "4295903148",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "WBA.OQ",
                    "Company Common Name": "Walgreens Boots Alliance Inc",
                    "Organization PermID": "5043951500",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MCD.N",
                    "Company Common Name": "McDonald's Corp",
                    "Organization PermID": "4295904499",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "UNH.N",
                    "Company Common Name": "UnitedHealth Group Inc",
                    "Organization PermID": "5046300101",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "KO.N",
                    "Company Common Name": "Coca-Cola Co",
                    "Organization PermID": "4295903091",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "JNJ.N",
                    "Company Common Name": "Johnson & Johnson",
                    "Organization PermID": "4295904341",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MSFT.OQ",
                    "Company Common Name": "Microsoft Corp",
                    "Organization PermID": "4295907168",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "HON.OQ",
                    "Company Common Name": "Honeywell International Inc",
                    "Organization PermID": "4295912155",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CRM.N",
                    "Company Common Name": "Salesforce Inc",
                    "Organization PermID": "4295915633",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "PG.N",
                    "Company Common Name": "Procter & Gamble Co",
                    "Organization PermID": "4295903247",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "IBM.N",
                    "Company Common Name": "International Business Machines Corp",
                    "Organization PermID": "4295904307",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MMM.N",
                    "Company Common Name": "3M Co",
                    "Organization PermID": "5000072036",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "AAPL.OQ",
                    "Company Common Name": "Apple Inc",
                    "Organization PermID": "4295905573",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "WMT.N",
                    "Company Common Name": "Walmart Inc",
                    "Organization PermID": "4295905298",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CAT.N",
                    "Company Common Name": "Caterpillar Inc",
                    "Organization PermID": "4295903678",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "AMGN.OQ",
                    "Company Common Name": "Amgen Inc",
                    "Organization PermID": "4295905537",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "V.N",
                    "Company Common Name": "Visa Inc",
                    "Organization PermID": "4298015179",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "TRV.N",
                    "Company Common Name": "Travelers Companies Inc",
                    "Organization PermID": "4295904877",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "BA.N",
                    "Company Common Name": "Boeing Co",
                    "Organization PermID": "4295903076",
                    "Reporting Currency": "USD",
                },
            ],
            "data": [
                ["GS.N", "1999-05-04T00:00:00", "GS.N"],
                ["NKE.N", "1990-10-19T00:00:00", "NKE.N"],
                ["CSCO.OQ", "2002-06-27T00:00:00", "CSCO.OQ"],
                ["JPM.N", "2001-01-02T00:00:00", "JPM.N"],
                ["DIS.N", "1990-03-23T00:00:00", "DIS.N"],
                ["INTC.OQ", "2002-06-27T00:00:00", "INTC.OQ"],
                ["DOW.N", "2019-04-02T00:00:00", "DOW.N"],
                ["MRK.N", "1990-03-23T00:00:00", "MRK.N"],
                ["CVX.N", "2001-10-10T00:00:00", "CVX.N"],
                ["AXP.N", "1990-03-23T00:00:00", "AXP.N"],
                ["VZ.N", "2000-07-01T00:00:00", "VZ.N"],
                ["HD.N", "1990-03-23T00:00:00", "HD.N"],
                ["WBA.OQ", "2014-12-31T00:00:00", "WBA.OQ"],
                ["MCD.N", "1990-03-23T00:00:00", "MCD.N"],
                ["UNH.N", "1991-10-09T00:00:00", "UNH.N"],
                ["KO.N", "1990-03-23T00:00:00", "KO.N"],
                ["JNJ.N", "1990-03-23T00:00:00", "JNJ.N"],
                ["MSFT.OQ", "2002-06-28T00:00:00", "MSFT.OQ"],
                ["HON.OQ", "2021-05-11T00:00:00", "HON.OQ"],
                ["CRM.N", "2004-06-21T00:00:00", "CRM.N"],
                ["PG.N", "1990-03-23T00:00:00", "PG.N"],
                ["IBM.N", "1990-03-23T00:00:00", "IBM.N"],
                ["MMM.N", "1990-03-23T00:00:00", "MMM.N"],
                ["AAPL.OQ", "2002-06-27T00:00:00", "AAPL.OQ"],
                ["WMT.N", "1990-03-23T00:00:00", "WMT.N"],
                ["CAT.N", "1990-03-23T00:00:00", "CAT.N"],
                ["AMGN.OQ", "2002-06-27T00:00:00", "AMGN.OQ"],
                ["V.N", "2007-12-26T00:00:00", "V.N"],
                ["TRV.N", "2007-02-27T00:00:00", "TRV.N"],
                ["BA.N", "1990-03-23T00:00:00", "BA.N"],
            ],
            "messages": {
                "codes": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                ],
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
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "RIC",
                    "title": "RIC",
                    "type": "string",
                    "description": "Refinitiv Identification Code consolidated with RICCode",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GS.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 315.04, 315.05],
                    ["2022-10-03", 299.07, 299.21],
                    ["2022-09-30", 293.11, 293.28],
                    ["2022-09-29", 296.11, 296.22],
                    ["2022-09-28", 300.71, 300.72],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 315.04, 315.05]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "NKE.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 88.66, 88.68],
                    ["2022-10-03", 85.39, 85.4],
                    ["2022-09-30", 83.11, 83.12],
                    ["2022-09-29", 95.49, 95.5],
                    ["2022-09-28", 98.66, 98.67],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 88.66, 88.68]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CSCO.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 41.82, 41.83],
                    ["2022-10-03", 41.28, 41.3],
                    ["2022-09-30", 40.01, 40.02],
                    ["2022-09-29", 40.58, 40.59],
                    ["2022-09-28", 41.32, 41.33],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 41.82, 41.83]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JPM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 112.79, 112.8],
                    ["2022-10-03", 107.72, 107.73],
                    ["2022-09-30", 104.61, 104.67],
                    ["2022-09-29", 106.17, 106.18],
                    ["2022-09-28", 108.04, 108.05],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 112.79, 112.8]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DIS.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 101.44, 101.47],
                    ["2022-10-03", 97.09, 97.1],
                    ["2022-09-30", 94.42, 94.49],
                    ["2022-09-29", 97.51, 97.52],
                    ["2022-09-28", 99.36, 99.4],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 101.44, 101.47]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "INTC.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 27.69, 27.7],
                    ["2022-10-03", 26.95, 26.96],
                    ["2022-09-30", 25.78, 25.79],
                    ["2022-09-29", 26.38, 26.39],
                    ["2022-09-28", 27.11, 27.12],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 27.69, 27.7]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DOW.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 46.62, 46.63],
                    ["2022-10-03", 45.28, 45.29],
                    ["2022-09-30", 43.91, 43.94],
                    ["2022-09-29", 44.16, 44.17],
                    ["2022-09-28", 45.05, 45.06],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 46.62, 46.63]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MRK.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 88.39, 88.4],
                    ["2022-10-03", 87.55, 87.59],
                    ["2022-09-30", 86.17, 86.21],
                    ["2022-09-29", 86.7, 86.71],
                    ["2022-09-28", 86.78, 86.79],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 88.39, 88.4]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CVX.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 157.55, 157.56],
                    ["2022-10-03", 151.64, 151.65],
                    ["2022-09-30", 143.79, 143.9],
                    ["2022-09-29", 144.87, 144.88],
                    ["2022-09-28", 145.62, 145.63],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 157.55, 157.56]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AXP.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 145.47, 145.51],
                    ["2022-10-03", 139.99, 140],
                    ["2022-09-30", 134.94, 135.02],
                    ["2022-09-29", 137.82, 137.87],
                    ["2022-09-28", 140.46, 140.49],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 145.47, 145.51]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VZ.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 39.81, 39.82],
                    ["2022-10-03", 39.17, 39.18],
                    ["2022-09-30", 37.99, 38.01],
                    ["2022-09-29", 38.67, 38.68],
                    ["2022-09-28", 39.35, 39.36],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 39.81, 39.82]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HD.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 289.75, 289.76],
                    ["2022-10-03", 283.69, 283.88],
                    ["2022-09-30", 276.38, 276.63],
                    ["2022-09-29", 278.09, 278.17],
                    ["2022-09-28", 282.19, 282.2],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 289.75, 289.76]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WBA.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 33.38, 33.39],
                    ["2022-10-03", 32.41, 32.43],
                    ["2022-09-30", 31.4, 31.42],
                    ["2022-09-29", 31.56, 31.57],
                    ["2022-09-28", 33.18, 33.19],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 33.38, 33.39]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MCD.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 238.5, 238.51],
                    ["2022-10-03", 235.26, 235.33],
                    ["2022-09-30", 230.84, 231],
                    ["2022-09-29", 234.33, 234.4],
                    ["2022-09-28", 236.89, 236.94],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 238.5, 238.51]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "UNH.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 522.84, 523.16],
                    ["2022-10-03", 515.09, 515.1],
                    ["2022-09-30", 505.76, 506.18],
                    ["2022-09-29", 509.35, 509.36],
                    ["2022-09-28", 513.45, 513.75],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 522.84, 523.16]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "KO.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 56.78, 56.8],
                    ["2022-10-03", 56.65, 56.66],
                    ["2022-09-30", 56.07, 56.08],
                    ["2022-09-29", 56.58, 56.59],
                    ["2022-09-28", 56.97, 56.98],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 56.78, 56.8]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JNJ.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 165.61, 165.63],
                    ["2022-10-03", 163.17, 163.22],
                    ["2022-09-30", 163.54, 163.64],
                    ["2022-09-29", 164.58, 164.65],
                    ["2022-09-28", 166.47, 166.53],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 165.61, 165.63]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 248.88, 248.9],
                    ["2022-10-03", 240.65, 240.67],
                    ["2022-09-30", 232.81, 232.84],
                    ["2022-09-29", 237.51, 237.54],
                    ["2022-09-28", 241.02, 241.03],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 248.88, 248.9]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HON.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 178.19, 178.29],
                    ["2022-10-03", 173.03, 173.04],
                    ["2022-09-30", 166.96, 166.99],
                    ["2022-09-29", 170.1, 170.14],
                    ["2022-09-28", 173.8, 173.83],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 178.19, 178.29]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CRM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 155.82, 155.85],
                    ["2022-10-03", 147.8, 147.85],
                    ["2022-09-30", 143.98, 144.02],
                    ["2022-09-29", 146.92, 146.95],
                    ["2022-09-28", 150.17, 150.18],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 155.82, 155.85]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "PG.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 130.18, 130.19],
                    ["2022-10-03", 128.5, 128.51],
                    ["2022-09-30", 126.35, 126.41],
                    ["2022-09-29", 128.73, 128.74],
                    ["2022-09-28", 131.93, 131.98],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 130.18, 130.19]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 125.47, 125.5],
                    ["2022-10-03", 121.51, 121.56],
                    ["2022-09-30", 118.83, 118.92],
                    ["2022-09-29", 121.68, 121.71],
                    ["2022-09-28", 122.71, 122.72],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 125.47, 125.5]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MMM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 115.58, 115.59],
                    ["2022-10-03", 113.18, 113.19],
                    ["2022-09-30", 110.57, 110.64],
                    ["2022-09-29", 112.26, 112.31],
                    ["2022-09-28", 114.25, 114.26],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 115.58, 115.59]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AAPL.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 146.16, 146.17],
                    ["2022-10-03", 142.43, 142.45],
                    ["2022-09-30", 138.08, 138.18],
                    ["2022-09-29", 142.59, 142.6],
                    ["2022-09-28", 149.79, 149.8],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 146.16, 146.17]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WMT.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 134.3, 134.31],
                    ["2022-10-03", 132.53, 132.54],
                    ["2022-09-30", 129.78, 129.89],
                    ["2022-09-29", 132.29, 132.34],
                    ["2022-09-28", 133.07, 133.11],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 134.3, 134.31]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CAT.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 179.76, 179.79],
                    ["2022-10-03", 171.4, 171.41],
                    ["2022-09-30", 164.1, 164.17],
                    ["2022-09-29", 166.06, 166.1],
                    ["2022-09-28", 167.69, 167.74],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 179.76, 179.79]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AMGN.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 233.04, 233.05],
                    ["2022-10-03", 230.43, 230.52],
                    ["2022-09-30", 225.41, 225.57],
                    ["2022-09-29", 228.43, 228.51],
                    ["2022-09-28", 230.91, 230.98],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 233.04, 233.05]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "V.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 185.7, 185.77],
                    ["2022-10-03", 181.59, 181.69],
                    ["2022-09-30", 177.74, 177.9],
                    ["2022-09-29", 180.07, 180.13],
                    ["2022-09-28", 179.1, 179.24],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 185.7, 185.77]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "TRV.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 161.46, 161.51],
                    ["2022-10-03", 157.04, 157.1],
                    ["2022-09-30", 153.23, 153.34],
                    ["2022-09-29", 154.68, 154.69],
                    ["2022-09-28", 152.98, 152.99],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 161.46, 161.51]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BA.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 133.49, 133.53],
                    ["2022-10-03", 125.99, 126.02],
                    ["2022-09-30", 121.21, 121.26],
                    ["2022-09-29", 125.39, 125.4],
                    ["2022-09-28", 133.36, 133.37],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 133.49, 133.53]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_CHAINS_ADC_PRICING_FIELDS = [
    StubResponse(
        {
            "links": {"count": 30},
            "variability": "",
            "universe": [
                {
                    "Instrument": "GS.N",
                    "Company Common Name": "Goldman Sachs Group Inc",
                    "Organization PermID": "4295911963",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "NKE.N",
                    "Company Common Name": "Nike Inc",
                    "Organization PermID": "4295904620",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CSCO.OQ",
                    "Company Common Name": "Cisco Systems Inc",
                    "Organization PermID": "5080018615",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "JPM.N",
                    "Company Common Name": "JPMorgan Chase & Co",
                    "Organization PermID": "5000021791",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "DIS.N",
                    "Company Common Name": "Walt Disney Co",
                    "Organization PermID": "5064610769",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "INTC.OQ",
                    "Company Common Name": "Intel Corp",
                    "Organization PermID": "4295906830",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "DOW.N",
                    "Company Common Name": "Dow Inc",
                    "Organization PermID": "5000296881",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MRK.N",
                    "Company Common Name": "Merck & Co Inc",
                    "Organization PermID": "4295904886",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CVX.N",
                    "Company Common Name": "Chevron Corp",
                    "Organization PermID": "4295903744",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "AXP.N",
                    "Company Common Name": "American Express Co",
                    "Organization PermID": "4295903329",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "VZ.N",
                    "Company Common Name": "Verizon Communications Inc",
                    "Organization PermID": "4295911976",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "HD.N",
                    "Company Common Name": "Home Depot Inc",
                    "Organization PermID": "4295903148",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "WBA.OQ",
                    "Company Common Name": "Walgreens Boots Alliance Inc",
                    "Organization PermID": "5043951500",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MCD.N",
                    "Company Common Name": "McDonald's Corp",
                    "Organization PermID": "4295904499",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "UNH.N",
                    "Company Common Name": "UnitedHealth Group Inc",
                    "Organization PermID": "5046300101",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "KO.N",
                    "Company Common Name": "Coca-Cola Co",
                    "Organization PermID": "4295903091",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "JNJ.N",
                    "Company Common Name": "Johnson & Johnson",
                    "Organization PermID": "4295904341",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MSFT.OQ",
                    "Company Common Name": "Microsoft Corp",
                    "Organization PermID": "4295907168",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "HON.OQ",
                    "Company Common Name": "Honeywell International Inc",
                    "Organization PermID": "4295912155",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CRM.N",
                    "Company Common Name": "Salesforce Inc",
                    "Organization PermID": "4295915633",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "PG.N",
                    "Company Common Name": "Procter & Gamble Co",
                    "Organization PermID": "4295903247",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "IBM.N",
                    "Company Common Name": "International Business Machines Corp",
                    "Organization PermID": "4295904307",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "MMM.N",
                    "Company Common Name": "3M Co",
                    "Organization PermID": "5000072036",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "AAPL.OQ",
                    "Company Common Name": "Apple Inc",
                    "Organization PermID": "4295905573",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "WMT.N",
                    "Company Common Name": "Walmart Inc",
                    "Organization PermID": "4295905298",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "CAT.N",
                    "Company Common Name": "Caterpillar Inc",
                    "Organization PermID": "4295903678",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "AMGN.OQ",
                    "Company Common Name": "Amgen Inc",
                    "Organization PermID": "4295905537",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "V.N",
                    "Company Common Name": "Visa Inc",
                    "Organization PermID": "4298015179",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "TRV.N",
                    "Company Common Name": "Travelers Companies Inc",
                    "Organization PermID": "4295904877",
                    "Reporting Currency": "USD",
                },
                {
                    "Instrument": "BA.N",
                    "Company Common Name": "Boeing Co",
                    "Organization PermID": "4295903076",
                    "Reporting Currency": "USD",
                },
            ],
            "data": [
                ["GS.N", "2021-12-31T00:00:00", 64989000000],
                ["NKE.N", "2022-05-31T00:00:00", 46710000000],
                ["CSCO.OQ", "2022-07-30T00:00:00", 51557000000],
                ["JPM.N", None, None],
                ["DIS.N", "2021-10-02T00:00:00", 67418000000],
                ["INTC.OQ", "2021-12-25T00:00:00", 79024000000],
                ["DOW.N", "2021-12-31T00:00:00", 54968000000],
                ["MRK.N", "2021-12-31T00:00:00", 48704000000],
                ["CVX.N", "2021-12-31T00:00:00", 155606000000],
                ["AXP.N", "2021-12-31T00:00:00", 42838000000],
                ["VZ.N", "2021-12-31T00:00:00", 133613000000],
                ["HD.N", "2022-01-30T00:00:00", 151157000000],
                ["WBA.OQ", "2021-08-31T00:00:00", 132509000000],
                ["MCD.N", "2021-12-31T00:00:00", 23222900000],
                ["UNH.N", None, None],
                ["KO.N", "2021-12-31T00:00:00", 38655000000],
                ["JNJ.N", "2022-01-02T00:00:00", 93775000000],
                ["MSFT.OQ", "2022-06-30T00:00:00", 198270000000],
                ["HON.OQ", "2021-12-31T00:00:00", 34392000000],
                ["CRM.N", "2022-01-31T00:00:00", 26492000000],
                ["PG.N", "2022-06-30T00:00:00", 80187000000],
                ["IBM.N", "2021-12-31T00:00:00", 57350000000],
                ["MMM.N", "2021-12-31T00:00:00", 35355000000],
                ["AAPL.OQ", "2021-09-25T00:00:00", 365817000000],
                ["WMT.N", "2022-01-31T00:00:00", 572754000000],
                ["CAT.N", "2021-12-31T00:00:00", 50971000000],
                ["AMGN.OQ", "2021-12-31T00:00:00", 25979000000],
                ["V.N", "2021-09-30T00:00:00", 24105000000],
                ["TRV.N", None, None],
                ["BA.N", "2021-12-31T00:00:00", 62286000000],
            ],
            "messages": {
                "codes": [
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -2, -2],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -2, -2],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -2, -2],
                    [-1, -1, -1],
                ],
                "descriptions": [
                    {"code": -2, "description": "empty"},
                    {"code": -1, "description": "ok"},
                ],
            },
            "headers": [
                {
                    "name": "instrument",
                    "title": "Instrument",
                    "type": "string",
                    "description": "The requested Instrument as defined by the user.",
                },
                {
                    "name": "date",
                    "title": "Date",
                    "type": "datetime",
                    "description": "Date associated with the returned data.",
                },
                {
                    "name": "TR.Revenue",
                    "title": "Revenue",
                    "type": "number",
                    "decimalChar": ".",
                    "description": "Is used for industrial and utility companies. It consists of revenue from the sale of merchandise, manufactured goods and services, and the distribution of regulated energy resources, depending on a specific company's industry.",
                },
            ],
        }
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "GS.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 315.04, 315.05],
                    ["2022-10-03", 299.07, 299.21],
                    ["2022-09-30", 293.11, 293.28],
                    ["2022-09-29", 296.11, 296.22],
                    ["2022-09-28", 300.71, 300.72],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 315.04, 315.05]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "NKE.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 88.66, 88.68],
                    ["2022-10-03", 85.39, 85.4],
                    ["2022-09-30", 83.11, 83.12],
                    ["2022-09-29", 95.49, 95.5],
                    ["2022-09-28", 98.66, 98.67],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 88.66, 88.68]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CSCO.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 41.82, 41.83],
                    ["2022-10-03", 41.28, 41.3],
                    ["2022-09-30", 40.01, 40.02],
                    ["2022-09-29", 40.58, 40.59],
                    ["2022-09-28", 41.32, 41.33],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 41.82, 41.83]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JPM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 112.79, 112.8],
                    ["2022-10-03", 107.72, 107.73],
                    ["2022-09-30", 104.61, 104.67],
                    ["2022-09-29", 106.17, 106.18],
                    ["2022-09-28", 108.04, 108.05],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 112.79, 112.8]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DIS.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 101.44, 101.47],
                    ["2022-10-03", 97.09, 97.1],
                    ["2022-09-30", 94.42, 94.49],
                    ["2022-09-29", 97.51, 97.52],
                    ["2022-09-28", 99.36, 99.4],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 101.44, 101.47]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "INTC.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 27.69, 27.7],
                    ["2022-10-03", 26.95, 26.96],
                    ["2022-09-30", 25.78, 25.79],
                    ["2022-09-29", 26.38, 26.39],
                    ["2022-09-28", 27.11, 27.12],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 27.69, 27.7]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "DOW.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 46.62, 46.63],
                    ["2022-10-03", 45.28, 45.29],
                    ["2022-09-30", 43.91, 43.94],
                    ["2022-09-29", 44.16, 44.17],
                    ["2022-09-28", 45.05, 45.06],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 46.62, 46.63]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MRK.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 88.39, 88.4],
                    ["2022-10-03", 87.55, 87.59],
                    ["2022-09-30", 86.17, 86.21],
                    ["2022-09-29", 86.7, 86.71],
                    ["2022-09-28", 86.78, 86.79],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 88.39, 88.4]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CVX.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 157.55, 157.56],
                    ["2022-10-03", 151.64, 151.65],
                    ["2022-09-30", 143.79, 143.9],
                    ["2022-09-29", 144.87, 144.88],
                    ["2022-09-28", 145.62, 145.63],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 157.55, 157.56]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AXP.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 145.47, 145.51],
                    ["2022-10-03", 139.99, 140],
                    ["2022-09-30", 134.94, 135.02],
                    ["2022-09-29", 137.82, 137.87],
                    ["2022-09-28", 140.46, 140.49],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 145.47, 145.51]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "VZ.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 39.81, 39.82],
                    ["2022-10-03", 39.17, 39.18],
                    ["2022-09-30", 37.99, 38.01],
                    ["2022-09-29", 38.67, 38.68],
                    ["2022-09-28", 39.35, 39.36],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 39.81, 39.82]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HD.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 289.75, 289.76],
                    ["2022-10-03", 283.69, 283.88],
                    ["2022-09-30", 276.38, 276.63],
                    ["2022-09-29", 278.09, 278.17],
                    ["2022-09-28", 282.19, 282.2],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 289.75, 289.76]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WBA.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 33.38, 33.39],
                    ["2022-10-03", 32.41, 32.43],
                    ["2022-09-30", 31.4, 31.42],
                    ["2022-09-29", 31.56, 31.57],
                    ["2022-09-28", 33.18, 33.19],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 33.38, 33.39]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MCD.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 238.5, 238.51],
                    ["2022-10-03", 235.26, 235.33],
                    ["2022-09-30", 230.84, 231],
                    ["2022-09-29", 234.33, 234.4],
                    ["2022-09-28", 236.89, 236.94],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 238.5, 238.51]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "UNH.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 522.84, 523.16],
                    ["2022-10-03", 515.09, 515.1],
                    ["2022-09-30", 505.76, 506.18],
                    ["2022-09-29", 509.35, 509.36],
                    ["2022-09-28", 513.45, 513.75],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 522.84, 523.16]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "KO.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 56.78, 56.8],
                    ["2022-10-03", 56.65, 56.66],
                    ["2022-09-30", 56.07, 56.08],
                    ["2022-09-29", 56.58, 56.59],
                    ["2022-09-28", 56.97, 56.98],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 56.78, 56.8]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "JNJ.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 165.61, 165.63],
                    ["2022-10-03", 163.17, 163.22],
                    ["2022-09-30", 163.54, 163.64],
                    ["2022-09-29", 164.58, 164.65],
                    ["2022-09-28", 166.47, 166.53],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 165.61, 165.63]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MSFT.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 248.88, 248.9],
                    ["2022-10-03", 240.65, 240.67],
                    ["2022-09-30", 232.81, 232.84],
                    ["2022-09-29", 237.51, 237.54],
                    ["2022-09-28", 241.02, 241.03],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 248.88, 248.9]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "HON.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 178.19, 178.29],
                    ["2022-10-03", 173.03, 173.04],
                    ["2022-09-30", 166.96, 166.99],
                    ["2022-09-29", 170.1, 170.14],
                    ["2022-09-28", 173.8, 173.83],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 178.19, 178.29]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CRM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 155.82, 155.85],
                    ["2022-10-03", 147.8, 147.85],
                    ["2022-09-30", 143.98, 144.02],
                    ["2022-09-29", 146.92, 146.95],
                    ["2022-09-28", 150.17, 150.18],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 155.82, 155.85]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "PG.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 130.18, 130.19],
                    ["2022-10-03", 128.5, 128.51],
                    ["2022-09-30", 126.35, 126.41],
                    ["2022-09-29", 128.73, 128.74],
                    ["2022-09-28", 131.93, 131.98],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 130.18, 130.19]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "IBM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 125.47, 125.5],
                    ["2022-10-03", 121.51, 121.56],
                    ["2022-09-30", 118.83, 118.92],
                    ["2022-09-29", 121.68, 121.71],
                    ["2022-09-28", 122.71, 122.72],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 125.47, 125.5]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "MMM.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 115.58, 115.59],
                    ["2022-10-03", 113.18, 113.19],
                    ["2022-09-30", 110.57, 110.64],
                    ["2022-09-29", 112.26, 112.31],
                    ["2022-09-28", 114.25, 114.26],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 115.58, 115.59]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AAPL.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 146.16, 146.17],
                    ["2022-10-03", 142.43, 142.45],
                    ["2022-09-30", 138.08, 138.18],
                    ["2022-09-29", 142.59, 142.6],
                    ["2022-09-28", 149.79, 149.8],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 146.16, 146.17]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "WMT.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 134.3, 134.31],
                    ["2022-10-03", 132.53, 132.54],
                    ["2022-09-30", 129.78, 129.89],
                    ["2022-09-29", 132.29, 132.34],
                    ["2022-09-28", 133.07, 133.11],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 134.3, 134.31]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "CAT.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 179.76, 179.79],
                    ["2022-10-03", 171.4, 171.41],
                    ["2022-09-30", 164.1, 164.17],
                    ["2022-09-29", 166.06, 166.1],
                    ["2022-09-28", 167.69, 167.74],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 179.76, 179.79]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "AMGN.OQ"},
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
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 233.04, 233.05],
                    ["2022-10-03", 230.43, 230.52],
                    ["2022-09-30", 225.41, 225.57],
                    ["2022-09-29", 228.43, 228.51],
                    ["2022-09-28", 230.91, 230.98],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 233.04, 233.05]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "V.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 185.7, 185.77],
                    ["2022-10-03", 181.59, 181.69],
                    ["2022-09-30", 177.74, 177.9],
                    ["2022-09-29", 180.07, 180.13],
                    ["2022-09-28", 179.1, 179.24],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 185.7, 185.77]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "TRV.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 161.46, 161.51],
                    ["2022-10-03", 157.04, 157.1],
                    ["2022-09-30", 153.23, 153.34],
                    ["2022-09-29", 154.68, 154.69],
                    ["2022-09-28", 152.98, 152.99],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 161.46, 161.51]],
                    }
                },
            }
        ]
    ),
    StubResponse(
        [
            {
                "universe": {"ric": "BA.N"},
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
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
                "headers": [
                    {"name": "DATE", "type": "string"},
                    {"name": "BID", "type": "number", "decimalChar": "."},
                    {"name": "ASK", "type": "number", "decimalChar": "."},
                ],
                "data": [
                    ["2022-10-04", 133.49, 133.53],
                    ["2022-10-03", 125.99, 126.02],
                    ["2022-09-30", 121.21, 121.26],
                    ["2022-09-29", 125.39, 125.4],
                    ["2022-09-28", 133.36, 133.37],
                ],
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-10-04", 133.49, 133.53]],
                    }
                },
            }
        ]
    ),
]

RDP_GET_HISTORY_MERGE_DUPLICATE_ROWS_WITHOUT_ONE_ITEM = [
    StubResponse(
        {
            "links": {"count": 48},
            "variability": "",
            "universe": [{
                "Instrument": "D-PCAQE00",
                "Company Common Name": "Failed to resolve identifier(s).",
                "Organization PermID": "Failed to resolve identifier(s).",
                "Reporting Currency": "Failed to resolve identifier(s)."
            }, {
                "Instrument": "D-WTMYA00",
                "Company Common Name": "Failed to resolve identifier(s).",
                "Organization PermID": "Failed to resolve identifier(s).",
                "Reporting Currency": "Failed to resolve identifier(s)."
            }, {
                "Instrument": "D-AAYAN00",
                "Company Common Name": "Failed to resolve identifier(s).",
                "Organization PermID": "Failed to resolve identifier(s).",
                "Reporting Currency": "Failed to resolve identifier(s)."
            }, {
                "Instrument": "D-AALVZ00",
                "Company Common Name": "Failed to resolve identifier(s).",
                "Organization PermID": "Failed to resolve identifier(s).",
                "Reporting Currency": "Failed to resolve identifier(s)."
            }],
            "data": [["D-PCAQE00", "2022-11-01T00:00:00", 96.92],
                     ["D-PCAQE00", "2022-11-02T00:00:00", 96.79],
                     ["D-PCAQE00", "2022-11-03T00:00:00", 96.23],
                     ["D-PCAQE00", "2022-11-04T00:00:00", 98.43],
                     ["D-PCAQE00", "2022-11-07T00:00:00", 99.38],
                     ["D-PCAQE00", "2022-11-08T00:00:00", 99],
                     ["D-PCAQE00", "2022-11-09T00:00:00", 96.67],
                     ["D-PCAQE00", "2022-11-10T00:00:00", 94.12],
                     ["D-PCAQE00", "2022-11-11T00:00:00", 97.77],
                     ["D-PCAQE00", "2022-11-14T00:00:00", 97.97],
                     ["D-PCAQE00", "2022-11-15T00:00:00", 94.17],
                     ["D-PCAQE00", "2022-11-15T00:00:00", 94.17],
                     ["D-WTMYA00", "2022-11-01T00:00:00", 96.91],
                     ["D-WTMYA00", "2022-11-02T00:00:00", 98.15],
                     ["D-WTMYA00", "2022-11-03T00:00:00", 98.14],
                     ["D-WTMYA00", "2022-11-04T00:00:00", 99.99],
                     ["D-WTMYA00", "2022-11-07T00:00:00", 101.06],
                     ["D-WTMYA00", "2022-11-08T00:00:00", 101.14],
                     ["D-WTMYA00", "2022-11-09T00:00:00", 98.22],
                     ["D-WTMYA00", "2022-11-10T00:00:00", 95.21],
                     ["D-WTMYA00", "2022-11-11T00:00:00", 98.33],
                     ["D-WTMYA00", "2022-11-14T00:00:00", 98.63],
                     ["D-WTMYA00", "2022-11-15T00:00:00", 95],
                     ["D-WTMYA00", "2022-11-15T00:00:00", 95],
                     ["D-AAYAN00", "2022-11-01T00:00:00", 89.43],
                     ["D-AAYAN00", "2022-11-02T00:00:00", 90.18],
                     ["D-AAYAN00", "2022-11-03T00:00:00", 90.22],
                     ["D-AAYAN00", "2022-11-04T00:00:00", 91.85],
                     ["D-AAYAN00", "2022-11-07T00:00:00", 92.96],
                     ["D-AAYAN00", "2022-11-08T00:00:00", 93.31],
                     ["D-AAYAN00", "2022-11-09T00:00:00", 90.81],
                     ["D-AAYAN00", "2022-11-10T00:00:00", 88.49],
                     ["D-AAYAN00", "2022-11-11T00:00:00", 91.5],
                     ["D-AAYAN00", "2022-11-14T00:00:00", 91.82],
                     ["D-AAYAN00", "2022-11-15T00:00:00", 89.46],
                     ["D-AAYAN00", "2022-11-15T00:00:00", 89.46],
                     ["D-AALVZ00", "2022-11-01T00:00:00", -6.825],
                     ["D-AALVZ00", "2022-11-02T00:00:00", -6.675],
                     ["D-AALVZ00", "2022-11-03T00:00:00", -6.625],
                     ["D-AALVZ00", "2022-11-04T00:00:00", -6.795],
                     ["D-AALVZ00", "2022-11-07T00:00:00", -7.3],
                     ["D-AALVZ00", "2022-11-08T00:00:00", -7.38],
                     ["D-AALVZ00", "2022-11-09T00:00:00", -7.555],
                     ["D-AALVZ00", "2022-11-10T00:00:00", -7.755],
                     ["D-AALVZ00", "2022-11-11T00:00:00", -7.995],
                     ["D-AALVZ00", "2022-11-14T00:00:00", -8.045],
                     ["D-AALVZ00", "2022-11-15T00:00:00", -8.305]],
            "messages": {
                "codes": [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}]
            },
            "headers": [{
                "name": "instrument",
                "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user."
            }, {
                "name": "date",
                "title": "Date",
                "type": "datetime",
                "description": "Date associated with the returned data."
            }, {
                "name": "TR.CLOSEPRICE",
                "title": "Close Price",
                "type": "number",
                "decimalChar": ".",
                "description": "Last trade price or value."
            }]
        }
    )
]

RDP_GET_HISTORY_MERGE_DUPLICATE_ROWS = [
    StubResponse(
        {
            "links": {"count": 48},
            "variability": "",
            "universe": [{
                             "Instrument": "D-PCAQE00",
                             "Company Common Name": "Failed to resolve identifier(s).",
                             "Organization PermID": "Failed to resolve identifier(s).",
                             "Reporting Currency": "Failed to resolve identifier(s)."
                         }, {
                             "Instrument": "D-WTMYA00",
                             "Company Common Name": "Failed to resolve identifier(s).",
                             "Organization PermID": "Failed to resolve identifier(s).",
                             "Reporting Currency": "Failed to resolve identifier(s)."
                         }, {
                             "Instrument": "D-AAYAN00",
                             "Company Common Name": "Failed to resolve identifier(s).",
                             "Organization PermID": "Failed to resolve identifier(s).",
                             "Reporting Currency": "Failed to resolve identifier(s)."
                         }, {
                             "Instrument": "D-AALVZ00",
                             "Company Common Name": "Failed to resolve identifier(s).",
                             "Organization PermID": "Failed to resolve identifier(s).",
                             "Reporting Currency": "Failed to resolve identifier(s)."
                         }],
            "data": [["D-PCAQE00", "2022-11-01T00:00:00", 96.92],
                     ["D-PCAQE00", "2022-11-02T00:00:00", 96.79],
                     ["D-PCAQE00", "2022-11-03T00:00:00", 96.23],
                     ["D-PCAQE00", "2022-11-04T00:00:00", 98.43],
                     ["D-PCAQE00", "2022-11-07T00:00:00", 99.38],
                     ["D-PCAQE00", "2022-11-08T00:00:00", 99],
                     ["D-PCAQE00", "2022-11-09T00:00:00", 96.67],
                     ["D-PCAQE00", "2022-11-10T00:00:00", 94.12],
                     ["D-PCAQE00", "2022-11-11T00:00:00", 97.77],
                     ["D-PCAQE00", "2022-11-14T00:00:00", 97.97],
                     ["D-PCAQE00", "2022-11-15T00:00:00", 94.17],
                     ["D-PCAQE00", "2022-11-15T00:00:00", 94.17],
                     ["D-WTMYA00", "2022-11-01T00:00:00", 96.91],
                     ["D-WTMYA00", "2022-11-02T00:00:00", 98.15],
                     ["D-WTMYA00", "2022-11-03T00:00:00", 98.14],
                     ["D-WTMYA00", "2022-11-04T00:00:00", 99.99],
                     ["D-WTMYA00", "2022-11-07T00:00:00", 101.06],
                     ["D-WTMYA00", "2022-11-08T00:00:00", 101.14],
                     ["D-WTMYA00", "2022-11-09T00:00:00", 98.22],
                     ["D-WTMYA00", "2022-11-10T00:00:00", 95.21],
                     ["D-WTMYA00", "2022-11-11T00:00:00", 98.33],
                     ["D-WTMYA00", "2022-11-14T00:00:00", 98.63],
                     ["D-WTMYA00", "2022-11-15T00:00:00", 95],
                     ["D-WTMYA00", "2022-11-15T00:00:00", 95],
                     ["D-AAYAN00", "2022-11-01T00:00:00", 89.43],
                     ["D-AAYAN00", "2022-11-02T00:00:00", 90.18],
                     ["D-AAYAN00", "2022-11-03T00:00:00", 90.22],
                     ["D-AAYAN00", "2022-11-04T00:00:00", 91.85],
                     ["D-AAYAN00", "2022-11-07T00:00:00", 92.96],
                     ["D-AAYAN00", "2022-11-08T00:00:00", 93.31],
                     ["D-AAYAN00", "2022-11-09T00:00:00", 90.81],
                     ["D-AAYAN00", "2022-11-10T00:00:00", 88.49],
                     ["D-AAYAN00", "2022-11-11T00:00:00", 91.5],
                     ["D-AAYAN00", "2022-11-14T00:00:00", 91.82],
                     ["D-AAYAN00", "2022-11-15T00:00:00", 89.46],
                     ["D-AAYAN00", "2022-11-15T00:00:00", 89.46],
                     ["D-AALVZ00", "2022-11-01T00:00:00", -6.825],
                     ["D-AALVZ00", "2022-11-02T00:00:00", -6.675],
                     ["D-AALVZ00", "2022-11-03T00:00:00", -6.625],
                     ["D-AALVZ00", "2022-11-04T00:00:00", -6.795],
                     ["D-AALVZ00", "2022-11-07T00:00:00", -7.3],
                     ["D-AALVZ00", "2022-11-08T00:00:00", -7.38],
                     ["D-AALVZ00", "2022-11-09T00:00:00", -7.555],
                     ["D-AALVZ00", "2022-11-10T00:00:00", -7.755],
                     ["D-AALVZ00", "2022-11-11T00:00:00", -7.995],
                     ["D-AALVZ00", "2022-11-14T00:00:00", -8.045],
                     ["D-AALVZ00", "2022-11-15T00:00:00", -8.305],
                     ["D-AALVZ00", "2022-11-15T00:00:00", -8.305]],
            "messages": {
                "codes": [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1],
                          [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}]
            },
            "headers": [{
                            "name": "instrument",
                            "title": "Instrument",
                            "type": "string",
                            "description": "The requested Instrument as defined by the user."
                        }, {
                            "name": "date",
                            "title": "Date",
                            "type": "datetime",
                            "description": "Date associated with the returned data."
                        }, {
                            "name": "TR.CLOSEPRICE",
                            "title": "Close Price",
                            "type": "number",
                            "decimalChar": ".",
                            "description": "Last trade price or value."
                        }]
        }
    )
]

UDF_GET_HISTORY_MANAGE_RICS_WITH_SPECIAL_CHARACTERS = [
    StubResponse(
        [{
             "universe": {"ric": "aUSCXTRF/C"},
             "interval": "P1M",
             "summaryTimestampLabel": "endPeriod",
             "defaultPricingField": "VALUE",
             "headers": [{"name": "DATE", "type": "string"},
                         {"name": "VALUE", "type": "number", "decimalChar": "."}],
             "data": [["2022-10-31", 133.97489061298486],
                      ["2022-09-30", 132.11978301463336],
                      ["2022-08-31", 128.91516585794412],
                      ["2022-07-31", 129.47131268915072],
                      ["2022-06-30", 127.43074939500677],
                      ["2022-05-31", 126.22066199276954],
                      ["2022-04-30", 123.16416711092643],
                      ["2022-03-31", 122.53071036377784],
                      ["2022-02-28", 121.01556816501738],
                      ["2022-01-31", 120.80291083213423],
                      ["2021-12-31", 121.4223813124386],
                      ["2021-11-30", 120.21405595956757],
                      ["2021-10-31", 119.05826170342635],
                      ["2021-09-30", 118.07294572346488],
                      ["2021-08-31", 117.86469351399724],
                      ["2021-07-31", 117.46647035723623],
                      ["2021-06-30", 115.87853349403468],
                      ["2021-05-31", 114.80192133128703],
                      ["2021-04-30", 115.83723546201439],
                      ["2021-03-31", 116.17654009309311]]
         }]
        ),
    StubResponse(
        [{
             "universe": {"ric": "aUSCXTWF/C"},
             "interval": "P1M",
             "summaryTimestampLabel": "endPeriod",
             "defaultPricingField": "VALUE",
             "headers": [{"name": "DATE", "type": "string"},
                         {"name": "VALUE", "type": "number", "decimalChar": "."}],
             "data": [["2022-10-31", 136.97304459096443],
                      ["2022-09-30", 134.97232570112573],
                      ["2022-08-31", 130.5227934882566],
                      ["2022-07-31", 130.69894554807212],
                      ["2022-06-30", 127.53475728773186],
                      ["2022-05-31", 127.02084170049451],
                      ["2022-04-30", 123.98441085719752],
                      ["2022-03-31", 121.75304043598098],
                      ["2022-02-28", 119.683503476145],
                      ["2022-01-31", 119.46794752141176],
                      ["2021-12-31", 120.1005187809508],
                      ["2021-11-30", 118.79819230469681],
                      ["2021-10-31", 117.32326566901432],
                      ["2021-09-30", 116.88582693698355],
                      ["2021-08-31", 116.53996063680394],
                      ["2021-07-31", 116.15968530162571],
                      ["2021-06-30", 114.10801884061162],
                      ["2021-05-31", 113.22226368161505],
                      ["2021-04-30", 115.23008637222769],
                      ["2021-03-31", 115.67174298596795]]
         }]
        ),
    StubResponse(
        [{
             "universe": {"ric": "USPMI=ECI"},
             "interval": "P1M",
             "summaryTimestampLabel": "endPeriod",
             "defaultPricingField": "VALUE",
             "headers": [{"name": "DATE", "type": "string"},
                         {"name": "VALUE", "type": "number", "decimalChar": "."}],
             "data": [["2022-10-31", 50.2], ["2022-09-30", 50.9], ["2022-08-31", 52.8],
                      ["2022-07-31", 52.8], ["2022-06-30", 53], ["2022-05-31", 56.1],
                      ["2022-04-30", 55.4], ["2022-03-31", 57.1], ["2022-02-28", 58.6],
                      ["2022-01-31", 57.6], ["2021-12-31", 58.8], ["2021-11-30", 60.6],
                      ["2021-10-31", 60.8], ["2021-09-30", 60.5], ["2021-08-31", 59.7],
                      ["2021-07-31", 59.9], ["2021-06-30", 60.9], ["2021-05-31", 61.6],
                      ["2021-04-30", 60.6], ["2021-03-31", 63.7]]
         }]
        ),
]

RDP_GET_HISTORY_MANAGE_RICS_WITH_SPECIAL_CHARACTERS = [
    StubResponse(
        [{
             "universe": {"ric": "aUSCXTRF/C"},
             "interval": "P1M",
             "summaryTimestampLabel": "endPeriod",
             "defaultPricingField": "VALUE",
             "headers": [{"name": "DATE", "type": "string"},
                         {"name": "VALUE", "type": "number", "decimalChar": "."}],
             "data": [["2022-10-31", 133.97489061298486],
                      ["2022-09-30", 132.11978301463336],
                      ["2022-08-31", 128.91516585794412],
                      ["2022-07-31", 129.47131268915072],
                      ["2022-06-30", 127.43074939500677],
                      ["2022-05-31", 126.22066199276954],
                      ["2022-04-30", 123.16416711092643],
                      ["2022-03-31", 122.53071036377784],
                      ["2022-02-28", 121.01556816501738],
                      ["2022-01-31", 120.80291083213423],
                      ["2021-12-31", 121.4223813124386],
                      ["2021-11-30", 120.21405595956757],
                      ["2021-10-31", 119.05826170342635],
                      ["2021-09-30", 118.07294572346488],
                      ["2021-08-31", 117.86469351399724],
                      ["2021-07-31", 117.46647035723623],
                      ["2021-06-30", 115.87853349403468],
                      ["2021-05-31", 114.80192133128703],
                      ["2021-04-30", 115.83723546201439],
                      ["2021-03-31", 116.17654009309311]]
         }]
        ),
    StubResponse(
        [{
             "universe": {"ric": "aUSCXTWF/C"},
             "interval": "P1M",
             "summaryTimestampLabel": "endPeriod",
             "defaultPricingField": "VALUE",
             "headers": [{"name": "DATE", "type": "string"},
                         {"name": "VALUE", "type": "number", "decimalChar": "."}],
             "data": [["2022-10-31", 136.97304459096443],
                      ["2022-09-30", 134.97232570112573],
                      ["2022-08-31", 130.5227934882566],
                      ["2022-07-31", 130.69894554807212],
                      ["2022-06-30", 127.53475728773186],
                      ["2022-05-31", 127.02084170049451],
                      ["2022-04-30", 123.98441085719752],
                      ["2022-03-31", 121.75304043598098],
                      ["2022-02-28", 119.683503476145],
                      ["2022-01-31", 119.46794752141176],
                      ["2021-12-31", 120.1005187809508],
                      ["2021-11-30", 118.79819230469681],
                      ["2021-10-31", 117.32326566901432],
                      ["2021-09-30", 116.88582693698355],
                      ["2021-08-31", 116.53996063680394],
                      ["2021-07-31", 116.15968530162571],
                      ["2021-06-30", 114.10801884061162],
                      ["2021-05-31", 113.22226368161505],
                      ["2021-04-30", 115.23008637222769],
                      ["2021-03-31", 115.67174298596795]]
         }]
        ),
    StubResponse(
        [{
             "universe": {"ric": "USPMI=ECI"},
             "interval": "P1M",
             "summaryTimestampLabel": "endPeriod",
             "defaultPricingField": "VALUE",
             "headers": [{"name": "DATE", "type": "string"},
                         {"name": "VALUE", "type": "number", "decimalChar": "."}],
             "data": [["2022-10-31", 50.2], ["2022-09-30", 50.9], ["2022-08-31", 52.8],
                      ["2022-07-31", 52.8], ["2022-06-30", 53], ["2022-05-31", 56.1],
                      ["2022-04-30", 55.4], ["2022-03-31", 57.1], ["2022-02-28", 58.6],
                      ["2022-01-31", 57.6], ["2021-12-31", 58.8], ["2021-11-30", 60.6],
                      ["2021-10-31", 60.8], ["2021-09-30", 60.5], ["2021-08-31", 59.7],
                      ["2021-07-31", 59.9], ["2021-06-30", 60.9], ["2021-05-31", 61.6],
                      ["2021-04-30", 60.6], ["2021-03-31", 63.7]]
         }]
        ),
]

RDP_GET_HISTORY_MISSED_DATA = [
    StubResponse(
        {
            "links": {"count": 2},
            "variability": "",
            "universe": [{
                             "Instrument": "USPMI=ECI",
                             "Company Common Name": "Failed to resolve identifier(s).",
                             "Organization PermID": "Failed to resolve identifier(s).",
                             "Reporting Currency": "Failed to resolve identifier(s)."
                         }, {
                             "Instrument": "D-PCAQE00",
                             "Company Common Name": "Failed to resolve identifier(s).",
                             "Organization PermID": "Failed to resolve identifier(s).",
                             "Reporting Currency": "Failed to resolve identifier(s)."
                         }],
            "data": [["USPMI=ECI", None, None], ["D-PCAQE00", None, None]],
            "messages": {
                "codes": [[-1, -2, -2], [-1, -2, 416]],
                "descriptions": [{"code": -2, "description": "empty"},
                                 {"code": -1, "description": "ok"}, {
                                     "code": 416,
                                     "description": "Unable to collect data for the "
                                                    "field 'TR.CLOSEPRICE' and some "
                                                    "specific identifier(s)."
                                 }]
            },
            "headers": [{
                            "name": "instrument",
                            "title": "Instrument",
                            "type": "string",
                            "description": "The requested Instrument as defined by the user."
                        }, {
                            "name": "date",
                            "title": "Date",
                            "type": "datetime",
                            "description": "Date associated with the returned data."
                        }, {
                            "name": "TR.CLOSEPRICE",
                            "title": "Close Price",
                            "type": "number",
                            "decimalChar": ".",
                            "description": "Last trade price or value."
                        }]
        }
        ),
    StubResponse(
        [{
             "universe": {"ric": "USPMI=ECI"},
             "status": {
                 "code": "TSCC.Economics.UserRequestError.96103",
                 "message": "The request interval (P1D) must be greater than or equal to the native interval (P1M)."
             }
         }]
        ),
    StubResponse(
        [{
             "universe": {"ric": "D-PCAQE00"},
             "status": {
                 "code": "TSCC.QS.UserNotPermission.92000",
                 "message": "User has no permission."
             }
         }]
        ),
]

HP_ONE_UNIVERSE_TWO_FIELDS = StubResponse(
    [
        {
            "universe": {"ric": "EUR="},
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
                {"name": "ASK", "type": "number", "decimalChar": "."},
            ],
            "data": [
                ["2022-09-26", 0.9606, 0.9609],
                ["2022-09-23", 0.969, 0.9694],
                ["2022-09-22", 0.9836, 0.984],
                ["2022-09-21", 0.9837, 0.9839],
                ["2022-09-20", 0.997, 0.9974],
            ],
        }
    ]
)

HP_TWO_UNIVERSES_ONE_FIELD = [
    StubResponse(
        [{
            'universe': {'ric': 'EUR='},
            'interval': 'P1D',
            'summaryTimestampLabel': 'endPeriod',
            'adjustments': ['exchangeCorrection', 'manualCorrection', 'CCH', 'CRE',
                            'RTS', 'RPO'],
            'defaultPricingField': 'BID',
            'headers': [{'name': 'DATE', 'type': 'string'},
                        {'name': 'BID', 'type': 'number', 'decimalChar': '.'}],
            'data': [['2022-09-26', 0.9606], ['2022-09-23', 0.969],
                     ['2022-09-22', 0.9836], ['2022-09-21', 0.9837],
                     ['2022-09-20', 0.997]]
        }]
    ),
    StubResponse(
        [{
            'universe': {'ric': 'VOD.L'},
            'interval': 'P1D',
            'summaryTimestampLabel': 'endPeriod',
            'adjustments': ['exchangeCorrection', 'manualCorrection', 'CCH', 'CRE',
                            'RTS', 'RPO'],
            'defaultPricingField': 'OFF_CLOSE',
            'headers': [{'name': 'DATE', 'type': 'string'},
                        {'name': 'BID', 'type': 'number', 'decimalChar': '.'}],
            'data': [['2022-09-26', 106.66], ['2022-09-23', 108.12],
                     ['2022-09-22', 108.84], ['2022-09-21', 108.78],
                     ['2022-09-20', 106.38]],
            'meta': {
                'blendingEntry': {
                    'headers': [{'name': 'DATE', 'type': 'string'},
                                {'name': 'BID', 'type': 'number', 'decimalChar': '.'}],
                    'data': [['2022-09-26', 106.66]]
                }
            }
        }]
    ),
]

CUSTOM_INST_ONE_UNIVERSE_TWO_FIELDS = StubResponse(
    [{
        'data': [['2022-09-26', 2.1368], ['2022-09-23', 2.1712],
                 ['2022-09-22', 2.2514], ['2022-09-21', 2.2532],
                 ['2022-09-20', 2.2758]],
        'defaultPricingField': 'TRDPRC_1',
        'headers': [{'name': 'DATE', 'type': 'string'},
                    {'decimalChar': '.', 'name': 'TRDPRC_1', 'type': 'number'}],
        'interval': 'P1D',
        'summaryTimestampLabel': 'endPeriod',
        'universe': {'ric': 'S)Batman_df3fe62e.GESG1-111923'}
    }]
)

CUSTOM_INST_TWO_UNIVERSES_ONE_FIELD = [
    StubResponse(
        [{
            'data': [['2022-09-26', 2.1368], ['2022-09-23', 2.1712],
                     ['2022-09-22', 2.2514], ['2022-09-21', 2.2532],
                     ['2022-09-20', 2.2758]],
            'defaultPricingField': 'TRDPRC_1',
            'headers': [{'name': 'DATE', 'type': 'string'},
                        {'decimalChar': '.', 'name': 'TRDPRC_1', 'type': 'number'}],
            'interval': 'P1D',
            'summaryTimestampLabel': 'endPeriod',
            'universe': {'ric': 'S)Batman_df3fe62e.GESG1-111923'}
        }]
    ),
    StubResponse(
        [{
            'data': [['2022-09-26', 2.1368], ['2022-09-23', 2.1712],
                     ['2022-09-22', 2.2514], ['2022-09-21', 2.2532],
                     ['2022-09-20', 2.2758]],
            'defaultPricingField': 'TRDPRC_1',
            'headers': [{'name': 'DATE', 'type': 'string'},
                        {'decimalChar': '.', 'name': 'TRDPRC_1', 'type': 'number'}],
            'interval': 'P1D',
            'summaryTimestampLabel': 'endPeriod',
            'universe': {'ric': 'S)Batman_92734226.GESG1-111923'}
        }]
    ),
]
