import inspect
from unittest import mock

import pandas as pd
import pytest

from refinitiv.data.content import pricing
from refinitiv.data.content.pricing._pricing_content_provider import pricing_build_df
from refinitiv.data.errors import RDError
from tests.unit.conftest import StubConfig, StubResponse
from tests.unit.conftest import StubSession
from tests.unit.content.data_for_tests import PRICING_DF_CREATING_RESPONSE


def test_call_get_data_without_session():
    # given
    definition = pricing.Definition("universe")

    # then
    with pytest.raises(Exception):
        # when
        definition.get_data()


def test_call_get_data_with_session():
    # given
    session = StubSession(
        is_open=True,
        config=StubConfig(
            {
                "apis.data.pricing": {
                    "url": "test",
                    "endpoints.snapshots": "test",
                },
                "raise_exception_on_error": True,
            }
        ),
        response=StubResponse(content_data=[{"Type": {}, "Fields": {}}]),
    )
    definition = pricing.Definition("universe")

    # when
    testing_value = definition.get_data(session)

    # then
    assert testing_value


def test_get_stream():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition("universe")

    # when
    stream = definition.get_stream(session)
    stream._stream._log

    # then
    assert stream


def test_get_fields_with_fields():
    # given
    expected_value = {"EUR=": {"field1": "aaa"}}
    session = StubSession(is_open=True)
    definition = pricing.Definition("universe")
    stream = definition.get_stream(session=session)

    with mock.patch(
        "refinitiv.data.content._universe_streams._UniverseStreams.__getitem__",
        return_value={"field1": "aaa", "field2": "bbb"},
    ):
        # when
        testing_value = stream._get_fields("EUR=", ["field1"])

        # then
        assert testing_value == expected_value


def test_get_fields_without_fields():
    # given
    expected_value = {"EUR=": {"field1": "aaa", "field2": "bbb"}}
    definition = pricing.Definition("universe")
    session = StubSession(is_open=True)
    stream = definition.get_stream(session=session)

    with mock.patch(
        "refinitiv.data.content._universe_streams._UniverseStreams.__getitem__",
        return_value={"field1": "aaa", "field2": "bbb"},
    ):
        # when
        testing_value = stream._get_fields("EUR=")

        # then
        assert testing_value == expected_value


def test_open_stream_with_empty_list_as_universe():
    session = StubSession(is_open=True)

    stream = pricing.Definition(universe=[], fields=["BID", "ASK"]).get_stream(session)

    with pytest.raises(ValueError):
        stream.open()


def test_pricing_definition__repr__():
    # given
    definition = pricing.Definition(universe="universe")
    hex_id = hex(id(definition))
    expected_value = (
        f"<refinitiv.data.content.pricing.Definition object at {hex_id} "
        f"{{name=['universe']}}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value


def test_input_user_attributes():
    # given
    excepted_attributes = ["_universe", "_fields", "_service", "_extended_params"]
    definition = pricing.Definition("")

    # when
    attributes = definition.__dict__

    # then
    assert all(x in attributes for x in excepted_attributes)


def test_inspect_init_pricing():
    # given
    excepted_attributes = [
        "universe",
        "fields",
        "service",
        "extended_params",
    ]
    inspect_pricing_init = inspect.signature(pricing.Definition.__init__)

    # when
    attributes = inspect_pricing_init.parameters

    # then
    assert all(x in attributes for x in excepted_attributes)


def test_smoke_get_stream_into_pricing():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition("universe")

    with mock.patch(
        "refinitiv.data.content.pricing._stream_facade.Stream.__init__",
        return_value=None,
    ) as mock_stream:
        # when
        definition.get_stream(session=session)

        # then
        mock_stream.assert_called_once_with(
            universe=["universe"],
            session=session,
            fields=[],
            service=None,
            api=None,
            extended_params={},
        )


def test_error_message_for_more_100_rics():
    # given
    response = StubResponse(
        content_data={
            "error": {
                "id": "6c44f198-b44e-42cb-b7a9-ce0ddb792256",
                "code": "400",
                "message": "Validation error",
                "status": "Bad Request",
                "errors": [
                    {
                        "key": "universe",
                        "reason": "validation failure list:\nuniverse in query should "
                        "have at most 100 instruments",
                    }
                ],
            }
        },
        status_code=400,
    )
    session = StubSession(is_open=True, response=response)
    definition = pricing.Definition(universe=["100Rics"], fields=["BID", "ASK"])

    # then
    error_message = (
        "Error code 400 | Validation error. validation failure "
        "list:\nuniverse in query should have at most 100 instruments"
    )
    with pytest.raises(RDError, match=error_message):
        # when
        definition.get_data(session)


@pytest.mark.parametrize("convert", [True, False])
def test_pricing_get_snapshot_should_not_return_none_in_df(convert):
    # given
    from refinitiv.data.content._universe_streams import build_df

    universe = ["AIR.PA", "CAPP.PA"]
    fields = ["PDTRDTM_MS", "VEH_PERMID"]
    values_by_field = {"PDTRDTM_MS": [None, None], "VEH_PERMID": [None, None]}

    # when
    df = build_df(universe, fields, values_by_field, convert)

    # then
    """
      Instrument PDTRDTM_MS VEH_PERMID
    0     AIR.PA       <NA>       <NA>
    1    CAPP.PA       <NA>       <NA>
    """
    assert df["VEH_PERMID"][0] is pd.NA
    assert df["PDTRDTM_MS"][1] is pd.NA


@pytest.mark.parametrize("convert", [True, False])
def test_pricing_get_snapshot_should_not_return_none_in_df_another_case(convert):
    # given
    from refinitiv.data.content._universe_streams import build_df

    universe = ["EUP=", "GBP=", "JPY=", "CAD="]
    fields = ["BID", "ASK"]
    values_by_field = {
        "BID": [None, 1.2085, 134.49, 1.2937],
        "ASK": [None, 1.2082, 134.46, 1.2932],
    }

    # when
    df = build_df(universe, fields, values_by_field, convert)

    # then
    expected_str = (
        "  Instrument     BID     ASK\n"
        "0       EUP=    <NA>    <NA>\n"
        "1       GBP=  1.2085  1.2082\n"
        "2       JPY=  134.49  134.46\n"
        "3       CAD=  1.2937  1.2932"
    )
    assert df.to_string() == expected_str


def test_universe_and_fields_order_get_snapshot_without_params():
    # given
    expected_snapshot = (
        "  Instrument BField AField DField CField\n"
        "0      BInst   <NA>   <NA>   <NA>   <NA>\n"
        "1      AInst   <NA>   <NA>   <NA>   <NA>\n"
        "2      DInst   <NA>   <NA>   <NA>   <NA>\n"
        "3      CInst   <NA>   <NA>   <NA>   <NA>"
    )
    session = StubSession(is_open=True)
    definition = pricing.Definition(
        universe=["BInst", "AInst", "DInst", "CInst"],
        fields=["BField", "AField", "DField", "CField"],
    )
    stream = definition.get_stream(session=session)

    # when
    snapshot = stream.get_snapshot()

    # then
    assert snapshot.to_string() == expected_snapshot


def test_universe_and_fields_order_get_snapshot_with_universe():
    # given
    expected_snapshot = (
        "  Instrument BField AField DField CField\n"
        "0      DInst   <NA>   <NA>   <NA>   <NA>\n"
        "1      AInst   <NA>   <NA>   <NA>   <NA>\n"
        "2      BInst   <NA>   <NA>   <NA>   <NA>"
    )
    session = StubSession(is_open=True)
    definition = pricing.Definition(
        universe=["BInst", "AInst", "DInst", "CInst"],
        fields=["BField", "AField", "DField", "CField"],
    )
    stream = definition.get_stream(session=session)

    # when
    snapshot = stream.get_snapshot(universe=["DInst", "AInst", "BInst"])

    # then
    assert snapshot.to_string() == expected_snapshot


def test_universe_and_fields_order_get_snapshot_with_fields():
    # given
    expected_snapshot = (
        "  Instrument DField AField BField\n"
        "0      BInst   <NA>   <NA>   <NA>\n"
        "1      AInst   <NA>   <NA>   <NA>\n"
        "2      DInst   <NA>   <NA>   <NA>\n"
        "3      CInst   <NA>   <NA>   <NA>"
    )
    session = StubSession(is_open=True)
    definition = pricing.Definition(
        universe=["BInst", "AInst", "DInst", "CInst"],
        fields=["BField", "AField", "DField", "CField"],
    )
    stream = definition.get_stream(session=session)

    # when
    snapshot = stream.get_snapshot(fields=["DField", "AField", "BField"])

    # then
    assert snapshot.to_string() == expected_snapshot


def test_return_none_if_no_field_not_raise_error():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(
        ["EUP=", "GBP=", "JPY=", "CAD="],
        fields=["BID", "ASK"],
    )
    non_streaming = definition.get_stream(session=session)

    # then
    try:
        # when
        testing_value = non_streaming["EUP="]["TEST"]
    except Exception as e:
        assert False, str(e)

    assert testing_value is None


def test_return_none_if_no_universe_not_raise_error():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(
        ["EUP=", "GBP=", "JPY=", "CAD="],
        fields=["BID", "ASK"],
    )
    non_streaming = definition.get_stream(session=session)

    # then
    try:
        # when
        testing_value = non_streaming["TEST"]
    except Exception as e:
        assert False, str(e)

    assert testing_value == {}


def test_get_snapshot_can_expect_one_string_in_fields():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(
        ["EUP=", "GBP=", "JPY=", "CAD="],
        fields=["BID", "ASK"],
    )
    non_streaming = definition.get_stream(session=session)

    # when
    testing_value = non_streaming.get_snapshot("EUP=", fields="BID")

    # then
    try:
        testing_value["BID"]
    except KeyError as e:
        assert False, str(e)
    else:
        assert True


@pytest.mark.parametrize(
    "input_fields, expected_fields",
    [
        (["BID", "ASK", "BID", "ASK"], ["BID", "ASK"]),
        # order is important
        (["EUP=", "GBP=", "JPY=", "CAD="], ["EUP=", "GBP=", "JPY=", "CAD="]),
        ("EUP=", ["EUP="]),
        ([], []),
        (None, []),
        ("", []),
    ],
)
def test_pricing_definition_can_expect_fields(input_fields, expected_fields):
    # when
    definition = pricing.Definition("EUP=", fields=input_fields)
    testing_fields = definition._fields

    # then
    assert testing_fields == expected_fields


def test_pricing_build_df_none_to_na():
    raw = [{"Type": "Refresh", "Fields": {"NONE_FIELD": None}}]
    universe = ["EUR="]

    result = pricing_build_df(raw, universe, [])

    # assert that universe is the first dataframe column
    assert result.at[0, "Instrument"] == "EUR="

    # assert that None turned into pd.NA in result dataframe
    assert result.at[0, "NONE_FIELD"] is pd.NA


def test_pricing_build_df_item_type_status():
    raw = [
        {
            "Type": "Status",
            "State": {"Code": "NotFound"},
        }
    ]
    universe = ["USD="]
    fields = ["FIRST_FIELD", "SECOND_FIELD"]
    result = pricing_build_df(raw, universe, fields)

    assert result.at[0, "Instrument"] == "USD="
    assert len(result.columns) == 3  # RIC and two fields
    assert result.at[0, "FIRST_FIELD"] == "#N/F"
    assert result.at[0, "SECOND_FIELD"] == "#N/F"


def test_df_without_nan():
    expected_str = (
        "  Instrument CF_NAME  DDS_DSO_ID  BR_LINK1  QUOTIM_2  QUOTE_DT2     ASKHI1_MS\n"
        "0       EUR=    Euro       12348      <NA>  10:30:40 2022-06-22  22:55:25.876"
    )
    session = StubSession(is_open=True, response=PRICING_DF_CREATING_RESPONSE)
    definition = pricing.Definition("EUR=")
    response = definition.get_data(session=session)
    df = response.data.df
    assert df.to_string() == expected_str


def test_add_instruments():
    # given
    test_universe = ["VOD.L", "IBM.N"]
    test_instruments = ["EUR="]
    test_result = ["VOD.L", "IBM.N", "EUR="]
    session = StubSession(is_open=True)
    stream = pricing.Definition(universe=test_universe).get_stream(session=session)

    # when
    stream.add_instruments(test_instruments)

    # then
    assert stream._universe == test_result


def test_remove_instruments():
    # given
    test_universe = ["VOD.L", "IBM.N"]
    test_instruments = ["IBM.N"]
    test_result = ["VOD.L"]
    session = StubSession(is_open=True)
    stream = pricing.Definition(universe=test_universe).get_stream(session=session)

    # when
    stream.remove_instruments(test_instruments)

    # then
    assert stream._universe == test_result


def test_add_fields():
    # given
    test_fields = ["BID", "ASK"]
    test_new_fields = ["TRDPRC_1"]
    test_result = ["BID", "ASK", "TRDPRC_1"]
    session = StubSession(is_open=True)
    stream = pricing.Definition(universe=["VOD.L"], fields=test_fields).get_stream(
        session=session
    )

    # when
    stream.add_fields(test_new_fields)

    # then
    assert stream._fields == test_result


def test_remove_fields():
    # given
    test_fields = ["BID", "ASK"]
    test_remove_fields = ["ASK"]
    test_result = ["BID"]
    session = StubSession(is_open=True)
    stream = pricing.Definition(universe=["VOD.L"], fields=test_fields).get_stream(
        session=session
    )

    # when
    stream.remove_fields(test_remove_fields)

    # then
    assert stream._fields == test_result
