from typing import TYPE_CHECKING, List

from .._content_data_validator import ContentDataValidator
from .._request_factory import DatesAndCalendarsResponseFactory
from ..holidays._holidays_data_provider import Holiday
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ...._df_builder import build_dates_calendars_df
from .....content.ipa._content_provider import DatesAndCalendarsRequestFactory
from .....delivery._data._data_provider import ValidatorContainer

if TYPE_CHECKING:
    from .....delivery._data._data_provider import ParsedData


class Period:
    _holidays = None

    def __init__(self, date: str, holidays: list = None, tag: str = ""):
        self._date = date
        self._response_holidays_items = holidays or []
        self._tag = tag

    @property
    def tag(self):
        return self._tag

    @property
    def date(self):
        return self._date

    @property
    def holidays(self):
        if self._holidays is None:
            self._holidays = [
                Holiday(holiday=holiday, tag=self.tag)
                for holiday in self._response_holidays_items
            ]

        return self._holidays


class AddedPeriods(Data):
    _added_periods = None

    @property
    def added_periods(self):
        if self._added_periods is None:
            self._added_periods = [
                Period(
                    date=raw_item["date"],
                    holidays=raw_item.get("holidays"),
                    tag=raw_item.get("tag"),
                )
                for raw_item in self._raw
                if not raw_item.get("error")
            ]

        return self._added_periods

    def __getitem__(self, item):
        return self.added_periods[item]


class AddedPeriod(Data):
    def __init__(
        self, raw: List[dict], date: str, holidays: None, tag: str = "", **kwargs
    ):
        super().__init__(raw, **kwargs)
        self._period = Period(date=date, holidays=holidays, tag=tag)

    @property
    def added_period(self):
        return self._period


class AddPeriodsResponseFactory(DatesAndCalendarsResponseFactory):
    def create_data_success(self, parsed_data: "ParsedData", **kwargs):
        raw: List[dict] = self.get_raw(parsed_data)

        if len(raw) > 1:
            data = AddedPeriods(raw, build_dates_calendars_df)

        else:
            raw_item = raw[0]
            data = AddedPeriod(
                raw=raw,
                date=raw_item["date"],
                holidays=raw_item.get("holidays"),
                tag=raw_item.get("tag"),
                dfbuilder=build_dates_calendars_df,
            )

        return data


add_period_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=AddPeriodsResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
