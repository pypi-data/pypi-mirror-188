from refinitiv.data.content.ownership.investor import holdings


def test_holdings():
    try:
        definition = holdings.Definition(universe="")
    except Exception as e:
        assert False, str(e)
