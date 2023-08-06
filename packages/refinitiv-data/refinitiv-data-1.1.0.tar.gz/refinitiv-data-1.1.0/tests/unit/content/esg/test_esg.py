import numpy as np
import pytest
from pandas.core.dtypes.common import is_datetime64_any_dtype

import refinitiv.data as rd
from refinitiv.data._content_type import ContentType
from refinitiv.data.content import esg
from refinitiv.data.content.esg._base_definition import get_package_name
from refinitiv.data.content.esg._esg_data_provider import ESGRequestFactory
from tests.unit.conftest import StubResponse, StubSession


def test_esg_request_factory():
    # given
    expected_value = [("universe", "universe"), ("start", 0), ("end", 0)]
    factory = ESGRequestFactory()

    # when
    testing_value = factory.get_query_parameters(universe="universe", start=0, end=0)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "esg_definition, expected_repr",
    [
        (
            rd.content.esg.basic_overview.Definition(universe="IBM111.N"),
            "<refinitiv.data.content.esg.basic_overview.Definition object at {0} {{universe='IBM111.N'}}>",
        ),
        (
            rd.content.esg.full_measures.Definition(universe="BNPP.PA"),
            "<refinitiv.data.content.esg.full_measures.Definition object at {0} {{universe='BNPP.PA', start='None', end='None', closure='None'}}>",
        ),
        (
            rd.content.esg.full_scores.Definition(universe="5000002406"),
            "<refinitiv.data.content.esg.full_scores.Definition object at {0} {{universe='5000002406', start='None', end='None', closure='None'}}>",
        ),
        (
            rd.content.esg.standard_measures.Definition(universe="BNPP.PA"),
            "<refinitiv.data.content.esg.standard_measures.Definition object at {0} {{universe='BNPP.PA', start='None', end='None', closure='None'}}>",
        ),
        (
            rd.content.esg.standard_scores.Definition(universe="5000002406"),
            "<refinitiv.data.content.esg.standard_scores.Definition object at {0} {{universe='5000002406', start='None', end='None', closure='None'}}>",
        ),
        (
            rd.content.esg.universe.Definition(),
            "<refinitiv.data.content.esg.universe.Definition object at {0} {{closure='None'}}>",
        ),
    ],
)
def test_esg_content_repr(esg_definition, expected_repr):
    # given
    obj_id = hex(id(esg_definition))

    # when
    s = repr(esg_definition)

    # then
    assert s == expected_repr.format(obj_id)


def test_universe_get_data_when_session_is_not_open_will_raise_error():
    definition = rd.content.esg.universe.Definition()

    with pytest.raises(AttributeError):
        rd.session.set_default(None)
        definition.get_data()


def test_get_package_name_return_value():
    # given
    input_value = ContentType.ESG_STANDARD_SCORES

    # when
    package_name = get_package_name(input_value)

    # then
    assert package_name


def test_get_package_name_raise_error_if_not_exists():
    # given
    input_value = "invalid value"

    # then
    with pytest.raises(Exception):
        # when
        get_package_name(input_value)


def test_header_period_end_date_has_type_date_and_we_convert_it_to_datetime64():
    # fmt: off
    response = StubResponse({
            "links": {"count": 1}, "variability": "variable", "universe": [{
            "Instrument": "IBM.N",
            "Company Common Name": "International Business Machines Corp",
            "Organization PermID": "4295904307",
            "Reporting Currency": "USD"
        }],
            "data": [
                ["IBM.N", "2021-12-31", 100, "2023-01-12T00:00:00", 780567, 31.7, 84]],
            "messages": {
                "codes": [[-1, -1, -1, -1, -1, -1, -1]],
                "descriptions": [{"code": -1, "description": "ok"}]
            }, "headers": [{
            "name": "instrument", "title": "Instrument", "type": "string",
        }, {
            "name": "periodenddate", "title": "Period End Date",
            "type": "date",
        }, {
            "name": "TR.CSRReportingScope", "title": "ESG Reporting Scope",
            "type": "number", "decimalChar": ".",
        }, {
            "name": "TR.ESGPeriodLastUpdateDate",
            "title": "ESG Period Last Update Date", "type": "datetime",
        }, {
            "name": "TR.CO2EmissionTotal",
            "title": "CO2 Equivalents Emission Total", "type": "number",
            "decimalChar": ".",
        }, {
            "name": "TR.WomenManagers", "title": "Women Managers",
            "type": "number", "decimalChar": ".",
        }, {
            "name": "TR.AvgTrainingHours", "title": "Average Training Hours",
            "type": "number", "decimalChar": ".",
        }]})
    # fmt: on
    session = StubSession(is_open=True, response=response)

    definition = esg.basic_overview.Definition(universe=["IBM.N"])
    response = definition.get_data(session)

    df = response.data.df
    assert is_datetime64_any_dtype(df["Period End Date"])
