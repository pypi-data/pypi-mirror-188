from typing import List, TYPE_CHECKING

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


class WorkingDay:
    def __init__(
        self,
        is_weekend: bool,
        is_working_day: bool,
        tag: str = "",
        holidays: list = None,
    ):
        self._is_weekend = is_weekend
        self._response_holidays_items = holidays or []
        self._is_working_day = is_working_day
        self._tag = tag
        self._holidays = []

    @property
    def is_weekend(self):
        return self._is_weekend

    @property
    def is_working_day(self):
        return self._is_working_day

    @property
    def tag(self):
        return self._tag

    @property
    def holidays(self) -> List[Holiday]:
        if self._holidays:
            return self._holidays

        for holiday in self._response_holidays_items:
            holiday_ = Holiday(holiday=holiday, tag=self.tag)
            self._holidays.append(holiday_)
        return self._holidays


class IsWorkingDay(Data):
    def __init__(self, raw: dict, tag: str = "", **kwargs):
        super().__init__(raw, **kwargs)
        self._day = WorkingDay(
            is_weekend=raw[0]["isWeekEnd"],
            is_working_day=raw[0]["isWorkingDay"],
            tag=tag,
            holidays=raw[0].get("holidays", []),
        )

    @property
    def day(self):
        return self._day


class IsWorkingDays(Data):
    _is_working_days_ = None

    @property
    def _is_working_days(self):
        if self._is_working_days_ is None:
            self._is_working_days_ = [
                WorkingDay(
                    raw_item["isWeekEnd"],
                    raw_item.get("isWorkingDay"),
                    tag=raw_item.get("tag"),
                    holidays=raw_item.get("holidays"),
                )
                for raw_item in self.raw
                if not raw_item.get("error")
            ]

        return self._is_working_days_

    @property
    def days(self):
        return self._is_working_days

    def __getitem__(self, item: int):
        return self._is_working_days[item]


class IsWorkingDayResponseFactory(DatesAndCalendarsResponseFactory):
    def create_data_success(self, parsed_data: "ParsedData", **kwargs):
        raw = self.get_raw(parsed_data)

        if len(raw) > 1:
            data = IsWorkingDays(raw, build_dates_calendars_df, **kwargs)

        else:
            data = IsWorkingDay(
                raw, raw[0].get("tag"), dfbuilder=build_dates_calendars_df, **kwargs
            )

        return data


is_working_day_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=IsWorkingDayResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
