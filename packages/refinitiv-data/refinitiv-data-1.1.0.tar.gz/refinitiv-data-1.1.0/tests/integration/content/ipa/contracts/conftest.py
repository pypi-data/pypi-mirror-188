import json
from datetime import datetime

import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from tests.integration.conftest import is_open
from tests.integration.constants_list import HttpStatusCode


def get_first_bond_definition():
    definition = rdf.bond.Definition(
        instrument_code="US1YT=RR",
        fields=[
            "InstrumentCode",
            "MarketDataDate",
            "YieldPercent",
            "GovernmentSpreadBp",
            "GovCountrySpreadBp",
            "RatingSpreadBp",
            "SectorRatingSpreadBp",
            "EdsfSpreadBp",
            "IssuerSpreadBp",
            "ErrorMessage",
        ],
    )
    return definition


def get_second_bond_definition():
    definition = rdf.bond.Definition(
        issue_date="2002-02-28",
        end_date="2032-02-28",
        notional_ccy="USD",
        interest_payment_frequency="Annual",
        fixed_rate_percent=7,
        interest_calculation_method="Dcb_Actual_Actual",
    )
    return definition


def get_third_bond_definition():
    definition = rdf.bond.Definition(
        instrument_code="US1YT=RR",
        fields=[
            "InstrumentCode",
            "MarketDataDate",
            "YieldPercent",
            "GovernmentSpreadBp",
            "GovCountrySpreadBp",
            "RatingSpreadBp",
            "SectorRatingSpreadBp",
            "EdsfSpreadBp",
            "IssuerSpreadBp",
        ],
        pricing_parameters=rdf.bond.PricingParameters(
            market_data_date="2019-07-05", price_side=rdf.bond.PriceSide.BID
        ),
    )
    return definition


def get_invalid_bond_definition():
    definition = rdf.bond.Definition(
        issue_date="2002-02-28",
        end_date="2032-02-28",
        notional_ccy="INVALCCY",
        interest_payment_frequency="Annual",
        fixed_rate_percent=7,
        interest_calculation_method="Dcb_Actual_Actual",
    )
    return definition


def option_definition_01():
    definition = rdf.option.Definition(
        underlying_type=rdf.option.UnderlyingType.FX,
        strike=265,
        underlying_definition=rdf.option.FxUnderlyingDefinition("AUDUSD"),
        notional_ccy="AUD",
        tenor="5M",
        pricing_parameters=rdf.option.PricingParameters(
            price_side=rdf.option.PriceSide.MID,
            valuation_date="2018-08-06",
            pricing_model_type=rdf.option.PricingModelType.BLACK_SCHOLES,
            fx_spot_object=rdf.option.BidAskMid(
                bid=0.7387,
                ask=0.7387,
                mid=0.7387,
            ),
        ),
    )
    return definition


def financial_contracts_definition_with_fields():
    definition = rdf.Definitions(
        [
            get_first_bond_definition(),
            get_second_bond_definition(),
            get_third_bond_definition(),
        ],
        fields=[
            "InstrumentCode",
            "MarketDataDate",
            "YieldPercent",
            "GovernmentSpreadBp",
            "GovCountrySpreadBp",
            "RatingSpreadBp",
            "SectorRatingSpreadBp",
            "EdsfSpreadBp",
            "IssuerSpreadBp",
            "ErrorMessage",
            "INVALID_FIELD",
        ],
    )
    return definition


def financial_contracts_definition_without_fields():
    definition = rdf.Definitions(
        [
            get_second_bond_definition(),
            option_definition_01(),
        ]
    )

    return definition


def get_valid_and_invalid_financial_contracts_definition():
    definition = rdf.Definitions(
        [
            get_first_bond_definition(),
            get_second_bond_definition(),
            get_invalid_bond_definition(),
        ],
        fields=[
            "InstrumentCode",
            "MarketDataDate",
            "YieldPercent",
            "GovernmentSpreadBp",
            "GovCountrySpreadBp",
            "RatingSpreadBp",
            "SectorRatingSpreadBp",
            "EdsfSpreadBp",
            "IssuerSpreadBp",
            "ErrorMessage",
            "INVALID_FIELD",
        ],
    )
    return definition


@pytest.fixture(
    scope="function", params=[False, True], ids=["async_mode=False", "async_mode=True"]
)
def async_mode(request):
    return request.param


def check_http_status_is_success_and_df_value_not_empty(response):
    status = response.http_status
    df = response.data.df
    assert status["http_status_code"] == HttpStatusCode.TWO_HUNDRED, (
        f"Actual status code is {status['http_status_code']}, "
        f"Error: {response.http_status['error']}"
    )

    assert df is not None, f"DataFrame is {df}"
    assert not df.empty, f"DataFrame is empty: {df}"
    assert not bool(df.ErrorMessage[0]), f"{df.ErrorMessage[0]}"
    assert df.MarketDataDate is not None, f"{df.MarketDataDate}"


def check_http_status_bad_request_and_error_message(response):
    status = response.http_status
    message = response.error_message
    assert (
        status["http_status_code"] == HttpStatusCode.FOUR_HUNDRED
    ), f"Actual status code is {status['http_status_code']}"

    assert message == "Validation error", f"Message: {message}"


def check_stream_state_and_df_from_stream(stream, expected_value=None):
    df = stream.get_snapshot()
    if expected_value is not None:
        actual_value = df.InstrumentDescription[0]
        assert expected_value in actual_value, f"Actual value: {actual_value}"

    assert is_open(stream), f"Stream is not open"
    assert df is not None, f"DataFrame is {df}"
    assert not df.empty, f"DataFrame is empty: {df}"
    assert df.MarketDataDate is not None, f"{df.MarketDataDate}"
    assert not bool(df.ErrorMessage[0]), f"{df.ErrorMessage[0]}"

    stream.close()


def check_http_status_is_success(response):
    status = response.http_status

    assert status["http_status_code"] == HttpStatusCode.TWO_HUNDRED, (
        f"Actual status code is {status['http_status_code']}, "
        f"Error: {response.http_status['error']}"
    )


def check_request_message_contains_expected_fields(response, expected_fields_names):
    request_byte = response.request_message.content
    request = json.loads(request_byte.decode("utf-8"))
    actual_list = request["fields"]
    actual_list_lowercase = list(map(lambda x: x.lower(), actual_list))
    for field_name in expected_fields_names:
        assert (
            field_name.lower() in actual_list_lowercase
        ), f"Expected field name '{field_name}' is not found in list of fields in request: {actual_list}"


def display_event(
    data, instrument_name, stream, event_type, triggered_events_list=None
):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append(event_type)
    print("----------------------------------------------------------")
    print(">>> {} - {} - at {}".format(event_type, data, current_time))


def add_call_backs(stream, triggered_events_list=None):
    stream.on_update(
        lambda data, instrument_name, item_stream: display_event(
            data,
            instrument_name,
            item_stream,
            "Update received for",
            triggered_events_list,
        )
    )
    stream.on_response(
        lambda data, instrument_name, item_stream: display_event(
            data,
            instrument_name,
            item_stream,
            "Response received for",
            triggered_events_list,
        )
    )
    stream.on_state(
        lambda event, item_stream: display_event(
            event, item_stream, "State received for", triggered_events_list
        )
    )
