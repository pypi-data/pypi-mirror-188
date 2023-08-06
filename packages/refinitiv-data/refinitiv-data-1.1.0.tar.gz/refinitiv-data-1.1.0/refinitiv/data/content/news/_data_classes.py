import datetime
from dataclasses import dataclass
from typing import List, TYPE_CHECKING


import pandas as pd

from ._tools import _get_headline_from_story
from ._udf_html_parser import HeadlineHTMLParser
from ._urgency import Urgency

if TYPE_CHECKING:
    from pandas.core.tools.datetimes import DatetimeScalar


@dataclass
class NewsStoryContent:
    html: "str"
    text: "str"


class NewsData(object):
    def __init__(
        self,
        title: str,
        creator: str,
        source: List[dict],
        language: List[dict],
        item_codes: List[str],
        urgency: int,
        creation_date: str,
        update_date: str,
        raw: dict,
        news_type: str,
        html: str = None,
        text: str = None,
    ) -> None:
        self.title = title
        self.creator = creator
        self.source = source
        self.language = language
        self.item_codes = item_codes
        self.urgency: Urgency = Urgency(urgency)

        if news_type == "story":
            self.content: NewsStoryContent = NewsStoryContent(html, text)
            self.headline: str = _get_headline_from_story(raw)
            self.creation_date: "DatetimeScalar" = pd.to_datetime(creation_date)
            self.update_date: "DatetimeScalar" = pd.to_datetime(update_date)
        elif news_type == "headline":
            self.first_created: "DatetimeScalar" = pd.to_datetime(creation_date)
            self.version_created: "DatetimeScalar" = pd.to_datetime(update_date)
            self.story_id: str = raw["storyId"]


class HeadlineRDP(NewsData):
    @staticmethod
    def from_dict(datum: dict) -> "HeadlineRDP":
        news_item = datum.get("newsItem")
        content_meta = news_item.get("contentMeta")
        item_meta = news_item.get("itemMeta")
        subject = content_meta.get("subject")
        headline = HeadlineRDP(
            title=item_meta.get("title")[0].get("$"),
            creator=content_meta.get("creator")[0].get("_qcode"),
            source=content_meta.get("infoSource"),
            language=content_meta.get("language"),
            item_codes=[item.get("_qcode") for item in subject],
            urgency=content_meta.get("urgency").get("$"),
            creation_date=item_meta.get("firstCreated").get("$"),
            update_date=item_meta.get("versionCreated").get("$"),
            raw=datum,
            news_type="headline",
        )
        return headline


class HeadlineUDF:
    def __init__(
        self,
        display_direction,
        document_type,
        first_created,
        is_alert,
        language,
        report_code,
        source_name,
        story_id,
        text,
        version_created,
    ) -> None:
        self.display_direction = display_direction
        self.document_type = document_type
        self.first_created = pd.to_datetime(first_created)
        self.is_alert = is_alert
        self.language = language
        self.report_code = report_code
        self.source_name = source_name
        self.story_id = story_id
        self.text = text
        self.version_created = pd.to_datetime(version_created)

    @classmethod
    def from_dict(cls, datum: dict) -> "HeadlineUDF":
        display_direction = datum.get("displayDirection")
        document_type = datum.get("documentType")
        first_created = datum.get("firstCreated")
        is_alert = datum.get("isAlert")
        language = datum.get("language")
        report_code = datum.get("reportCode")
        source_name = datum.get("sourceName")
        story_id = datum.get("storyId")
        text = datum.get("text")
        version_created = datum.get("versionCreated")
        headline = cls(
            display_direction=display_direction,
            document_type=document_type,
            first_created=first_created,
            is_alert=is_alert,
            language=language,
            report_code=report_code,
            source_name=source_name,
            story_id=story_id,
            text=text,
            version_created=version_created,
        )
        return headline


class Story(NewsData):
    @classmethod
    def from_dict(cls, datum: dict) -> "Story":
        news_item = datum.get("newsItem")
        content_meta = news_item.get("contentMeta")
        html = news_item.get("contentSet", {}).get("inlineXML", [{}])[0].get("$")
        text = news_item.get("contentSet", {}).get("inlineData", [{}])[0].get("$")
        item_meta = news_item.get("itemMeta")
        subject = content_meta.get("subject")
        story = cls(
            title=item_meta.get("title")[0].get("$"),
            creator=content_meta.get("creator")[0].get("_qcode"),
            source=content_meta.get("infoSource"),
            language=content_meta.get("language"),
            item_codes=[item.get("_qcode") for item in subject],
            urgency=content_meta.get("urgency").get("$"),
            creation_date=item_meta.get("firstCreated").get("$"),
            update_date=item_meta.get("versionCreated").get("$"),
            raw=datum,
            news_type="story",
            html=html,
            text=text,
        )
        return story


class StoryUDF:
    def __init__(
        self,
        title: str,
        text: str,
        html: str,
        creation_date: datetime.datetime,
        headline: str,
        creator=None,
    ) -> None:
        self.title = title
        self.content: NewsStoryContent = NewsStoryContent(html, text)
        self.creator = creator
        self.creation_date = creation_date
        self.headline = headline

    @classmethod
    def from_dict(cls, datum: dict) -> "StoryUDF":
        parser = HeadlineHTMLParser()
        story = datum["story"]
        for i in story:
            parser.feed(story[i])
        text = parser.data.get("text") or []
        text = "\n".join(text)
        html = parser.data.get("html") or datum.get("story", {}).get("storyHtml") or []
        story = cls(
            title=parser.data.get("headline"),
            text=text,
            html=html,
            creator=parser.data.get("creator"),
            creation_date=pd.to_datetime(parser.data.get("creation_date")),
            headline=parser.data.get("headline"),
        )
        return story
