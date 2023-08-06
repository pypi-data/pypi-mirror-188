import pytest

from refinitiv.data.delivery.cfs import file_sets


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
    definition = file_sets.Definition("")

    # then
    assert hasattr(definition, value)
