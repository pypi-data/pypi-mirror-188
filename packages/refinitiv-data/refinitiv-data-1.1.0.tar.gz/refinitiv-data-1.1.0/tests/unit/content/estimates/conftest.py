import pytest
from refinitiv.data.content.estimates._enums import Package

success_param = [
    ({"universe": "test_value", "package": Package.BASIC}),
    ({"universe": "test_value", "package": Package.STANDARD}),
    ({"universe": "test_value", "package": Package.PROFESSIONAL}),
    (
        {
            "universe": "test_value",
            "package": Package.BASIC,
            "use_field_names_in_headers": False,
        }
    ),
    (
        {
            "universe": "test_value",
            "package": Package.STANDARD,
            "use_field_names_in_headers": False,
        }
    ),
    (
        {
            "universe": "test_value",
            "package": Package.PROFESSIONAL,
            "use_field_names_in_headers": False,
        }
    ),
    (
        {
            "universe": "test_value",
            "package": Package.BASIC,
            "use_field_names_in_headers": True,
        }
    ),
    (
        {
            "universe": "test_value",
            "package": Package.STANDARD,
            "use_field_names_in_headers": True,
        }
    ),
    (
        {
            "universe": "test_value",
            "package": Package.PROFESSIONAL,
            "use_field_names_in_headers": True,
        }
    ),
]

error_param = [
    ({"universe": "test_value", "package": 1}),
    ({"universe": "test_value", "package": []}),
    ({"universe": "test_value", "package": {}}),
    (
        {
            "universe": "test_value",
            "package": Package.BASIC,
            "use_field_names_in_headers": 1,
        }
    ),
    (
        {
            "universe": "test_value",
            "package": Package.BASIC,
            "use_field_names_in_headers": "true",
        }
    ),
]

success_param_kpi = [
    ({"universe": "test_value"}),
    ({"universe": "test_value", "use_field_names_in_headers": False}),
    ({"universe": "test_value", "use_field_names_in_headers": True}),
]

error_param_kpi = [
    ({"universe": "test_value", "package": 1}),
    ({"universe": "test_value", "package": []}),
    ({"universe": "test_value", "package": {}}),
    ({"universe": "test_value", "use_field_names_in_headers": 1}),
    ({"universe": "test_value", "use_field_names_in_headers": "true"}),
]


@pytest.fixture(params=success_param)
def create_estimates_definition(request):
    try:
        yield request.param
    except Exception as e:
        assert False, str(e)


@pytest.fixture(params=error_param)
def create_estimates_definition_with_error(request):
    return request.param


@pytest.fixture(params=success_param_kpi)
def create_estimates_kpi_definition(request):
    try:
        yield request.param
    except Exception as e:
        assert False, str(e)


@pytest.fixture(params=error_param_kpi)
def create_estimates_kpi_definition_with_error(request):
    return request.param
