def test_cross_stream_has_correct_field_in_request_message(cross_stream):
    try:
        # when
        cross_stream._stream.universe["instrumentDefinition"]
    except Exception as e:
        assert False, str(e)

    else:
        assert True


def test_cross_stream_doesnot_have_incorrect_field_in_request_message(cross_stream):
    try:
        # when
        cross_stream._stream.universe["InstrumentDefinition"]
    except Exception as e:
        assert True, str(e)

    else:
        assert False
