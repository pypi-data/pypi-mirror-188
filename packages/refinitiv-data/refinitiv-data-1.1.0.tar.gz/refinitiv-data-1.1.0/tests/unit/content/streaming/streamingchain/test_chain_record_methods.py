import pytest

from refinitiv.data.content.pricing.chain._chain_record import can_create_chain_record


@pytest.mark.parametrize(
    "input_data,expected_value",
    [
        ({}, False),
        ({"REF_COUNT": 10}, False),
        (
            {"REF_COUNT": 10, **{f"LONGLINK{number}": None for number in range(1, 15)}},
            False,
        ),
        (
            {
                "REF_COUNT": 10,
                **{f"LONGLINK{number}": None for number in range(1, 15)},
                "LONGPREVLR": None,
                "LONGNEXTLR": None,
            },
            True,
        ),
    ],
)
def test_method_is_valid_chain_record(input_data, expected_value):

    try:
        result = can_create_chain_record(input_data)
    except Exception as e:
        assert False, e

    assert result is expected_value
