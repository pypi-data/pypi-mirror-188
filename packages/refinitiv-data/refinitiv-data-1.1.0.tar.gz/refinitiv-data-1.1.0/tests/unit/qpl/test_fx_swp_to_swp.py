from copy import deepcopy
from datetime import datetime, timedelta, date

import pytest

import refinitiv.data as rd
from refinitiv.data._errors import RDError
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.content.test_datetime import make_checker
from tests.unit.content.test_enums import get_json


def test_basic_case():
    # fmt: off
    expected_str = (
"  tenor   startDate     endDate  swapCcy1Bid  swapCcy1Ask  swapCcy2Bid  swapCcy2Ask  swapCc1Ccy2Bid  swapCc1Ccy2Ask  outrightCcy1Ccy2Bid  outrightCcy1Ccy2Ask\n"
"0    1M  2013-06-19  2013-07-19         1.84         1.88        -3.16        -3.11        2.852139        2.906775             0.850387             0.850908\n"
"1    2M  2013-06-19  2013-08-19         3.85         3.95        -6.25        -6.12        5.759443        5.897724             0.850678             0.851207"
    )
    raw = {
    "swapPoints": [{
        "tenor": "1M", "startDate": "2013-06-19",
        "endDate": "2013-07-19", "swapCcy1Bid": 1.84,
        "swapCcy1Ask": 1.88, "swapCcy2Bid": -3.16,
        "swapCcy2Ask": -3.11, "swapCc1Ccy2Bid": 2.85213907031734,
        "swapCc1Ccy2Ask": 2.90677481977641,
        "outrightCcy1Ccy2Bid": 0.850386969185587,
        "outrightCcy1Ccy2Ask": 0.850907804342901
    }, {
        "tenor": "2M", "startDate": "2013-06-19",
        "endDate": "2013-08-19", "swapCcy1Bid": 3.85,
        "swapCcy1Ask": 3.95, "swapCcy2Bid": -6.25,
        "swapCcy2Ask": -6.12, "swapCc1Ccy2Bid": 5.7594425853269,
        "swapCc1Ccy2Ask": 5.89772434189784,
        "outrightCcy1Ccy2Bid": 0.850677699537088,
        "outrightCcy1Ccy2Ask": 0.851206899295114
    }]
    }
    # fmt: on
    response = StubResponse(deepcopy(raw))
    session = StubSession(is_open=True, response=response)
    rd.session.set_default(session)
    response = rd._qpl.fx_swp_to_swp(
        fx_cross_code="EURGBP",
        market_data_date_time="2013-06-17",
        tenors=["1M", "2M"],
    )
    assert response.data.raw == raw
    assert response.data.df.to_string() == expected_str

    rd.session.set_default(None)


def test_manage_error_and_processing_information():
    error_code = "QPS-Curves.14"
    error_message = (
        "The service failed to build the curve, Invalid input : "
        "Definition of the fx forward curve is not valid. "
        "The fx forward curve doesn't contain a valid spot "
        "constituent for currency code 'XXXYYY'."
    )
    raw = {
        "error": {
            "id": "fe68b128-2ea6-44d7-9456-3196acd5856e/fe68b128-2ea6-44d7-9456-3196acd5856e",
            "status": "Error",
            "message": error_message,
            "code": error_code,
        }
    }
    response = StubResponse(deepcopy(raw))
    session = StubSession(is_open=True, response=response)
    rd.session.set_default(session)
    with pytest.raises(RDError) as error:
        rd._qpl.fx_swp_to_swp(
            fx_cross_code="XXXYYY",
            market_data_date_time="2013-06-17",
            tenors=["1M"],
        )

    assert error.value.code == error_code
    assert error.value.message == error_message
    rd.session.set_default(None)


def test_full_override_of_spot_and_swap_points_values():
    # fmt: off
    expected_str = (
"  tenor   startDate     endDate  swapCcy1Bid  swapCcy1Ask  swapCcy2Bid  swapCcy2Ask  swapCc1Ccy2Bid  swapCc1Ccy2Ask  outrightCcy1Ccy2Bid  outrightCcy1Ccy2Ask\n"
"0    1M  2022-11-21  2022-12-21        22.16        22.45         8.64         9.04       12.014555       12.552910             0.874284             0.874970\n"
"1    2M  2022-11-21  2023-01-23        55.66        56.16        24.49        28.49       25.882465       29.245585             0.875671             0.876639"
    )
    raw = {
        "swapPoints": [{
            "tenor": "1M", "startDate": "2022-11-21",
            "endDate": "2022-12-21", "swapCcy1Bid": 22.16,
            "swapCcy1Ask": 22.45, "swapCcy2Bid": 8.64,
            "swapCcy2Ask": 9.04, "swapCc1Ccy2Bid": 12.0145547910377,
            "swapCc1Ccy2Ask": 12.552910153959,
            "outrightCcy1Ccy2Bid": 0.874284212937388,
            "outrightCcy1Ccy2Ask": 0.874969673075757
        }, {
            "tenor": "2M", "startDate": "2022-11-21",
            "endDate": "2023-01-23", "swapCcy1Bid": 55.66,
            "swapCcy1Ask": 56.16, "swapCcy2Bid": 24.49,
            "swapCcy2Ask": 28.49, "swapCc1Ccy2Bid": 25.8824651078038,
            "swapCc1Ccy2Ask": 29.2455845109385,
            "outrightCcy1Ccy2Bid": 0.875671003969064,
            "outrightCcy1Ccy2Ask": 0.876638940511455
        }]
    }
    expected_raw = deepcopy(raw)
    expected_json = {
        'fxCrossCode': 'EURGBP', 'marketDataDate': '2022-11-17', 'tenors': ['1M', '2M'],
        'spotCcy1': {'ask': 1, 'bid': 1}, 'spotCcy2': {'ask': 1.3, 'bid': 1.3},
        'swapPointsCcy1': {
            'overrides': [{'tenor': '1M', 'ask': 30, 'bid': 20},
                          {'tenor': '2M', 'ask': 45, 'bid': 34}]
        },
        'swapPointsCcy2': {
            'overrides': [{'tenor': '1M', 'ask': 40, 'bid': 40},
                          {'tenor': '2M', 'ask': 45, 'bid': 45}]
        }
    }
    # fmt: on

    def make_assert_request():
        origin_session_http_request = session.http_request

        def assert_request(request):
            assert request.json == expected_json
            return origin_session_http_request(request)

        return assert_request

    response = StubResponse(raw)
    session = StubSession(is_open=True, response=response)
    session.http_request = make_assert_request()
    rd.session.set_default(session)
    response = rd._qpl.fx_swp_to_swp(
        fx_cross_code="EURGBP",
        market_data_date_time="2022-11-17",
        tenors=["1M", "2M"],
        spot_ccy_1=rd._qpl.FxSpotQuote(bid=1, ask=1),
        spot_ccy_2=rd._qpl.FxSpotQuote(bid=1.3, ask=1.3),
        swap_points_ccy_1=rd._qpl.FxSwapPoints(
            overrides=[
                rd._qpl.TenorBidAsk(tenor="1M", bid=20, ask=30),
                rd._qpl.TenorBidAsk(tenor="2M", bid=34, ask=45),
            ]
        ),
        swap_points_ccy_2=rd._qpl.FxSwapPoints(
            overrides=[
                rd._qpl.TenorBidAsk(tenor="1M", bid=40, ask=40),
                rd._qpl.TenorBidAsk(tenor="2M", bid=45, ask=45),
            ]
        ),
    )
    assert response.data.raw == expected_raw
    assert response.data.df.to_string() == expected_str

    rd.session.set_default(None)


def test_case_19():
    # fmt: off
    expected_str = (
"  tenor   startDate     endDate  swapCcy1Bid  swapCcy1Ask  swapCcy2Bid  swapCcy2Ask  swapCc1Ccy2Bid  swapCc1Ccy2Ask  outrightCcy1Ccy2Bid  outrightCcy1Ccy2Ask\n"
"0    1M  2022-11-21  2022-12-21        22.16        22.45         8.64         9.04       12.014555       12.552910             0.874284             0.874970\n"
"1    2M  2022-11-21  2023-01-23        55.66        56.16        24.49        28.49       25.882465       29.245585             0.875671             0.876639"
    )
    raw = {
        "swapPoints": [{
            "tenor": "1M", "startDate": "2022-11-21",
            "endDate": "2022-12-21", "swapCcy1Bid": 22.16,
            "swapCcy1Ask": 22.45, "swapCcy2Bid": 8.64,
            "swapCcy2Ask": 9.04, "swapCc1Ccy2Bid": 12.0145547910377,
            "swapCc1Ccy2Ask": 12.552910153959,
            "outrightCcy1Ccy2Bid": 0.874284212937388,
            "outrightCcy1Ccy2Ask": 0.874969673075757
        }, {
            "tenor": "2M", "startDate": "2022-11-21",
            "endDate": "2023-01-23", "swapCcy1Bid": 55.66,
            "swapCcy1Ask": 56.16, "swapCcy2Bid": 24.49,
            "swapCcy2Ask": 28.49, "swapCc1Ccy2Bid": 25.8824651078038,
            "swapCc1Ccy2Ask": 29.2455845109385,
            "outrightCcy1Ccy2Bid": 0.875671003969064,
            "outrightCcy1Ccy2Ask": 0.876638940511455
        }]
    }
    expected_raw = deepcopy(raw)
    expected_json = {
        'fxCrossCode': 'EURUSD',
        'marketDataDate': '2022-09-22',
        'spotCcy1': {'source': 'D3'},
        'spotCcy2': {'ask': 2, 'bid': 1},
        'swapPointsCcy1': {'additionalTenorTypes': ['Long'], 'source': 'ICAP'},
        'swapPointsCcy2': {
            'additionalTenorTypes': ['Long', 'Odd'],
            'overrides': [{'ask': 60, 'bid': 50, 'tenor': '1M'},
                          {'bid': 90, 'tenor': '2M'}],
            'source': 'D3'
        }
    }
    # fmt: on

    def make_assert_request():
        origin_session_http_request = session.http_request

        def assert_request(request):
            assert request.json == expected_json
            return origin_session_http_request(request)

        return assert_request

    response = StubResponse(raw)
    session = StubSession(is_open=True, response=response)
    session.http_request = make_assert_request()
    rd.session.set_default(session)
    response = rd._qpl.fx_swp_to_swp(
        fx_cross_code="EURUSD",
        market_data_date_time="2022-09-22",
        spot_ccy_1=rd._qpl.FxSpotQuote(source="D3"),
        spot_ccy_2=rd._qpl.FxSpotQuote(bid=1, ask=2),
        swap_points_ccy_1=rd._qpl.FxSwapPoints(
            additional_tenor_types=[rd._qpl.TenorTypes.LONG],
            source="ICAP",
        ),
        swap_points_ccy_2=rd._qpl.FxSwapPoints(
            additional_tenor_types=[rd._qpl.TenorTypes.LONG, rd._qpl.TenorTypes.ODD],
            source="D3",
            overrides=[
                rd._qpl.TenorBidAsk(tenor="1M", bid=50, ask=60),
                rd._qpl.TenorBidAsk(tenor="2M", bid=90),
            ],
        ),
    )
    assert response.data.raw == expected_raw
    assert response.data.df.to_string() == expected_str

    rd.session.set_default(None)


@pytest.mark.parametrize(
    (
        "input_datatime",
        "expected_str",
    ),
    [
        (datetime(2020, 1, 1), "2020-01-01"),
        ("2020-01-02", "2020-01-02"),
        (timedelta(0), datetime.now().date()),
        (date(2020, 1, 4), "2020-01-04"),
    ],
)
def test_qpl_function_datetime(input_datatime, expected_str):
    session = StubSession(is_open=True)
    session.http_request = make_checker(
        param_name="marketDataDate",
        value=expected_str,
        func_get_params=get_json,
        mocked_json=None,
    )
    rd.session.set_default(session)

    rd._qpl.fx_swp_to_swp(fx_cross_code="code", market_data_date_time=input_datatime)

    rd.session.set_default(None)
