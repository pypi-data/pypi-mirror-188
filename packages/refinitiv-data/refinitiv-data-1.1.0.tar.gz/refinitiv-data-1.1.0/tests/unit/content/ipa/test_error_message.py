import pytest

from refinitiv.data.errors import RDError
from tests.unit.conftest import StubSession, StubResponse, parametrize_with_test_case
from tests.unit.content.ipa.conftest import ERROR_MESSAGE_TEST_CASES

args_names = "defn,cnt_data,err_msg,err_code"


@parametrize_with_test_case(
    args_names,
    ERROR_MESSAGE_TEST_CASES,
    "zc_curve_error_message",
    "forward_curve_error_message",
    "zc_curves_error_message",
    "surface_cap_error_message",
    "cap_floor_error_message",
    "cds_error_message",
    "options_error_message",
)
def test_error_message(defn, cnt_data, err_msg, err_code):
    # given
    error_match = f"Error code {err_code} | {err_msg}"

    try:
        status_code = int(err_code)
    except (ValueError, TypeError):
        status_code = None

    response = StubResponse(cnt_data, status_code)
    session = StubSession(is_open=True, response=response)
    definition = defn

    # then
    with pytest.raises(RDError, match=error_match) as e:
        # when
        definition.get_data(session)

    assert e.value.code == err_code
    assert e.value.message == err_msg
