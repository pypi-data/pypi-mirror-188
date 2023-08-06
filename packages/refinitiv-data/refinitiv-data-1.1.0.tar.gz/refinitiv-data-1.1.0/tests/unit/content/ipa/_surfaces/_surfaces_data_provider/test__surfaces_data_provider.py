import pytest

from refinitiv.data.content.ipa._enums import Axis
from refinitiv.data.content.ipa._surfaces._surfaces_data_provider import (
    SurfaceResponseFactory,
    SurfacesContentValidator,
    get_type_by_axis,
    parse_axis,
    OneSurfaceData,
)
from refinitiv.data.delivery._data._data_provider import ParsedData
from .conftest import StubDefinition


def test_surface_response_factory_create_success():
    # given
    input_value = ParsedData({}, {}, [{}])
    universe = [StubDefinition(axis=None)]
    response_factory = SurfaceResponseFactory()

    # when
    testing_value = response_factory.create_success(input_value, universe=universe)

    # then
    assert testing_value is not None


def test_data_class_surface_property():
    # given
    input_value = {"data": [{"surface": [[1], [2]]}]}
    data = OneSurfaceData(input_value, [(Axis.TENOR, Axis.TENOR)])

    # when
    surface = data.surface

    # then
    assert surface is not None


def test_curves_and_surfaces_content_validator_validate_content_data_is_false():
    # given
    input_value = ParsedData({}, {}, {"data": [{"error": {"status": "Error"}}]})
    expected_value = False
    validator = SurfacesContentValidator()

    # when
    testing_value = validator.validate(input_value)

    # then
    assert testing_value == expected_value


def test_get_type_by_axis_raise_error_if__cannot_find():
    with pytest.raises(ValueError, match="Cannot find axis's values type for axis"):
        get_type_by_axis(None)


def test_parse_axis_raise_error_if_axis_dont_passed():
    universe = {"surface": [[1], [2]]}
    with pytest.raises(ValueError, match="Cannot parse surface without information"):
        parse_axis(universe, None, None)
