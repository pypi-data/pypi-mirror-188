import refinitiv.data as rd
from tests.unit.conftest import StubSession, StubResponse


def test_df_not_empty_if_date_is_none():
    # fmt: off
    response = StubResponse({
            "links": {"count": 2}, "variability": "", "universe": [{
            "Instrument": "IBM",
            "Company Common Name": "International Business Machines Corp",
            "Organization PermID": "4295904307",
            "Reporting Currency": "USD"
        }],
            "data": [["IBM", "2023-01-18T00:00:00", None, "USD", 60210414250],
                     ["IBM", "2021-12-31T00:00:00", "2021-12-31T00:00:00", None, None]],
            "messages": {
                "codes": [[-1, -1, -2, -1, -1], [-1, -1, -1, -2, -2]],
                "descriptions": [{"code": -2, "description": "empty"},
                                 {"code": -1, "description": "ok"}]
            }, "headers": [{
            "name": "instrument", "title": "Instrument", "type": "string",
        }, {
            "name": "date", "title": "Date", "type": "datetime",
        }, {
            "name": "TR.Revenue", "title": "Date", "type": "datetime",
        }, {
            "name": "TR.RevenueMean", "title": "Currency", "type": "string",
        }, {
            "name": "TR.RevenueMean", "title": "Revenue - Mean",
            "type": "number", "decimalChar": ".",
        }]})
    # fmt: on
    session = StubSession(is_open=True, response=response)
    session.config.set_param("apis.data.datagrid.underlying-platform", "rdp")
    rd.session.set_default(session)

    df = rd.get_history(
        universe="IBM",
        fields=["TR.Revenue.date", "TR.RevenueMean.currency", "TR.RevenueMean"],
        interval="daily",
        use_field_names_in_headers=True,
    )

    rd.session.set_default(None)

    assert not df.empty
