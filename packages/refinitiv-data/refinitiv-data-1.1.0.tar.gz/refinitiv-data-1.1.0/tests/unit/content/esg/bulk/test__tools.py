import pytest

from refinitiv.data.content.esg.bulk._tools import (
    get_the_newest_file,
    get_init_archives,
    get_date_from_filename,
    is_correct_filename,
    get_filesets_with_delta_files,
    get_filesets_with_the_newest_init_file_and_delta_files,
    sorted_files,
    join_path_to_field,
    is_init_file,
)


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ("RFT-ESG-Raw-Full-SchemeB-Social-delta-2021-04-11.jsonl.gz", True),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl.gz", True),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11", False),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-03-12.jsonl.gz", True),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-05-09.jsonl", True),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-0-09.jsonl", False),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Init.jsonl", False),
    ],
)
def test_is_correct_filename(test_value, expected_result):
    # given

    # when
    result = is_correct_filename(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ("RFT-ESG-Raw-Full-SchemeB-Social-Jsonl-delta-2021-04-11.jsonl.gz", False),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Jsonl-Delta-2021-04-11.jsonl.gz", False),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Jsonl-init-2021-03-12.jsonl.gz", True),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Jsonl-Init-2021-05-09.jsonl", True),
    ],
)
def test_is_init_file(test_value, expected_result):
    # given

    # when
    result = is_init_file(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ("RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl.gz", "2021-04-11"),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-03-12.jsonl.gz", "2021-03-12"),
        ("RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-05-09.jsonl", "2021-05-09"),
    ],
)
def test_get_date_from_filename(test_value, expected_result):
    # given

    # when
    result = get_date_from_filename(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        (
            [
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-05-08.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-03-12.jsonl",
            ],
            "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-05-08.jsonl",
        ),
        ([], None),
    ],
)
def test_get_the_newest_file(test_value, expected_result):
    # given

    # when
    result = get_the_newest_file(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        (
            [
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-05-11.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2019-11-12.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-05-11.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2020-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl",
            ],
            [
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2020-04-11.jsonl.gz",
            ],
        ),
        (
            [
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-05-11.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2019-11-12.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-05-11.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Delta-2021-04-11.jsonl",
            ],
            [
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-04-11.jsonl.gz",
            ],
        ),
        (
            [
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-01-1.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-02-11.jsonl",
                "RFT-ESG-Raw-Full-SchemeB-Soci-Init-2021-03-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social--2021-04-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-05-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-06-11.jsonl.gz",
            ],
            [
                "RFT-ESG-Raw-Full-SchemeB-Soci-Init-2021-03-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-05-11.jsonl.gz",
                "RFT-ESG-Raw-Full-SchemeB-Social-Init-2021-06-11.jsonl.gz",
            ],
        ),
        ([], []),
    ],
)
def test_get_init_archives(test_value, expected_result):
    # given

    # when
    result = get_init_archives(test_value)

    # then
    assert set(result) == set(expected_result)


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        (
            [
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-05-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-init-2021-05-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-delta-2021-05-09"},
            ],
            [
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-05-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-delta-2021-05-09"},
            ],
        ),
    ],
)
def test_get_filesets_with_delta_files(test_value, expected_result):
    # given

    # when
    result = get_filesets_with_delta_files(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        (
            [
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-04-11"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Init-2021-03-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-03-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-04-22"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Init-2021-05-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-05-09"},
            ],
            [
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Init-2021-05-09"},
                {"name": "RFT-ESG-Scores-Wealth-Standard-Jsonl-Delta-2021-05-09"},
            ],
        ),
        ([], []),
    ],
)
def test_get_filesets_with_the_newest_init_file_and_delta_files(
    test_value, expected_result
):
    # given

    # when
    result = get_filesets_with_the_newest_init_file_and_delta_files(test_value)

    # then
    assert list(result) == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ([], []),
        (
            [
                "RFT-ESG-Scores-Wealth-Standard-delta-2021-06-13.jsonl.gz",
                "RFT-ESG-Scores-Wealth-Standard-init-2021-06-13.jsonl.gz",
            ],
            [
                "RFT-ESG-Scores-Wealth-Standard-init-2021-06-13.jsonl.gz",
                "RFT-ESG-Scores-Wealth-Standard-delta-2021-06-13.jsonl.gz",
            ],
        ),
    ],
)
def test_sorted_files(test_value, expected_result):
    # given

    # when
    result = sorted_files(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ([], ""),
        (["test_field_name"], "test_field_name"),
        (["test_field_name", "field"], "test_field_name.field"),
    ],
)
def test_join_path_to_field(test_value, expected_result):
    # given

    # when
    result = join_path_to_field(*test_value)

    # then
    assert result == expected_result
