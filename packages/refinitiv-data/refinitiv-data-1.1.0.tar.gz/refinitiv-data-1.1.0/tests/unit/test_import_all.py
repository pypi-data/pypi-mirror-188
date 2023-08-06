import pytest
import refinitiv.data as rd
from types import ModuleType

testing_modules = [
    rd,
    rd.content,
    rd.content.custom_instruments,
    rd.content.custom_instruments.events,
    rd.content.custom_instruments.manage,
    rd.content.custom_instruments.search,
    rd.content.custom_instruments.summaries,
    rd.dates_and_calendars,
    rd.news,
    rd.content.esg,
    rd.content.esg.basic_overview,
    rd.content.esg.bulk,
    rd.content.esg.full_measures,
    rd.content.esg.full_scores,
    rd.content.esg.standard_measures,
    rd.content.esg.standard_scores,
    rd.content.esg.universe,
    rd.content.estimates,
    rd.content.estimates.view_actuals,
    rd.content.estimates.view_actuals.annual,
    rd.content.estimates.view_actuals.interim,
    rd.content.estimates.view_actuals_kpi,
    rd.content.estimates.view_actuals_kpi.annual,
    rd.content.estimates.view_actuals_kpi.interim,
    rd.content.estimates.view_summary,
    rd.content.estimates.view_summary.annual,
    rd.content.estimates.view_summary.historical_snapshots_non_periodic_measures,
    rd.content.estimates.view_summary.historical_snapshots_periodic_measures_annual,
    rd.content.estimates.view_summary.historical_snapshots_periodic_measures_interim,
    rd.content.estimates.view_summary.historical_snapshots_recommendations,
    rd.content.estimates.view_summary.interim,
    rd.content.estimates.view_summary.non_periodic_measures,
    rd.content.estimates.view_summary.recommendations,
    rd.content.estimates.view_summary_kpi,
    rd.content.estimates.view_summary_kpi.annual,
    rd.content.estimates.view_summary_kpi.historical_snapshots_kpi,
    rd.content.estimates.view_summary_kpi.interim,
    rd.content.filings,
    rd.content.filings.retrieval,
    rd.content.filings.search,
    rd.content.fundamental_and_reference,
    rd.content.historical_pricing,
    rd.content.historical_pricing.events,
    rd.content.historical_pricing.summaries,
    rd.content.ipa,
    rd.content.ipa.curves,
    rd.content.ipa.curves.forward_curves,
    rd.content.ipa.curves.zc_curve_definitions,
    rd.content.ipa.curves.zc_curves,
    rd.content.ipa.dates_and_calendars,
    rd.content.ipa.dates_and_calendars.add_periods,
    rd.content.ipa.dates_and_calendars.count_periods,
    rd.content.ipa.dates_and_calendars.date_schedule,
    rd.content.ipa.dates_and_calendars.holidays,
    rd.content.ipa.dates_and_calendars.is_working_day,
    rd.content.ipa.financial_contracts,
    rd.content.ipa.financial_contracts.bond,
    rd.content.ipa.financial_contracts.cap_floor,
    rd.content.ipa.financial_contracts.cds,
    rd.content.ipa.financial_contracts.cross,
    rd.content.ipa.financial_contracts.option,
    rd.content.ipa.financial_contracts.repo,
    rd.content.ipa.financial_contracts.swap,
    rd.content.ipa.financial_contracts.swaption,
    rd.content.ipa.financial_contracts.term_deposit,
    rd.content.ipa.surfaces,
    rd.content.ipa.surfaces.cap,
    rd.content.ipa.surfaces.eti,
    rd.content.ipa.surfaces.fx,
    rd.content.ipa.surfaces.swaption,
    rd.content.news,
    rd.content.news.headlines,
    rd.content.news.story,
    rd.content.news.top_news,
    rd.content.news.top_news.hierarchy,
    rd.content.news.images,
    rd.content.ownership,
    rd.content.ownership.consolidated,
    rd.content.ownership.consolidated.breakdown,
    rd.content.ownership.consolidated.concentration,
    rd.content.ownership.consolidated.investors,
    rd.content.ownership.consolidated.recent_activity,
    rd.content.ownership.consolidated.shareholders_history_report,
    rd.content.ownership.consolidated.shareholders_report,
    rd.content.ownership.consolidated.top_n_concentration,
    rd.content.ownership.fund,
    rd.content.ownership.fund.breakdown,
    rd.content.ownership.fund.concentration,
    rd.content.ownership.fund.holdings,
    rd.content.ownership.fund.investors,
    rd.content.ownership.fund.recent_activity,
    rd.content.ownership.fund.shareholders_history_report,
    rd.content.ownership.fund.shareholders_report,
    rd.content.ownership.fund.top_n_concentration,
    rd.content.ownership.insider,
    rd.content.ownership.insider.shareholders_report,
    rd.content.ownership.insider.transaction_report,
    rd.content.ownership.investor,
    rd.content.ownership.investor.holdings,
    rd.content.ownership.org_info,
    rd.content.pricing,
    rd.content.pricing.chain,
    rd.content.search,
    rd.content.search.lookup,
    rd.content.search.metadata,
    rd.content.symbol_conversion,
    rd.content.trade_data_service,
    rd.delivery,
    rd.delivery.cfs,
    rd.delivery.cfs.buckets,
    rd.delivery.cfs.file_downloader,
    rd.delivery.cfs.file_sets,
    rd.delivery.cfs.files,
    rd.delivery.cfs.packages,
    rd.delivery.endpoint_request,
    rd.delivery.omm_stream,
    rd.delivery.rdp_stream,
    rd.eikon,
    rd.errors,
    rd.discovery,
    rd.session,
    rd.session.desktop,
    rd.session.platform,
    rd.usage_collection,
]


@pytest.mark.parametrize("module", testing_modules)
def test_import_all(module):
    """Test that __all__ contains only names that are actually exported."""
    missing = set(n for n in module.__all__ if getattr(module, n, None) is None)
    assert not missing, f"__all__ contains unresolved names: {', '.join(missing)}"


def test_number_modules():
    counter = 0

    def count_module(pack):
        nonlocal counter
        for s in dir(pack):
            if s.startswith("_"):
                continue

            attr = getattr(pack, s)

            if isinstance(attr, ModuleType):
                counter += 1
                count_module(attr)

    # given
    expected_number = 124

    # when
    count_module(rd)
    existing_number = counter + 1  # 1 for rd
    testing_number = len(testing_modules)

    # then
    assert existing_number == expected_number, existing_number
    assert testing_number == existing_number, testing_number
