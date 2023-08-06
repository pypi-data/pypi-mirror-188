import pytest

from refinitiv.data._errors import RDError
from refinitiv.data.content.historical_pricing import events, summaries
from tests.unit.conftest import StubSession

from .data_for_tests import (
    DF_EMPTY_ONE_INST,
    DF_EMPTY_TWO_INSTS,
    DF_EMPTY_ONE_INST_IS_BAD,
    INST_IS_BAD,
    INSTS_ARE_BAD,
    DF_EMPTY_ONE_INST_IS_BAD_OTHER_WITHOUT_HEADERS,
    DF_EMPTY_WITHOUT_HEADERS,
)


@pytest.mark.parametrize(
    "universe,object_definition,response",
    [
        # events
        ("LSEG.L", events.Definition, DF_EMPTY_ONE_INST),
        (["LSEG.L", "VOD.L"], events.Definition, DF_EMPTY_TWO_INSTS),
        (["LSEG.L", "VOD.Lffff"], events.Definition, DF_EMPTY_ONE_INST_IS_BAD),
        # summaries
        ("LSEG.L", summaries.Definition, DF_EMPTY_ONE_INST),
        (["LSEG.L", "VOD.L"], summaries.Definition, DF_EMPTY_TWO_INSTS),
        (["LSEG.L", "VOD.Lffff"], summaries.Definition, DF_EMPTY_ONE_INST_IS_BAD),
    ],
)
def test_empty_df(universe, object_definition, response):
    # given
    session = StubSession(is_open=True, response=response)
    expected_str = "Empty DataFrame\n" "Columns: []\n" "Index: []"
    definition = object_definition(
        universe=universe,
        start="09-09-2020T16:30:00",
        end="09-09-2021T04:00:01",
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.empty
    assert df.to_string() == expected_str


@pytest.mark.parametrize(
    "universe, response",
    [
        (["EUR=", "GBP="], DF_EMPTY_WITHOUT_HEADERS),
        (["EUR=", "GBP"], DF_EMPTY_ONE_INST_IS_BAD_OTHER_WITHOUT_HEADERS),
    ],
)
def test_empty_df_without_headers_for_events_endpoints(universe, response):
    # given
    session = StubSession(is_open=True, response=response)
    expected_str = "Empty DataFrame\n" "Columns: []\n" "Index: []"
    definition = events.Definition(
        universe=universe,
        eventTypes="trade",
        start="09-09-1992T16:30:00",
        end="09-09-1993T04:00:01",
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.empty
    assert df.to_string() == expected_str


@pytest.mark.parametrize(
    "universe,object_definition,response",
    [
        # events
        ("VOD.Lffff", events.Definition, INST_IS_BAD),
        (["LSEG.Lffff", "VOD.Lffff"], events.Definition, INSTS_ARE_BAD),
        # summaries
        ("VOD.Lffff", summaries.Definition, INST_IS_BAD),
        (["LSEG.Lffff", "VOD.Lffff"], summaries.Definition, INSTS_ARE_BAD),
    ],
)
def test_raise_error(universe, object_definition, response):
    # given
    error_message = "Error code 1 | No data to return, please check errors: ERROR: No successful response."
    session = StubSession(is_open=True, response=response)
    definition = object_definition(universe=universe)
    # when
    with pytest.raises(expected_exception=RDError, match=error_message):
        definition.get_data(session=session)
