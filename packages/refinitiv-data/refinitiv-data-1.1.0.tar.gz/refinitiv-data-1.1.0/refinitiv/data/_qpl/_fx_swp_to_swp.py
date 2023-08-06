from typing import Optional, Union, TYPE_CHECKING

from ._data_provider import fx_swp_to_swp_data_provider as data_provider
from .._core.session import get_default
from .._tools import Copier
from ..delivery._data._data_provider_layer import _check_response

if TYPE_CHECKING:
    from ._fx_spot_quote import FxSpotQuote
    from ._fx_swap_points import FxSwapPoints
    from .._types import OptDateTime, OptStrStrs
    from ..delivery._data._response import Response


def fx_swp_to_swp(
    fx_cross_code: str,
    market_data_date_time: "OptDateTime" = None,
    tenors: "OptStrStrs" = None,
    fields: "OptStrStrs" = None,
    spot_ccy_1: Optional[Union[dict, "FxSpotQuote"]] = None,
    spot_ccy_2: Optional[Union[dict, "FxSpotQuote"]] = None,
    swap_points_ccy_1: Optional[Union[dict, "FxSwapPoints"]] = None,
    swap_points_ccy_2: Optional[Union[dict, "FxSwapPoints"]] = None,
) -> "Response":
    """
    Computes the cross currency curve using the swap points and
    spot rates of each of the currencies in the FX Cross pair against the pivot currency

    Parameters
    ----------
    fx_cross_code : str
        The currency pair of FX Cross, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF').
        The user can specify a pivot currency with 3-currency ISO code in the FX Cross (e.g., 'GBPEURCHF'),
        where the second currency is the pivot currency. By default, the pivot currency is 'USD'
    market_data_date_time : OptDateTime, optional
        The date at which the market data is retrieved. The value is expressed
        in ISO 8601 format YYYY-MM-DD (e.g. '2021-01-01').
    tenors : str, list of str, optional
        An array of requested tenors, or/and end dates. the value can be expressed as
        the code indicating the time period (e.g., '1m', '6m', '4y'), or in iso 8601
        format 'yyy-mm-dd' (e.g., '2021-01-01')
    fields : str, list of str, optional
        An array of the requested fields
    spot_ccy_1 : dict or FxSpotQuote, optional

    spot_ccy_2 : dict or FxSpotQuote, optional

    swap_points_ccy_1 : dict or FxSwapPoints, optional

    swap_points_ccy_2 : dict or FxSwapPoints, optional

    Returns
    -------
    Response

    Examples
    -------
    >>> import refinitiv.data as rd
    >>> response = rd.qpl.fx_swp_to_swp(
    ...     fx_cross_code="EURUSD",
    ...     market_data_date_time="2022-09-22",
    ...     spot_ccy_1=rd.qpl.FxSpotQuote(source="D3"),
    ...     spot_ccy_2=rd.qpl.FxSpotQuote(bid=1, ask=2),
    ...     swap_points_ccy_1=rd.qpl.FxSwapPoints(
    ...         additional_tenor_types=[rd.qpl.TenorTypes.LONG],
    ...         source="ICAP",
    ...     ),
    ...     swap_points_ccy_2=rd.qpl.FxSwapPoints(
    ...         additional_tenor_types=[rd.qpl.TenorTypes.LONG, rd.qpl.TenorTypes.ODD],
    ...         source="D3",
    ...         overrides=[
    ...             rd.qpl.TenorBidAsk(tenor="1M", bid=50, ask=60),
    ...             rd.qpl.TenorBidAsk(tenor="2M", bid=90),
    ...         ],
    ...     ),
    ... )
    >>> response.data.df
    >>> response.data.raw
    """
    session = get_default()
    url = session.config.get("apis.data.qpl-functions.endpoints.fx_swp_to_swp")
    tenors = tenors and Copier.get_list(tenors)
    fields = fields and Copier.get_list(fields)
    response = data_provider.get_data(
        session,
        url,
        fx_cross_code=fx_cross_code,
        market_data_date_time=market_data_date_time,
        tenors=tenors,
        fields=fields,
        spot_ccy_1=spot_ccy_1,
        spot_ccy_2=spot_ccy_2,
        swap_points_ccy_1=swap_points_ccy_1,
        swap_points_ccy_2=swap_points_ccy_2,
    )
    _check_response(response, session.config)
    return response
