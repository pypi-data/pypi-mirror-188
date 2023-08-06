import pytest
from refinitiv.data.delivery._data._endpoint_data import EndpointData


@pytest.mark.parametrize(
    ("attrib_name", "expected_has_attrib"), [("raw", True), ("df", False)]
)
def test_endpoint_data_attrib(attrib_name, expected_has_attrib):
    # when
    testing_has_attrib = hasattr(EndpointData, attrib_name)

    assert testing_has_attrib == expected_has_attrib
