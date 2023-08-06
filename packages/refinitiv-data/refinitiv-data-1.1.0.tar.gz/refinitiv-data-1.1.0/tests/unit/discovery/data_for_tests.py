from tests.unit.conftest import StubResponse


EXPECTED_CONSTITUENTS_LIST = ["MT.AS", "ESLX.PA"]
EXPECTED_SUMMARY_LIST = [".FCHI", ".DJI", "/.STOXX50E", ".AD.FCHI", "EUR="]
BUNCH_CONSTITUENTS = [
    StubResponse(
        {
            "meta": {
                "nextLink": "bGltaXQ9MSZjdXJzb3I9MSMuRkNISQ==",
                "prevLink": "",
            },
            "universe": {"ric": "0#.FCHI"},
            "data": {"constituents": ["MT.AS"] + EXPECTED_SUMMARY_LIST},
        }
    ),
    StubResponse(
        {
            "meta": {
                "nextLink": "",
                "prevLink": "bGltaXQ9MSZjdXJzb3I9MCMuRkNISQ==",
            },
            "universe": {"ric": "1#.FCHI"},
            "data": {"constituents": ["ESLX.PA"]},
        }
    ),
]
