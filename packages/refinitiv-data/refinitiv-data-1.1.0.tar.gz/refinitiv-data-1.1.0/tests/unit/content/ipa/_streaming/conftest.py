import pytest

from refinitiv.data.content.ipa.financial_contracts import cross
from tests.unit.conftest import StubSession


@pytest.fixture(scope="function")
def cross_stream():
    session = StubSession(is_open=True)
    stream = cross.Definition(
        instrument_tag="00102700008910C",
        fx_cross_type=cross.FxCrossType.FX_FORWARD,
        fx_cross_code="USDEUR",
        legs=[
            cross.LegDefinition(
                end_date="2015-04-09T00:00:00Z",
            )
        ],
        pricing_parameters=cross.PricingParameters(
            valuation_date="2015-02-02T00:00:00Z",
            price_side=cross.PriceSide.MID,
        ),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "ValuationDate",
            "FxOutrightCcy1Ccy2",
        ],
    ).get_stream(session=session)
    return stream
