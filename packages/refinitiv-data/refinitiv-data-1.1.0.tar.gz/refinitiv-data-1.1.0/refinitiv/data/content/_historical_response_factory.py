from typing import TYPE_CHECKING

from ._content_response_factory import ContentResponseFactory

if TYPE_CHECKING:
    from ..delivery._data._data_provider import ParsedData

error_message_by_code = {
    "default": "{error_message}. Requested ric: {rics}. Requested fields: {fields}",
    "TS.Intraday.UserRequestError.90001": "{rics} - The universe is not found",
    "TS.Intraday.Warning.95004": "{rics} - Trades interleaving with corrections is currently not supported. Corrections will not be returned.",
    "TS.Intraday.UserRequestError.90006": "{error_message} Requested ric: {rics}",
}


class HistoricalResponseFactory(ContentResponseFactory):
    def get_raw(self, data: "ParsedData") -> dict:
        return data.content_data[0] if data.content_data else {}

    def create_success(self, parsed_data: "ParsedData", **kwargs):
        self._try_write_error(parsed_data, **kwargs)
        return super().create_success(parsed_data, **kwargs)

    def create_fail(self, parsed_data: "ParsedData", **kwargs):
        self._try_write_error(parsed_data, **kwargs)
        return super().create_fail(parsed_data, **kwargs)

    def _try_write_error(
        self, parsed_data: "ParsedData", universe=None, fields=None, **kwargs
    ):
        raw = self.get_raw(parsed_data)
        error_code = parsed_data.first_error_code or raw.get("status", {}).get("code")

        if not error_code:
            return

        error_message = parsed_data.first_error_message or raw.get("status", {}).get(
            "message"
        )
        rics = raw.get("universe", {}).get("ric", universe)
        parsed_data.error_codes = error_code

        if error_code not in error_message_by_code.keys():
            parsed_data.error_messages = error_message_by_code["default"].format(
                error_message=error_message, rics=rics, fields=fields
            )

        else:
            parsed_data.error_messages = error_message_by_code[error_code].format(
                rics=rics, error_message=error_message
            )
