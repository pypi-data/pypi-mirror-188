from unittest.mock import Mock

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.content._content_data import Data
from refinitiv.data.delivery._data._data_factory import DataFactory
from refinitiv.data.delivery._data._data_provider import Response, ParsedData
from tests.unit.conftest import StubSession


def test_option_stream_definition_with_fields():
    # given
    session = StubSession(is_open=True)
    expected_fields = ["BID", "ASK"]

    # when
    definition = rdf.option.Definition(fields=expected_fields)
    definition.get_stream(session=session)

    # then
    assert definition._kwargs["fields"] == expected_fields


def test_option_stream_definition_without_fields():
    # given
    session = StubSession(is_open=True)

    # when
    definition = rdf.option.Definition()
    definition.get_stream(session=session)

    # then
    assert definition._kwargs["fields"] == [], str(definition._kwargs["fields"])


def test_option_stream_definition_without_fields_mock_response():
    # given
    path_response = Response(
        True,
        ParsedData({}, {}, {"headers": [{"name": "ASK"}, {"name": "IBM"}]}),
        DataFactory(),
    )

    session = StubSession(is_open=True)
    definition = rdf.option.Definition()
    definition.get_data = Mock(return_value=path_response)

    # when
    definition.get_stream(session=session)

    # then
    assert definition._kwargs["fields"] == ["ASK", "IBM"]
