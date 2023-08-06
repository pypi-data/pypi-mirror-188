from refinitiv.data.content.ipa.curves import zc_curve_definitions
from tests.unit.conftest import StubSession, StubResponse


def test_zc_curve_definition_empty_data():
    # given
    response = StubResponse({"data": [{}]})
    session = StubSession(is_open=True, response=response)
    definition = zc_curve_definitions.Definition(source="INVALID_SOURCE")

    # when
    response = definition.get_data(session)

    # then
    try:
        df = response.data.df
    except Exception as e:
        assert False, str(e)

    assert df.empty is True
    assert response.errors == []
