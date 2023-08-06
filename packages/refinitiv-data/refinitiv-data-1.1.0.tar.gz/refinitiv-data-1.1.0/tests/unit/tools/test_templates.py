from refinitiv.data._tools.templates import InvalidPlaceholderError


class TestInvalidPlaceholderError:
    def test_noncut(self):
        exc = InvalidPlaceholderError(2, "abcd")
        assert str(exc) == (
            "Invalid placeholder in the template string: line 1, col 3:\n"
            "abcd\n"
            "--^"
        )

    def test_noncut_multiline(self):
        exc = InvalidPlaceholderError(7, "abcd\nefgh")
        assert str(exc) == (
            "Invalid placeholder in the template string: line 2, col 3:\n"
            "efgh\n"
            "--^"
        )

    def test_cursor_inside_limit(self):
        exc = InvalidPlaceholderError(4, "one two three", 7)
        assert str(exc) == (
            "Invalid placeholder in the template string: line 1, col 5:\n"
            "one two\n"
            "----^"
        )

    def test_cursor_outside_limit(self):
        exc = InvalidPlaceholderError(9, "one two three", 7)
        assert str(exc) == (
            "Invalid placeholder in the template string: line 1, col 10:\n"
            " two th\n"
            "------^"
        )

    def test_cursor_inside_limit_with_padding(self):
        exc = InvalidPlaceholderError(4, "one two three", 7, 3)
        assert str(exc) == (
            "Invalid placeholder in the template string: line 1, col 5:\n"
            "ne two \n"
            "---^"
        )
