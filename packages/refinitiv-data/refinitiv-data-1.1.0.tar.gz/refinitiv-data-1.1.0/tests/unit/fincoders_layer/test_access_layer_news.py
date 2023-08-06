import pandas as pd

from refinitiv.data._core.session import set_default
from tests.unit.conftest import StubSession
from ..content.data_for_tests import (
    NEWS_STORY_RESPONSE_DATA,
    NEWS_HEADLINES_RESPONSE_UDF,
)
from refinitiv.data._fin_coder_layer import news

MOCKED_STORY_HTML_RESPONSE = '<div class="storyContent" lang="es"><style type="text/css">.storyContent * {border-color:inherit !important;outline-color:inherit !important;}</style><p class="tr-advisory">.</p><p class="tr-by">Por Shreyashi Sanyal y Bansari Mayur Kamdar</p><p class="tr-story-p1"><span class="tr-dateline">10 oct (Reuters)</span><span class="tr-dl-sep"> - </span>El índice Nasdaq caía el lunes hasta tocar mínimos de dos años, ya que los fabricantes de semiconductores se llevaban la peor parte de los esfuerzos de Estados Unidos para obstaculizar la industria de chips de China, mientras los inversores operaban con cautela antes del comienzo de la temporada de resultados. </p><p>* El índice SE Semiconductor de Filadelfia <a href="reuters://REALTIME/Verb=FullQuote/ric=.SOX" data-type="ric" data-ric=".SOX" translate="no" dir="ltr">.SOX</a> bajó un 2,7%, después de que el Gobierno del presidente Joe Biden publicó un amplio conjunto de controles de exportación el viernes, incluida una medida para aislar a China de ciertos chips semiconductores fabricados en cualquier parte del mundo con equipos estadounidenses.</p><p>* Algunos de los componentes más importantes del índice, incluida Nvidia Corp. <a href="reuters://REALTIME/Verb=FullQuote/ric=NVDA.O" data-type="ric" data-ric="NVDA.O" translate="no" dir="ltr">NVDA.O</a>, Qualcomm Inc. <a href="reuters://REALTIME/Verb=FullQuote/ric=QCOM.O" data-type="ric" data-ric="QCOM.O" translate="no" dir="ltr">QCOM.O</a> y Micron Technology Inc. <a href="reuters://REALTIME/Verb=FullQuote/ric=MU.O" data-type="ric" data-ric="MU.O" translate="no" dir="ltr">MU.O</a> perdieron entre 1,3% y 3,3% al inicio de la sesión.</p><p>* En las operaciones de media mañana, el Promedio Industrial Dow Jones <a href="reuters://REALTIME/Verb=FullQuote/ric=.DJI" data-type="ric" data-ric=".DJI" translate="no" dir="ltr">.DJI</a> subía 54,93 puntos, o un 0,19%, a 29.351,72 unidades; mientras que el S&amp;P 500 <a href="reuters://REALTIME/Verb=FullQuote/ric=.SPX" data-type="ric" data-ric=".SPX" translate="no" dir="ltr">.SPX</a> bajaba 9,31 puntos, o un 0,26%, a 3.630,35 unidades; y el índice Nasdaq Composite <a href="reuters://REALTIME/Verb=FullQuote/ric=.IXIC" data-type="ric" data-ric=".IXIC" translate="no" dir="ltr">.IXIC</a> cedía 73,99 puntos, o un 0,69%, a 10.578,41 unidades.</p><p>* Los gigantes tecnológicos Apple Inc. <a href="reuters://REALTIME/Verb=FullQuote/ric=AAPL.O" data-type="ric" data-ric="AAPL.O" translate="no" dir="ltr">AAPL.O</a> y Microsoft Corp. <a href="reuters://REALTIME/Verb=FullQuote/ric=MSFT.O" data-type="ric" data-ric="MSFT.O" translate="no" dir="ltr">MSFT.O</a> caían un 0,9% y un 1,5%, respectivamente, lastrando el subíndice del sector tecnológico del S&amp;P 500 <a href="reuters://REALTIME/Verb=FullQuote/ric=.SPLRCT" data-type="ric" data-ric=".SPLRCT" translate="no" dir="ltr">.SPLRCT</a> .</p><p><br/></p><p><br/></p><p class="tr-signoff"> (Reportes de Ankika Biswas y Shreyashi Sanyal en Bengaluru; reporte adicional de Bansari Mayur Kamdar. Editado en español por Marion Giraldo)</p><p class="tr-contactinfo">((Mesa de edición en español +562 24374447. Twitter: <a href="https://twitter.com/ReutersLatam" data-type="url" class="tr-link" translate="no">https://twitter.com/ReutersLatam</a>; ))</p><div class="tr-additinfo tr-desktop-part"><pre>REUTERS MG/\n</pre></div><p class="line-break"><br/></p><p class="tr-copyright">(c) Copyright Thomson Reuters 2022. Click For Restrictions - https://agency.reuters.com/en/copyright.html</p><p class="line-break"><br/></p><p class="tr-slugline">Keywords: MERCADOS-WALLST/ (MEDIA)</p></div>'

MOCKED_STORY_RAW_RESPONSE = {
    "newsItem": {
        "_conformance": "power",
        "_guid": "tag:reuters.com,2022-04-08:newsml_RTV7TbbdW",
        "_standard": "NewsML-G2",
        "_standardversion": "2.18",
        "_version": 5,
        "catalogRef": [
            {
                "_href": "http://xml.media.reuters.com/g2-standards/catalogs/ReutersMedia_G2-Standards-Catalog_v1.xml"
            }
        ],
        "rightsInfo": [
            {
                "copyrightHolder": {"_literal": "Thomson Reuters"},
                "copyrightNotice": [
                    {
                        "$": "(c) Copyright Thomson Reuters 2022. Click For Restrictions - http://about.reuters.com/fulllegal.asp"
                    }
                ],
            }
        ],
        "itemMeta": {
            "itemClass": {"_qcode": "ninat:text", "_rtr:msgType": "A"},
            "provider": {"_literal": "reuters.com"},
            "versionCreated": {"$": "2022-04-08T06:02:25.633Z"},
            "firstCreated": {"$": "2022-04-08T06:00:00.972Z"},
            "pubStatus": {"_qcode": "stat:usable"},
            "role": {"_qcode": "itemRole:N"},
            "title": [
                {
                    "$": "Refinitiv Newscasts - Scholz lobt Schulterschluss bei Kriegsflüchtlingen"
                }
            ],
            "signal": [{"_qcode": "edStat:C"}],
            "expires": [{"$": "2023-05-08T06:02:25.633Z"}],
            "link": [
                {
                    "_rel": "irel:seeAlso",
                    "_residref": "urn:newsml:reuters.com:20220408:nRTV7TbbdW",
                }
            ],
            "itemMetaExtProperty": [
                {
                    "_creator": "rftResRef:sys26",
                    "_id": "cse1",
                    "_rel": "extCptRel:hasMduMinorVersion",
                    "_value": "0.1",
                    "_valuedatatype": "xs:string",
                    "related": [
                        {
                            "_rel": "extCptRel:hasRelatedTimestamp",
                            "_value": "2022-04-08T06:02:25.694",
                            "_valuedatatype": "xs:dateTime",
                        }
                    ],
                }
            ],
            "rtr:versionedId": [
                {"_guid": "tag:reuters.com,2022-04-08:newsml_RTV7TbbdW:5"}
            ],
        },
        "contentMeta": {
            "urgency": {"$": 3},
            "infoSource": [{"_qcode": "NS:RTRS", "_role": "cRole:source"}],
            "creator": [{"_qcode": "NS:RTRS", "_role": "cRole:source"}],
            "contributor": [{"_qcode": "NS:RTRS", "_role": "cRole:enhancer"}],
            "audience": [{"_qcode": "NP:RITV"}],
            "altId": [{"_type": "idType:USN", "$": "RTV7TbbdW"}],
            "language": [{"_tag": "de"}],
            "subject": [
                {
                    "_confidence": 100,
                    "_creator": "rftResRef:sys26",
                    "_how": "howextr:tool",
                    "_id": "S1",
                    "_qcode": "G:1",
                    "_why": "why:inferred",
                    "related": [
                        {
                            "_creator": "rftResRef:sys24",
                            "_how": "howextr:tool",
                            "_id": "grp0",
                            "_qcode": "hmlInd:high",
                            "_rel": "extCptRel:hasRelevanceGroup",
                            "_why": "why:inferred",
                        }
                    ],
                }
            ],
            "headline": [
                {
                    "_dir": "ltr",
                    "_xml:lang": "de",
                    "$": "Refinitiv Newscasts - Scholz lobt Schulterschluss bei Kriegsflüchtlingen",
                }
            ],
            "contentMetaExtProperty": [
                {
                    "_creator": "rftResRef:sys26",
                    "_how": "howextr:tool",
                    "_id": "DK1",
                    "_qcode": "dedupeKey:strict:20220408_-78987acd6c0b959f0dbcca11ea11464c110268e4",
                    "_rel": "extCptRel:hasDedupeKey",
                    "_why": "why:inferred",
                    "related": [
                        {
                            "_creator": "rftResRef:sys26",
                            "_how": "howextr:tool",
                            "_qcode": "dedupeKeyType:strict",
                            "_rel": "extCptRel:hasDedupeKeyType",
                            "_why": "why:inferred",
                        }
                    ],
                }
            ],
        },
        "assert": [{"_qcode": "NP:RITV", "type": [{"_qcode": "cptType:15"}]}],
        "derivedFrom": [{"_idrefs": "A1", "_qcode": "NP:RITV"}],
        "contentSet": {
            "inlineXML": [
                {
                    "_contenttype": "application/xhtml+xml",
                    "$": '<html lang="en"xml:lang="en"xmlns="http://www.w3.org/1999/xhtml"><head ><title >Refinitiv Newscasts - Scholz lobt Schulterschluss bei Kriegsflüchtlingen</title></head><body ><div class="storyframe"id="storydiv"><div class="TEXT"id="storybody"name="storybody"xmlns:custExtension="urn:xslExtensions"xmlns:xsi="http://www.w3.org/2001/XMLSchema/"><div id="storybodycontent0"><span class="storycontent"><pre >Click the following link to watch video: <a href="https://share.newscasts.refinitiv.com/link?entryId=1_bonf89p1&referenceId=tag:reuters.com,2022:newsml_OV039108042022RP1_996&pageId=RefinitivNewscasts">https://share.newscasts.refinitiv.com/link?entryId=1_bonf89p1&referenceId=tag:reuters.com,2022:newsml_OV039108042022RP1_996&pageId=RefinitivNewscasts</a></pre><a class="storylink_item"href=""/>Source: Thomson Reuters<br /><br />Description: Die Einigung von Bund und Ländern sei eine gute Grundlage für den Umgang mit den Ukraine-Flüchtlingen, sagt der Bundeskanzler.<br />Short Link: <a href="https://refini.tv/3jfkLXx">https://refini.tv/3jfkLXx</a><br /><br />Video Transcript:<br /><br />Verified transcript not available</span></div></div></div></body></html>',
                }
            ],
            "inlineData": [
                {
                    "_contenttype": "text/plain",
                    "_dir": "ltr",
                    "_xml:lang": "de",
                    "$": "\nClick the following link to watch video: https://share.newscasts.refinitiv.com/link?entryId=1_bonf89p1&referenceId=tag:reuters.com,2022:newsml_OV039108042022RP1_996&pageId=RefinitivNewscasts\nSource: Thomson Reuters\n\nDescription: Die Einigung von Bund und Ländern sei eine gute Grundlage für\nden Umgang mit den Ukraine-Flüchtlingen, sagt der Bundeskanzler.\nShort Link: https://refini.tv/3jfkLXx\n\nVideo Transcript:\n\nVerified transcript not available\n",
                }
            ],
        },
    },
    "topNewsMetadata": [],
}

MOCKED_HEADLINES_RAW_RESPONSE = [
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
    {
        "headlines": [
            {
                "displayDirection": "LeftToRight",
                "documentType": "Story",
                "firstCreated": "2022-04-08T11:19:38.000Z",
                "isAlert": False,
                "language": "L:en",
                "reportCode": "",
                "sourceCode": "NS:RFT",
                "sourceName": "Refinitiv",
                "storyId": "urn:newsml:reuters.com:20220408:nIfp955dm0:3",
                "text": "CARE ratings for Indian debt instruments-Apr 8",
                "versionCreated": "2022-04-08T14:23:23.661Z",
            }
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    },
]


def test_access_layer_story():
    session = StubSession(is_open=True, response=NEWS_STORY_RESPONSE_DATA)
    set_default(session)
    response = news.get_story("urn:newsml:reuters.com:20201026:nPt6BSyBh")
    set_default(None)
    assert response == MOCKED_STORY_HTML_RESPONSE


def test_access_layer_headlines():
    session = StubSession(is_open=True, response=NEWS_HEADLINES_RESPONSE_UDF)
    session.config.set_param("apis.data.news.underlying-platform", "udf")
    set_default(session)
    response = news.get_headlines("Refinitiv")
    set_default(None)
    assert isinstance(response, pd.DataFrame)
    assert not response.empty
