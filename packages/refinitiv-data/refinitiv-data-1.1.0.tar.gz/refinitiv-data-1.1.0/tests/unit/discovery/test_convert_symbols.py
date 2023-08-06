import mock
from unittest.mock import MagicMock

from refinitiv.data.discovery import convert_symbols, SymbolTypes


def test_convert_symbols():
    mocked_response = MagicMock()
    with mock.patch(
        "refinitiv.data.content.symbol_conversion.Definition.get_data",
        new=mocked_response,
    ):
        convert_symbols(
            symbols=["US5949181045", "US02079K1079"],
            from_symbol_type=SymbolTypes.ISIN,
            to_symbol_types="RIC",
        )
        assert mocked_response.call_count == 1
