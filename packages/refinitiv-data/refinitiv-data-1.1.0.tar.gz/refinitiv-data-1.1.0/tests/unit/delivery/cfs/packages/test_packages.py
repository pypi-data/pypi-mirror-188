import pytest

from refinitiv.data._tools import inspect_parameters_without_self
from refinitiv.data.delivery.cfs import packages
from tests.unit.conftest import StubSession
from tests.unit.delivery.cfs.conftest import PACKAGES_RESPONSES
import refinitiv.data as rd


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


def test_fist_argument():
    # when
    args_class = list(inspect_parameters_without_self(packages.Definition))
    test_first_arg = args_class[0]

    # then
    assert test_first_arg == "package_name"


@pytest.mark.parametrize(
    "is_default_session",
    [True, False],
    ids=[
        "use default session",
        "without default session",
    ],
)
def test_iteration_by_packages_without_error(is_default_session):
    # given
    session = StubSession(is_open=True, response=PACKAGES_RESPONSES)
    definition = packages.Definition("Bulk-ESG-Global-Scores-Wealth-Standard-v1")

    if is_default_session:
        rd.session.set_default(session)
        response = definition.get_data()

    else:
        response = definition.get_data(session=session)

    # when
    try:
        for package in response.data.packages:
            for fileset in package:
                value = fileset
    except Exception as e:
        rd.session.set_default(None)
        assert False, str(e)

    # then
    else:
        rd.session.set_default(None)
        assert True
