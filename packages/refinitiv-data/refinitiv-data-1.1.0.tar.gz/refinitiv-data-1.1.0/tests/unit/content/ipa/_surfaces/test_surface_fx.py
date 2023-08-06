from unittest.mock import Mock

from refinitiv.data.content.ipa.surfaces import fx


def test_surfaces_fx_definition_repr():
    # given
    mock_surface_layout = Mock()
    mock_surface_parameters = Mock()
    definition = fx.Definition(
        surface_layout=mock_surface_layout,
        surface_parameters=mock_surface_parameters,
        underlying_definition={},
    )
    expected_value = (
        f"<refinitiv.data.content.ipa.surfaces.fx.Definition "
        f"object at {hex(id(definition))}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value


def test_surfaces_fx_definition_output_repr():
    # given
    definition = fx.SurfaceLayout()
    expected_value = (
        f"<refinitiv.data.content.ipa.surfaces.fx.SurfaceLayout "
        f"object at {hex(id(definition))}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value
