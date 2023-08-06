from refinitiv.data._qpl import TenorBidAsk


def test_tenor_bid_ask():
    ask = 1.10
    bid = 2.20
    tenor = "tenor"

    tenor_bid_ask = TenorBidAsk(ask=ask, bid=bid, tenor=tenor)

    assert tenor_bid_ask.ask == ask
    assert tenor_bid_ask.bid == bid
    assert tenor_bid_ask.tenor == tenor

    assert tenor_bid_ask.get_dict() == {"ask": ask, "bid": bid, "tenor": tenor}
