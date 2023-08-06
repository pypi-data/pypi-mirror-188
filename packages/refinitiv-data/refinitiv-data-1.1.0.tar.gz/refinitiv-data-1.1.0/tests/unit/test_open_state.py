import pytest

from refinitiv.data.content import pricing, trade_data_service
from refinitiv.data.content.ipa import financial_contracts
from refinitiv.data.content.pricing import chain
from refinitiv.data.delivery import rdp_stream, omm_stream
from refinitiv.data import OpenState
from tests.unit.conftest import StubSession


def test_session_open_state():
    import refinitiv.data as rd

    try:
        rd.OpenState
    except Exception as e:
        assert False, str(e)


@pytest.mark.parametrize(
    "definition",
    [
        chain.Definition("0#.FTSE"),
        pricing.Definition("EUR="),
        rdp_stream.Definition(
            service=None, universe=[], view=None, parameters={}, api="api"
        ),
        omm_stream.Definition("EUR"),
        trade_data_service.Definition(),
    ],
    ids=[
        "chain",
        "pricing",
        "rdp_stream",
        "omm_stream",
        "trade_data_service",
    ],
)
def test_stream_pending_state(definition):
    def do_open(*args, **kwargs):
        # then
        assert stream.open_state is OpenState.Pending

    # given
    session = StubSession(is_open=True)
    stream = definition.get_stream(session=session)
    stream._stream._do_open = do_open

    # when
    stream.open()


@pytest.mark.parametrize(
    "definition",
    [
        financial_contracts.bond.Definition("[]"),
        financial_contracts.cap_floor.Definition(),
        financial_contracts.cds.Definition(),
        financial_contracts.cross.Definition(),
        financial_contracts.option.Definition(),
        financial_contracts.repo.Definition(),
        financial_contracts.swap.Definition(),
        financial_contracts.swaption.Definition(),
        financial_contracts.term_deposit.Definition(),
    ],
    ids=[
        "financial_contracts.bond",
        "financial_contracts.cap_floor",
        "financial_contracts.cds",
        "financial_contracts.cross",
        "financial_contracts.option",
        "financial_contracts.repo",
        "financial_contracts.swap",
        "financial_contracts.swaption",
        "financial_contracts.term_deposit",
    ],
)
def test_financial_contracts_stream_pending_state(definition):
    def do_open(*args, **kwargs):
        # then
        assert stream.open_state is OpenState.Pending

    # given
    session = StubSession(is_open=True)
    stream = definition.get_stream(session=session)
    stream._stream._stream._do_open = do_open

    # when
    stream.open()
