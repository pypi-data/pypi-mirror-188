import pandas as pd
import pytest

import refinitiv.data.content as rdc
from refinitiv.data._core.session import SessionType
from refinitiv.data.content import estimates
from refinitiv.data.content import ownership
from refinitiv.data.content import search

from tests.unit.conftest import StubSession, args, StubResponse, StubConfig
from tests.unit.content.data_for_tests import (
    NEWS_STORY_RESPONSE,
    FUNDAMENTAL_AND_REFERENCE_DEFINITION,
    NEWS_HEADLINES_DEFINITION,
    NEWS_HEADLINES_RESPONSE,
    NEWS_STORY_DEFINITION,
    SURFACES_DEFINITION,
    SURFACE_SWAPTION_DEFINITION,
    SURFACE_SWAPTION_RESPONSE,
    SURFACES_RESPONSE,
    PRICING_DEFINITION,
    PRICING_RESPONSE,
    FORWARD_CURVE_RESPONSE,
    FORWARD_CURVES_RESPONSE,
    ZC_CURVE_RESPONSE,
    ZC_CURVE_DEFINITION_RESPONSE,
    ZC_CURVE_DEFINITIONS_RESPONSE,
    ZC_CURVES_RESPONSE,
    SURFACE_CAP_DEFINITION,
    SURFACE_CAP_RESPONSE,
    SURFACE_ETI_DEFINITION,
    SURFACE_ETI_RESPONSE,
    SURFACE_FX_DEFINITION,
    SURFACE_FX_RESPONSE,
    NEWS_HEADLINES_RESPONSE_UDF,
    FUNDAMENTAL_AND_REFERENCE_RESPONSE_DESKTOP,
    FUNDAMENTAL_AND_REFERENCE_RESPONSE_PLATFORM,
)


def assert_create_df_on_demand(response):
    assert response.data._dataframe is None

    # when
    df = response.data.df

    # then
    assert df is not None
    assert isinstance(response.data._dataframe, pd.DataFrame)


def assert_create_df_immediately(response):
    assert response.data._dataframe is not None

    # when
    df = response.data.df

    # then
    assert df is not None
    assert isinstance(response.data._dataframe, pd.DataFrame)


def assert_create_empty_df(response):
    assert response.data._dataframe is None

    # when
    df = response.data.df

    # then
    assert df is not None
    assert isinstance(response.data._dataframe, pd.DataFrame)
    assert df.empty


@pytest.mark.parametrize(
    argnames="definition",
    ids=[
        "custom_instruments.search.Definition",
        "esg.basic_overview.Definition",
        "esg.full_measures.Definition",
        "esg.full_scores.Definition",
        "esg.standard_measures.Definition",
        "esg.standard_scores.Definition",
        "esg.universe.Definition",
        "estimates.view_actuals.annual.Definition",
        "estimates.view_actuals.interim.Definition",
        "estimates.view_actuals_kpi.annual.Definition",
        "estimates.view_actuals_kpi.interim.Definition",
        "estimates.view_summary.annual.Definition",
        "estimates.view_summary.historical_snapshots_non_periodic_measures.Definition",
        "estimates.view_summary.historical_snapshots_periodic_measures_annual.Definition",
        "estimates.view_summary.historical_snapshots_periodic_measures_interim.Definition",
        "estimates.view_summary.historical_snapshots_recommendations.Definition",
        "estimates.view_summary.interim.Definition",
        "estimates.view_summary.non_periodic_measures.Definition",
        "estimates.view_summary.recommendations.Definition",
        "estimates.view_summary_kpi.annual.Definition",
        "estimates.view_summary_kpi.historical_snapshots_kpi.Definition",
        "estimates.view_summary_kpi.interim.Definition",
        "ownership.consolidated.breakdown.Definition",
        "ownership.consolidated.concentration.Definition",
        "ownership.consolidated.investors.Definition",
        "ownership.consolidated.recent_activity.Definition",
        "ownership.consolidated.shareholders_history_report.Definition",
        "ownership.consolidated.shareholders_report.Definition",
        "ownership.consolidated.top_n_concentration.Definition",
        "ownership.fund.breakdown.Definition",
        "ownership.fund.concentration.Definition",
        "ownership.fund.holdings.Definition",
        "ownership.fund.investors.Definition",
        "ownership.fund.recent_activity.Definition",
        "ownership.fund.shareholders_history_report.Definition",
        "ownership.fund.shareholders_report.Definition",
        "ownership.fund.top_n_concentration.Definition",
        "ownership.insider.shareholders_report.Definition",
        "ownership.insider.transaction_report.Definition",
        "ownership.investor.holdings.Definition",
        "ownership.org_info.Definition",
        "search.Definition",
        "search.lookup.Definition",
        "search.metadata.Definition",
        "symbol_conversion.Definition",
    ],
    argvalues=[
        # <editor-fold desc="custom_instruments">
        rdc.custom_instruments.search.Definition("VOD.L"),
        # </editor-fold>
        # <editor-fold desc="esg">
        rdc.esg.basic_overview.Definition("IBM.N"),
        rdc.esg.full_measures.Definition("BNPP.PA"),
        rdc.esg.full_scores.Definition(universe="4295904307", start=0, end=-5),
        rdc.esg.standard_measures.Definition("BNPP.PA"),
        rdc.esg.standard_scores.Definition("6758.T"),
        rdc.esg.universe.Definition(),
        # </editor-fold>
        # <editor-fold desc="estimates">
        rdc.estimates.view_actuals.annual.Definition("IBM.N", estimates.Package.BASIC),
        rdc.estimates.view_actuals.interim.Definition("IBM.N", estimates.Package.BASIC),
        rdc.estimates.view_actuals_kpi.annual.Definition("BNPP.PA"),
        rdc.estimates.view_actuals_kpi.interim.Definition("BNPP.PA"),
        rdc.estimates.view_summary.annual.Definition("IBM.N", estimates.Package.BASIC),
        rdc.estimates.view_summary.historical_snapshots_non_periodic_measures.Definition(
            "IBM.N", estimates.Package.BASIC
        ),
        rdc.estimates.view_summary.historical_snapshots_periodic_measures_annual.Definition(
            "IBM.N", estimates.Package.BASIC
        ),
        rdc.estimates.view_summary.historical_snapshots_periodic_measures_interim.Definition(
            "IBM.N", estimates.Package.BASIC
        ),
        rdc.estimates.view_summary.historical_snapshots_recommendations.Definition(
            "IBM.N", estimates.Package.BASIC
        ),
        rdc.estimates.view_summary.interim.Definition("IBM.N", estimates.Package.BASIC),
        rdc.estimates.view_summary.non_periodic_measures.Definition(
            "IBM.N", estimates.Package.BASIC
        ),
        rdc.estimates.view_summary.recommendations.Definition(
            "IBM.N", estimates.Package.BASIC
        ),
        rdc.estimates.view_summary_kpi.annual.Definition("ORCL.N"),
        rdc.estimates.view_summary_kpi.historical_snapshots_kpi.Definition("BNPP.PA"),
        rdc.estimates.view_summary_kpi.interim.Definition("BNPP.PA"),
        # </editor-fold>
        # <editor-fold desc="ownership">
        rdc.ownership.consolidated.breakdown.Definition(
            "TRI.N", ownership.StatTypes.INVESTOR_TYPE
        ),
        rdc.ownership.consolidated.concentration.Definition("TRI.N"),
        rdc.ownership.consolidated.investors.Definition("TRI.N"),
        rdc.ownership.consolidated.recent_activity.Definition("TRI.N", "asc"),
        rdc.ownership.consolidated.shareholders_history_report.Definition(
            "TRI.N", ownership.Frequency.MONTHLY
        ),
        rdc.ownership.consolidated.shareholders_report.Definition("TRI.N"),
        rdc.ownership.consolidated.top_n_concentration.Definition("TRI.N", 30),
        rdc.ownership.fund.breakdown.Definition(
            "TRI.N", ownership.StatTypes.INVESTOR_TYPE
        ),
        rdc.ownership.fund.concentration.Definition("TRI.N"),
        rdc.ownership.fund.holdings.Definition("LP40189339"),
        rdc.ownership.fund.investors.Definition("TRI.N"),
        rdc.ownership.fund.recent_activity.Definition(
            "TRI.N", ownership.SortOrder.ASCENDING
        ),
        rdc.ownership.fund.shareholders_history_report.Definition(
            "TRI.N", "M", start="-1Q"
        ),
        rdc.ownership.fund.shareholders_report.Definition("TRI.N"),
        rdc.ownership.fund.top_n_concentration.Definition("TRI.N", 30),
        rdc.ownership.insider.shareholders_report.Definition("TRI.N"),
        rdc.ownership.insider.transaction_report.Definition("TRI.N", start="-1Q"),
        rdc.ownership.investor.holdings.Definition("TRI.N"),
        rdc.ownership.org_info.Definition("TRI.N"),
        # </editor-fold>
        # <editor-fold desc="search">
        rdc.search.Definition(query="cfo", view=search.Views.PEOPLE),
        rdc.search.lookup.Definition(
            view=search.Views.SEARCH_ALL,
            scope="RIC",
            terms="A,B,NOSUCHRIC,C,D",
            select="BusinessEntity,DocumentTitle",
        ),
        rdc.search.metadata.Definition(search.Views.PEOPLE),
        # </editor-fold>
        # <editor-fold desc="symbol_conversion">
        rdc.symbol_conversion.Definition(["US5949181045", "US02079K1079"]),
        # </editor-fold>
    ],
)
def test_creating_df_on_demand_simple(definition):
    # given
    session = StubSession(is_open=True)
    response = definition.get_data(session)

    assert_create_df_on_demand(response)


@pytest.mark.parametrize(
    argnames="definition,response",
    ids=[
        "historical_pricing.events",
        "historical_pricing.summaries",
        "ipa.curves.forward_curves",
        "ipa.curves.zc_curve_definitions",
        "ipa.curves.zc_curves",
        "ipa.financial_contracts.bond",
        "ipa.financial_contracts.cap_floor",
        "ipa.financial_contracts.cds",
        "ipa.financial_contracts.cross",
        "ipa.financial_contracts.option",
        "ipa.financial_contracts.repo",
        "ipa.financial_contracts.swap",
        "ipa.financial_contracts.swaption",
        "ipa.financial_contracts.term_deposit",
        "ipa.surfaces.cap",
        "ipa.surfaces.eti",
        "ipa.surfaces.fx",
        "ipa.surfaces.swaption",
        "ipa.surfaces",
        "pricing",
    ],
    argvalues=[
        # <editor-fold desc="ipa">
        args(
            definition=rdc.ipa.curves.forward_curves.Definition(),
            response=FORWARD_CURVE_RESPONSE,
        ),
        args(
            definition=rdc.ipa.curves.forward_curves.Definitions([]),
            response=FORWARD_CURVES_RESPONSE,
        ),
        args(
            definition=rdc.ipa.curves.zc_curves.Definition(), response=ZC_CURVE_RESPONSE
        ),
        args(
            definition=rdc.ipa.curves.zc_curve_definitions.Definition(),
            response=ZC_CURVE_DEFINITION_RESPONSE,
        ),
        args(
            definition=rdc.ipa.curves.zc_curve_definitions.Definitions([]),
            response=ZC_CURVE_DEFINITIONS_RESPONSE,
        ),
        args(
            definition=rdc.ipa.curves.zc_curves.Definitions([]),
            response=ZC_CURVES_RESPONSE,
        ),
        args(
            definition=rdc.ipa.financial_contracts.bond.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.cap_floor.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.cds.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.cross.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.option.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.repo.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.swap.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.swaption.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(
            definition=rdc.ipa.financial_contracts.term_deposit.Definition(),
            response=StubResponse({"data": [], "headers": []}),
        ),
        args(definition=SURFACE_CAP_DEFINITION, response=SURFACE_CAP_RESPONSE),
        args(definition=SURFACE_ETI_DEFINITION, response=SURFACE_ETI_RESPONSE),
        args(definition=SURFACE_FX_DEFINITION, response=SURFACE_FX_RESPONSE),
        args(
            definition=SURFACE_SWAPTION_DEFINITION, response=SURFACE_SWAPTION_RESPONSE
        ),
        args(definition=SURFACES_DEFINITION, response=SURFACES_RESPONSE),
        # </editor-fold>
        # <editor-fold desc="pricing">
        args(definition=PRICING_DEFINITION, response=PRICING_RESPONSE),
        # </editor-fold>
    ],
)
def test_creating_df_on_demand_complex(definition, response):
    # given
    session = StubSession(is_open=True, response=response)
    response = definition.get_data(session)

    assert_create_df_on_demand(response)


@pytest.mark.parametrize(
    argnames="definition,response",
    ids=[
        "historical_pricing.events",
        "historical_pricing.summaries",
        "custom_instruments.events",
        "custom_instruments.summaries",
    ],
    argvalues=[
        # <editor-fold desc="historical_pricing">
        args(
            definition=rdc.historical_pricing.events.Definition("EUR"),
            response=StubResponse(
                [{"headers": [{"name": "DATE"}], "data": [{}], "universe": {"ric": ""}}]
            ),
        ),
        args(
            definition=rdc.historical_pricing.summaries.Definition("EUR"),
            response=StubResponse(
                [{"headers": [{"name": "DATE"}], "data": [{}], "universe": {"ric": ""}}]
            ),
        ),
        # </editor-fold>
        # <editor-fold desc="custom_instruments">
        args(
            definition=rdc.custom_instruments.events.Definition("VOD.L"),
            response=StubResponse(
                [{"headers": [{"name": "DATE"}], "data": [{}], "universe": {"ric": ""}}]
            ),
        ),
        args(
            definition=rdc.custom_instruments.summaries.Definition("VOD.L"),
            response=StubResponse(
                [{"headers": [{"name": "DATE"}], "data": [{}], "universe": {"ric": ""}}]
            ),
        ),
        # </editor-fold>
    ],
)
def test_creating_df_on_demand_complex(definition, response):
    # given
    session = StubSession(is_open=True, response=response)
    response = definition.get_data(session)

    assert_create_df_on_demand(response)


@pytest.mark.parametrize(
    argnames="definition,response",
    ids=[
        "fundamental_and_reference",
        "news.headlines",
    ],
    argvalues=[
        args(
            definition=FUNDAMENTAL_AND_REFERENCE_DEFINITION,
            response=FUNDAMENTAL_AND_REFERENCE_RESPONSE_PLATFORM,
        ),
        args(definition=NEWS_HEADLINES_DEFINITION, response=NEWS_HEADLINES_RESPONSE),
    ],
)
def test_creating_df_on_demand_rdp(definition, response):
    # given
    platform = "rdp"
    config = StubConfig(
        {
            "apis.data.datagrid": {
                "url": "/data/datagrid/beta1",
                "underlying-platform": platform,
                "endpoints.standard": "/",
            },
            "apis.data.news": {"endpoints.headlines": "headlines/url", "url": "url"},
            "apis.data.news.underlying-platform": platform,
            "raise_exception_on_error": True,
        }
    )
    session = StubSession(is_open=True, response=response, config=config)
    response = definition.get_data(session=session)

    assert_create_df_on_demand(response)


@pytest.mark.parametrize(
    argnames="definition,response",
    ids=[
        "fundamental_and_reference",
        "news.headlines",
    ],
    argvalues=[
        args(
            definition=FUNDAMENTAL_AND_REFERENCE_DEFINITION,
            response=FUNDAMENTAL_AND_REFERENCE_RESPONSE_DESKTOP,
        ),
        args(
            definition=NEWS_HEADLINES_DEFINITION, response=NEWS_HEADLINES_RESPONSE_UDF
        ),
    ],
)
def test_creating_df_on_demand_udf(definition, response):
    # given
    platform = "udf"
    config = StubConfig(
        {
            "apis.data.datagrid": {
                "url": "/data/datagrid/beta1",
                "underlying-platform": platform,
                "endpoints.standard": "/",
            },
            "apis.data.news": {"endpoints.headlines": "headlines/url", "url": "url"},
            "apis.data.news.underlying-platform": platform,
            "raise_exception_on_error": True,
        }
    )
    session = StubSession(is_open=True, response=response, config=config)
    session.type = SessionType.DESKTOP
    response = definition.get_data(session=session)

    assert_create_df_on_demand(response)
