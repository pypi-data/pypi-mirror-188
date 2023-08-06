from unittest import mock

import pytest

import refinitiv.data as rd
from refinitiv.data.content import trade_data_service
from tests.unit.conftest import StubSession

mocked_session = mock.MagicMock()

UNIVERSE = [
    {
        "type": "swap",
        "definition": {
            "startDate": "2019-07-28T00:00:00Z",
            "swapType": "Vanilla",
            "tenor": "3Y",
        },
    }
]

FIELDS = ["ContractType", "ContractDate"]
API = "streaming/trading-analytics/redi"


def test_import():
    try:
        from refinitiv.data.content import trade_data_service
    except ImportError:
        assert False


def test_error_import():
    try:
        from refinitiv.data import trade_data_stream
    except ImportError:
        assert True


def test_import_data():
    data = [
        elem for elem in dir(rd.content.trade_data_service) if not elem.startswith("_")
    ]
    assert ["Definition", "Events", "FinalizedOrders", "UniverseTypes"] == data


def test_public_data_definition():
    data = [
        elem
        for elem in dir(rd.content.trade_data_service.Definition)
        if not elem.startswith("_")
    ]
    assert ["get_stream"] == data


def test_definition_creation():
    definition = rd.content.trade_data_service.Definition(
        universe=UNIVERSE, fields=FIELDS
    )

    assert definition._universe == UNIVERSE
    assert definition._fields == FIELDS


def test_get_stream_callbacks():
    list_attr = [
        "open",
        "open_async",
        "close",
        "on_complete",
        "on_add",
        "on_update",
        "on_remove",
        "on_event",
        "on_state",
    ]

    stream = rd.content.trade_data_service.Definition(
        universe=UNIVERSE, fields=FIELDS
    ).get_stream(mocked_session)

    for attr in list_attr:
        assert hasattr(stream, attr), f"{attr} method not exist {type(stream)}"


def test_trade_data_service_raise_error_when_try_open_and_session_is_close():
    # given
    session = StubSession(is_open=True)
    definition = trade_data_service.Definition(
        universe=[],
        finalized_orders=trade_data_service.FinalizedOrders.P1D,
        events=trade_data_service.Events.Full,
    )
    stream = definition.get_stream(session=session)

    # then
    with pytest.raises(AssertionError, match="Session must be open"):
        # when
        session.close()
        stream.open()
