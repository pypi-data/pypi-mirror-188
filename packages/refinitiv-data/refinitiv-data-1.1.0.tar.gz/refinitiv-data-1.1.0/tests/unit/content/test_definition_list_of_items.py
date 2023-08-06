import types
from functools import partial

import pytest

import refinitiv.data as rd
import refinitiv.data.content as rdc
from refinitiv.data.delivery._data._request import Request
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.content.data_for_tests import (
    zc_curves_definitions,
    calendars_definitions,
    universe_definitions,
    fields_in_json_definitions,
    calendars_jsons,
)
from tests.unit.content.test_enums import (
    get_query_params_from_url,
    get_json,
)

defns_with_list_of_items = [
    rdc.custom_instruments.Definition,
    rdc.custom_instruments.events.Definition,
    rdc.custom_instruments.summaries.Definition,
    rdc.esg.basic_overview.Definition,
    rdc.esg.bulk.Definition,
    rdc.esg.full_measures.Definition,
    rdc.esg.full_scores.Definition,
    rdc.esg.standard_measures.Definition,
    rdc.esg.standard_scores.Definition,
    rdc.estimates.view_actuals.annual.Definition,
    rdc.estimates.view_actuals.interim.Definition,
    rdc.estimates.view_actuals_kpi.annual.Definition,
    rdc.estimates.view_actuals_kpi.interim.Definition,
    rdc.estimates.view_summary.annual.Definition,
    rdc.estimates.view_summary.historical_snapshots_non_periodic_measures.Definition,
    rdc.estimates.view_summary.historical_snapshots_periodic_measures_annual.Definition,
    rdc.estimates.view_summary.historical_snapshots_periodic_measures_interim.Definition,
    rdc.estimates.view_summary.historical_snapshots_recommendations.Definition,
    rdc.estimates.view_summary.interim.Definition,
    rdc.estimates.view_summary.non_periodic_measures.Definition,
    rdc.estimates.view_summary.recommendations.Definition,
    rdc.estimates.view_summary_kpi.annual.Definition,
    rdc.estimates.view_summary_kpi.historical_snapshots_kpi.Definition,
    rdc.estimates.view_summary_kpi.interim.Definition,
    rdc.fundamental_and_reference.Definition,
    rdc.historical_pricing.events.Definition,
    rdc.historical_pricing.summaries.Definition,
    rdc.ipa.curves.forward_curves.Definition,
    rdc.ipa.curves.forward_curves.Definitions,
    rdc.ipa.curves.zc_curve_definitions.Definitions,
    rdc.ipa.curves.zc_curves.Definitions,
    rdc.ipa.dates_and_calendars.add_periods.Definition,
    rdc.ipa.dates_and_calendars.add_periods.Definitions,
    rdc.ipa.dates_and_calendars.count_periods.Definition,
    rdc.ipa.dates_and_calendars.count_periods.Definitions,
    rdc.ipa.dates_and_calendars.date_schedule.Definition,
    rdc.ipa.dates_and_calendars.holidays.Definition,
    rdc.ipa.dates_and_calendars.holidays.Definitions,
    rdc.ipa.dates_and_calendars.is_working_day.Definition,
    rdc.ipa.dates_and_calendars.is_working_day.Definitions,
    rdc.ipa.financial_contracts.bond.Definition,
    rdc.ipa.financial_contracts.cap_floor.Definition,
    rdc.ipa.financial_contracts.cds.Definition,
    rdc.ipa.financial_contracts.cross.Definition,
    rdc.ipa.financial_contracts.Definitions,
    rdc.ipa.financial_contracts.option.Definition,
    rdc.ipa.financial_contracts.repo.Definition,
    rdc.ipa.financial_contracts.swap.Definition,
    rdc.ipa.financial_contracts.swaption.Definition,
    rdc.ipa.financial_contracts.term_deposit.Definition,
    rdc.ipa.surfaces.Definitions,
    rdc.ownership.consolidated.breakdown.Definition,
    rdc.ownership.consolidated.concentration.Definition,
    rdc.ownership.consolidated.investors.Definition,
    rdc.ownership.consolidated.recent_activity.Definition,
    rdc.ownership.consolidated.shareholders_report.Definition,
    rdc.ownership.consolidated.top_n_concentration.Definition,
    rdc.ownership.fund.breakdown.Definition,
    rdc.ownership.fund.concentration.Definition,
    rdc.ownership.fund.holdings.Definition,
    rdc.ownership.fund.investors.Definition,
    rdc.ownership.fund.recent_activity.Definition,
    rdc.ownership.fund.shareholders_report.Definition,
    rdc.ownership.fund.top_n_concentration.Definition,
    rdc.ownership.insider.shareholders_report.Definition,
    rdc.ownership.insider.transaction_report.Definition,
    rdc.ownership.investor.holdings.Definition,
    rdc.ownership.org_info.Definition,
    rdc.pricing.Definition,
    rdc.symbol_conversion.Definition,
    rdc.trade_data_service.Definition,
    rd.delivery.cfs.buckets.Definition,
    rd.delivery.omm_stream.Definition,
    rd.delivery.rdp_stream.Definition,
    rd._qpl.fx_swp_to_swp,
]

list_of_items_types = [
    "StrStrings",
    "DefnDefns",
    "OptStrStrs",
    "OptRowHeaders",
    "OptEventTypes",
    "OptAdjustments",
    "OptMarketSession",
    "OptForwardCurveDefinitions",
    "OptHolidayOutputs",
    "OptAssetClass",
    "OptSymbolTypes",
]


def test_count():
    num = len(defns_with_list_of_items)
    assert num == 75, num


def test_definition_has_list_of_items():
    for defn in defns_with_list_of_items:
        if not isinstance(defn, types.FunctionType):
            defn = getattr(defn, "__init__")
        annotations = defn.__annotations__
        if not annotations:
            continue

        has = False
        for param_name, type_notation in annotations.items():
            if type_notation in list_of_items_types:
                has = True
                break

        assert has, defn


def make_checker(param_name, value, func_get_params, response=None):
    def http_request(request, *args, **kwargs):
        nonlocal response
        url = request.url
        if url.startswith(
            "test_get_rdp_url_root/data/pricing/snapshots"
        ) or url.startswith("test_get_rdp_url_root/data/historical-pricing"):
            response = [{}]

        params = func_get_params(request)
        param_value = params.get(param_name)
        assert str(param_value) == str(value), (
            f"Param{param_name}:\n"
            f"Expected value {param_value}. \n"
            f"Value {str(value)}"
        )
        return StubResponse(content_data=response)

    return http_request


def get_request_fundamental_and_reference(request: Request):
    json = request.json
    entity = json.get("Entity", {})
    w = entity.get("W", {})
    requests = w.get("requests", [{}])
    return requests[0]


universe_params = [
    (
        i,
        "universe",
        "universe",
        [
            ("test_universe", "test_universe"),
            (["test_universe"], "test_universe"),
            (["test_universe", "universe"], "test_universe%2Cuniverse"),
        ],
        get_query_params_from_url,
        None,
    )
    for i in universe_definitions
]

fields_in_json = [
    (
        i,
        "fields",
        "fields",
        [
            ("BID", ["BID"]),
            (["BID", "ASK"], ["BID", "ASK"]),
        ],
        get_json,
        None,
    )
    for i in fields_in_json_definitions
]


def get_calendars_json(request: Request):
    json = get_json(request)
    return {"universe": json}


def get_forward_curves(request: Request):
    return get_json(request).get("universe", [{}])[0]


@pytest.mark.parametrize(
    (
        "definition",
        "arg_name",
        "request_param_name",
        "test_data",
        "func_get_params",
        "response",
    ),
    [
        *universe_params,
        (
            partial(rdc.fundamental_and_reference.Definition, fields=[]),
            "universe",
            "instruments",
            [
                ("test_universe", ["TEST_UNIVERSE"]),
                (["test_universe"], ["TEST_UNIVERSE"]),
                (["test_universe", "universe"], ["TEST_UNIVERSE", "UNIVERSE"]),
            ],
            get_request_fundamental_and_reference,
            None,
        ),
        *fields_in_json,
        (
            partial(rdc.fundamental_and_reference.Definition, universe="universe"),
            "fields",
            "fields",
            [
                (["TR.RIC"], [{"name": "TR.RIC"}]),
                (
                    ["TR.RIC", "TR.REVENUE"],
                    [{"name": "TR.RIC"}, {"name": "TR.REVENUE"}],
                ),
            ],
            get_request_fundamental_and_reference,
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.add_periods.Definition,
            "calendars",
            "calendars",
            [
                ("BID", "BID"),
                (["BID", "ASK"], ["BID", "ASK"]),
            ],
            lambda request: get_json(request)[0],
            [{"date": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.count_periods.Definition,
            "calendars",
            "calendars",
            [
                ("BID", "BID"),
                (["BID", "ASK"], ["BID", "ASK"]),
            ],
            lambda request: get_json(request)[0],
            [{"count": ..., "tenor": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.date_schedule.Definition,
            "calendars",
            "calendars",
            [
                ("BID", "BID"),
                (["BID", "ASK"], ["BID", "ASK"]),
            ],
            get_json,
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.holidays.Definition,
            "calendars",
            "calendars",
            [
                ("BID", "BID"),
                (["BID", "ASK"], ["BID", "ASK"]),
            ],
            lambda request: get_json(request)[0],
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.is_working_day.Definition,
            "calendars",
            "calendars",
            [
                ("BID", "BID"),
                (["BID", "ASK"], ["BID", "ASK"]),
            ],
            lambda request: get_json(request)[0],
            [{"isWeekEnd": ..., "isWorkingDay": ...}],
        ),
        (
            partial(rdc.historical_pricing.summaries.Definition, universe="universe"),
            "adjustments",
            "adjustments",
            [
                ("unadjusted", "unadjusted"),
                (
                    ["unadjusted", rdc.historical_pricing.Adjustments.CCH],
                    "unadjusted%2CCCH",
                ),
            ],
            get_query_params_from_url,
            [{"universe": {"ric": "universe"}, "data": [{}]}],
        ),
        (
            partial(rdc.historical_pricing.summaries.Definition, universe="universe"),
            "sessions",
            "sessions",
            [
                ("normal", "normal"),
                (["normal", rdc.historical_pricing.MarketSession.PRE], "normal%2Cpre"),
            ],
            get_query_params_from_url,
            [{"universe": {"ric": "universe"}, "data": [{}]}],
        ),
        (
            partial(rdc.pricing.Definition, universe="universe"),
            "fields",
            "fields",
            [
                ("BID", "BID"),
                (["BID", "ASK"], "BID%2CASK"),
            ],
            get_query_params_from_url,
            None,
        ),
        (
            partial(rdc.historical_pricing.events.Definition, universe="universe"),
            "eventTypes",
            "eventTypes",
            [
                ("trade", "trade"),
                (["trade", rdc.historical_pricing.EventTypes.QUOTE], "trade%2Cquote"),
            ],
            get_query_params_from_url,
            [{"universe": {"ric": "universe"}, "data": [{}]}],
        ),
        (
            partial(rdc.historical_pricing.events.Definition, universe="universe"),
            "adjustments",
            "adjustments",
            [
                ("unadjusted", "unadjusted"),
                (
                    ["unadjusted", rdc.historical_pricing.Adjustments.CCH],
                    "unadjusted%2CCCH",
                ),
            ],
            get_query_params_from_url,
            [{"universe": {"ric": "universe"}, "data": [{}]}],
        ),
        (
            rdc.ipa.curves.forward_curves.Definitions,
            "universe",
            "universe",
            [
                (zc_curves_definitions[0], [{"source": "Refinitiv"}]),
                (
                    zc_curves_definitions,
                    [{"source": "Refinitiv"}, {"source": "Peugeot"}],
                ),
            ],
            get_json,
            None,
        ),
        (
            rdc.ipa.curves.zc_curves.Definitions,
            "universe",
            "universe",
            [
                (zc_curves_definitions[0], [{"source": "Refinitiv"}]),
                (
                    zc_curves_definitions,
                    [{"source": "Refinitiv"}, {"source": "Peugeot"}],
                ),
            ],
            get_json,
            None,
        ),
        (
            rdc.ipa.curves.zc_curve_definitions.Definitions,
            "universe",
            "universe",
            [
                (zc_curves_definitions[0], [{"source": "Refinitiv"}]),
                (
                    zc_curves_definitions,
                    [{"source": "Refinitiv"}, {"source": "Peugeot"}],
                ),
            ],
            get_json,
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.add_periods.Definitions,
            "universe",
            "universe",
            [
                (calendars_definitions[0], [calendars_jsons[0]]),
                (calendars_definitions, calendars_jsons),
            ],
            get_calendars_json,
            [{"date": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.count_periods.Definitions,
            "universe",
            "universe",
            [
                (calendars_definitions[0], [calendars_jsons[0]]),
                (calendars_definitions, calendars_jsons),
            ],
            get_calendars_json,
            [{"count": ..., "tenor": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.holidays.Definitions,
            "universe",
            "universe",
            [
                (calendars_definitions[0], [calendars_jsons[0]]),
                (calendars_definitions, calendars_jsons),
            ],
            get_calendars_json,
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.is_working_day.Definitions,
            "universe",
            "universe",
            [
                (calendars_definitions[0], [calendars_jsons[0]]),
                (calendars_definitions, calendars_jsons),
            ],
            get_calendars_json,
            [{"isWeekEnd": ..., "isWorkingDay": ...}],
        ),
        (
            rd.delivery.cfs.buckets.Definition,
            "attributes",
            "attributes",
            [
                ("attr1", "attr1"),
                (["attr1", "attr2"], "attr1;attr2"),
            ],
            get_query_params_from_url,
            None,
        ),
        (
            rdc.ipa.curves.forward_curves.Definition,
            "forward_curve_definitions",
            "forwardCurveDefinitions",
            [
                (
                    rdc.ipa.curves.forward_curves.ForwardCurveDefinition(
                        index_tenor="3M",
                        forward_curve_tag="ForwardTag",
                    ),
                    [{"indexTenor": "3M", "forwardCurveTag": "ForwardTag"}],
                )
            ],
            get_forward_curves,
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.add_periods.Definition,
            "currencies",
            "currencies",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
            lambda request: get_json(request)[0],
            [{"date": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.add_periods.Definition,
            "holiday_outputs",
            "holidayOutputs",
            [
                (["Date"], ["Date"]),
                (rdc.ipa.dates_and_calendars.holidays.HolidayOutputs.DATE, ["Date"]),
                (rdc.ipa.dates_and_calendars.add_periods.HolidayOutputs.DATE, ["Date"]),
                (
                    [
                        "Date",
                        rdc.ipa.dates_and_calendars.add_periods.HolidayOutputs.CALENDARS,
                    ],
                    ["Date", "Calendars"],
                ),
            ],
            lambda request: get_json(request)[0],
            [{"date": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.count_periods.Definition,
            "currencies",
            "currencies",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
            lambda request: get_json(request)[0],
            [{"count": ..., "tenor": ...}],
        ),
        (
            rdc.ipa.dates_and_calendars.date_schedule.Definition,
            "currencies",
            "currencies",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
            get_json,
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.holidays.Definition,
            "currencies",
            "currencies",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
            lambda request: get_json(request)[0],
            None,
        ),
        (
            rdc.ipa.dates_and_calendars.is_working_day.Definition,
            "currencies",
            "currencies",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
            lambda request: get_json(request)[0],
            [{"isWeekEnd": ..., "isWorkingDay": ...}],
        ),
        (
            rdc.ipa.financial_contracts.Definitions,
            "universe",
            "universe",
            [
                (
                    rdc.ipa.financial_contracts.option.Definition(),
                    [{"instrumentType": "Option", "instrumentDefinition": {}}],
                ),
                (
                    [rdc.ipa.financial_contracts.option.Definition()],
                    [{"instrumentType": "Option", "instrumentDefinition": {}}],
                ),
            ],
            get_json,
            None,
        ),
        (
            rdc.ipa.surfaces.Definitions,
            "universe",
            "universe",
            [
                (rdc.ipa.surfaces.cap.Definition(), [{"underlyingType": "Cap"}]),
                (
                    [
                        rdc.ipa.surfaces.swaption.Definition(),
                        rdc.ipa.surfaces.cap.Definition(),
                    ],
                    [{"underlyingType": "Swaption"}, {"underlyingType": "Cap"}],
                ),
            ],
            get_json,
            None,
        ),
        (
            rdc.symbol_conversion.Definition,
            "symbols",
            "Terms",
            [("symbol1", "symbol1"), (["symbol1", "symbol2"], "symbol1,symbol2")],
            get_json,
            None,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "to_symbol_types",
            "ToSymbolTypes",
            [("RIC", None), (["RIC", rdc.symbol_conversion.SymbolTypes.ISIN], None)],
            get_json,
            None,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "asset_class",
            "assetClass",
            [
                ("Commodities", None),
                (["Commodities", rdc.symbol_conversion.AssetClass.COMMODITIES], None),
            ],
            get_json,
            None,
        ),
        (
            partial(rdc.historical_pricing.events.Definition, universe="universe"),
            "fields",
            "fields",
            [
                ("BID", "BID%2CDATE_TIME"),
                (["BID", "ASK"], "BID%2CASK%2CDATE_TIME"),
            ],
            get_query_params_from_url,
            None,
        ),
        (
            partial(rdc.historical_pricing.summaries.Definition, universe="universe"),
            "fields",
            "fields",
            [
                ("BID", "BID%2CDATE"),
                (["BID", "ASK"], "BID%2CASK%2CDATE"),
            ],
            get_query_params_from_url,
            None,
        ),
        (
            partial(rd._qpl.fx_swp_to_swp, fx_cross_code=""),
            "tenors",
            "tenors",
            [
                ("1M", ["1M"]),
                (["1M"], ["1M"]),
            ],
            get_json,
            None,
        ),
        (
            partial(rd._qpl.fx_swp_to_swp, fx_cross_code=""),
            "fields",
            "fields",
            [
                ("OutrightCcy1Ccy2Bid", ["OutrightCcy1Ccy2Bid"]),
                (["OutrightCcy1Ccy2Bid"], ["OutrightCcy1Ccy2Bid"]),
            ],
            get_json,
            None,
        ),
    ],
)
def test_list_of_items_get_data_one_request(
    definition, arg_name, request_param_name, test_data, func_get_params, response
):
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    for input_value, expected_value in test_data:
        assert_list_of_items_in_one_request(
            session, request_param_name, expected_value, func_get_params, response
        )
        params = {arg_name: input_value}
        try:
            obj = definition(**params)
            if hasattr(obj, "get_data"):
                obj.get_data(session=session)
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute '_get_enum_parameter'":
                continue
            else:
                raise e

    rd.session.set_default(None)


def assert_list_of_items_in_one_request(
    session, request_param_name, test_result, func_get_params, response
):
    session.http_request = make_checker(
        request_param_name, test_result, func_get_params, response
    )


def make_checker_multi_request(expected_values):
    if not isinstance(expected_values, list):
        expected_values = [expected_values]
    expected_values = iter(expected_values)

    def http_request(request, *args, **kwargs):
        url = request.url
        if url.endswith("S%29Instrument.UUID-0000"):
            return StubResponse()

        value = url.rsplit("/", 1)[-1]
        assert value == next(expected_values)

        return StubResponse([{"data": [{}]}])

    return http_request


def make_get_data_bulk(key, value):
    def get_data(*args, **kwargs):
        assert kwargs[key] == value

    return get_data


@pytest.mark.parametrize(
    ("definition", "param_name", "attribute_name", "test_values"),
    [
        (
            rdc.trade_data_service.Definition,
            "universe",
            "_universe",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
        ),
        (
            partial(rdc.trade_data_service.Definition, universe="universe"),
            "fields",
            "_fields",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
        ),
        (
            partial(rdc.trade_data_service.Definition, universe="universe"),
            "filters",
            "_filters",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
        ),
        (
            partial(rd.delivery.omm_stream.Definition, name="universe"),
            "fields",
            "_fields",
            [
                ("val1", ["val1"]),
                (["val1", "val2"], ["val1", "val2"]),
            ],
        ),
        (
            partial(
                rd.delivery.rdp_stream.Definition,
                service="service",
                view="view",
                parameters={},
                api="",
            ),
            "universe",
            "_universe",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
        ),
        (
            partial(
                rd.delivery.rdp_stream.Definition,
                universe="universe",
                service="service",
                parameters={},
                api="",
            ),
            "view",
            "_view",
            [
                ("val1", "val1"),
                (["val1", "val2"], ["val1", "val2"]),
            ],
        ),
        (
            rdc.custom_instruments.Definition,
            "universe",
            "_universe",
            [
                ("val1", ["S)val1."]),
                (["val1", "val2"], ["S)val1.", "S)val2."]),
            ],
        ),
    ],
)
def test_list_of_items_stream(definition, param_name, attribute_name, test_values):
    session = StubSession(is_open=True)
    for test_item in test_values:
        test_value, expected_value = test_item
        stream = definition(**{param_name: test_value}).get_stream(session)
        assert getattr(stream, attribute_name) == expected_value


@pytest.mark.parametrize(
    ("definition", "test_values"),
    [
        (
            rdc.custom_instruments.events.Definition,
            (
                ("universe", "S%29universe."),
                (["universe1", "universe2"], ["S%29universe1.", "S%29universe2."]),
            ),
        ),
        (
            rdc.custom_instruments.summaries.Definition,
            (
                ("universe", "S%29universe."),
                (["universe1", "universe2"], ["S%29universe1.", "S%29universe2."]),
            ),
        ),
        (
            rdc.historical_pricing.events.Definition,
            (
                ("universe", "universe"),
                (["universe1", "universe2"], ["universe1", "universe2"]),
            ),
        ),
        (
            rdc.historical_pricing.summaries.Definition,
            (
                ("universe", "universe"),
                (["universe1", "universe2"], ["universe1", "universe2"]),
            ),
        ),
    ],
)
def test_list_of_items_multi_requests(definition, test_values):
    session = StubSession(is_open=True)
    for test_value in test_values:
        value, expected_result = test_value
        assert_list_of_items_in_multi_request(session, expected_result)
        definition(value).get_data(session=session)


def assert_list_of_items_in_multi_request(session, expected_result):
    session.http_request = make_checker_multi_request(expected_result)


@pytest.mark.parametrize(
    ("params", "param_name", "expected_result"),
    [
        ({"universe": "val1"}, "universe", ["val1"]),
        ({"universe": "universe", "fields": "val1"}, "fields", ["val1"]),
        (
            {"universe": "universe", "fields": ["val1", "val2"]},
            "fields",
            ["val1", "val2"],
        ),
        ({"universe": ["val1", "val2"]}, "universe", ["val1", "val2"]),
    ],
)
def test_bulk_list_of_items(params, param_name, expected_result):
    from refinitiv.data import _configure

    _configure.set_param(
        "bulk.esg.test",
        {
            "db": {
                "connection": {
                    "module": "sqlite3",
                    "parameters": {"database": "file::memory:"},
                }
            },
            "package": {
                "bucket": "test",
                "name": "test",
                "download": {
                    "path": "...",
                },
            },
        },
        True,
    )
    definition = rdc.esg.bulk.Definition("esg.test", **params)
    assert_bulk_list_of_items(definition, param_name, expected_result)
    definition.get_db_data()


def assert_bulk_list_of_items(definition, param_name, expected_result):
    definition._db_manager.get_data = make_get_data_bulk(param_name, expected_result)
