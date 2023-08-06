import pytest

from refinitiv.data.content.ipa.curves import forward_curves
from tests.unit.conftest import load_json


forward_curves_json = load_json("./tests/unit/content/ipa/_curves/forward_curves.json")
zc_curves_json = load_json("./tests/unit/content/ipa/_curves/zc_curves.json")
zc_curve_definitions_json = load_json(
    "./tests/unit/content/ipa/_curves/zc_curve_definitions.json"
)
zc_curves_definitions_json = load_json(
    "./tests/unit/content/ipa/_curves/zc_curves_definitions.json"
)


def create_forward_curve_definition1():
    forward_curve_def = create_forward_curve_def()
    swap_zc_curve_def = create_swap_zc_curve_def()

    definition = forward_curves.Definition(
        curve_definition=swap_zc_curve_def,
        forward_curve_definitions=[forward_curve_def],
        curve_parameters=forward_curves.SwapZcCurveParameters(),
        curve_tag="some_tag",
    )
    return definition


def create_forward_curve_definition2():
    swap_zc_curve_def = create_swap_zc_curve_def()
    forward_curve_def = create_forward_curve_def()

    definition = forward_curves.Definition(swap_zc_curve_def, [forward_curve_def])
    return definition


@pytest.fixture(
    scope="function",
    params=[create_forward_curve_definition1, create_forward_curve_definition2],
)
def forward_curve_definition(request):
    return request.param()


def create_swap_zc_curve_def():
    definition = forward_curves.SwapZcCurveDefinition(
        currency="EUR",
        index_name="EURIBOR",
        discounting_tenor="OIS",
    )
    return definition


def create_forward_curve_def():
    definition = forward_curves.ForwardCurveDefinition(
        index_tenor="3M",
        forward_curve_tag="ForwardTag",
        forward_start_date="2021-02-01",
        forward_curve_tenors=["0D", "1D"],
        forward_start_tenor="some_start_tenor",
    )
    return definition


def create_outputs():
    outputs = forward_curves.Outputs.CONSTITUENTS
    return outputs
