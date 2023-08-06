from refinitiv.data.content.ipa.curves._cross_currency_curves.definitions import manage
from tests.unit.conftest import StubResponse, StubSession


def test_delete_function():
    # given
    response = StubResponse({"status": "200"})
    session = StubSession(is_open=True, response=response)
    response = manage.delete(
        id="7bdb00f3-0a48-40be-ace2-6d3cfd0e8e59",
        session=session,
    )

    # then
    assert response.data.raw
    assert response.data.df.empty
