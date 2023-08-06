import json
import os
import uuid
from importlib import reload
from typing import TYPE_CHECKING

import pytest

import refinitiv.data as rd
import refinitiv.data.eikon as ek
from refinitiv.data import OpenState
from refinitiv.data import _configure as configure
from refinitiv.data.content import custom_instruments
from tests.integration.credentials import (
    config_for_beta_user,
    config_for_prod_user,
    Credentials,
)
from tests.integration.helpers import (
    write_prj_config,
    create_obj_with_value_by_path,
)

if TYPE_CHECKING:
    from refinitiv.data.delivery._stream.base_stream import StreamOpenMixin

CONFIG_PROD = "./tests/integration/refinitiv-data.custom.config-prod.json"
CONFIG_BETA = "./tests/integration/refinitiv-data.custom.config-beta.json"

PATH = "sessions.platform.default.base-url"
BASE_URL_BETA = "https://api.ppe.refinitiv.com"
ENV_NAME = os.environ.get("ENV_NAME")
RDP_PLATFORM = "rdp"
UDF_PLATFORM = "udf"

config_credentials = config_for_beta_user
conf = CONFIG_BETA

if ENV_NAME == "PROD":
    config_credentials = config_for_prod_user
    conf = CONFIG_PROD


def get_env_var(key):
    retval = os.environ.get(config_credentials[key])
    if retval is None:
        raise Exception(f"{config_credentials[key]} is not an env variable.")
    return retval


desktop_app_key = get_env_var("app_key")

edp = Credentials(get_env_var("username"), get_env_var("password"))
edp2 = Credentials(get_env_var("username_second"), get_env_var("password_second"))
edp3 = Credentials(get_env_var("username_third"), get_env_var("password_third"))

rdp = Credentials(get_env_var("rdp_username"), get_env_var("rdp_password"))
rdp2 = Credentials(
    get_env_var("rdp_username_second"), get_env_var("rdp_password_second")
)

eikon = Credentials(get_env_var("eikon_username"), get_env_var("eikon_password"))

PROJECT_CONFIG_PATH = os.path.join(os.getcwd(), configure._default_config_file_name)


def remove_config(path):
    while os.path.exists(path):
        try:
            os.remove(path)
            import time

            time.sleep(1)
        except (PermissionError, FileNotFoundError):
            pass


def remove_project_config():
    remove_config(PROJECT_CONFIG_PATH)


@pytest.fixture(scope="function")
def load_config():
    rd.load_config(conf)


@pytest.fixture()
def project_config_path():
    return PROJECT_CONFIG_PATH


@pytest.fixture(scope="function")
def write_project_config(project_config_path):
    def inner(arg):
        if isinstance(arg, dict):
            arg = json.dumps(arg)
        f = open(project_config_path, "w")
        f.write(arg)
        f.close()
        return project_config_path

    yield inner

    configure._dispose()
    remove_project_config()


@pytest.fixture(scope="function", autouse=False)
def set_env_base_url(write_project_config, credential_config):
    if ENV_NAME == "BETA":
        config = create_obj_with_value_by_path(PATH, BASE_URL_BETA)
        write_prj_config(config)
        reload(configure)


def _create_platform_session(credential=edp, scope="trapi"):
    return rd.session.platform.Definition(
        app_key=desktop_app_key,
        grant=rd.session.platform.GrantPassword(
            username=credential.username,
            password=credential.password,
            token_scope=scope,
        ),
    ).get_session()


def create_platform_session(credential=edp, scope="trapi"):
    return _create_platform_session(credential=credential, scope=scope)


def create_platform_session_with_rdp_creds():
    return _create_platform_session(credential=rdp)


def create_desktop_session():
    return rd.session.desktop.Definition(app_key=desktop_app_key).get_session()


@pytest.fixture(
    scope="function", params=[create_desktop_session], ids=["desktop_session"]
)
def open_desktop_session(set_env_base_url, request):
    create_session = request.param
    session = create_session()
    session.open()
    rd.session.set_default(session)
    yield session
    session.close()
    rd.session.set_default(None)


@pytest.fixture(scope="function")
def open_platform_session(set_env_base_url):
    session = create_platform_session()
    session.open()
    rd.session.set_default(session)
    yield session
    session.close()
    rd.session.set_default(None)


@pytest.fixture(scope="function")
def open_platform_session_with_rdp_creds(set_env_base_url):
    session = create_platform_session(credential=rdp)
    session.open()
    rd.session.set_default(session)
    yield session
    session.close()
    rd.session.set_default(None)


credential_sets = [
    (edp, rdp),
    (edp2, rdp2),
    (edp3, rdp),
]


@pytest.fixture()
def credential_config(request):
    if hasattr(request.config, "workerinput"):  # xdist
        node_id = int(request.config.workerinput["workerid"].replace("gw", ""))
        if (
            request.instance.pytestmark[0].args[0] == "tds"
        ):  # "tds" test suites access granted with cred #0
            node_id = 0

        global edp, rdp
        (edp, rdp) = credential_sets[node_id]


@pytest.fixture(
    scope="function",
    params=[create_platform_session, create_desktop_session],
    ids=["platform_session", "desktop_session"],
)
def open_session(request, set_env_base_url):
    create_session = request.param
    if request.instance is not None:
        if request.instance.pytestmark[0].args[0] == "news":
            set_underlying_param(request.param_index)
    session = create_session()
    session.open()
    rd.session.set_default(session)
    yield session
    session.close()
    rd.session.set_default(None)


@pytest.fixture(
    scope="function", params=[create_desktop_session], ids=["desktop_session"]
)
async def open_desktop_session_async(set_env_base_url, request):
    create_session = request.param
    session = create_session()
    await session.open_async()
    rd.session.set_default(session)
    yield session
    await session.close_async()
    rd.session.set_default(None)


@pytest.fixture(scope="function")
async def open_platform_session_async(set_env_base_url):
    session = create_platform_session()
    await session.open_async()
    rd.session.set_default(session)
    yield session
    await session.close_async()
    rd.session.set_default(None)


@pytest.fixture(scope="function")
async def open_platform_session_with_rdp_creds_async(set_env_base_url):
    session = create_platform_session(credential=rdp)
    await session.open_async()
    rd.session.set_default(session)
    yield session
    await session.close_async()
    rd.session.set_default(None)


@pytest.fixture(
    scope="function",
    params=[create_platform_session, create_desktop_session],
    ids=["platform_session", "desktop_session"],
)
async def open_session_async(request, set_env_base_url):
    create_session = request.param
    if request.instance is not None:
        if request.instance.pytestmark[0].args[0] == "news":
            set_underlying_param(request.param_index)
    session = create_session()
    await session.open_async()
    rd.session.set_default(session)
    yield session
    await session.close_async()
    rd.session.set_default(None)


def set_underlying_param(param):
    if param == 0:
        set_rdp_config("news")
    elif param == 1:
        set_udf_config("news")


def get_dict_values_as_list(dict_response):
    return [*dict_response.values()]


def get_dict_keys_as_list(dict_response):
    return [*dict_response.keys()]


def is_open(stream: "StreamOpenMixin") -> bool:
    return stream.open_state is OpenState.Opened


def set_udf_config(content_name):
    rd.get_config().set_param(
        param=f"apis.data.{content_name}.underlying-platform", value=UDF_PLATFORM
    )


def set_rdp_config(content_name):
    rd.get_config().set_param(
        param=f"apis.data.{content_name}.underlying-platform", value=RDP_PLATFORM
    )


@pytest.fixture(
    scope="function",
    params=[set_rdp_config, set_udf_config],
    ids=["rdp-underlying-platform", "udf-underlying-platform"],
)
def set_underlying_platform_config(request):
    content_name = request.instance.pytestmark[0].args[0]
    request.param(content_name)
    underlying_platform_type = request.node.callspec.id[:23]
    yield underlying_platform_type


@pytest.fixture(scope="function", params=["desktop_session"], ids=["desktop_session"])
def setup_app_key():
    ek.set_app_key(desktop_app_key)


@pytest.fixture(name="create_instrument")
def create_unique_instrument():
    instruments = []

    def create_instrument(
        session=None, type_=None, formula=None, udc=None, basket=None
    ):
        universe_name = str(uuid.uuid4())[:8]
        if type_ is None and formula is None:
            formula = "GBP=*3"
        instrument = custom_instruments.manage.create(
            symbol=universe_name,
            instrument_name="FinTechRate",
            type_=type_,
            formula=formula,
            basket=basket,
            udc=udc,
            currency="USD",
            time_zone="UTC",
            description="Story about custom instrument",
            exchange_name="1234",
            session=session,
        )
        symbol = instrument.symbol
        instruments.append((symbol, session))
        return symbol

    yield create_instrument

    for symbol, session in instruments:
        if session is not None:
            session.open()
        response = custom_instruments.search.Definition().get_data(session=session)
        symbols = response.data.df["symbol"].values
        if symbol in symbols:
            custom_instruments.manage.delete(universe=symbol, session=session)


@pytest.fixture
def create_session_with_scope(set_env_base_url):
    tmp = {}

    def _create_session_with_scope(scope, acc):
        session = None
        if acc == "machine":
            session = create_platform_session(credential=edp, scope=scope)
        elif acc == "eikon":
            session = create_platform_session(credential=eikon, scope=scope)
        session.open()
        rd.session.set_default(session)
        tmp.update({"session": session})
        return session

    yield _create_session_with_scope
    session = tmp.get("session")
    session.close()
