import asyncio
import re
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import pytest
import time
from functools import partial
from threading import Thread

from httpx import Client, AsyncClient

from refinitiv.data._core.session._retry_transport import (
    RetryAsyncTransport,
    RetryTransport,
    RequestRetryException,
    RequestTimeout,
    RequestAttemptsExhausted,
)


class NoLogHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return


class SuccessHTTPHandler(NoLogHTTPHandler):
    attempts_counter = 1

    def __init__(self, answer_at_attempt: int, *args, **kwargs):
        self.answer_at_attempt = answer_at_attempt
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if SuccessHTTPHandler.attempts_counter >= self.answer_at_attempt:
            self.send_response(HTTPStatus.OK)
        else:
            self.send_response(HTTPStatus.NOT_IMPLEMENTED)
        self.end_headers()
        SuccessHTTPHandler.attempts_counter += 1


_err_still_in_flight_pattern = re.compile(
    r"The connection pool was closed while [0-9]+ HTTP requests/responses were still in-flight."
)


@pytest.fixture(scope="module")
def mock_server(handler=NoLogHTTPHandler):
    # Passing 0 to server port argument claims a random free port
    server = HTTPServer(("127.0.0.1", 0), handler)
    server_thread = Thread(
        target=partial(server.serve_forever, poll_interval=0.1), daemon=True
    )
    server_thread.start()
    yield server
    server.shutdown()


def test_asynchronous_execution(mock_server):
    async def create_client(server_port: int):
        with pytest.raises(RequestRetryException):
            async_transport = RetryAsyncTransport(
                total_timeout=10,
                total_attempts=20,
                on_statuses=[501],
                on_methods=["GET"],
                backoff_factor=0.1,
            )
            async with AsyncClient(transport=async_transport) as async_client:
                await async_client.get(f"http://127.0.0.1:{server_port}")

    async def async_run(server_port: int):
        task = asyncio.create_task(create_client(server_port))
        # Check in a loop to make sure there is no small synchronous code in transport.
        # Synchronous code that takes less than 0.25 seconds may be skipped
        for _ in range(3):
            t_start = time.perf_counter()
            await asyncio.sleep(0.2)
            t_finish = time.perf_counter()
            assert t_finish - t_start < 0.25
        task.cancel()
        await asyncio.wait({task})

    mock_server.RequestHandlerClass = NoLogHTTPHandler
    asyncio.run(async_run(mock_server.server_port))


def test_retry_success_async(mock_server):
    async def async_run(server_port: int, succeed_on_attempt: int):
        async_transport = RetryAsyncTransport(
            total_timeout=50,
            total_attempts=10,
            on_statuses=[501],
            on_methods=["GET"],
            backoff_factor=0,
        )
        async_client = AsyncClient(transport=async_transport)
        response = await async_client.get(f"http://127.0.0.1:{server_port}")

        try:
            await async_client.aclose()
        except RuntimeError as e:
            assert _err_still_in_flight_pattern.match(str(e)), str(e)

        assert response.status_code == 200
        assert (
            async_transport._retrying.statistics["attempt_number"] == succeed_on_attempt
        )

    for successful_attempt in [1, 2, 5]:
        handler = partial(
            SuccessHTTPHandler, successful_attempt
        )  # Needed to pass custom argument to the handler
        SuccessHTTPHandler.attempts_counter = 1

        mock_server.RequestHandlerClass = handler
        asyncio.run(async_run(mock_server.server_port, successful_attempt))


def test_timeout_async(mock_server):
    async def async_run(server_port: int):
        timeout = 0.1

        with pytest.raises(RequestTimeout) as error:
            async_transport = RetryAsyncTransport(
                total_timeout=timeout,
                total_attempts=20,
                on_statuses=[501],
                on_methods=["GET"],
                backoff_factor=0.025,
            )
            async_client = AsyncClient(transport=async_transport)
            await async_client.get(f"http://127.0.0.1:{server_port}")

            try:
                await async_client.aclose()
            except RuntimeError as e:
                assert _err_still_in_flight_pattern.match(str(e)), str(e)

        assert timeout <= error.value.total_time

    mock_server.RequestHandlerClass = NoLogHTTPHandler
    asyncio.run(async_run(mock_server.server_port))


def test_attempts_exceeded_async(mock_server):
    async def async_run(server_port: int):
        for attempt_count in [1, 2, 5]:
            with pytest.raises(RequestAttemptsExhausted) as error:
                async_transport = RetryAsyncTransport(
                    total_timeout=50,
                    total_attempts=attempt_count,
                    on_statuses=[501],
                    on_methods=["GET"],
                    backoff_factor=0,
                )
                async_client = AsyncClient(transport=async_transport)
                await async_client.get(f"http://127.0.0.1:{server_port}")

                try:
                    await async_client.aclose()
                except RuntimeError as e:
                    assert _err_still_in_flight_pattern.match(str(e)), str(e)

            assert attempt_count == error.value.attempts_count

    mock_server.RequestHandlerClass = NoLogHTTPHandler
    asyncio.run(async_run(mock_server.server_port))


def test_retry_success(mock_server):
    for successful_attempt in [1, 2, 5]:
        handler = partial(
            SuccessHTTPHandler, successful_attempt
        )  # Needed to pass custom argument to the handler
        SuccessHTTPHandler.attempts_counter = 1
        mock_server.RequestHandlerClass = handler
        transport = RetryTransport(
            total_timeout=50,
            total_attempts=10,
            on_statuses=[501],
            on_methods=["GET"],
            backoff_factor=0,
        )
        client = Client(transport=transport)
        response = client.get(f"http://127.0.0.1:{mock_server.server_port}")

        try:
            client.close()
        except RuntimeError as e:
            assert _err_still_in_flight_pattern.match(str(e)), str(e)

        assert response.status_code == 200
        assert transport._retrying.statistics["attempt_number"] == successful_attempt


def test_timeout(mock_server):
    timeout = 0.1
    mock_server.RequestHandlerClass = NoLogHTTPHandler
    with pytest.raises(RequestTimeout) as error:
        transport = RetryTransport(
            total_timeout=timeout,
            total_attempts=20,
            on_statuses=[501],
            on_methods=["GET"],
            backoff_factor=0.025,
        )
        client = Client(transport=transport)
        client.get(f"http://127.0.0.1:{mock_server.server_port}")

        try:
            client.close()
        except RuntimeError as e:
            assert _err_still_in_flight_pattern.match(str(e)), str(e)

    assert timeout <= error.value.total_time


def test_attempts_exceeded(mock_server):
    mock_server.RequestHandlerClass = NoLogHTTPHandler
    for attempt_count in [1, 2, 5]:
        with pytest.raises(RequestAttemptsExhausted) as error:
            transport = RetryTransport(
                total_timeout=50,
                total_attempts=attempt_count,
                on_statuses=[501],
                on_methods=["GET"],
                backoff_factor=0,
            )
            client = Client(transport=transport)
            client.get(f"http://127.0.0.1:{mock_server.server_port}")

            try:
                client.close()
            except RuntimeError as e:
                assert _err_still_in_flight_pattern.match(str(e)), str(e)

        assert attempt_count == error.value.attempts_count
