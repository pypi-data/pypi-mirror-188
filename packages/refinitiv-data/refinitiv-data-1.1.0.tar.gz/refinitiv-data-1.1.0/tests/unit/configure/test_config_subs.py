import pytest

from refinitiv.data import _configure as configure
from .conftest import ENV_NAME, ENV_VALUE


def test_substitution_path(tmp_path):
    import os
    import platform

    env = os.environ
    p = tmp_path / "config.json"
    subs_name = ""
    if platform.system() == "Linux":
        subs_name = "PATH"
    elif platform.system() == "Windows":
        subs_name = "Path"
    else:
        subs_name = "PATH"
    p.write_text('{"prop": "${%s}"}' % subs_name)

    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop") == env.get(subs_name)


def test_substitution_no(tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"prop": "value"}')

    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop") == "value"


def test_substitution_many(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_NAME_1", "TEST_VALUE_1")
    monkeypatch.setenv("TEST_NAME_2", "TEST_VALUE_2")
    p = tmp_path / "config.json"
    p.write_text('{"prop_1": "${TEST_NAME_1}", "prop_2": "${TEST_NAME_2}"}')

    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop_1") == "TEST_VALUE_1"
    assert cfg.get("prop_2") == "TEST_VALUE_2"


def test_substitution_empty(tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"prop": "${}"}')

    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop") == "${}"


@pytest.mark.parametrize("value", [r"win\path\to\test", r"nix/path/to/test"])
def test_substitution_platform_path(tmp_path, monkeypatch, value):
    monkeypatch.setenv("TEST_PATH", value)
    p = tmp_path / "config.json"
    p.write_text('{"prop": "${TEST_PATH}", "prop_1": "path\\to\\test"}')

    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop") == value


def test_substitution_exists(mock_env_user, tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"prop": "${%s}"}' % ENV_NAME)
    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop") == ENV_VALUE


def test_substitution_not_exists(mock_env_missing, tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"prop": "${%s}"}' % ENV_NAME)
    configure.reload()
    cfg = configure._read_config_file(p)
    assert cfg.get("prop") == ENV_NAME


@pytest.mark.parametrize(
    "testing_data",
    [
        ({"root": ["root_value"], "content": {"prop": "${root}"}}, "${root}"),
        ({"root": ["root_value"], "content": {"prop": "${root:0}"}}, "root_value"),
        (
            {"root": ["foo", "root_value"], "content": {"prop": "${root:1}"}},
            "root_value",
        ),
        (
            {"root": [{"foo": "root_value"}], "content": {"prop": "${root:0:foo}"}},
            "root_value",
        ),
        ({"root": "root_value", "content": {"prop": "${root}"}}, "root_value"),
        ({"ro-ot": "root_value", "content": {"prop": "${ro-ot}"}}, "root_value"),
        ({"ro_ot": "root_value", "content": {"prop": "${ro_ot}"}}, "root_value"),
        (
            {"root": "root_value", "content": {"prop": "${root}${root}"}},
            "root_valueroot_value",
        ),
        (
            {"root": {"prop": "root_value"}, "content": {"prop": "${root:prop}"}},
            "root_value",
        ),
        (
            {
                "root": {"prop": "root_value"},
                "content": {"prop": "${root:prop}${root:prop}"},
            },
            "root_valueroot_value",
        ),
        (
            {
                "root": {"prop_1": "root_1_value", "prop_2": "root_2_value"},
                "content": {"prop": "${root:prop_1}${root:prop_2}"},
            },
            "root_1_valueroot_2_value",
        ),
        (
            {"path": {"to": {"prop": "value"}}, "content": {"prop": "${path:to:prop}"}},
            "value",
        ),
        (
            {
                "path": {"to": {"prop": "value"}},
                "content": {"prop": "${path:to:prop}_1"},
            },
            "value_1",
        ),
        (
            {
                "path": {"to": {"prop": "value"}},
                "content": {"prop_": "value_", "prop": "${content:prop_}"},
            },
            "value_",
        ),
    ],
)
def test_substitute_values(testing_data):
    input_data, expected = testing_data
    configure.reload()
    cfg = configure._substitute_values(input_data, input_data)
    assert cfg.get("content").get("prop") == expected, input_data


@pytest.mark.parametrize(
    "testing_data",
    [
        ({"content": {"prop": "${root}"}}, "${root}"),
        ({"content": {"prop": "${root}${root}"}}, "${root}${root}"),
    ],
)
def test_substitute_values_cannot_substitute(testing_data):
    input_data, expected = testing_data
    configure.reload()
    cfg = configure._substitute_values(input_data, input_data)
    assert cfg.get("content").get("prop") == expected, input_data


def test_python_configuration_package():
    """
    https://jira.refinitiv.com/browse/EAPI-1777
    https://github.com/tr11/python-configuration/issues/49
    """

    from refinitiv.data._external_libraries import (
        python_configuration as ext_config_mod,
    )

    d = {"path": {"to": {"value-a": "A", "value-b": "B"}}}
    base_cfg = ext_config_mod.config_from_dict(d)

    d = {"path": {"to": {"value-a": "C"}}}
    cfg = ext_config_mod.config_from_dict(d)

    cfg_set = ext_config_mod.ConfigurationSet(cfg, base_cfg)

    path_config = cfg_set.get("path")
    assert path_config == {"to.value-a": "C", "to.value-b": "B"}
