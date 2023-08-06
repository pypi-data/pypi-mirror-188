import pytest

import refinitiv.data as rd
from refinitiv.data._errors import RDError
from refinitiv.data.delivery import cfs
from refinitiv.data.delivery.cfs import packages
from tests.unit.conftest import StubSession, StubResponse


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
    definition = packages.Definition("")

    # then
    assert hasattr(definition, value)


def test_invalid_fileset_id():
    session = StubSession(
        is_open=True,
        response=StubResponse(
            {
                "error": {
                    "id": "716e6298-24db-456a-b30f-2995f4c0ae84",
                    "code": "EDS.CFS.NoFilesetFound",
                    "status": 404,
                    "message": "No resource found for: ResourceType=Fileset; ResourceId=invalid fileset id",
                }
            },
            status_code=404,
        ),
    )
    rd.session.set_default(session)

    with pytest.raises(
        RDError,
        match=r"Error code 404 | No resource found for: ResourceType=Fileset; ResourceId=invalid fileset id",
    ):
        cfs.files.Definition("invalid fileset id").get_data()

    rd.session.set_default(None)


def test_non_existing_bucket_name():
    session = StubSession(
        is_open=True,
        response=StubResponse(
            {
                "error": {
                    "id": "53a7dae3-e455-483b-98d1-4500ce067065",
                    "code": "EDS.CFS.NoBucketFound",
                    "status": 404,
                    "message": "No resource found for: ResourceType=Bucket; ResourceId=non-existing bucket name",
                }
            },
            status_code=404,
        ),
    )
    rd.session.set_default(session)
    with pytest.raises(
        RDError,
        match=r"Error code 404 | No resource found for: ResourceType=Bucket; ResourceId=non-existing bucket name",
    ):
        cfs.file_sets.Definition(bucket="non-existing bucket name").get_data()

    rd.session.set_default(None)
