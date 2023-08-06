import pytest

from refinitiv.data.delivery.cfs._data_types import BucketData
from refinitiv.data.delivery.cfs._iter_object import BaseCFSObject


@pytest.mark.parametrize(
    "input_session, expected_session",
    [
        (None, None),
        ([], []),
        ("filename", "filename"),
    ],
)
def test_attribute_session_in_BaseCFSObject(input_session, expected_session):
    # when
    obj = BaseCFSObject({}, BucketData, session=input_session)

    # then
    assert hasattr(obj, "_session")
    assert obj._session == expected_session
