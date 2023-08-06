import refinitiv.data as rd
import inspect

from refinitiv.data.delivery._data._request import Request
from tests.unit.conftest import StubResponse, StubSession

_defns_with_ext_params = [
    rd.content.custom_instruments.Definition,
    rd.content.custom_instruments.events.Definition,
    rd.content.custom_instruments.search.Definition,
    rd.content.custom_instruments.summaries.Definition,
    rd.content.estimates.view_actuals.annual.Definition,
    rd.content.estimates.view_actuals.interim.Definition,
    rd.content.estimates.view_actuals_kpi.annual.Definition,
    rd.content.estimates.view_actuals_kpi.interim.Definition,
    rd.content.estimates.view_summary.annual.Definition,
    rd.content.estimates.view_summary.historical_snapshots_non_periodic_measures.Definition,
    rd.content.estimates.view_summary.historical_snapshots_periodic_measures_annual.Definition,
    rd.content.estimates.view_summary.historical_snapshots_periodic_measures_interim.Definition,
    rd.content.estimates.view_summary.historical_snapshots_recommendations.Definition,
    rd.content.estimates.view_summary.interim.Definition,
    rd.content.estimates.view_summary.non_periodic_measures.Definition,
    rd.content.estimates.view_summary.recommendations.Definition,
    rd.content.estimates.view_summary_kpi.annual.Definition,
    rd.content.estimates.view_summary_kpi.historical_snapshots_kpi.Definition,
    rd.content.estimates.view_summary_kpi.interim.Definition,
    rd.content.fundamental_and_reference.Definition,
    rd.content.historical_pricing.events.Definition,
    rd.content.historical_pricing.summaries.Definition,
    rd.content.ipa.curves.forward_curves.Definition,
    rd.content.ipa.curves.zc_curve_definitions.Definition,
    rd.content.ipa.curves.zc_curves.Definition,
    rd.content.ipa.dates_and_calendars.add_periods.Definition,
    rd.content.ipa.dates_and_calendars.count_periods.Definition,
    rd.content.ipa.dates_and_calendars.date_schedule.Definition,
    rd.content.ipa.dates_and_calendars.holidays.Definition,
    rd.content.ipa.dates_and_calendars.is_working_day.Definition,
    rd.content.ipa.financial_contracts.bond.Definition,
    rd.content.ipa.financial_contracts.cap_floor.Definition,
    rd.content.ipa.financial_contracts.cds.Definition,
    rd.content.ipa.financial_contracts.cross.Definition,
    rd.content.ipa.financial_contracts.option.Definition,
    rd.content.ipa.financial_contracts.repo.Definition,
    rd.content.ipa.financial_contracts.swap.Definition,
    rd.content.ipa.financial_contracts.swaption.Definition,
    rd.content.ipa.financial_contracts.term_deposit.Definition,
    rd.content.ipa.surfaces.cap.Definition,
    rd.content.ipa.surfaces.eti.Definition,
    rd.content.ipa.surfaces.fx.Definition,
    rd.content.ipa.surfaces.swaption.Definition,
    rd.content.news.headlines.Definition,
    rd.content.ownership.consolidated.breakdown.Definition,
    rd.content.ownership.consolidated.concentration.Definition,
    rd.content.ownership.consolidated.investors.Definition,
    rd.content.ownership.consolidated.recent_activity.Definition,
    rd.content.ownership.consolidated.shareholders_history_report.Definition,
    rd.content.ownership.consolidated.shareholders_report.Definition,
    rd.content.ownership.consolidated.top_n_concentration.Definition,
    rd.content.ownership.fund.breakdown.Definition,
    rd.content.ownership.fund.concentration.Definition,
    rd.content.ownership.fund.holdings.Definition,
    rd.content.ownership.fund.investors.Definition,
    rd.content.ownership.fund.recent_activity.Definition,
    rd.content.ownership.fund.shareholders_history_report.Definition,
    rd.content.ownership.fund.shareholders_report.Definition,
    rd.content.ownership.fund.top_n_concentration.Definition,
    rd.content.ownership.insider.shareholders_report.Definition,
    rd.content.ownership.insider.transaction_report.Definition,
    rd.content.ownership.investor.holdings.Definition,
    rd.content.ownership.org_info.Definition,
    rd.content.pricing.chain.Definition,
    rd.content.pricing.Definition,
    rd.content.search.Definition,
    rd.content.search.lookup.Definition,
    rd.content.symbol_conversion.Definition,
    rd.content.trade_data_service.Definition,
    rd.delivery.omm_stream.Definition,
    rd.delivery.rdp_stream.Definition,
]

_defns_without_ext_params = [
    rd.content.esg.basic_overview.Definition,
    rd.content.esg.bulk.Definition,
    rd.content.esg.full_measures.Definition,
    rd.content.esg.full_scores.Definition,
    rd.content.esg.standard_measures.Definition,
    rd.content.esg.standard_scores.Definition,
    rd.content.esg.universe.Definition,
    rd.content.filings.retrieval.Definition,
    rd.content.filings.search.Definition,
    rd.content.ipa.curves.forward_curves.Definitions,
    rd.content.ipa.curves.zc_curve_definitions.Definitions,
    rd.content.ipa.curves.zc_curves.Definitions,
    rd.content.ipa.dates_and_calendars.add_periods.Definitions,
    rd.content.ipa.dates_and_calendars.count_periods.Definitions,
    rd.content.ipa.dates_and_calendars.holidays.Definitions,
    rd.content.ipa.dates_and_calendars.is_working_day.Definitions,
    rd.content.ipa.financial_contracts.Definitions,
    rd.content.ipa.surfaces.Definitions,
    rd.content.news.story.Definition,
    rd.content.search.metadata.Definition,
    rd.delivery.cfs.buckets.Definition,
    rd.delivery.cfs.file_downloader.Definition,
    rd.delivery.cfs.file_sets.Definition,
    rd.delivery.cfs.files.Definition,
    rd.delivery.cfs.packages.Definition,
    rd.delivery.endpoint_request.Definition,
    rd.session.Definition,
    rd.session.desktop.Definition,
    rd.session.platform.Definition,
]

_defns = _defns_without_ext_params + _defns_with_ext_params

_count_no_has_ext_params = 0
_count_has_ext_params = 0


def write_count():
    global _count_has_ext_params, _count_no_has_ext_params

    for definition in _defns:
        arg_spec = inspect.getfullargspec(definition.__init__)

        if "extended_params" in arg_spec.args:
            _count_has_ext_params += 1
        else:
            _count_no_has_ext_params += 1


def test_definitions_on_extended_params():
    write_count()

    assert _count_has_ext_params == 71, _count_has_ext_params
    assert _count_no_has_ext_params == 29, _count_no_has_ext_params


def test_custom_instruments_definition():
    # region response_400
    response_400 = StubResponse(
        status_code=400,
        content_data=[
            {
                "state": {
                    "code": 400,
                    "status": "Bad Request",
                    "message": "Validation Error",
                },
                "data": [
                    {
                        "key": "symbol",
                        "reason": ".UUID suffix UUID not matched with userID GESG1-60983",
                    }
                ],
            }
        ],
    )
    # endregion
    # region response_200
    response_200 = StubResponse(
        [
            {
                "data": [
                    ["2022-08-26T07:16:54.286Z", 1.9908],
                    ["2022-08-26T07:16:49.777Z", 1.991],
                    ["2022-08-26T07:16:49.297Z", 1.991],
                    ["2022-08-26T07:16:48.796Z", 1.9908],
                    ["2022-08-26T07:16:48.257Z", 1.991],
                    ["2022-08-26T07:16:47.782Z", 1.9908],
                    ["2022-08-26T07:16:47.495Z", 1.991],
                ],
                "defaultPricingField": "TRDPRC_1",
                "headers": [
                    {"name": "DATE_TIME", "type": "string"},
                    {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
                ],
                "interval": None,
                "summaryTimestampLabel": None,
                "universe": {"ric": "S)MyInstrumentEUR.GESG1-60983"},
            }
        ]
    )
    # endregion
    expected_url_usd = "test_get_rdp_url_root/data/custom-instruments/v1/events/S%29MyInstrumentUSD.GESG1-60983?start=2022-05-06T05%3A00%3A00.000000000Z&count=7"
    expected_url_eur = "test_get_rdp_url_root/data/custom-instruments/v1/events/S%29MyInstrumentEUR.GESG1-60983?start=2022-05-06T05%3A00%3A00.000000000Z&count=7"

    def mock_http_request(request: Request):
        testing_url = request.url
        response = response_400
        if "MyInstrumentUSD" in testing_url:
            assert testing_url == expected_url_usd
            response = response_200
        elif "MyInstrumentEUR" in testing_url:
            assert testing_url == expected_url_eur
            response = response_200
        return response

    session = StubSession(is_open=True)
    session.http_request = mock_http_request
    rd.content.custom_instruments.events.Definition(
        universe=["S)MyInstrumentUSD", "S)MyInstrumentEUR"],
        extended_params={
            "start": "2022-05-06T05:00:00.000000000Z",
            "count": 7,
        },
    ).get_data(session)


def test_fundamental_and_reference_definition_udf():
    # region expected_json
    expected_json = {
        "Entity": {
            "E": "DataGrid_StandardAsync",
            "W": {
                "requests": [
                    {
                        "instruments": ["GOOG.O", "AAPL.O"],
                        "fields": [
                            {"name": "TR.Revenue"},
                            {"name": "TR.Revenue.date"},
                            {"name": "TR.GrossProfit"},
                        ],
                        "parameters": {
                            "Scale": 6,
                            "SDate": 0,
                            "EDate": -3,
                            "FRQ": "FY",
                            "Curn": "EUR",
                        },
                        "universe": ["GOOG.O", "AAPL.O"],
                    }
                ]
            },
        }
    }

    # endregion

    def mock_http_request(request: Request):
        testing_json = request.json
        assert testing_json == expected_json
        return response_200

    # region response_200
    response_200 = StubResponse(
        {
            "responses": [
                {
                    "links": {"count": 8},
                    "variability": "",
                    "universe": [
                        {
                            "Instrument": "GOOG.O",
                            "Company Common Name": "Alphabet Inc",
                            "Organization PermID": "5030853586",
                            "Reporting Currency": "USD",
                        },
                        {
                            "Instrument": "AAPL.O",
                            "Company Common Name": "Apple Inc",
                            "Organization PermID": "4295905573",
                            "Reporting Currency": "USD",
                        },
                    ],
                    "data": [
                        ["GOOG.O", 226632.96342, "2021-12-31T00:00:00", 129044.36268],
                        ["GOOG.O", 149453.1076, "2020-12-31T00:00:00", 80074.546],
                        ["GOOG.O", 144386.15542, "2019-12-31T00:00:00", 80250.60966],
                        ["GOOG.O", 119295.22248, "2018-12-31T00:00:00", 67373.2584],
                        ["AAPL.O", 312290.65656, "2021-09-25T00:00:00", 130473.03648],
                        ["AAPL.O", 236041.72275, "2020-09-26T00:00:00", 90246.4166],
                        ["AAPL.O", 237861.47776, "2019-09-28T00:00:00", 89953.90208],
                        ["AAPL.O", 228802.12465, "2018-09-29T00:00:00", 87731.24333],
                    ],
                    "messages": {
                        "codes": [
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
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
                            "name": "TR.Revenue",
                            "title": "Revenue",
                            "type": "number",
                            "decimalChar": ".",
                        },
                        {
                            "name": "TR.Revenue",
                            "title": "Date",
                            "type": "datetime",
                        },
                        {
                            "name": "TR.GrossProfit",
                            "title": "Gross Profit",
                            "type": "number",
                            "decimalChar": ".",
                        },
                    ],
                }
            ]
        }
    )
    # endregion

    session = StubSession(is_open=True)
    session.http_request = mock_http_request
    rd.content.fundamental_and_reference.Definition(
        universe=["MSFT.O", "FB.O", "AMZN.O", "TWTR.K"],
        fields=["TR.Revenue", "TR.Revenue.date", "TR.GrossProfit"],
        parameters={"Scale": 6, "SDate": 0, "EDate": -3, "FRQ": "FY", "Curn": "EUR"},
        use_field_names_in_headers=True,
        extended_params={"universe": ["GOOG.O", "AAPL.O"]},
    ).get_data(session)


def test_historical_pricing_events_definition():
    # region response_200
    response = StubResponse(
        [
            {
                "universe": {"ric": "VOD.L"},
                "adjustments": ["exchangeCorrection", "manualCorrection"],
                "defaultPricingField": "TRDPRC_1",
                "qos": {"timeliness": "delayed"},
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
                        "2022-07-19T15:40:00.158000000Z",
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
            }
        ]
    )
    # endregion
    expected_url_goog = "test_get_rdp_url_root/data/historical-pricing/v1/views/events/GOOG.O?eventTypes=quote&count=5&start=2022-07-18T10%3A00%3A00.000000000Z&end=2022-07-19T16%3A00%3A00.000000000Z"
    expected_url_vod = "test_get_rdp_url_root/data/historical-pricing/v1/views/events/VOD.L?eventTypes=quote&count=5&start=2022-07-18T10%3A00%3A00.000000000Z&end=2022-07-19T16%3A00%3A00.000000000Z"

    def mock_http_request(request: Request):
        testing_url = request.url
        if "GOOG" in testing_url:
            assert testing_url == expected_url_goog
        elif "VOD" in testing_url:
            assert testing_url == expected_url_vod
        return response

    session = StubSession(is_open=True)
    session.http_request = mock_http_request
    rd.content.historical_pricing.events.Definition(
        universe=["VOD.L", "GOOG.O"],
        eventTypes="quote",
        extended_params={
            "count": 5,
            "start": "2022-07-18T10:00:00",
            "end": "2022-07-19T16:00:00",
        },
    ).get_data(session)


def test_historical_pricing_summaries_definition():
    # region response_200
    response = StubResponse(
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
                    ["2022-01-05", 1.1313, 1.1315],
                    ["2022-01-04", 1.1285, 1.1289],
                    ["2022-01-03", 1.1294, 1.1298],
                    ["2021-12-31", 1.1368, 1.1372],
                    ["2021-12-30", 1.1323, 1.1327],
                ],
                "status": {
                    "code": "TS.Interday.UserRequestError.70007",
                    "message": "The universe does not support the following fields: [MKT_OPEN].",
                },
                "meta": {
                    "blendingEntry": {
                        "headers": [
                            {"name": "DATE", "type": "string"},
                            {"name": "BID", "type": "number", "decimalChar": "."},
                            {"name": "ASK", "type": "number", "decimalChar": "."},
                        ],
                        "data": [["2022-01-05", 1.1313, 1.1315]],
                    }
                },
            }
        ]
    )
    # endregion
    expected_url_eur = "test_get_rdp_url_root/data/historical-pricing/v1/views/interday-summaries/EUR%3D?start=2021-12-30T00%3A10%3A00.000000000Z&end=2022-01-05T05%3A10%3A00.000000000Z&interval=P1D&adjustments=CCH&count=5&fields=DATE%2CMKT_OPEN%2CBID%2CASK"
    expected_url_gbp = "test_get_rdp_url_root/data/historical-pricing/v1/views/interday-summaries/GBP%3D?start=2021-12-30T00%3A10%3A00.000000000Z&end=2022-01-05T05%3A10%3A00.000000000Z&interval=P1D&adjustments=CCH&count=5&fields=DATE%2CMKT_OPEN%2CBID%2CASK"

    def mock_http_request(request: Request):
        testing_url = request.url
        if "EUR" in testing_url:
            assert testing_url == expected_url_eur
        elif "GBP" in testing_url:
            assert testing_url == expected_url_gbp
        return response

    session = StubSession(is_open=True)
    session.http_request = mock_http_request
    rd.content.historical_pricing.summaries.Definition(
        universe=["EUR=", "GBP="],
        start="2021-12-30T00:10:00",
        end="2022-01-05T05:10:00",
        extended_params={
            "interval": "P1D",
            "adjustments": "CCH",
            "count": 5,
            "fields": "DATE,MKT_OPEN,BID,ASK",
        },
    ).get_data(session)


def test_dates_and_calendars():
    response_200 = StubResponse(
        [
            {"date": "2023-05-30", "holidays": [], "tag": "first req"},
            {"date": "2022-03-30", "holidays": [], "tag": "first req"},
        ]
    )
    expected_json = [
        {
            "startDate": "2020-05-30",
            "tag": "first req",
            "period": "3Y",
            "calendars": ["GER", "UKR"],
            "currencies": ["EUR"],
            "dateMovingConvention": "ModifiedFollowing",
            "endOfMonthConvention": "Same",
            "holidayOutputs": ["Countries", "Names"],
        },
        {
            "startDate": "2022-03-20",
            "tag": "second req",
            "period": "10D",
            "calendars": ["JAP", "UKR"],
            "currencies": ["USD"],
            "dateMovingConvention": "ModifiedFollowing",
            "endOfMonthConvention": "Same",
            "holidayOutputs": ["Countries", "Names"],
        },
    ]

    def mock_http_request(request: Request):
        testing_json = request.json
        assert testing_json == expected_json
        return response_200

    session = StubSession(is_open=True)
    session.http_request = mock_http_request

    def1 = rd.content.ipa.dates_and_calendars.add_periods.Definition(
        tag="my request",
        start_date="2020-04-24",
        period="4D",
        calendars=["BAR", "KOR", "JAP"],
        currencies=["USD"],
        date_moving_convention="NextBusinessDay",
        end_of_month_convention="Last",
        holiday_outputs=["Date", "Calendars", "Names"],
        extended_params={
            "startDate": "2020-05-30",
            "tag": "first req",
            "period": "3Y",
            "calendars": ["GER", "UKR"],
            "currencies": ["EUR"],
            "dateMovingConvention": "ModifiedFollowing",
            "endOfMonthConvention": "Same",
            "holidayOutputs": ["Countries", "Names"],
        },
    )

    def2 = rd.content.ipa.dates_and_calendars.add_periods.Definition(
        tag="my 2 request",
        start_date="2020-04-24",
        period="4D",
        calendars=["BAR", "KOR", "JAP"],
        currencies=["EUR"],
        date_moving_convention="NextBusinessDay",
        end_of_month_convention="Last",
        holiday_outputs=["Date", "Calendars", "Names"],
        extended_params={
            "startDate": "2022-03-20",
            "tag": "second req",
            "period": "10D",
            "calendars": ["JAP", "UKR"],
            "currencies": ["USD"],
            "dateMovingConvention": "ModifiedFollowing",
            "endOfMonthConvention": "Same",
            "holidayOutputs": ["Countries", "Names"],
        },
    )

    defn = rd.content.ipa.dates_and_calendars.add_periods.Definitions([def1, def2])
    defn.get_data(session)


def test_financial_contracts_bond():
    import refinitiv.data.content.ipa.financial_contracts as rdf

    response_200 = StubResponse()
    expected_json = {
        "universe": [
            {
                "instrumentType": "Bond",
                "instrumentDefinition": {
                    "issueDate": "2022-02-28",
                    "endDate": "2032-02-28",
                    "notionalCcy": "USD",
                    "fixedRatePercent": 7,
                    "interestPaymentFrequency": "Annual",
                    "interestCalculationMethod": "Dcb_Actual_Actual",
                },
                "pricingParameters": {"cleanPrice": 155},
            }
        ]
    }

    def mock_http_request(request: Request):
        testing_json = request.json
        assert testing_json == expected_json
        return response_200

    session = StubSession(is_open=True)
    session.http_request = mock_http_request

    definition = rdf.bond.Definition(
        fixed_rate_percent=7,
        interest_calculation_method=rdf.bond.DayCountBasis.DCB_ACTUAL_ACTUAL,
        interest_payment_frequency=rdf.bond.Frequency.ANNUAL,
        pricing_parameters=rdf.bond.PricingParameters(clean_price=122),
        extended_params={
            "instrumentDefinition": {
                "issueDate": "2022-02-28",
                "endDate": "2032-02-28",
                "notionalCcy": "USD",
            },
            "pricingParameters": {"cleanPrice": 155},
        },
    )
    definition.get_data(session)


def test_curves_forward_curves():
    import refinitiv.data.content.ipa.curves as curves

    response_200 = StubResponse()
    expected_json = {
        "universe": [
            {
                "curveDefinition": {
                    "indexName": "EURIBOR",
                    "currency": "EUR",
                    "discountingTenor": "OIS",
                },
                "curveParameters": {"calendarAdjustment": "Calendar"},
                "forwardCurveDefinitions": [
                    {
                        "indexTenor": "3M",
                        "forwardCurveTenors": ["0D", "1D"],
                        "forwardCurveTag": "ForwardTag",
                        "forwardStartDate": "2021-02-01",
                        "forwardStartTenor": "some_start_tenor",
                    }
                ],
                "curveTag": "new_test_curve",
            }
        ]
    }

    def mock_http_request(request: Request):
        testing_json = request.json
        assert testing_json == expected_json
        return response_200

    session = StubSession(is_open=True)
    session.http_request = mock_http_request

    definition = curves.forward_curves.Definition(
        curve_definition=curves.forward_curves.SwapZcCurveDefinition(
            currency="EUR",
            index_name="EURIBOR",
            discounting_tenor="OIS",
        ),
        curve_tag="test_curve",
        extended_params={
            "curveParameters": {"calendarAdjustment": "Calendar"},
            "forwardCurveDefinitions": [
                {
                    "indexTenor": "3M",
                    "forwardCurveTenors": ["0D", "1D"],
                    "forwardCurveTag": "ForwardTag",
                    "forwardStartDate": "2021-02-01",
                    "forwardStartTenor": "some_start_tenor",
                }
            ],
            "curveTag": "new_test_curve",
        },
    )
    definition.get_data(session)


def test_financial_contracts_swap():
    import refinitiv.data.content.ipa.financial_contracts as rdf

    expected_json = {
        "streamID": "5",
        "method": "Subscribe",
        "universe": {
            "instrumentType": "Swap",
            "instrumentDefinition": {
                "tenor": "5Y",
                "legs": [
                    {
                        "direction": "Paid",
                        "interestType": "Float",
                        "notionalCcy": "EUR",
                        "notionalAmount": 1,
                        "interestPaymentFrequency": "Quarterly",
                    },
                    {
                        "direction": "Received",
                        "interestType": "Float",
                        "notionalCcy": "EUR",
                        "indexTenor": "5Y",
                        "interestPaymentFrequency": "Quarterly",
                    },
                ],
            },
            "pricingParameters": {
                "indexConvexityAdjustmentIntegrationMethod": "RiemannSum",
                "indexConvexityAdjustmentMethod": "BlackScholes",
                "valuationDate": "2020-06-01",
            },
        },
        "view": ["InstrumentDescription", "Structure", "Tenor", "InterestType"],
    }

    session = StubSession(is_open=True)

    swap_def = rdf.swap.Definition(
        pricing_parameters=rdf.swap.PricingParameters(
            index_convexity_adjustment_integration_method=rdf.swap.IndexConvexityAdjustmentIntegrationMethod.RIEMANN_SUM,
            index_convexity_adjustment_method=rdf.swap.IndexConvexityAdjustmentMethod.BLACK_SCHOLES,
            valuation_date="2020-06-01",
        ),
        fields=[
            "InstrumentDescription",
            "Structure",
            "Tenor",
            "InterestType",
        ],
        extended_params={
            "instrumentDefinition": {
                "tenor": "5Y",
                "legs": [
                    {
                        "direction": "Paid",
                        "interestType": "Float",
                        "notionalCcy": "EUR",
                        "notionalAmount": 1,
                        "interestPaymentFrequency": "Quarterly",
                    },
                    {
                        "direction": "Received",
                        "interestType": "Float",
                        "notionalCcy": "EUR",
                        "indexTenor": "5Y",
                        "interestPaymentFrequency": "Quarterly",
                    },
                ],
            },
        },
    )
    stream = swap_def.get_stream(session)
    assert stream._stream._stream.open_message == expected_json
