from refinitiv.data._qpl import FxSwapPoints, TenorTypes, TenorBidAsk


def test_fx_swap_points_complex():
    fx_swap_points = FxSwapPoints(
        additional_tenor_types=[TenorTypes.LONG, TenorTypes.ODD],
        source="D3",
        overrides=[
            TenorBidAsk(tenor="1M", bid=50, ask=60),
            TenorBidAsk(tenor="2M", bid=90),
        ],
    )

    assert fx_swap_points.overrides == [
        {"ask": 60, "bid": 50, "tenor": "1M"},
        {"bid": 90, "tenor": "2M"},
    ]
    assert fx_swap_points.source == "D3"
    assert fx_swap_points.additional_tenor_types == ["Long", "Odd"]

    assert fx_swap_points.get_dict() == {
        "additionalTenorTypes": ["Long", "Odd"],
        "overrides": [
            {"ask": 60, "bid": 50, "tenor": "1M"},
            {"bid": 90, "tenor": "2M"},
        ],
        "source": "D3",
    }


def test_fx_swap_points_primitive():
    fx_swap_points = FxSwapPoints(
        additional_tenor_types=["Long", "Odd"],
        source="D3",
        overrides=[{"ask": 60, "bid": 50, "tenor": "1M"}, {"bid": 90, "tenor": "2M"}],
    )

    assert fx_swap_points.overrides == [
        {"ask": 60, "bid": 50, "tenor": "1M"},
        {"bid": 90, "tenor": "2M"},
    ]
    assert fx_swap_points.source == "D3"
    assert fx_swap_points.additional_tenor_types == ["Long", "Odd"]

    assert fx_swap_points.get_dict() == {
        "additionalTenorTypes": ["Long", "Odd"],
        "overrides": [
            {"ask": 60, "bid": 50, "tenor": "1M"},
            {"bid": 90, "tenor": "2M"},
        ],
        "source": "D3",
    }


def test_tenor_types():
    assert str(TenorTypes.ODD) == "Odd"
    assert str(TenorTypes.LONG) == "Long"
    assert str(TenorTypes.IMM) == "IMM"
    assert str(TenorTypes.BEGINNING_OF_MONTH) == "BeginningOfMonth"
    assert str(TenorTypes.END_OF_MONTH) == "EndOfMonth"
