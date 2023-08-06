import asyncio

import pytest

from refinitiv.data import _configure as configure

TIME_OUT = 1


@pytest.mark.asyncio
async def test_rewrite_user_config(write_user_config):
    write_user_config({"prop": "value", "config-change-notifications-enabled": True})

    configure.reload()

    assert "value" == configure.get_config().get("prop")

    write_user_config('{"prop":"new_value"}')

    await asyncio.sleep(TIME_OUT)

    assert "new_value" == configure.get_config().get("prop")


@pytest.mark.asyncio
async def test_rewrite_project_config(write_project_config):
    write_project_config({"prop": "value", "config-change-notifications-enabled": True})

    configure.reload()

    assert "value" == configure.get_config().get("prop")

    write_project_config('{"prop":"new_value"}')

    await asyncio.sleep(TIME_OUT)

    assert "new_value" == configure.get_config().get("prop")


@pytest.mark.asyncio
async def test_update_event(write_project_config):
    fut = asyncio.Future()

    def on_config_updated():
        assert "new_value" == configure.get_config().get("prop")
        if not fut.done():
            fut.set_result(1)

    write_project_config('{"prop":"value"}')
    configure.reload()
    configure.get_config().on("update", on_config_updated)
    write_project_config('{"prop":"new_value"}')

    await asyncio.sleep(TIME_OUT)

    await fut


@pytest.mark.asyncio
async def test_update_event(write_project_config):
    def on_config_updated():
        assert False

    write_project_config({"prop": "value", "config-change-notifications-enabled": True})
    configure.reload()
    configure.get_config().on("update", on_config_updated)
    configure.get_config().remove_listener("update", on_config_updated)
    write_project_config('{"prop":"new_value"}')

    await asyncio.sleep(TIME_OUT)

    assert "new_value" == configure.get_config().get("prop")
