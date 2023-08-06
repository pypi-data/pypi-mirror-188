import pytest
from unittest.mock import patch

from refinitiv.data._content_type import ContentType


@pytest.fixture(
    scope="function",
    params=[
        ContentType.FORWARD_CURVE,
        ContentType.ZC_CURVES,
        ContentType.ZC_CURVE_DEFINITIONS,
        ContentType.SURFACES,
        ContentType.CONTRACTS,
    ],
)
def content_type(request):
    return request.param


@pytest.fixture(autouse=True, scope="module")
def change_delays():
    with patch.multiple(
        "refinitiv.data.content.ipa._ipa_content_provider",
        DELAY_BETWEEN_TWO_GET_ASYNC_OPERATION=0,
        DELAY_BEFORE_FIRST_GET_ASYNC_OPERATION=0,
    ):
        yield
