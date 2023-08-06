import pytest
from refinitiv.data.content.ownership.fund import (
    breakdown,
    concentration,
    holdings,
    investors,
    recent_activity,
    shareholders_history_report,
    shareholders_report,
    top_n_concentration,
)


def test_breakdown():
    try:
        definition = breakdown.Definition(universe="", stat_type=1)
    except Exception as e:
        assert False, str(e)


def test_concentration():
    try:
        definition = concentration.Definition(universe="")
    except Exception as e:
        assert False, str(e)


def test_holdings():
    try:
        definition = holdings.Definition(universe="")
    except Exception as e:
        assert False, str(e)


def test_investors():
    try:
        definition = investors.Definition(universe="")
    except Exception as e:
        assert False, str(e)


def test_recent_activity():
    try:
        definition = recent_activity.Definition(universe="", sort_order="asc")
    except Exception as e:
        assert False, str(e)


def test_shareholders_history_report():
    try:
        definition = shareholders_history_report.Definition(universe="", frequency="Q")
    except Exception as e:
        assert False, str(e)


def test_shareholders_history_report_universe_is_list():
    with pytest.raises(ValueError):
        definition = shareholders_history_report.Definition(universe=[], frequency="Q")


def test_shareholders_report():
    try:
        definition = shareholders_report.Definition(universe="")
    except Exception as e:
        assert False, str(e)


def test_top_n_concentration():
    try:
        definition = top_n_concentration.Definition(universe="", count=10)
    except Exception as e:
        assert False, str(e)
