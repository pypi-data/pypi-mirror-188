import logging
from types import SimpleNamespace

import pytest

from refinitiv.data.content.esg.bulk._actions import Actions
from refinitiv.data.content.esg.bulk._db_manager import create_db_manager
from refinitiv.data.content.esg.bulk._file_manager import FileManager


def create_actions():
    actions = SimpleNamespace()
    actions.add = lambda *_, **__: None
    actions.updated = lambda *_, **__: None
    actions.update = lambda *_, **__: None
    actions.get_created_tables = lambda: []
    return actions


logger = logging.getLogger("test-db-manager")

config = {
    "connection.parameters.database": ":memory:",
    "create-table-queries": [],
    "insert-queries": [],
    "connection.module": "sqlite3",
}

id_counter = 0


@pytest.fixture(scope="function")
def actions():
    global id_counter
    id_counter += 1
    actions_ = Actions(id_=id_counter, logpath="./tests/unit/content/esg/bulk/log.txt")
    yield actions_
    actions_.dispose()


@pytest.fixture
def file_manager(actions):
    file_manager = FileManager(
        logger=logger,
        actions=actions,
        package_name="",
        bucket="",
        path="",
        session=None,
    )
    return file_manager


@pytest.fixture()
def db_manager():
    manager = create_db_manager(config, create_actions(), logger)
    return manager


def raise_(exception):
    raise exception
