from types import SimpleNamespace

import pytest
from pandas.core.dtypes.common import is_datetime64_any_dtype, is_datetime64tz_dtype


class ExceptionInjection:
    _stream = SimpleNamespace()
    _stream.universe = None

    def __init__(self, *args, **kwargs):
        raise ValueError


args_names = (
    "adc_df,pricing_df,data,expected_result,adc_stub,pricing_stub,exception_expected"
)


def assert_datetime_dtype_for_df(df):
    dict_values = df.dtypes.to_dict().values()
    assert any(is_datetime64_any_dtype(dtype) for dtype in dict_values)

    for dtype in dict_values:
        if is_datetime64_any_dtype(dtype):
            assert not is_datetime64tz_dtype(dtype)
