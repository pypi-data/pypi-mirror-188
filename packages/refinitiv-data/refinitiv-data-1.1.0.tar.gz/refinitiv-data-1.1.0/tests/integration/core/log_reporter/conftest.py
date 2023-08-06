import pytest

import refinitiv.data as rd


@pytest.fixture(scope="function", autouse=False)
def enabled_log():
    rd.get_config().set_param(param=f"logs.transports.console.enabled", value=True)
    rd.get_config().set_param(param=f"logs.transports.file.enabled", value=True)
