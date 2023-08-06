from enum import Enum

import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data._core.session import SessionType
from refinitiv.data.content.fundamental_and_reference import RowHeaders
from refinitiv.data.content.fundamental_and_reference._definition import (
    row_headers_arg_parser,
)


def create_definition_and_session(platform, session_type):
    config = StubConfig(
        {
            "apis.data.datagrid": {
                "url": "/data/datagrid/beta1",
                "underlying-platform": platform,
                "endpoints.standard": "/",
            },
            "raise_exception_on_error": True,
        }
    )
    response = StubResponse(content_data={"responses": [fund_and_ref_response]})
    session = StubSession(response=response, config=config, is_open=True)
    session.type = session_type
    definition = fundamental_and_reference.Definition([], [], row_headers="date")
    return definition, session


class EnumTest(Enum):
    TEST = "test"
    DATE = "date"


@pytest.mark.parametrize(
    "input_value,expected_value",
    [
        (None, []),
        ([], []),
        ("date", [RowHeaders.DATE]),
        (["date"], [RowHeaders.DATE]),
        (RowHeaders.DATE.value, [RowHeaders.DATE]),
        (RowHeaders.DATE, [RowHeaders.DATE]),
    ],
)
def test_parse_row_headers_correct(input_value, expected_value):
    # when
    testing_value = row_headers_arg_parser.get_list(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value",
    [
        1,
        {},
        EnumTest,
        EnumTest.TEST,
        EnumTest.TEST.value,
        EnumTest.DATE,
    ],
)
def test_parse_row_headers_failed(input_value):
    # then
    with pytest.raises(ValueError):
        # when
        row_headers_arg_parser.get_list(input_value)


from refinitiv.data.content import fundamental_and_reference
from tests.unit.conftest import StubSession, StubResponse, StubConfig
from tests.unit.content.fundamental.conftest import fund_and_ref_response


def test_workspace():
    from refinitiv.data.content import fundamental_and_reference

    assert hasattr(fundamental_and_reference, "Definition")


def test_attributes():
    # given
    excepted_attributes = [
        "universe",
        "fields",
        "parameters",
        "use_field_names_in_headers",
        "extended_params",
        "row_headers",
        "_kwargs",
        "_data_type",
        "_content_type",
        "_provider",
    ]

    # when
    definition = fundamental_and_reference.Definition(universe=[], fields=[])
    attributes = list(definition.__dict__.keys())

    # then
    assert attributes == excepted_attributes


def test_definition_fundamental_and_reference_repr():
    # given
    definition = fundamental_and_reference.Definition([], [])
    obj_id = hex(id(definition))
    expected_value = (
        f"<refinitiv.data.content.fundamental_and_reference.Definition object at {obj_id} {{universe='["
        f"]', fields='[]', parameters='None', row_headers='None'}}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value


def test_platform_session_and_udf_layout_config_will_be_string():
    # given
    definition, session = create_definition_and_session("udf", SessionType.PLATFORM)

    # when
    definition.get_data(session)

    # then
    assert isinstance(definition._kwargs["layout"]["output"], str) is True
    assert definition._content_type == ContentType.DATA_GRID_RDP


def test_desktop_session_and_udf_layout_config_will_be_dict():
    # given
    definition, session = create_definition_and_session("udf", SessionType.DESKTOP)

    # when
    definition.get_data(session)

    # then
    assert isinstance(definition._kwargs["layout"], dict) is True
    assert definition._content_type == ContentType.DATA_GRID_UDF


def test_desktop_session_and_rdp_layout_config_will_be_dict():
    # given
    definition, session = create_definition_and_session("rdp", SessionType.DESKTOP)

    # when
    definition.get_data(session)

    # then
    assert isinstance(definition._kwargs["layout"]["output"], str) is True
    assert definition._content_type == ContentType.DATA_GRID_RDP


def test_platform_session_and_rdp_layout_config_will_be_string():
    # given
    definition, session = create_definition_and_session("rdp", SessionType.PLATFORM)

    # when
    definition.get_data(session)

    # then
    assert isinstance(definition._kwargs["layout"]["output"], str) is True
    assert definition._content_type == ContentType.DATA_GRID_RDP


def test_rdp_do_not_convert_number_to_date_if_field_have_function_and_date_into():
    response = StubResponse(
        # fmt: off
        {
            "links": {"count": 5}, "variability": "",
            "universe": [{
                "Instrument": "GOOG.O",
                "Company Common Name": "Alphabet Inc",
                "Organization PermID": "5030853586",
                "Reporting Currency": "USD"
            }, {
                "Instrument": "MSFT.O",
                "Company Common Name": "Microsoft Corp",
                "Organization PermID": "4295907168",
                "Reporting Currency": "USD"
            }, {
                "Instrument": "FB.O",
                "Company Common Name": "Meta Platforms Inc",
                "Organization PermID": "4297297477",
                "Reporting Currency": "USD"
            }, {
                "Instrument": "AMZN.O",
                "Company Common Name": "Amazon.com Inc",
                "Organization PermID": "4295905494",
                "Reporting Currency": "USD"
            }, {
                "Instrument": "TWTR.K",
                "Company Common Name": "Twitter Inc",
                "Organization PermID": "4296301199",
                "Reporting Currency": "USD"
            }],
            "data": [["GOOG.O", 92.168064516129], ["MSFT.O", 241.904193548387],
                     ["FB.O", 121.724838709677], ["AMZN.O", 88.6803225806452],
                     ["TWTR.K", 53.7]],
            "messages": {
                "codes": [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}]
            },
            "headers": [{
                "name": "instrument", "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user."
            }, {
                "name": "AVG(TR.Close(Edate=0, SDate = -30))",
                "title": "AVG(TR.Close(Edate=0, SDate = -30))",
                "type": "number", "decimalChar": ".", "description": None
            }]
        }
        # fmt: on
    )
    session = StubSession(is_open=True, response=response)
    session.config.set_param("apis.data.datagrid.underlying-platform", "rdp")
    field = "AVG(TR.Close(Edate=0, SDate = -30))"
    definition = fundamental_and_reference.Definition(
        universe=["GOOG.O", "MSFT.O", "FB.O", "AMZN.O", "TWTR.K"], fields=[field]
    )
    response = definition.get_data(session)

    assert response.data.df[field][0] == 92.168064516129


def test_udf_do_not_convert_number_to_date_if_field_have_function_and_date_into():
    response = StubResponse(
        # fmt: off
        {
            "responses": [{
                "columnHeadersCount": 1,
                "data": [["GOOG.O", 91.8683870967742], ["MSFT.O", 241.427096774194],
                         ["FB.O", 122.281612903226], ["AMZN.O", 88.6645161290323],
                         ["TWTR.K", 53.7]],
                "headerOrientation": "horizontal",
                "headers": [
                    [{"displayName": "Instrument"}, {
                        "displayName": "AVG(TR.Close(Edate=0, SDate = -30))",
                        "field": "AVG(TR.Close(Edate=0, SDate = -30))"
                    }]], "rowHeadersCount": 1, "totalColumnsCount": 2,
                "totalRowsCount": 6
            }]
        }
        # fmt: on
    )
    session = StubSession(is_open=True, response=response)
    session.type = SessionType.DESKTOP
    session.config.set_param("apis.data.datagrid.underlying-platform", "udf")
    field = "AVG(TR.Close(Edate=0, SDate = -30))"
    instrument = "GOOG.O"
    definition = fundamental_and_reference.Definition(
        universe=[instrument, "MSFT.O", "FB.O", "AMZN.O", "TWTR.K"], fields=[field]
    )
    response = definition.get_data(session)

    assert response.data.df[field][0] == 91.8683870967742
    assert response.data.df["Instrument"][0] == instrument
