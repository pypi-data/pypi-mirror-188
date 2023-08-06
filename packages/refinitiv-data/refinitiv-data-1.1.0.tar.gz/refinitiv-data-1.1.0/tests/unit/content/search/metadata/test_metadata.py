import pytest

from refinitiv.data._errors import RDError
from refinitiv.data.content import search

from tests.unit.conftest import StubSession, StubFailedResponse


def test_raise_error_when_not_valid_request():
    # given
    session = StubSession(is_open=True, response=StubFailedResponse())
    definition = search.metadata.Definition(view="invalid_value")

    with pytest.raises(RDError):
        definition.get_data(session=session)
