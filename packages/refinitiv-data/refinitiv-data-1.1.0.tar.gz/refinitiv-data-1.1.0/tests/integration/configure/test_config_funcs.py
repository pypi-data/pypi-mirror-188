from refinitiv.data import _configure as configure


def test_get_config_default_user(write_user_config):
    write_user_config('{"user_prop": "user_value"}')

    configure.reload()

    assert configure.get_config().get("user_prop") == "user_value"


def test_get_config_default_project(write_project_config):
    write_project_config('{"project_prop": "project_value"}')

    configure.reload()

    assert configure.get_config().get("project_prop") == "project_value"


def test_get_config_default_user_project(write_user_config, write_project_config):
    write_project_config('{"project_prop": "project_value"}')
    write_user_config('{"user_prop": "user_value"}')

    configure.reload()

    assert configure.get_config().get("user_prop") == "user_value"
    assert configure.get_config().get("project_prop") == "project_value"


def test_get_config_override_default_prop_by_user(write_user_config):
    default_prop = "endpoint.env"
    user_value = "user_value"
    write_user_config('{"%s": "%s"}' % (default_prop, user_value))

    configure.reload()
    assert configure.get_config().get(default_prop) == user_value


def test_get_config_override_default_prop_by_project(write_project_config):
    default_prop = "endpoint.env"
    project_value = "project_value"
    write_project_config('{"%s": "%s"}' % (default_prop, project_value))

    configure.reload()
    assert configure.get_config().get(default_prop) == project_value


def test_get_config_override_user_prop_by_project(
    write_user_config, write_project_config
):
    prop = "endpoint.env"
    project_value = "project_value"
    user_value = "user_value"
    write_project_config('{"%s": "%s"}' % (prop, project_value))
    write_user_config('{"%s": "%s"}' % (prop, user_value))

    configure.reload()
    assert configure.get_config().get(prop) == project_value


def test_get_config_does_not_override_project_prop_by_user(
    write_user_config, write_project_config
):
    default_prop = "endpoint.env"
    project_value = "project_value"
    user_value = "user_value"
    write_project_config('{"%s": "%s"}' % (default_prop, project_value))
    write_user_config('{"%s": "%s"}' % (default_prop, user_value))

    configure.reload()
    value = configure.get_config().get(default_prop)
    assert value != user_value and value == project_value
