import pytest

from refinitiv.data.content.filings import search


def test_search_definition_attributes():
    # given
    # when
    s = search.Definition()

    # then
    assert hasattr(s, "query")
    assert hasattr(s, "variables")
