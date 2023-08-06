import urllib

import pytest

from refinitiv.data._tools import parse_url, ParseResult, ParseResultBytes
from tests.unit.conftest import args


@pytest.mark.parametrize(
    "input_url,expected_result",
    [
        args(
            input="http://1.2.3.4:80",
            expected=ParseResult(
                scheme="http",
                netloc="1.2.3.4:80",
                path="",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="http://1.2.3.4",
            expected=ParseResult(
                scheme="http",
                netloc="1.2.3.4",
                path="",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="://1.2.3.4:80",
            expected=ParseResult(
                scheme="",
                netloc="",
                path="://1.2.3.4:80",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="//1.2.3.4:80",
            expected=ParseResult(
                scheme="",
                netloc="1.2.3.4:80",
                path="",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="1.2.3.4:80",
            expected=ParseResult(
                scheme="",
                netloc="",
                path="1.2.3.4:80",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="//1.2.3.4",
            expected=ParseResult(
                scheme="",
                netloc="1.2.3.4",
                path="",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="scheme://netloc/path;parameters?query#fragment",
            expected=ParseResult(
                scheme="scheme",
                netloc="netloc",
                path="/path;parameters",
                params="",
                query="query",
                fragment="fragment",
            ),
        ),
        args(
            input="http://docs.python.org:80/3/library/urllib.parse.html?highlight=params#url-parsing",
            expected=ParseResult(
                scheme="http",
                netloc="docs.python.org:80",
                path="/3/library/urllib.parse.html",
                params="",
                query="highlight=params",
                fragment="url-parsing",
            ),
        ),
        args(
            input="//www.cwi.nl:80/%7Eguido/Python.html",
            expected=ParseResult(
                scheme="",
                netloc="www.cwi.nl:80",
                path="/%7Eguido/Python.html",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="www.cwi.nl/%7Eguido/Python.html",
            expected=ParseResult(
                scheme="",
                netloc="",
                path="www.cwi.nl/%7Eguido/Python.html",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="help/Python.html",
            expected=ParseResult(
                scheme="",
                netloc="",
                path="help/Python.html",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="abc:123.html",
            expected=ParseResult(
                scheme="abc",
                netloc="",
                path="123.html",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="123.html:abc",
            expected=ParseResult(
                scheme="",
                netloc="",
                path="123.html:abc",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="abc:123/",
            expected=ParseResult(
                scheme="abc",
                netloc="",
                path="123/",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="abc:123",
            expected=ParseResult(
                scheme="abc",
                netloc="",
                path="123",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input="",
            expected=ParseResult(
                scheme="",
                netloc="",
                path="",
                params="",
                query="",
                fragment="",
            ),
        ),
        args(
            input={},
            expected=ParseResultBytes(
                scheme=b"",
                netloc=b"",
                path=b"",
                params=b"",
                query=b"",
                fragment=b"",
            ),
        ),
        args(
            input=None,
            expected=ParseResultBytes(
                scheme=b"",
                netloc=b"",
                path=b"",
                params=b"",
                query=b"",
                fragment=b"",
            ),
        ),
    ],
)
def test_parse_value(input_url, expected_result):
    # when
    testing_result = parse_url(input_url)

    # then
    assert testing_result == expected_result, input_url


def test_result_type():
    # given
    url = "http://1.2.3.4:80"

    # when
    rd_result = parse_url(url)
    urllib_result = urllib.parse.urlparse(url)

    # then
    assert type(rd_result) == type(urllib_result)
