import datetime

import pytest
from pandas.core.dtypes.common import is_datetime64_any_dtype

from refinitiv.data._core.session import set_default
from refinitiv.data._tools import get_params, ParamItem
from refinitiv.data.content import custom_instruments as ci
from refinitiv.data._errors import RDError
from refinitiv.data.content import custom_instruments
from refinitiv.data._content_type import ContentType
from refinitiv.data.content.custom_instruments._custom_instruments_data_provider import (
    get_content_type_by_interval,
    get_user_id,
    CustomInstsRequestFactory,
    CustomInstsSearchRequestFactory,
    custom_instruments_intervals_build_df,
    convert_to_holidays,
)
from refinitiv.data.delivery._data._endpoint_data import RequestMethod
from refinitiv.data.delivery._data._request import Request
from tests.unit.conftest import StubSession, StubResponse, args
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.content.custom_instruments.conftest import (
    volume_based_udc,
    volume_based_dict_udc,
    day_based_udc,
    day_based_dict_udc,
    manual_udc,
    manual_dict_udc,
    basket_dict,
    ci_udc_response,
    ci_basket_response,
    ci_create_formula_response,
    basket_obj,
)
from tests.unit.content.custom_instruments.test__stream_facade import get_uuid_url


@pytest.mark.parametrize(
    ("input_params_details", "input_data", "test_result"),
    [
        (
            [ParamItem("key", "KEY")],
            {"key": "value"},
            [
                ("KEY", "value"),
            ],
        ),
        (
            [ParamItem("key", "KEY")],
            {"key": "value", "dasd": "1"},
            [
                ("KEY", "value"),
            ],
        ),
        (
            [ParamItem("key", "KEY", lambda a, **_: a.upper())],
            {"key": "value"},
            [
                ("KEY", "VALUE"),
            ],
        ),
    ],
)
def test_get_params(input_params_details, input_data, test_result):
    # given
    # when
    result = get_params(input_params_details, **input_data)
    # then
    assert result == test_result


@pytest.mark.parametrize(
    ("input_interval", "test_result"),
    [
        ("PT1M", ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES),
        ("P1D", ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES),
    ],
)
def test_get_content_type_by_interval(input_interval, test_result):
    # given
    # when
    result = get_content_type_by_interval(input_interval)
    # then
    assert result == test_result


@pytest.mark.parametrize(
    ("content_data", "expected_uuid"),
    [
        args(
            content_data=[
                {
                    "state": {
                        "code": 400,
                        "status": "Bad Request",
                        "message": "Validation Error",
                    },
                    "data": [
                        {
                            "key": "symbol",
                            "reason": f".UUID suffix UUID-0000 not matched with userID GE-1234",
                        }
                    ],
                }
            ],
            expected_uuid="GE-1234",
        ),
        args(
            content_data=[
                {
                    "state": {
                        "code": 400,
                        "status": "Bad Request",
                        "message": "Validation Error",
                    },
                    "data": [
                        {
                            "key": "symbol",
                            "reason": ".UUID suffix UUID-0000 not matched with userID SL1-1RZ2M3V",
                        }
                    ],
                }
            ],
            expected_uuid="SL1-1RZ2M3V",
        ),
    ],
)
def test_get_user_id(content_data, expected_uuid):
    # given
    def _http_request(request: Request):
        if request.url == get_uuid_url:
            return StubResponse(
                content_data=content_data,
                status_code=content_data[0].get("state", {}).get("code", -1),
            )

    session = StubSession(is_open=True)
    session.http_request = _http_request

    # when
    testing_uuid = get_user_id(session=session)

    # then
    assert testing_uuid == expected_uuid


@pytest.mark.parametrize(
    ("content_data", "test_result"),
    [
        ([{}], ""),
    ],
)
def test_get_uuid_error(content_data, test_result):
    def _http_request(request: Request):
        if request.url == get_uuid_url:
            return StubResponse(
                content_data=content_data,
                status_code=content_data[0].get("state", {}).get("code", -1),
            )

    session = StubSession(is_open=True)
    session.http_request = _http_request

    # then
    with pytest.raises(RDError):
        # when
        get_user_id(session=session)


def test_get_user_id_when_not_expected_error():
    session = StubSession(
        is_open=True, response=StubResponse(content_data="", status_code=401)
    )
    with pytest.raises(RDError):
        get_user_id(session)


@pytest.mark.parametrize(
    ("input_kwargs", "request_method", "test_result"),
    [
        (
            {"symbol": "MyInstrument", "description": "Description"},
            RequestMethod.GET,
            {},
        ),
        (
            {
                "symbol": "MyInstrument",
                "currency": "GBP",
                "description": "Description",
                "exchange_name": "ADSE",
                "formula": "VOD.L*3",
                "holidays": [{"reason": "New Year", "date": "1.01.2022"}],
                "time_zone": "LON",
                "instrument_name": "InstrName",
            },
            RequestMethod.POST,
            {
                "symbol": "S)MyInstrument.",
                "currency": "GBP",
                "description": "Description",
                "exchangeName": "ADSE",
                "formula": "VOD.L*3",
                "holidays": [{"reason": "New Year", "date": "1.01.2022"}],
                "timeZone": "LON",
                "instrumentName": "InstrName",
            },
        ),
    ],
)
def test_custom_insts_request_factory_get_body_parameters(
    input_kwargs, request_method, test_result
):
    # given
    request_factory = CustomInstsRequestFactory()
    request_factory.get_request_method = lambda *args, **kwargs: request_method
    session = StubSession(is_open=True)
    set_default(session)

    # when
    result = request_factory.get_body_parameters(session, **input_kwargs)

    # then
    assert result == test_result


def test_search_request_factory_get_query_parameters():
    # given
    params = {"access": "owner"}
    test_result = [("access", "owner")]

    # when
    request_factory = CustomInstsSearchRequestFactory()
    result = request_factory.get_query_parameters(**params)

    # then
    assert result == test_result


def test_custom_instruments_intervals_build_df_datetime_type():
    # given
    testing_column_name = "DATE"
    input_content_data = {
        "data": [["2012-11-01T04:16:13"]],
        "headers": [{"name": testing_column_name}],
    }

    # when
    result_df = custom_instruments_intervals_build_df(input_content_data)

    # then
    assert is_datetime64_any_dtype(result_df[testing_column_name])


summaries_response = [
    {
        "data": [
            ["2022-09-27", 2.8776],
            ["2022-09-26", 2.8818],
            ["2022-09-23", 2.907],
            ["2022-09-22", 2.9508],
            ["2022-09-21", 2.9511],
            ["2022-09-20", 2.991],
            ["2022-09-19", 3.0066],
            ["2022-09-16", 3.0045],
            ["2022-09-15", 2.9997],
            ["2022-09-14", 2.9931],
            ["2022-09-13", 2.991],
            ["2022-09-12", 3.0357],
            ["2022-09-09", 3.0117],
            ["2022-09-08", 2.9982],
            ["2022-09-07", 2.9997],
            ["2022-09-06", 2.9706],
            ["2022-09-05", 2.9778],
            ["2022-09-02", 2.9853],
            ["2022-09-01", 2.9832],
            ["2022-08-31", 3.0171],
        ],
        "defaultPricingField": "TRDPRC_1",
        "headers": [
            {"name": "DATE", "type": "string"},
            {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
        ],
        "interval": "P1D",
        "summaryTimestampLabel": "endPeriod",
        "universe": {"ric": "S)TR12.GESG1-106493"},
    }
]
events_reponse = [
    {
        "data": [
            ["2022-09-28T06:33:57.622Z", 2.8692],
            ["2022-09-28T06:33:57.062Z", 2.8695],
            ["2022-09-28T06:33:56.052Z", 2.8695],
            ["2022-09-28T06:33:55.595Z", 2.8695],
            ["2022-09-28T06:33:55.255Z", 2.8692],
            ["2022-09-28T06:33:54.585Z", 2.8695],
            ["2022-09-28T06:33:54.167Z", 2.8698],
            ["2022-09-28T06:33:53.598Z", 2.8692],
            ["2022-09-28T06:33:53.086Z", 2.8698],
            ["2022-09-28T06:33:52.586Z", 2.8695],
            ["2022-09-28T06:33:51.583Z", 2.8692],
            ["2022-09-28T06:33:50.054Z", 2.8692],
            ["2022-09-28T06:33:48.432Z", 2.8692],
            ["2022-09-28T06:33:47.971Z", 2.8692],
            ["2022-09-28T06:33:47.751Z", 2.8698],
            ["2022-09-28T06:33:47.555Z", 2.8692],
            ["2022-09-28T06:33:46.782Z", 2.8692],
            ["2022-09-28T06:33:46.544Z", 2.8692],
            ["2022-09-28T06:33:45.117Z", 2.8698],
            ["2022-09-28T06:33:44.554Z", 2.8692],
        ],
        "defaultPricingField": "TRDPRC_1",
        "headers": [
            {"name": "DATE_TIME", "type": "string"},
            {"decimalChar": ".", "name": "TRDPRC_1", "type": "number"},
        ],
        "interval": None,
        "summaryTimestampLabel": None,
        "universe": {"ric": "S)TR12.GESG1-106493"},
    }
]


def test_fields_events():
    # given
    session = StubSession(is_open=True, response=StubResponse(events_reponse))

    # when
    response = custom_instruments.events.Definition(
        universe=["S)TR12"], fields=["TRDPRC_1"]
    ).get_data(session=session)
    df = response.data.df

    # then
    assert "TRDPRC_1" in df


def test_fields_events_empty_df():
    # given
    session = StubSession(is_open=True, response=StubResponse(events_reponse))

    # when
    response = custom_instruments.events.Definition(
        universe=["S)TR12"], fields=["BID"]
    ).get_data(session=session)
    df = response.data.df

    # then
    assert df.empty


def test_fields_summaries():
    # given
    session = StubSession(is_open=True, response=StubResponse(summaries_response))

    # when
    response = custom_instruments.summaries.Definition(
        universe=["S)TR12"], fields=["TRDPRC_1"]
    ).get_data(session=session)
    df = response.data.df

    # then
    assert "TRDPRC_1" in df


def test_fields_summaries_empty_df():
    # given
    session = StubSession(is_open=True, response=StubResponse(summaries_response))

    # when
    response = custom_instruments.summaries.Definition(
        universe=["S)TR12"], fields=["BID"]
    ).get_data(session=session)
    df = response.data.df

    # then
    assert df.empty


@pytest.mark.parametrize(
    ("ci_object", "ci_dict"),
    [
        (volume_based_udc, volume_based_dict_udc),
        (day_based_udc, day_based_dict_udc),
        (manual_udc, manual_dict_udc),
        (basket_obj, basket_dict),
    ],
    ids=["volumeBased_udc", "dayBased_udc", "manual_udc", "basket"],
)
def test_custom_instrument_serialize_into_json(ci_object, ci_dict):
    # given
    ci_cls = ci_object

    # when
    converted_ci_to_dict = ci_cls._to_dict()

    # then
    assert ci_dict == converted_ci_to_dict


@pytest.mark.parametrize(
    ("ci_object", "ci_dict"),
    [
        (volume_based_udc, volume_based_dict_udc),
        (day_based_udc, day_based_dict_udc),
        (basket_obj, basket_dict),
    ],
    ids=["volumeBased_udc", "dayBased_udc", "basket"],
)
def test_custom_instrument_deserialize_into_python_obj(ci_object, ci_dict):
    # given
    ci_cls = ci_object

    # when
    converted_ci_from_dict = ci_cls._from_dict(ci_dict)

    # then
    assert ci_cls == converted_ci_from_dict


def test_create_udc_custom_instrument():
    # given
    session = StubSession(is_open=True, response=StubResponse(ci_udc_response))

    # when
    instrument = ci.manage.create_udc(
        symbol="My_UDC_instrument",
        instrument_name="9789",
        exchange_name="5050",
        currency="GBP",
        time_zone="LON",
        description="fintech trading tool",
        holidays=[
            ci.manage.Holiday(date="1991-08-23", name="Independence Day of Ukraine"),
            {"date": "2022-12-18", "reason": "Hanukkah"},
        ],
        udc=volume_based_udc,
        session=session,
    )

    # then
    assert instrument.symbol == ci_udc_response.get("symbol")
    assert instrument.udc._to_dict() == ci_udc_response.get("udc")
    assert instrument.exchange_name == ci_udc_response.get("exchangeName")
    assert instrument.holidays == ci_udc_response.get("holidays")


def test_create_basket_custom_instrument():
    # given
    session = StubSession(is_open=True, response=StubResponse(ci_basket_response))

    # when
    instrument = ci.manage.create_basket(
        symbol="My_Basket_instrument",
        instrument_name="9789",
        exchange_name="5050",
        currency="GBP",
        time_zone="LON",
        description="fintech trading tool",
        holidays=[
            ci.manage.Holiday(date="1991-08-23", name="Independence Day of Ukraine"),
            {"date": "2022-12-18", "reason": "Hanukkah"},
        ],
        basket=basket_obj,
        session=session,
    )

    # then
    assert instrument.symbol == ci_basket_response.get("symbol")
    assert instrument.basket._to_dict() == ci_basket_response.get("basket")
    assert instrument.instrument_name == ci_basket_response.get("instrumentName")
    assert instrument.time_zone == ci_basket_response.get("timeZone")


def test_formula_custom_instrument_getting_the_same_obj():
    # given
    session = StubSession(
        is_open=True, response=StubResponse(ci_create_formula_response)
    )

    # when
    instrument = ci.manage.create_formula(
        symbol="My_formula_instrument",
        instrument_name="9789",
        exchange_name="5050",
        currency="GBP",
        time_zone="LON",
        description="fintech trading tool",
        holidays=[
            ci.manage.Holiday(date="1991-08-23", name="Independence Day of Ukraine"),
            {"date": "2022-12-18", "reason": "Hanukkah"},
        ],
        formula="GBP=*3",
        session=session,
    )

    requested_instrument = ci.manage.get(
        universe="My_formula_instrument", session=session
    )

    # then
    assert instrument.symbol == requested_instrument.symbol
    assert instrument.formula == requested_instrument.formula
    assert instrument.currency == requested_instrument.currency
    assert instrument.holidays == requested_instrument.holidays


@pytest.mark.parametrize(
    ("changed_params"),
    [
        ({"formula": "EUR=*3", "currency": "EUR", "exchange_name": "9898"}),
    ],
)
def test_update_formula_custom_instrument(changed_params):
    # given
    session = StubSession(
        is_open=True, response=StubResponse(ci_create_formula_response)
    )

    # when
    instrument = ci.manage.get(universe="My_formula_instrument", session=session)
    instrument.formula = "EUR=*3"
    instrument.currency = "EUR"
    instrument.exchange_name = "9898"
    instrument.save()

    requested_instrument = ci.manage.get(
        universe="My_formula_instrument", session=session
    )

    # then
    assert instrument.formula == changed_params["formula"]
    assert instrument.currency == changed_params["currency"]
    assert instrument.exchange_name == changed_params["exchange_name"]
    assert instrument.formula == requested_instrument.formula
    assert instrument.currency == requested_instrument.currency
    assert instrument.exchange_name == requested_instrument.exchange_name


def test_param_item_arg_name_query_param_name():
    # given
    param_item = ParamItem(arg_name="name", query_param_name="NAME")

    # then
    assert param_item.arg_name == "name"
    assert param_item.query_param_name == "NAME"


def test_param_item_arg_name():
    # given
    param_item = ParamItem(arg_name="name")

    # then
    assert param_item.arg_name == "name"
    assert param_item.query_param_name == "name"


def test_convert_holiday_obj_to_dict():
    # given
    holidays = [
        ci.manage.Holiday(date="1991-10-24", name="Labour Day"),
        ci.manage.Holiday(
            date=datetime.date(2021, 8, 24), name="Independence Day of Ukraine"
        ),
        ci.manage.Holiday(date=datetime.timedelta(days=-30), name="Alaska Day"),
        {"date": "2022-04-23", "reason": "Shakespeare Day"},
    ]

    # when
    converted_holidays = convert_to_holidays(holidays)

    # then
    assert len(converted_holidays) == 4
    for holiday in converted_holidays:
        assert isinstance(holiday, dict)
        assert "date" in holiday and "reason" in holiday
        assert isinstance(holiday.get("date"), str)
        assert isinstance(holiday.get("reason"), str)
