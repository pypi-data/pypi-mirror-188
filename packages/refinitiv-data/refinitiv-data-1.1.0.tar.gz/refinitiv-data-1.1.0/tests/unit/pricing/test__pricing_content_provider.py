import pytest

from refinitiv.data.delivery._data._data_provider import ParsedData
from refinitiv.data.delivery._stream.stream_cache import StreamCache
from refinitiv.data.content.pricing._pricing_content_provider import (
    PricingRequestFactory,
    PricingContentValidator,
    PricingResponseFactory,
    PriceCache,
)


def test_pricing_request_factory():
    # given
    expected_value = [("universe", "sun,moon"), ("fields", "corn,rice")]
    factory = PricingRequestFactory()

    # when
    testing_value = factory.get_query_parameters(
        universe=["sun", "moon"], fields=["corn", "rice"]
    )

    # then
    assert testing_value == expected_value, testing_value


def test_pricing_content_validator_return_false():
    # given
    validator = PricingContentValidator()
    input_value = ParsedData("Error", {}, {})
    expected_value = False

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value, testing_value


def test_pricing_content_validator_add_error_message():
    # given
    validator = PricingContentValidator()
    code = 100500
    message = "invalid"
    input_value = ParsedData(
        "Error",
        {},
        {"status": "Error", "code": code, "message": message},
        code,
        message,
    )
    expected_value = {
        "status": "Error",
        "raw_response": {},
        "content_data": {"status": "Error", "code": 100500, "message": "invalid"},
        "error_codes": [100500],
        "error_messages": ["invalid"],
    }

    # when
    validator.validate(input_value)
    testing_value = input_value

    # then
    assert testing_value == expected_value, testing_value


def test_pricing_response_factory_create_not_empty_df():
    # given
    factory = PricingResponseFactory()
    input_value = ParsedData(
        {},
        {},
        [
            {
                "Fields": {"BID": 1.1},
                "Type": "Refresh",
                "State": {"Stream": "NonStreaming", "Data": "Ok"},
                "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            },
            {
                "Fields": {"BID": None},
                "Type": "Refresh",
                "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            },
            {
                "Fields": {"BID": 1.1},
                "Type": "Status",
                "State": {"Code": "NotEntitled"},
                "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            },
            {
                "Fields": {"BID": 1.1},
                "Type": "Status",
                "State": {"Code": "NotFound"},
                "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            },
            {
                "Fields": {"BID": 1.1},
                "Type": "__stub__",
                "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            },
        ],
    )

    # when
    testing_value = factory.create_success(
        input_value,
        universe=["sun", "moon", "mars", "jupiter", "earth"],
        fields=[],
    )

    # then
    assert not testing_value.data.df.empty


def test_price_cache_keys():
    cache = PriceCache({})

    keys = cache.keys()

    assert keys is not None


def test_price_cache_values():
    cache = PriceCache({})

    values = cache.values()

    assert values is not None


def test_price_cache_items():
    cache = PriceCache({})

    items = cache.items()

    assert items is not None


def test_price_cache___iter___raise_error():
    cache = PriceCache({})

    iterator = iter(cache)

    with pytest.raises(StopIteration):
        next(iterator)


def test_price_cache___iter___():
    expected_value = StreamCache("name")
    cache = PriceCache({"EUR=": expected_value})

    iterator = iter(cache)
    testing_value = next(iterator)

    assert testing_value == expected_value


def test_price_cache___getitem__raise_error():
    cache = PriceCache({})
    key = "key"

    with pytest.raises(KeyError, match=f"{key} not in PriceCache"):
        cache[key]


def test_price_cache___getitem__():
    expected_value = "value"
    cache = PriceCache({"key": expected_value})

    testing_value = cache["key"]

    assert testing_value == expected_value, testing_value


def test_price_cache___len__():
    cache = PriceCache({})

    length = len(cache)

    assert length == 0


def test_price_cache___str__():
    cache = PriceCache({})

    s = str(cache)

    assert s == "{}"
