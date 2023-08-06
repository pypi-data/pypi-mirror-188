import pytest

import refinitiv.data as rd
from refinitiv.data._errors import RDError
from tests.unit.conftest import StubSession, StubFailedResponse


def test_search_definition():
    ############################################
    #   prepare things

    ############################################
    #   test
    definition = rd.content.search.Definition(query="foo")

    assert definition._query == "foo"

    #   check default value
    assert definition._view == rd.content.search.Views.SEARCH_ALL
    assert definition._top == 10
    assert definition._skip == 0
    assert definition._group_count == 3


def test_search_definition_with_boost_option():
    ############################################
    #   prepare things

    ############################################
    #   test
    filter = "RCSAssetTypeLeaf eq 'oil refinery' and RCSRegionLeaf eq 'Venezuela'"
    boost = "PlantStatus ne 'Normal Operation'"
    definition = rd.content.search.Definition(
        view=rd.content.search.Views.VESSEL_PHYSICAL_ASSETS,
        filter=filter,
        boost=boost,
    )

    #   check
    assert definition._view == rd.content.search.Views.VESSEL_PHYSICAL_ASSETS
    assert definition._filter == filter
    assert definition._boost == boost


def test_search_definition_with_sort_option():
    ############################################
    #   prepare things

    ############################################
    #   test
    query = "ceo"
    order_by = "YearOfBirth desc,LastName,FirstName"
    select = "YearOfBirth,DocumentTitle"
    definition = rd.content.search.Definition(
        view=rd.content.search.Views.PEOPLE,
        query=query,
        select=select,
        order_by=order_by,
    )

    #   check
    assert definition._view == rd.content.search.Views.PEOPLE
    assert definition._query == query
    assert definition._select == select
    assert definition._order_by == order_by


def test_search_definition_with_paging_option():
    ############################################
    #   prepare things

    ############################################
    #   test
    query = "gold"
    order_by = "YearOfBirth desc,LastName,FirstName"
    select = "YearOfBirth,DocumentTitle"
    definition = rd.content.search.Definition(
        view=rd.content.search.Views.COMMODITY_QUOTES,
        query=query,
        top=10,
        skip=20,
    )

    #   check
    assert definition._view == rd.content.search.Views.COMMODITY_QUOTES
    assert definition._query == query
    assert definition._top == 10
    assert definition._skip == 20


def test_raise_error_when_not_valid_request():
    # given
    session = StubSession(is_open=True, response=StubFailedResponse())
    definition = rd.content.search.Definition(view="invalid_value")

    with pytest.raises(RDError):
        definition.get_data(session=session)
