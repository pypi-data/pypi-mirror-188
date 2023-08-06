from typing import TYPE_CHECKING

from ...._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ......_types import OptStr


class ValuationTime(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    city_name : str, optional
        The city name according to market identifier code (mic) (e.g., 'new york')  see
        iso 10383 for reference.
    local_time : str, optional
        Local time or other words time in offset timezone. the value is expressed in iso
        8601 format: [hh]:[mm]:[ss] (e.g., '14:00:00').
    market_identifier_code : str, optional
        Market identifier code (mic) is a unique identification code used to identify
        securities trading exchanges, regulated and non-regulated trading markets. e.g.
        xnas.  see iso 10383 for reference.
    time_zone_offset : str, optional
        Time offsets from utc. the value is expressed in iso 8601 format: [hh]:[mm]
        (e.g., '+05:00').
    """

    def __init__(
        self,
        city_name: "OptStr" = None,
        local_time: "OptStr" = None,
        market_identifier_code: "OptStr" = None,
        time_zone_offset: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.city_name = city_name
        self.local_time = local_time
        self.market_identifier_code = market_identifier_code
        self.time_zone_offset = time_zone_offset

    @property
    def city_name(self):
        """
        The city name according to market identifier code (mic) (e.g., 'new york')  see
        iso 10383 for reference.
        :return: str
        """
        return self._get_parameter("cityName")

    @city_name.setter
    def city_name(self, value):
        self._set_parameter("cityName", value)

    @property
    def local_time(self):
        """
        Local time or other words time in offset timezone. the value is expressed in iso
        8601 format: [hh]:[mm]:[ss] (e.g., '14:00:00').
        :return: str
        """
        return self._get_parameter("localTime")

    @local_time.setter
    def local_time(self, value):
        self._set_parameter("localTime", value)

    @property
    def market_identifier_code(self):
        """
        Market identifier code (mic) is a unique identification code used to identify
        securities trading exchanges, regulated and non-regulated trading markets. e.g.
        xnas.  see iso 10383 for reference.
        :return: str
        """
        return self._get_parameter("marketIdentifierCode")

    @market_identifier_code.setter
    def market_identifier_code(self, value):
        self._set_parameter("marketIdentifierCode", value)

    @property
    def time_zone_offset(self):
        """
        Time offsets from utc. the value is expressed in iso 8601 format: [hh]:[mm]
        (e.g., '+05:00').
        :return: str
        """
        return self._get_parameter("timeZoneOffset")

    @time_zone_offset.setter
    def time_zone_offset(self, value):
        self._set_parameter("timeZoneOffset", value)
