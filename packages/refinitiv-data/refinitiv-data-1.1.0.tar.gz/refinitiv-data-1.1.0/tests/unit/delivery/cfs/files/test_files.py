import pytest

from refinitiv.data.delivery.cfs import files


@pytest.mark.parametrize(
    "value",
    [
        "get_data",
        "get_data_async",
    ],
)
def test_attribute(value):
    # given

    # when
    definition = files.Definition("")

    # then
    assert hasattr(definition, value)
