from refinitiv.data.content.ipa.curves import zc_curve_definitions
from tests.unit.conftest import remove_dunder_methods, remove_private_attributes


def test_zc_curve_definitions_scope():
    expected_attributes = ["AssetClass", "Definition", "Definitions", "RiskType"]
    testing_attributes = dir(zc_curve_definitions)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes
