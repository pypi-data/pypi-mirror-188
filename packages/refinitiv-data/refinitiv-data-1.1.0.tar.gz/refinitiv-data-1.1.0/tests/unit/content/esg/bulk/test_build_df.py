from types import SimpleNamespace

from refinitiv.data._config_defaults import data as _config_defaults_data
from refinitiv.data._external_libraries import python_configuration as ext_config_mod
from refinitiv.data.content.esg.bulk._db_manager import DBManager
from tests.unit.conftest import StubLogger


def test_build_df():
    connection = SimpleNamespace()
    cursor = SimpleNamespace()
    cursor.description = []
    connection.cursor = lambda: cursor
    config = ext_config_mod.config_from_dict(
        _config_defaults_data["bulk"]["esg"]["standard_scores"]["db"]
    )
    actions = SimpleNamespace()
    db_manager = DBManager(connection, config, actions, StubLogger())
    db_manager.exec = lambda *args: {}

    data = db_manager.get_data(universe=[], fields=[])

    assert data.df.empty


def test_build_df_when_exec_raised_error():
    def exec(*args, **kwargs):
        raise Exception()

    connection = SimpleNamespace()
    cursor = SimpleNamespace()
    cursor.description = []
    connection.cursor = lambda: cursor
    config = ext_config_mod.config_from_dict(
        _config_defaults_data["bulk"]["esg"]["standard_scores"]["db"]
    )
    actions = SimpleNamespace()
    actions.add = lambda *args, **kwargs: None
    db_manager = DBManager(connection, config, actions, StubLogger())
    db_manager.exec = exec

    data = db_manager.get_data(universe=[], fields=[])

    assert data.df.empty
