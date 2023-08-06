import pytest
from http.server import HTTPServer, BaseHTTPRequestHandler
import pytest
from functools import partial
from threading import Thread

success_param = [
    ({"filename": "filename"}),
    ({"dcn": "dcn"}),
    ({"doc_id": "doc_id"}),
    ({"filing_id": "filing_id"}),
]

error_param = [
    ({}),
    (
        {
            "filename": "filename",
            "dcn": "dcn",
            "doc_id": "doc_id",
            "filing_id": "filing_id",
        }
    ),
    (
        {
            "filename": "filename",
            "dcn": "dcn",
        }
    ),
    (
        {
            "filename": "filename",
            "doc_id": "doc_id",
        }
    ),
    (
        {
            "filename": "filename",
            "filing_id": "filing_id",
        }
    ),
    (
        {
            "dcn": "dcn",
            "doc_id": "doc_id",
        }
    ),
    (
        {
            "dcn": "dcn",
            "filing_id": "filing_id",
        }
    ),
    (
        {
            "doc_id": "doc_id",
            "filing_id": "filing_id",
        }
    ),
    (
        {
            "filename": "filename",
            "dcn": "dcn",
            "doc_id": "doc_id",
        }
    ),
]


@pytest.fixture(params=success_param)
def create_filings_definition(request):
    try:
        yield request.param
    except Exception as e:
        assert False, str(e)


@pytest.fixture(params=error_param)
def create_filings_definition_with_error(request):
    return request.param


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("test text".encode("utf-8"))


class HTTPHandlerError(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("File not found".encode("utf-8"))


@pytest.fixture(scope="module")
def mock_server_success(handler=HTTPHandler):
    # Passing 0 to server port argument claims a random free port
    server = HTTPServer(("127.0.0.1", 0), handler)
    server_thread = Thread(
        target=partial(server.serve_forever, poll_interval=0.1), daemon=True
    )
    server_thread.start()
    yield server
    server.shutdown()


@pytest.fixture(scope="module")
def mock_server_error(handler=HTTPHandlerError):
    # Passing 0 to server port argument claims a random free port
    server = HTTPServer(("127.0.0.1", 0), handler)
    server_thread = Thread(
        target=partial(server.serve_forever, poll_interval=0.1), daemon=True
    )
    server_thread.start()
    yield server
    server.shutdown()
