from collections import namedtuple

from ...conftest import load_json

fund_and_ref_response = load_json(
    "./tests/unit/content/fundamental/fund_and_ref_response.json"
)

ExpectedArgs = namedtuple("ExpectedArgs", "universe, fields")

PATH_MOCK_FUNC = "refinitiv.data.content.fundamental_and_reference._data_provider.validate_correct_format_parameters"


def side_effect_func(*_, **kwargs):
    return kwargs
