from refinitiv.data.content.custom_instruments import Definition
from refinitiv.data.delivery._data._request import Request
from tests.unit.conftest import StubSession, StubResponse

get_uuid_url = "test_get_rdp_url_root/data/custom-instruments/v1/instruments/S%29Instrument.UUID-0000"


def test_get_uui_request_only_once():
    request_counter = 0
    my_uuid = "MY-0000"

    def _http_request(request: Request):
        nonlocal request_counter
        if request.url == get_uuid_url:
            request_counter += 1
            return StubResponse(
                content_data={
                    "state": {
                        "code": 400,
                        "status": "Bad Request",
                        "message": "Validation Error",
                    },
                    "data": [
                        {
                            "key": "symbol",
                            "reason": f".UUID suffix UUID-0000 not matched with userID {my_uuid}",
                        }
                    ],
                },
                status_code=400,
            )

    session = StubSession(is_open=True)
    session.http_request = _http_request

    universe = ["Instrument1.AA-0000", f"S)Instrument2.{my_uuid}"]
    stream = Definition(universe=universe).get_stream(session=session)
    _ = stream["INST"]
    _ = stream["Instrument2"]
    _ = stream["Instrument1"]
    _ = stream[universe[0]]
    assert request_counter == 1


def test_all_universe_with_uuid():
    my_uuid = "MY-0000"

    def _http_request(request: Request):
        if request.url == get_uuid_url:
            return StubResponse(
                content_data={
                    "state": {
                        "code": 400,
                        "status": "Bad Request",
                        "message": "Validation Error",
                    },
                    "data": [
                        {
                            "key": "symbol",
                            "reason": f".UUID suffix UUID-0000 not matched with userID {my_uuid}",
                        }
                    ],
                },
                status_code=400,
            )

    session = StubSession(is_open=True)
    session.http_request = _http_request

    universe = ["Instrument1.AA-0000", f"S)Instrument2.{my_uuid}"]
    stream = Definition(universe=universe).get_stream(session=session)

    result = set(stream_item.name for stream_item in stream)
    expected_result = {"S)Instrument1.AA-0000", f"S)Instrument2.{my_uuid}"}
    assert result == expected_result
    assert stream["Instrument1.AA-0000"].name == "S)Instrument1.AA-0000"
    assert stream[f"Instrument2.{my_uuid}"].name == universe[1]
    assert stream["Instrument2"].name == universe[1]
    assert stream["Instrument1"] == {}


def test_mixed_universe():
    my_uuid = "MY-0000"

    def _http_request(request: Request):
        if request.url == get_uuid_url:
            return StubResponse(
                content_data={
                    "state": {
                        "code": 400,
                        "status": "Bad Request",
                        "message": "Validation Error",
                    },
                    "data": [
                        {
                            "key": "symbol",
                            "reason": f".UUID suffix UUID-0000 not matched with userID {my_uuid}",
                        }
                    ],
                },
                status_code=400,
            )

    session = StubSession(is_open=True)
    session.http_request = _http_request

    universe = [
        "S)Instrument1.AA-0000",
        f"S)Instrument2.{my_uuid}",
        "Instrument1",
        "Instrument3",
    ]
    stream = Definition(universe=universe).get_stream(session=session)

    result = set(stream_item.name for stream_item in stream)
    expected_result = {
        "S)Instrument1.AA-0000",
        f"S)Instrument2.{my_uuid}",
        f"S)Instrument1.{my_uuid}",
        f"S)Instrument3.{my_uuid}",
    }

    assert result == expected_result
    assert stream["Instrument1.AA-0000"].name == "S)Instrument1.AA-0000"
    assert stream[f"Instrument2.{my_uuid}"].name == universe[1]
    assert stream["Instrument2"].name == universe[1]
    assert stream["Instrument1"].name == f"S)Instrument1.{my_uuid}"


def test_add_instruments():
    # given
    test_universe = ["Instrument1", "Instrument2"]
    test_items = ["Instrument3"]
    test_result = ["S)Instrument1.", "S)Instrument2.", "S)Instrument3."]
    session = StubSession(is_open=True)
    stream = Definition(universe=test_universe).get_stream(session=session)

    # when
    stream.add_instruments(test_items)

    # then
    assert stream._universe == test_result


def test_remove_instruments():
    # given
    test_universe = ["Instrument1", "Instrument2"]
    test_items = ["Instrument2"]
    test_result = ["S)Instrument1."]
    session = StubSession(is_open=True)
    stream = Definition(universe=test_universe).get_stream(session=session)

    # when
    stream.remove_instruments(test_items)

    # then
    assert stream._universe == test_result


def test_add_fields():
    # given
    test_fields = ["BID", "ASK"]
    test_new_fields = ["TRDPRC_1"]
    test_result = ["BID", "ASK", "TRDPRC_1"]
    session = StubSession(is_open=True)
    stream = Definition(universe=["VOD.L"], fields=test_fields).get_stream(
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
    stream = Definition(universe=["VOD.L"], fields=test_fields).get_stream(
        session=session
    )

    # when
    stream.remove_fields(test_remove_fields)

    # then
    assert stream._fields == test_result
