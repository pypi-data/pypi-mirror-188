import pytest
from refinitiv.data.content.ownership.insider import (
    shareholders_report,
    transaction_report,
)


def test_shareholders_report():
    try:
        shareholders_report.Definition(universe="")
    except Exception as e:
        assert False, str(e)


def test_transaction_report():
    try:
        transaction_report.Definition(universe="")
    except Exception as e:
        assert False, str(e)
