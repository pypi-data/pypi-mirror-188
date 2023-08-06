from tests.unit.conftest import args

from tests.unit.content.ipa import data_for_tests as dt

"""
"": args(
    defn=,
    cnt_data=,
    err_msg=,
    err_code=
)
"""
ERROR_MESSAGE_TEST_CASES = {
    "zc_curve_error_message": args(
        defn=dt.ZC_CURVE_DEFINITION,
        cnt_data=dt.ZC_CURVE_RESPONSE,
        err_msg="Validation error",
        err_code=400,
    ),
    "forward_curve_error_message": args(
        defn=dt.FORWARD_CURVE_DEFINITION,
        cnt_data=dt.FORWARD_CURVE_RESPONSE,
        err_msg="The service failed to find the curve constituents",
        err_code="QPS-Curves.10",
    ),
    "zc_curves_error_message": args(
        defn=dt.ZC_CURVES_DEFINITION,
        cnt_data=dt.ZC_CURVES_RESPONSE,
        err_msg="The service failed to find the curve definition",
        err_code="QPS-Curves.7",
    ),
    "surface_cap_error_message": args(
        defn=dt.SURFACE_CAP_DEFINITION,
        cnt_data=dt.SURFACE_CAP_RESPONSE,
        err_msg="The service failed to build the volatility surface",
        err_code="VolSurf.10300",
    ),
    "cap_floor_error_message": args(
        defn=dt.CAP_FLOOR_DEFINITION,
        cnt_data=dt.CAP_FLOOR_RESPONSE,
        err_msg="Market data error : an internal error occured. Failed to cast RateSurfaceInfoResponse.",
        err_code=None,
    ),
    "cds_error_message": args(
        defn=dt.CDS_DEFINITION,
        cnt_data=dt.CDS_RESPONSE,
        err_msg="Technical error occured.",
        err_code="QPS-DPS.1",
    ),
    "options_error_message": args(
        defn=dt.OPTION_DEFINITION,
        cnt_data=dt.OPTION_RESPONSE,
        err_msg="Technical error occured. No Realtime Data retrieved by DAL. Instrument='FCHI560000L1.p' does not exist!",
        err_code="QPS-DPS.1",
    ),
}
