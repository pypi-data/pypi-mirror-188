import pandas as pd
import pytest

from refinitiv.data.content.search import Views
from refinitiv.data.content.search._data_provider import (
    SearchRequestFactory,
    LookupRequestFactory,
    BaseSearchRequestFactory,
    MetadataRequestFactory,
    _get_unique_keys,
    discovery_search_build_df,
    discovery_lookup_build_df,
)
from refinitiv.data.delivery._data._endpoint_data import RequestMethod


def tests_base_search_request_factory_get_request_method():
    # given
    factory = BaseSearchRequestFactory()

    # when
    testing_value = factory.get_request_method()

    # then
    assert testing_value == RequestMethod.POST


def tests_base_search_request_factory_get_body_parameters():
    # given
    factory = SearchRequestFactory()

    # when
    testing_value = factory.get_body_parameters()

    # then
    assert testing_value == {}


def tests_search_request_factory_get_body_parameters_pass_view():
    # given
    factory = SearchRequestFactory()

    # when
    testing_value = factory.get_body_parameters(**{"view": Views.SEARCH_ALL})

    # then
    assert "View" in testing_value
    assert testing_value["View"] == Views.SEARCH_ALL.value


def tests_search_request_factory_get_body_parameters_pass_args():
    # given
    factory = SearchRequestFactory()
    extended_body_params = [
        "Boost",
        "Features",
        "Filter",
        "GroupBy",
        "GroupCount",
        "Navigators",
        "OrderBy",
        "Query",
        "Scope",
        "Select",
        "Skip",
        "Terms",
        "Top",
    ]

    # when
    testing_value = factory.get_body_parameters(
        **{
            "boost": "value_boost",
            "features": "value_features",
            "filter": "value_filter",
            "group_by": "value_group_by",
            "group_count": "value_group_count",
            "navigators": "value_navigators",
            "order_by": "value_order_by",
            "query": "value_query",
            "scope": "value_scope",
            "select": "value_select",
            "skip": "value_skip",
            "terms": "value_terms",
            "top": "value_top",
        }
    )

    # then
    for param in extended_body_params:
        assert param in testing_value
        assert testing_value[param]


def tests_lookup_request_factory_get_body_parameters_pass_args():
    # given
    factory = LookupRequestFactory()
    extended_body_params = [
        "Boost",
        "Filter",
        "Scope",
        "Select",
        "Terms",
    ]

    # when
    testing_value = factory.get_body_parameters(
        **{
            "boost": "value_boost",
            "filter": "value_filter",
            "scope": "value_scope",
            "select": "value_select",
            "terms": "value_terms",
        }
    )

    # then
    for param in extended_body_params:
        assert param in testing_value
        assert testing_value[param]


def tests_metadata_request_factory_get_query_parameters_pass_view():
    # given
    factory = MetadataRequestFactory()

    # when
    testing_value = factory.get_query_parameters(**{"view": Views.SEARCH_ALL})

    # then
    assert testing_value == Views.SEARCH_ALL.value


def test_metadata_request_factory_add_query_parameters():
    # given
    factory = MetadataRequestFactory()

    # when
    testing_value = factory.add_query_parameters(url="url", query_parameters="test")

    # then
    assert testing_value == "url/test"


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ([{}, {}], []),
        ([{"a": 1, "b": 2}, {"a": 11, "b": 22}], ["a", "b"]),
        (
            [{"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 1}, {"a": 1, "b": 2}],
            ["a", "b", "c"],
        ),
        (
            [{"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 1}, {"a": 1, "d": 4, "b": 2}],
            ["a", "b", "c", "d"],
        ),
    ],
)
def test__get_unique_keys(input_value, expected_value):
    # when
    result = _get_unique_keys(input_value)

    # then
    assert result == expected_value


def test_convert_search_json_to_pandas():
    data = {
        "Hits": [
            {
                "BusinessEntity": "ORGANISATION",
                "DocumentTitle": "International Business Machines Corp, "
                "Public Company",
                "PI": "37036",
                "RIC": None,
            },
            {
                "BusinessEntity": "ORGANISATION",
                "DocumentTitle": "Banco IBM SA, Private Company",
                "PI": "76208",
                "RIC": "",
            },
            {
                "BusinessEntity": "QUOTExEQUITY",
                "DocumentTitle": "International Business Machines Corp, Ordinary "
                "Share, NYSE Consolidated",
                "PermID": "55839165994",
                "PI": "1097326",
                "RIC": "IBM",
            },
        ]
    }
    df = discovery_search_build_df(data)
    for row in df.itertuples():
        if row.PI == "37036":
            assert row.RIC is pd.NA
        if row.PI == "76208":
            assert isinstance(row.RIC, str)
            assert row.RIC == ""
        if row.PI == "1097326":
            assert isinstance(row.RIC, str)
            assert row.RIC == "IBM"


@pytest.mark.parametrize(
    "name_field",
    [
        "Date",
        "IssueDate",
        "Issue Date",
        "DateIssue",
        "Date Issue",
        "IssDateue",
        "Iss Date ue",
    ],
)
def test_convert_search_json_to_pandas_date_data_successful(name_field):
    # given
    data = {"Hits": [{name_field: "2019-05-15T00:00:00.000Z"}]}

    # when
    df = discovery_search_build_df(data)

    # then
    assert df[name_field].dtypes == "datetime64[ns]"


@pytest.mark.parametrize(
    "name_field",
    [
        "date",
        "Da te",
        "Issuedate",
        "Issue date",
        "dateIssue",
        "date Issue",
        "Issdateue",
        "Iss date ue",
    ],
)
def test_convert_search_json_to_pandas_date_data_fail(name_field):
    # given
    data = {"Hits": [{name_field: "2019-05-15T00:00:00.000Z"}]}

    # when
    df = discovery_search_build_df(data)

    # then
    assert df[name_field].dtypes != "datetime64[ns, UTC]"


def test__convert_lookup_json_to_df():
    data = {
        "Matches": {
            "MSFT.O": {
                "BusinessEntity": "INSTRUMENTxEQUITY",
                "DocumentTitle": "Microsoft Corp, Ordinary Share",
                "CUSIP": "594918104",
            },
            "GOOG.O": {
                "BusinessEntity": "INSTRUMENTxEQUITY",
                "DocumentTitle": "Alphabet Inc, Ordinary Share",
                "CUSIP": "",
            },
            "KBANK.BK": {
                "BusinessEntity": "INSTRUMENTxEQUITY",
                "DocumentTitle": "Kasikornbank PCL, Ordinary Share",
                "SEDOL": "6888783",
            },
        }
    }
    df = discovery_lookup_build_df(data)
    for row in df.itertuples():
        if row.DocumentTitle[0] == "MSFT.O":
            assert row.SEDOL is pd.NA
            assert isinstance(row.CUSIP, str)
            assert row.CUSIP == "594918104"
        if row.DocumentTitle[0] == "GOOG.O":
            assert row.SEDOL is pd.NA
            assert isinstance(row.CUSIP, str)
            assert row.CUSIP == ""
        if row.DocumentTitle[0] == "KBANK.BK":
            assert row.CUSIP is pd.NA
            assert isinstance(row.SEDOL, str)
            assert row.SEDOL == "6888783"


def test_definition_parameters_is_not_none():
    # given
    request_factory = SearchRequestFactory()

    # when
    body_parameters = request_factory.get_body_parameters(**{"top": 0})

    # then
    assert body_parameters["Top"] == 0
