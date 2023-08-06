def test_public_get_config():
    # given
    import refinitiv.data as rd

    # when
    config = rd.get_config()

    # then
    assert config


def test_reload_method_is_creating_new_config_object():
    # given
    from refinitiv.data import _configure as configure

    prev_config = configure.get_config()

    # when
    configure.reload()
    cur_config = configure.get_config()

    # then
    assert prev_config is not cur_config


def test_no_new_config_object_without_calling_reload_method():
    # given
    from refinitiv.data import _configure as configure

    prev_config = configure.get_config()

    # when
    cur_config = configure.get_config()

    # then
    assert prev_config is cur_config
