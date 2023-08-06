import pytest

from refinitiv.data._errors import RDError
from refinitiv.data.content.search import lookup

from tests.unit.conftest import StubSession, StubFailedResponse


def test_raise_error_when_not_valid_request():
    # given
    session = StubSession(is_open=True, response=StubFailedResponse())
    definition = lookup.Definition(view="invalid_value", terms="", scope="", select="")

    with pytest.raises(RDError):
        definition.get_data(session=session)
