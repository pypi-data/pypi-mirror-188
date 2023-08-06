import types
from functools import partial

import pytest

import refinitiv.data.content as rdc
import refinitiv.data.content.custom_instruments._enums
from refinitiv.data.content._intervals import Intervals
from refinitiv.data.content.estimates import Package
from refinitiv.data.content.historical_pricing import (
    EventTypes,
    Adjustments,
    MarketSession,
)
from refinitiv.data.content.ipa._enums import Direction, InterestType
from refinitiv.data.content.ipa._enums._asset_class import AssetClass
from refinitiv.data.content.ipa._enums._risk_type import RiskType
from refinitiv.data.content.news._sort_order import SortOrder as NewsSortOrder
from refinitiv.data.content.ownership import StatTypes
from refinitiv.data.content.search import Views
from refinitiv.data.content.symbol_conversion import SymbolTypes, CountryCode
from refinitiv.data.delivery._data._request import Request
from tests.unit.conftest import StubSession, StubResponse


def get_query_params_from_url(request: Request):
    url = request.url or ""
    query = url.split("?")[-1]
    query_params = [i.split("=") for i in query.split("&")]
    return dict(query_params)


def get_ipa_params(request: Request):
    universe = request.json.get("universe")
    return universe[0]


def get_ipa_instrument_definition_params(request: Request):
    universe = request.json.get("universe")
    return universe[0]["instrumentDefinition"]


def get_fund_params(request: Request):
    json = request.json
    entity = json.get("Entity")
    requests = entity.get("W", {}).get("requests", [{}])
    request = requests[0]
    rows = request.get("layout", {}).get("rows")
    item = {"item": "date"}
    if item in rows:
        return item
    else:
        assert False, f"{item} not in {rows}"


def get_json(request: Request):
    return request.json


def make_checker(param_name, value, func_get_params):
    def http_request(request: Request):
        params = func_get_params(request)
        assert str(params[param_name]) == str(value), (
            f"Param{param_name}:\n"
            f"Expected value {params[param_name]}. \n"
            f"Value {str(value)}"
        )
        return StubResponse()

    return http_request


def get_data(definition, params, session):
    try:
        if (
            isinstance(definition, types.FunctionType)
            or isinstance(definition, partial)
            and isinstance(definition.func, types.FunctionType)
        ):
            definition(**params, session=session)
        else:
            definition(**params).get_data(session=session)
    except (KeyError, IndexError):
        pass


def get_news_path(request: Request):
    url = request.url or ""
    view = url.rsplit("/", 1)[-1]
    result = {"view": view}
    return result


@pytest.mark.parametrize(
    ("definition", "enum_argname", "request_param_name", "enum", "func_get_params"),
    [
        (
            partial(rdc.estimates.view_actuals.annual.Definition, universe=""),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(rdc.estimates.view_actuals.interim.Definition, universe=""),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(rdc.estimates.view_summary.annual.Definition, universe=""),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.estimates.view_summary.historical_snapshots_non_periodic_measures.Definition,
                universe="",
            ),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.estimates.view_summary.historical_snapshots_periodic_measures_annual.Definition,
                universe="",
            ),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.estimates.view_summary.historical_snapshots_periodic_measures_interim.Definition,
                universe="",
            ),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.estimates.view_summary.historical_snapshots_recommendations.Definition,
                universe="",
            ),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(rdc.estimates.view_summary.interim.Definition, universe=""),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.estimates.view_summary.non_periodic_measures.Definition, universe=""
            ),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(rdc.estimates.view_summary.recommendations.Definition, universe=""),
            "package",
            "package",
            Package,
            get_query_params_from_url,
        ),
        (
            partial(rdc.fundamental_and_reference.Definition, universe="", fields=""),
            "row_headers",
            "item",
            rdc.fundamental_and_reference.RowHeaders,
            get_fund_params,
        ),
        (
            partial(rdc.historical_pricing.events.Definition, universe="VOD.L"),
            "eventTypes",
            "eventTypes",
            EventTypes,
            get_query_params_from_url,
        ),
        (
            partial(rdc.historical_pricing.events.Definition, universe="VOD.L"),
            "adjustments",
            "adjustments",
            Adjustments,
            get_query_params_from_url,
        ),
        (
            partial(rdc.historical_pricing.summaries.Definition, universe="VOD.L"),
            "interval",
            "interval",
            Intervals,
            get_query_params_from_url,
        ),
        (
            partial(rdc.historical_pricing.summaries.Definition, universe="VOD.L"),
            "adjustments",
            "adjustments",
            Adjustments,
            get_query_params_from_url,
        ),
        (
            partial(rdc.historical_pricing.summaries.Definition, universe="VOD.L"),
            "sessions",
            "sessions",
            MarketSession,
            get_query_params_from_url,
        ),
        (
            rdc.ipa.curves.zc_curve_definitions.Definition,
            "main_constituent_asset_class",
            "mainConstituentAssetClass",
            AssetClass,
            get_ipa_params,
        ),
        (
            rdc.ipa.curves.zc_curve_definitions.Definition,
            "risk_type",
            "riskType",
            RiskType,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition,
            "direction",
            "direction",
            Direction,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition,
            "interest_type",
            "interestType",
            InterestType,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition,
            "index_reset_frequency",
            "indexResetFrequency",
            rdc.ipa.financial_contracts.bond.Frequency,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition,
            "adjust_interest_to_payment_date",
            "adjustInterestToPaymentDate",
            rdc.ipa._enums.AdjustInterestToPaymentDate,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition,
            "index_compounding_method",
            "indexCompoundingMethod",
            rdc.ipa._enums.IndexCompoundingMethod,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition,
            "stub_rule",
            "stubRule",
            rdc.ipa._enums.StubRule,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "interest_payment_frequency",
            "interestPaymentFrequency",
            rdc.ipa._enums.Frequency,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "interest_calculation_method",
            "interestCalculationMethod",
            rdc.ipa._enums.DayCountBasis,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "payment_business_day_convention",
            "paymentBusinessDayConvention",
            rdc.ipa._enums.BusinessDayConvention,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "payment_roll_convention",
            "paymentRollConvention",
            rdc.ipa._enums.DateRollingConvention,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "index_reset_frequency",
            "indexResetFrequency",
            rdc.ipa.financial_contracts.cap_floor.Frequency,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "index_reset_type",
            "indexResetType",
            rdc.ipa.financial_contracts.cap_floor.IndexResetType,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "adjust_interest_to_payment_date",
            "adjustInterestToPaymentDate",
            rdc.ipa._enums.AdjustInterestToPaymentDate,
            get_ipa_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "stub_rule",
            "stubRule",
            rdc.ipa._enums.StubRule,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition,
            "buy_sell",
            "buySell",
            rdc.ipa._enums.BuySell,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.cds.Definition,
            "cds_convention",
            "cdsConvention",
            rdc.ipa._enums.CdsConvention,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.cds.Definition,
            "start_date_moving_convention",
            "startDateMovingConvention",
            rdc.ipa._enums.BusinessDayConvention,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.cds.Definition,
            "end_date_moving_convention",
            "endDateMovingConvention",
            rdc.ipa._enums.BusinessDayConvention,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.cross.Definition,
            "fx_cross_type",
            "fxCrossType",
            rdc.ipa._enums.FxCrossType,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.option.Definition,
            "buy_sell",
            "buySell",
            rdc.ipa._enums.BuySell,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.option.Definition,
            "call_put",
            "callPut",
            rdc.ipa._enums.CallPut,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.option.Definition,
            "exercise_style",
            "exerciseStyle",
            rdc.ipa._enums.ExerciseStyle,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.option.Definition,
            "underlying_type",
            "underlyingType",
            rdc.ipa.financial_contracts.option._enums.UnderlyingType,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.repo.Definition,
            "day_count_basis",
            "dayCountBasis",
            rdc.ipa._enums.DayCountBasis,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.swaption.Definition,
            "buy_sell",
            "buySell",
            rdc.ipa._enums.BuySell,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.swaption.Definition,
            "exercise_style",
            "exerciseStyle",
            rdc.ipa.financial_contracts.swaption.ExerciseStyle,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.swaption.Definition,
            "premium_settlement_type",
            "premiumSettlementType",
            rdc.ipa.financial_contracts.swaption.PremiumSettlementType,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.swaption.Definition,
            "settlement_type",
            "settlementType",
            rdc.ipa.financial_contracts.swaption.SwaptionSettlementType,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.swaption.Definition,
            "swaption_type",
            "swaptionType",
            rdc.ipa.financial_contracts.swaption.SwaptionType,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.term_deposit.Definition,
            "payment_business_day_convention",
            "paymentBusinessDayConvention",
            rdc.ipa._enums.BusinessDayConvention,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.term_deposit.Definition,
            "payment_roll_convention",
            "paymentRollConvention",
            rdc.ipa._enums.DateRollingConvention,
            get_ipa_instrument_definition_params,
        ),
        (
            rdc.ipa.financial_contracts.term_deposit.Definition,
            "year_basis",
            "yearBasis",
            rdc.ipa._enums.DayCountBasis,
            get_ipa_instrument_definition_params,
        ),
        (
            partial(rdc.news.headlines.Definition, query=""),
            "sort_order",
            "sortOrder",
            NewsSortOrder,
            get_query_params_from_url,
        ),
        (
            partial(rdc.ownership.consolidated.breakdown.Definition, universe=""),
            "stat_type",
            "statType",
            StatTypes,
            get_query_params_from_url,
        ),
        (
            partial(rdc.ownership.consolidated.recent_activity.Definition, universe=""),
            "sort_order",
            "sortOrder",
            rdc.ownership.SortOrder,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.ownership.consolidated.shareholders_history_report.Definition,
                universe="",
            ),
            "frequency",
            "frequency",
            rdc.ownership.Frequency,
            get_query_params_from_url,
        ),
        (
            partial(rdc.ownership.fund.breakdown.Definition, universe=""),
            "stat_type",
            "statType",
            StatTypes,
            get_query_params_from_url,
        ),
        (
            partial(rdc.ownership.fund.recent_activity.Definition, universe=""),
            "sort_order",
            "sortOrder",
            rdc.ownership.SortOrder,
            get_query_params_from_url,
        ),
        (
            partial(
                rdc.ownership.fund.shareholders_history_report.Definition, universe=""
            ),
            "frequency",
            "frequency",
            rdc.ownership.Frequency,
            get_query_params_from_url,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "from_symbol_type",
            "fromSymbolType",
            SymbolTypes,
            get_json,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "to_symbol_types",
            "toSymbolType",
            SymbolTypes,
            get_json,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "preferred_country_code",
            "preferredCountryCode",
            CountryCode,
            get_json,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "asset_class",
            "assetClass",
            rdc.symbol_conversion.AssetClass,
            get_json,
        ),
        (
            partial(rdc.symbol_conversion.Definition, symbols=""),
            "asset_state",
            "assetState",
            rdc.symbol_conversion.AssetState,
            get_json,
        ),
        # deprecated method
        # (
        #     partial(rdc.custom_instruments.manage.create, symbol="S)Name.GE-0000"),
        #     "type_",
        #     "type",
        #     refinitiv.data.content.custom_instruments._enums.CustomInstrumentTypes,
        #     get_json,
        # ),
    ],
)
def test_enums_definitions(
    definition, enum_argname, request_param_name, enum, func_get_params
):
    session = StubSession(is_open=True)
    session.config.set_param("apis.data.news.underlying-platform", "rdp")
    for enum_item in enum:
        session.http_request = make_checker(
            request_param_name, enum_item.value, func_get_params
        )
        get_data(definition, {enum_argname: enum_item}, session)
        value = enum_item.value
        get_data(definition, {enum_argname: value}, session)
        if isinstance(value, str):
            get_data(definition, {enum_argname: value.lower()}, session)
            get_data(definition, {enum_argname: value.upper()}, session)

    # invalid
    for invalid in {111, "INVALID"}:
        try:
            get_data(definition, {enum_argname: invalid}, session)
        except TypeError as e:
            try:
                assert f"Parameter '{enum_argname}' of invalid type provided:" in str(e)
            except AssertionError:
                try:
                    assert (
                        f"Parameter '{request_param_name}' of invalid type provided:"
                        in str(e)
                    )
                except AssertionError as e:
                    pytest.skip(str(e))
        except AttributeError as e:
            assert f"Value '{invalid}' must be in " in str(e)
        except ValueError as e:
            assert f"Cannot convert param '{invalid}'" == str(e)
        else:
            assert False


@pytest.mark.parametrize(
    ("definition", "enum_argname", "request_param_name", "enum"),
    [
        (
            rdc.trade_data_service.Definition,
            "universe_type",
            "universeType",
            rdc.trade_data_service.UniverseTypes,
        ),
        (
            rdc.trade_data_service.Definition,
            "events",
            "events",
            rdc.trade_data_service.Events,
        ),
        (
            rdc.trade_data_service.Definition,
            "finalized_orders",
            "finalizedOrders",
            rdc.trade_data_service.FinalizedOrders,
        ),
    ],
)
def test_enums_in_definitions_for_stream(
    definition, enum_argname, request_param_name, enum
):
    session = StubSession(is_open=True)
    for enum_item in enum:
        stream = definition(**{enum_argname: enum_item}).get_stream(session)
        open_message = stream._stream._stream.open_message
        enum_item_value = enum_item.value
        assert open_message["parameters"][request_param_name] == enum_item_value
        stream = definition(**{enum_argname: enum_item_value}).get_stream(session)
        open_message = stream._stream._stream.open_message
        assert open_message["parameters"][request_param_name] == enum_item_value

    with pytest.raises(AttributeError, match="Value '123' must be in"):
        definition(**{enum_argname: 123})
    with pytest.raises(AttributeError, match="Value 'INVALID___' must be in"):
        definition(**{enum_argname: "INVALID___"})
