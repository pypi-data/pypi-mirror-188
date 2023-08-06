from types import SimpleNamespace

import pytest

import refinitiv.data as rd


@pytest.fixture(scope="function")
def session():
    session = rd.session.desktop.Definition(app_key="test_app_key").get_session()
    yield session
    rd.session.set_default(None)


@pytest.fixture(scope="function")
def stub_session():
    self = SimpleNamespace()
    self.debug = lambda *_: None
    self.error = lambda *_: None
    return self
