from refinitiv.data import _configure as configure


def test_watch_enabled():
    # given
    configure.reload()

    # when
    configure._enable_watch()

    # then
    assert configure._observer is not None
    assert configure._observer.should_keep_running() is True


def test_watch_disabled():
    # given
    configure.reload()
    configure._enable_watch()

    # when
    configure._disable_watch()

    # then
    assert configure._observer is not None
    assert configure._observer.should_keep_running() is False


def test_add_listener():
    # given
    configure.reload()
    event_update = configure.ConfigEvent.UPDATE

    # when
    configure.get_config().on(event_update, lambda: None)

    # then
    assert configure.get_config().count(event_update) == 1


def test_remove_listener():
    # given
    configure.reload()
    listener = lambda: None
    event_update = configure.ConfigEvent.UPDATE
    configure.get_config().on(event_update, listener)

    # when
    configure.get_config().remove_listener(event_update, listener)

    # then
    assert configure.get_config().count(event_update) == 0


def test_remove_all_listeners():
    # given
    configure.reload()
    event_update = configure.ConfigEvent.UPDATE
    configure.get_config().on(event_update, lambda: None)

    # when
    configure.get_config().remove_all_listeners()

    # then
    assert len(configure.get_config().listeners(event_update)) == 0


def test_no_watch_than_dispose():
    # given
    configure.reload()
    event_update = configure.ConfigEvent.UPDATE
    configure.get_config().on(event_update, lambda: None)

    # when
    configure._dispose()

    # then
    assert len(configure.get_config().listeners(event_update)) == 0


def test_watch_than_dispose():
    # given
    configure.reload()
    event_update = configure.ConfigEvent.UPDATE
    configure.get_config().on(event_update, lambda: None)
    configure._enable_watch()

    # when
    configure._dispose()

    # then
    assert len(configure.get_config().listeners(event_update)) == 0
    assert configure._observer is not None
    assert configure._observer.should_keep_running() is False
