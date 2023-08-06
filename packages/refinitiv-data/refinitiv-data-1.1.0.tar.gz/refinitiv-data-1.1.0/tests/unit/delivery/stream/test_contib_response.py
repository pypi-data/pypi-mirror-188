from refinitiv.data.delivery._stream.contrib._response import (
    NullContribResponse,
    ErrorContribResponse,
    AckContribResponse,
)


def test_null_contrib_response():
    response = NullContribResponse()

    assert response.ack_id == None
    assert response.debug == {}
    assert response.error == ""
    assert response.is_success is False
    assert response.nak_code == ""
    assert response.nak_message == ""
    assert response.type == ""
    assert (
        "<refinitiv.data.delivery._stream.contrib._response.NullContribResponse object at "
        in repr(response)
    )


def test_error_contrib_response():
    input_debug = {
        "File": "/local/jsonToRwfSimple.C",
        "Line": 7243,
        "Offset": 233,
        "Message": '{"Ack": true, "ID": 2, "Message": {"Fields": {"ASK": 1.2, "BID": 0.86, "PRIMACT_1": 103, "SEC_ACT_1": 203}, "ID": 0, "Type": "Update", "Domain": "MarketPrice"}, "PostID": 11, "Type": "Post", "Key": {"Name": "TEST02=NIK", "Service": "DDS_TRCE"}, "Domain": "MarketPrice"}',
    }
    expected_debug = input_debug
    input_text = "JSON Unexpected Value. Received 'DDS_TRCE' for key 'Service'"
    expected_text = input_text
    response = ErrorContribResponse(
        {
            "ID": 2,
            "Type": "Error",
            "NakCode": "NakCode",
            "Text": input_text,
            "Debug": input_debug,
        }
    )

    assert response.ack_id == None
    assert response.debug == expected_debug
    assert response.error == expected_text
    assert response.is_success is False
    assert response.nak_code == "NakCode"
    assert response.nak_message == ""
    assert response.type == "Error"
    assert repr(response) == str(
        {
            "Type": "Error",
            "Text": "",
            "Debug": {
                "File": "/local/jsonToRwfSimple.C",
                "Line": 7243,
                "Offset": 233,
                "Message": '{"Ack": true, "ID": 2, "Message": {"Fields": {"ASK": 1.2, "BID": 0.86, "PRIMACT_1": 103, "SEC_ACT_1": 203}, "ID": 0, "Type": "Update", "Domain": "MarketPrice"}, "PostID": 11, "Type": "Post", "Key": {"Name": "TEST02=NIK", "Service": "DDS_TRCE"}, "Domain": "MarketPrice"}',
            },
        }
    )


def test_ack_contrib_response():
    input_text = "[1]: Contribution Accepted"
    expected_text = input_text

    input_ackid = 5
    expected_ackid = 5
    response = AckContribResponse(
        {
            "ID": 2,
            "Type": "Ack",
            "AckID": input_ackid,
            "Text": input_text,
            "Key": {"Service": "ATS_GLOBAL_1", "Name": "TEST"},
        }
    )

    assert response.ack_id == expected_ackid
    assert response.debug == {}
    assert response.error == ""
    assert response.is_success is True
    assert response.nak_code == ""
    assert response.nak_message == expected_text
    assert response.type == "Ack"
    assert repr(response) == str({"Type": "Ack", "AckId": 5})


def test_ack_contrib_response_with_nak_code():
    input_text = "[1]: Contribution Accepted"
    expected_text = input_text

    input_ackid = 5
    expected_ackid = 5
    response = AckContribResponse(
        {
            "ID": 2,
            "Type": "Ack",
            "AckID": input_ackid,
            "Text": input_text,
            "Key": {"Service": "ATS_GLOBAL_1", "Name": "TEST"},
            "NakCode": "NakCode",
        }
    )

    assert response.ack_id == expected_ackid
    assert response.debug == {}
    assert response.error == ""
    assert response.is_success is False
    assert response.nak_code == "NakCode"
    assert response.nak_message == expected_text
    assert response.type == "Ack"
    assert repr(response) == str(
        {
            "Type": "Ack",
            "AckId": 5,
            "NakCode": "NakCode",
            "Message": "[1]: Contribution Accepted",
        }
    )
