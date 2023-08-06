# coding: utf8

from typing import TYPE_CHECKING, List, Callable

import pandas as pd

from .._content_data_provider import ContentDataProvider
from .._content_response_factory import ContentResponseFactory
from .._error_parser import ErrorParser
from ..._tools import PRICING_DATETIME_PATTERN
from ..._tools._common import fields_arg_parser, universe_arg_parser, cached_property
from ..._tools._dataframe import convert_df_columns_to_datetime_re, convert_dtypes
from ...delivery._data._data_provider import (
    ContentValidator,
    RequestFactory,
    ValidatorContainer,
)
from ...delivery._stream.stream_cache import StreamCache

if TYPE_CHECKING:
    from ...delivery._data._data_provider import ParsedData


# ---------------------------------------------------------------------------
#   Response factory
# ---------------------------------------------------------------------------


class PriceCache:
    def __init__(self, cache: dict):
        self._cache = cache

    def keys(self):
        return self._cache.keys()

    def values(self):
        return self._cache.values()

    def items(self):
        return self._cache.items()

    def __iter__(self):
        return PricingCacheIterator(self)

    def __getitem__(self, name):
        if name in self.keys():
            return self._cache[name]
        raise KeyError(f"{name} not in PriceCache")

    def __len__(self):
        return len(self.keys())

    def __str__(self):
        return str(self._cache)


class PricingCacheIterator:
    def __init__(self, price_cache: PriceCache):
        self._price_cache = price_cache
        self._universe = list(price_cache.keys())
        self._index = 0

    def __next__(self):
        if self._index < len(self._universe):
            name = self._universe[self._index]
            result = self._price_cache[name]
            self._index += 1
            return result
        raise StopIteration()


def create_price_cache(data: dict, fields) -> PriceCache:
    cache = {}
    for item in data:
        key = item.get("Key")
        if key:
            name = key.get("Name")
            service = key.get("Service")
            status = item.get("State")
            cache[name] = StreamCache(
                name=name,
                fields=fields,
                service=service,
                status=status,
                record=item,
            )
    return PriceCache(cache)


status_code_to_value = {"NotEntitled": "#N/P", "NotFound": "#N/F"}


def pricing_build_df(
    raw: List[dict], universe: list, fields: list, **kwargs
) -> pd.DataFrame:
    """Pricing dataframe builder.
    Args:
        raw (List[dict]): list of raw data to build dataframe.
        universe (list): list of RICs.
        fields (list): list of fields used to build dataframe.
        **kwargs: additional keyword arguments.
    Returns:
        DataFrame: properly created dataframe.
    """
    if not fields:
        fields = list(
            dict.fromkeys(key for item in raw for key in item.get("Fields", {}).keys())
        )

    data = []
    num_fields = len(fields)
    for idx, item in enumerate(raw):
        inst_name = universe[idx]
        if item["Type"] == "Status":
            value = status_code_to_value.get(item["State"]["Code"])
            values = [value] * num_fields
            data.append([inst_name, *values])
        else:
            row = [inst_name]
            for field in fields:
                value = item["Fields"].get(field)
                value = pd.NA if value is None else value
                row.append(value)
            data.append(row)

    df = pd.DataFrame(data=data, columns=["Instrument", *fields])
    convert_df_columns_to_datetime_re(df, PRICING_DATETIME_PATTERN)
    df = convert_dtypes(df)
    return df


class PricingResponseFactory(ContentResponseFactory):
    def create_data_success(self, parsed_data: "ParsedData", **kwargs):
        data = super().create_data_success(parsed_data, **kwargs)
        data.prices = create_price_cache(
            self.get_raw(parsed_data), kwargs.get("fields")
        )
        return data


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class PricingRequestFactory(RequestFactory):
    def get_query_parameters(self, *args, **kwargs) -> list:
        query_parameters = []

        #
        # universe
        #
        universe = kwargs.get("universe")
        if universe:
            universe = universe_arg_parser.get_str(universe, delim=",")
            query_parameters.append(("universe", universe))

        #
        # fields
        #
        fields = kwargs.get("fields")
        if fields:
            fields = fields_arg_parser.get_str(fields, delim=",")
            query_parameters.append(("fields", fields))

        return query_parameters


# ---------------------------------------------------------------------------
#   Content data validator
# ---------------------------------------------------------------------------


class PricingContentValidator(ContentValidator):
    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [self.status_is_not_error]


# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

pricing_data_provider = ContentDataProvider(
    request=PricingRequestFactory(),
    response=PricingResponseFactory(),
    parser=ErrorParser(),
    validator=ValidatorContainer(content_validator=PricingContentValidator()),
)
