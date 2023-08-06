from refinitiv.data._qpl import FxSpotQuote


def test_fx_spot_quote():
    ask = 1.10
    bid = 2.20
    source = "source"
    spot_quote = FxSpotQuote(source, ask, bid)

    assert spot_quote.ask == ask
    assert spot_quote.bid == bid
    assert spot_quote.source == source

    assert spot_quote.get_dict() == {"ask": 1.1, "bid": 2.2, "source": "source"}
