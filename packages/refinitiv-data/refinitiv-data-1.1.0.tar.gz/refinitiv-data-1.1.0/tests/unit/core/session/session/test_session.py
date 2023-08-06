import pytest

import refinitiv.data as rd


def test_get_default(session):
    rd.session.set_default(session)

    assert rd.session.get_default() is session


def test_get_default_error(session):
    with pytest.raises(
        AttributeError,
        match="No default session created yet. Please create a session first!",
    ):
        rd.session.get_default()


def test_set_default(session):
    try:
        rd.session.set_default(session)
        assert rd.session.get_default() is session
    except Exception as e:
        assert False, e


def test_clear_default_session(session):
    rd.session.set_default(None)

    with pytest.raises(
        AttributeError,
        match="No default session created yet. Please create a session first!",
    ):
        rd.session.get_default()


def test_invalid_input_set_default_session():
    session = "invalid_input_type"

    with pytest.raises(TypeError, match="Invalid argument"):
        rd.session.set_default(session)
