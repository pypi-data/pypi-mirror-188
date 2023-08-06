from refinitiv.data._core.session import Sensitive, GrantPassword


def test_sensitive():
    # given
    expected = "psadfjg@341F32"

    # when
    password = Sensitive("psadfjg@341F32")

    # then
    assert expected == password
    assert repr(password) == "********"


def test_password_is_sensitive():
    # given
    # when
    grant = GrantPassword("username", "password")

    # then
    assert isinstance(grant._password, Sensitive)
