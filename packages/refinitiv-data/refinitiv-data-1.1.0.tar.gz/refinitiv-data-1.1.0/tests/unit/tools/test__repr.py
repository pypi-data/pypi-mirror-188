from types import SimpleNamespace

import pytest

from refinitiv.data._tools import (
    create_repr,
    get_new_path,
)
from tests.unit.conftest import kwargs

PREFIX_PATH = "test"


def mock_object(path_module=f"{PREFIX_PATH}._data.public_path"):
    obj = SimpleNamespace()
    obj.__module__ = path_module
    return obj


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("", "<.Definition object at"),
        ("._data.", "<.Definition object at"),
        ("test", "<test.Definition object at"),
        ("test.public_path", "<test.public_path.Definition object at"),
    ],
)
def test_create_repr_without_correct_module_path(input_value, expected):
    # given
    mock_obj = mock_object(input_value)

    # when
    repr_str = create_repr(mock_obj)

    # then
    assert repr_str.startswith(expected), f"mismatch of initial strings {repr_str}"


def test_create_repr_not_validate_first_arg():
    # when
    with pytest.raises(AttributeError):
        create_repr({})


@pytest.mark.parametrize(
    "input_args, expected",
    [
        ({}, f"<{PREFIX_PATH}.Definition object at"),
        (
            kwargs(middle_path="context"),
            f"<{PREFIX_PATH}.context.Definition object at",
        ),
        (
            kwargs(middle_path="context", class_name="Stream"),
            f"<{PREFIX_PATH}.context.Stream object at",
        ),
    ],
)
def test_create_repr_with_validate_other_args(input_args, expected):
    # given
    mock_obj = mock_object()

    # when
    repr_str = create_repr(mock_obj, **input_args)

    # then
    assert repr_str.startswith(expected), f"mismatch of initial strings {repr_str}"


def test_create_repr_with_validate_content():
    # given
    mock_obj = mock_object()

    # when
    repr_str = create_repr(mock_obj, content="content_test")

    # then
    assert repr_str.startswith(f"<{PREFIX_PATH}.Definition object at")
    assert repr_str.endswith(" content_test>")


def test_create_repr_not_validate_content():
    # given
    mock_obj = mock_object()

    # when
    repr_str = create_repr(mock_obj, content="")

    # then
    assert repr_str.startswith(f"<{PREFIX_PATH}.Definition object at")
    assert repr_str.endswith(" >") is False


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (
            kwargs(
                module_path="refinitiv.data._definition",
                class_name="Definition",
                middle="content",
            ),
            "refinitiv.data.content.Definition",
        ),
        (
            kwargs(
                module_path="refinitiv.data._definition",
                class_name="Definition",
            ),
            "refinitiv.data.Definition",
        ),
        (
            kwargs(
                module_path="refinitiv.data._definition",
                class_name="Definition",
                middle="content.pricing",
            ),
            "refinitiv.data.content.pricing.Definition",
        ),
    ],
)
def test_get_new_path(input_value, expected_value):
    # when
    testing_value = get_new_path(**input_value)

    # then
    assert testing_value == expected_value
