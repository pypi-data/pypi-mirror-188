import pytest

from refinitiv.data.content import symbol_conversion
from refinitiv.data.content.symbol_conversion import (
    SymbolTypes,
    CountryCode,
    AssetClass,
    AssetState,
)
from refinitiv.data.content.symbol_conversion._definition import DEFAULT_SCOPE
from refinitiv.data.content.symbol_conversion._symbol_type import SYMBOL_TYPE_VALUES


def test_definition_repr():
    # given
    symbols_list = ["MSFT.O", "AAPL.O", "GOOG.O"]
    kwargs = {
        "symbols": symbols_list,
        "from_symbol_type": SymbolTypes.RIC,
        "to_symbol_types": None,
        "extended_params": {},
    }

    # when
    definition = symbol_conversion.Definition(**kwargs)

    # then
    assert "{symbols='MSFT.O,AAPL.O,GOOG.O'}" in repr(definition)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("US5949181045", "US5949181045"),
        (["US5949181045", "US02079K1079"], "US5949181045,US02079K1079"),
        ([""], ""),
        ([], None),
        (None, None),
        ("", None),
    ],
)
def test_symbols(input_value, expected_value):
    definition = symbol_conversion.Definition(input_value)

    assert definition.symbols == expected_value


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("RIC", "RIC"),
        (SymbolTypes.RIC, "RIC"),
        (["RIC", "IssueISIN"], "['RIC', 'IssueISIN']"),
        ([SymbolTypes.RIC, SymbolTypes.ISIN], "['RIC', 'IssueISIN']"),
        ("", "_AllUnique"),
        ([], "_AllUnique"),
        (None, "_AllUnique"),
    ],
)
def test_from_symbol_type(input_value, expected_value):
    definition = symbol_conversion.Definition("", from_symbol_type=input_value)

    assert definition.from_symbol_type == expected_value


def test_from_symbol_type_default_value():
    definition = symbol_conversion.Definition("")

    assert definition.from_symbol_type == DEFAULT_SCOPE


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("RIC", "DocumentTitle,RIC"),
        (SymbolTypes.RIC, "DocumentTitle,RIC"),
        (["RIC", "IssueISIN"], "DocumentTitle,RIC,IssueISIN"),
        ([SymbolTypes.RIC, SymbolTypes.ISIN], "DocumentTitle,RIC,IssueISIN"),
        ("", "DocumentTitle"),
        ([], "DocumentTitle"),
        (None, "DocumentTitle"),
    ],
)
def test_to_symbol_types(input_value, expected_value):
    definition = symbol_conversion.Definition("", to_symbol_types=input_value)

    assert definition.to_symbol_types == expected_value


def test_to_symbol_types_default_value():
    definition = symbol_conversion.Definition("")

    assert definition.to_symbol_types == ",".join(
        ["DocumentTitle"] + list(SYMBOL_TYPE_VALUES)
    )

    assert (
        definition.to_symbol_types
        == "DocumentTitle,RIC,IssueISIN,CUSIP,SEDOL,TickerSymbol,IssuerOAPermID,FundClassLipperID"
    )


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("ABW", "RCSExchangeCountry eq 'G:AD'"),
        (CountryCode.ABW, "RCSExchangeCountry eq 'G:AD'"),
        ("G:AD", "RCSExchangeCountry eq 'G:AD'"),
        ("", None),
        ([], None),
        (None, None),
    ],
)
def test_preferred_country_code(input_value, expected_value):
    definition = symbol_conversion.Definition("", preferred_country_code=input_value)

    assert definition.preferred_country_code == expected_value


def test_preferred_country_code_default_value():
    definition = symbol_conversion.Definition("")

    assert definition.preferred_country_code == None


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("Commodities", [AssetClass.COMMODITIES]),
        ("COMMODITIES", [AssetClass.COMMODITIES]),
        (AssetClass.COMMODITIES, [AssetClass.COMMODITIES]),
        ("", None),
        ([], None),
        (None, None),
    ],
)
def test_asset_class(input_value, expected_value):
    definition = symbol_conversion.Definition("", asset_class=input_value)

    assert definition.asset_class == expected_value


def test_asset_class_default_value():
    definition = symbol_conversion.Definition("")

    assert definition.asset_class == None


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("Active", AssetState.ACTIVE),
        ("ACTIVE", AssetState.ACTIVE),
        (AssetState.ACTIVE, AssetState.ACTIVE),
        ("", None),
        ([], None),
        (None, None),
    ],
)
def test_asset_state(input_value, expected_value):
    definition = symbol_conversion.Definition("", asset_state=input_value)

    assert definition.asset_state == expected_value


def test_asset_state_default_value():
    definition = symbol_conversion.Definition("")

    assert definition.asset_state == None


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ({"ABW"}, {"ABW"}),
        ("G:AD", "G:AD"),
        ("", None),
        ([], None),
        (None, None),
    ],
)
def test_extended_params(input_value, expected_value):
    definition = symbol_conversion.Definition("", extended_params=input_value)

    assert definition.extended_params == expected_value


def test_extended_params_default_value():
    definition = symbol_conversion.Definition("")

    assert definition.extended_params == None


@pytest.mark.parametrize(
    "input_asset_state, input_asset_class, expected_value",
    [
        (
            AssetState.ACTIVE,
            AssetClass.COMMODITIES,
            "AssetState eq 'AC' and (SearchAllCategoryv3 in ('Commodities'))",
        ),
        (
            AssetState.INACTIVE,
            AssetClass.EQUITIES,
            "(AssetState ne 'AC' and AssetState ne null) and (SearchAllCategoryv3 in ('Equities'))",
        ),
        (
            AssetState.ACTIVE,
            [AssetClass.COMMODITIES, AssetClass.EQUITIES],
            "AssetState eq 'AC' and (SearchAllCategoryv3 in ('Commodities' 'Equities'))",
        ),
        (
            AssetState.INACTIVE,
            [AssetClass.EQUITIES, AssetClass.EQUITIES],
            "(AssetState ne 'AC' and AssetState ne null) and (SearchAllCategoryv3 in ('Equities' 'Equities'))",
        ),
    ],
)
def test_filter(input_asset_state, input_asset_class, expected_value):
    definition = symbol_conversion.Definition(
        "", asset_state=input_asset_state, asset_class=input_asset_class
    )

    assert definition._filter == expected_value


def test_filter_with_asset_state():
    definition = symbol_conversion.Definition("", asset_state=AssetState.ACTIVE)

    assert definition._filter == "AssetState eq 'AC'"


def test_filter_with_asset_class():
    definition = symbol_conversion.Definition(
        "", asset_class=[AssetClass.EQUITIES, AssetClass.EQUITIES]
    )

    assert (
        definition._filter
        == "AssetState eq 'AC' and (SearchAllCategoryv3 in ('Equities' 'Equities'))"
    )


def test_filter_default_value():
    definition = symbol_conversion.Definition("")

    assert definition._filter == None
