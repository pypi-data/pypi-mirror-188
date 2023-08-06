import inspect
from unittest import mock

import pytest

from refinitiv.data.content.pricing import chain
from refinitiv.data.content.pricing.chain._chain_record import (
    _create_chain_record,
    config_17_chars,
)
from refinitiv.data.content.pricing.chain._stream_facade import Stream
from tests.unit.conftest import StubSession


def test_chain_record_num_constituents_is_not_none():
    fields = {
        "PROD_PERM": 5926,
        "RDNDISPLAY": 173,
        "DSPLY_NAME": "GERMAN VOLUME",
        "RDN_EXCHID": "GER",
        "TIMACT": "13:56:59",
        "CURRENCY": "EUR",
        "ACTIV_DATE": "2022-12-16",
        "NUM_MOVES": 1065349,
        "OFFCL_CODE": "0",
        "REF_COUNT": None,
        "RECORDTYPE": 117,
        "LONGLINK1": None,
        "LONGLINK2": None,
        "LONGLINK3": None,
        "LONGLINK4": None,
        "LONGLINK5": None,
        "LONGLINK6": None,
        "LONGLINK7": None,
        "LONGLINK8": None,
        "LONGLINK9": None,
        "LONGLINK10": None,
        "LONGLINK11": None,
        "LONGLINK12": None,
        "LONGLINK13": None,
        "LONGLINK14": None,
        "LONGPREVLR": "3.AV.DE",
        "PREF_DISP": 173,
        "TIMACT1": "13:56:59",
        "DDS_DSO_ID": 12388,
        "SPS_SP_RIC": ".[SPSXETRAVAE1",
    }
    chain_record = _create_chain_record(fields, config_17_chars)
    assert chain_record.num_constituents is not None
    assert chain_record.num_constituents == 0


def test_chain_stream_has_constituents_property():
    # given
    session = StubSession(is_open=True)
    stream = Stream("name", session=session)
    stream._stream.get_constituents = lambda: []

    try:
        stream.constituents
    except AttributeError as e:
        assert False, str(e)

    else:
        assert True


def test_delete_streaming_chain_class_from_public_layer():
    # given
    import refinitiv.data as rd

    # then
    with pytest.raises(AttributeError):
        # when
        rd.content.pricing.chain.StreamingChain


def test_attributes_definition():
    # given
    expected_attributes = [
        "_name",
        "_service",
        "_skip_summary_links",
        "_skip_empty",
        "_override_summary_links",
        "_extended_params",
    ]

    # when
    definition = chain.Definition("")
    attributes = list(definition.__dict__.keys())

    # then
    assert attributes == expected_attributes


def test_inspect_init_chain():
    # given
    expected_attributes = [
        "name",
        "service",
        "skip_summary_links",
        "skip_empty",
        "override_summary_links",
        "extended_params",
    ]
    inspect_pricing_init = inspect.signature(chain.Definition.__init__)

    # when
    attributes = inspect_pricing_init.parameters

    # then
    assert all(x in attributes for x in expected_attributes)


def test_smoke_get_stream_into_chain():
    # given
    session = StubSession(is_open=True)
    definition = chain.Definition("name")

    with mock.patch(
        "refinitiv.data.content.pricing.chain._stream_facade.Stream.__init__",
        return_value=None,
    ) as mock_stream:
        # when
        definition.get_stream(session=session)

        # then
        mock_stream.assert_called_once_with(
            name="name",
            session=session,
            service=None,
            skip_summary_links=True,
            skip_empty=True,
            override_summary_links=None,
            extended_params=None,
        )


def test_chain_repr():
    # given
    definition_chain = chain.Definition("0#.FTSE")
    obj_id = hex(id(definition_chain))
    expected_repr = (
        f"<refinitiv.data.content.pricing.chain.Definition object at "
        f"{obj_id} {{name='0#.FTSE'}}>"
    )

    # when
    s = repr(definition_chain)

    # then
    assert s == expected_repr
