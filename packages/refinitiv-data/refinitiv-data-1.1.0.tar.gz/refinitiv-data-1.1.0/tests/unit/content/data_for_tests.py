from functools import partial

import refinitiv.data.content as rdc
from refinitiv.data.content.ipa.surfaces import cap
from refinitiv.data.content.ipa.surfaces import fx
from tests.unit.conftest import StubResponse

NEWS_STORY_DEFINITION = rdc.news.story.Definition(
    "urn:newsml:reuters.com:20201026:nPt6BSyBh"
)
NEWS_STORY_RESPONSE = StubResponse(
    {
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
                "infoSource": [
                    {"_qcode": "NS:RTRS", "_role": "cRole:source"},
                ],
                "creator": [{"_qcode": "NS:RTRS", "_role": "cRole:source"}],
                "contributor": [{"_qcode": "NS:RTRS", "_role": "cRole:enhancer"}],
                "audience": [{"_qcode": "NP:RITV"}],
                "altId": [
                    {"_type": "idType:USN", "$": "RTV7TbbdW"},
                ],
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
                    },
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
                    },
                ],
            },
            "assert": [
                {"_qcode": "NP:RITV", "type": [{"_qcode": "cptType:15"}]},
            ],
            "derivedFrom": [
                {"_idrefs": "A1", "_qcode": "NP:RITV"},
            ],
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
)

NEWS_STORY_RESPONSE_DATA = StubResponse(
    {
        "story": {
            "headlineHtml": '<h1 class="storyHeadline">\n<span class="headline">Nasdaq cae por controles de exportación EEUU a China que afectan a semiconductores</span> -\n<span class="source" title="RTRS">Reuters</span>\n</h1>',
            "storyHtml": '<div class="storyContent" lang="es"><style type="text/css">.storyContent * {border-color:inherit !important;outline-color:inherit !important;}</style><p class="tr-advisory">.</p><p class="tr-by">Por Shreyashi Sanyal y Bansari Mayur Kamdar</p><p class="tr-story-p1"><span class="tr-dateline">10 oct (Reuters)</span><span class="tr-dl-sep"> - </span>El índice Nasdaq caía el lunes hasta tocar mínimos de dos años, ya que los fabricantes de semiconductores se llevaban la peor parte de los esfuerzos de Estados Unidos para obstaculizar la industria de chips de China, mientras los inversores operaban con cautela antes del comienzo de la temporada de resultados. </p><p>* El índice SE Semiconductor de Filadelfia <a href="reuters://REALTIME/Verb=FullQuote/ric=.SOX" data-type="ric" data-ric=".SOX" translate="no" dir="ltr">.SOX</a> bajó un 2,7%, después de que el Gobierno del presidente Joe Biden publicó un amplio conjunto de controles de exportación el viernes, incluida una medida para aislar a China de ciertos chips semiconductores fabricados en cualquier parte del mundo con equipos estadounidenses.</p><p>* Algunos de los componentes más importantes del índice, incluida Nvidia Corp. <a href="reuters://REALTIME/Verb=FullQuote/ric=NVDA.O" data-type="ric" data-ric="NVDA.O" translate="no" dir="ltr">NVDA.O</a>, Qualcomm Inc. <a href="reuters://REALTIME/Verb=FullQuote/ric=QCOM.O" data-type="ric" data-ric="QCOM.O" translate="no" dir="ltr">QCOM.O</a> y Micron Technology Inc. <a href="reuters://REALTIME/Verb=FullQuote/ric=MU.O" data-type="ric" data-ric="MU.O" translate="no" dir="ltr">MU.O</a> perdieron entre 1,3% y 3,3% al inicio de la sesión.</p><p>* En las operaciones de media mañana, el Promedio Industrial Dow Jones <a href="reuters://REALTIME/Verb=FullQuote/ric=.DJI" data-type="ric" data-ric=".DJI" translate="no" dir="ltr">.DJI</a> subía 54,93 puntos, o un 0,19%, a 29.351,72 unidades; mientras que el S&amp;P 500 <a href="reuters://REALTIME/Verb=FullQuote/ric=.SPX" data-type="ric" data-ric=".SPX" translate="no" dir="ltr">.SPX</a> bajaba 9,31 puntos, o un 0,26%, a 3.630,35 unidades; y el índice Nasdaq Composite <a href="reuters://REALTIME/Verb=FullQuote/ric=.IXIC" data-type="ric" data-ric=".IXIC" translate="no" dir="ltr">.IXIC</a> cedía 73,99 puntos, o un 0,69%, a 10.578,41 unidades.</p><p>* Los gigantes tecnológicos Apple Inc. <a href="reuters://REALTIME/Verb=FullQuote/ric=AAPL.O" data-type="ric" data-ric="AAPL.O" translate="no" dir="ltr">AAPL.O</a> y Microsoft Corp. <a href="reuters://REALTIME/Verb=FullQuote/ric=MSFT.O" data-type="ric" data-ric="MSFT.O" translate="no" dir="ltr">MSFT.O</a> caían un 0,9% y un 1,5%, respectivamente, lastrando el subíndice del sector tecnológico del S&amp;P 500 <a href="reuters://REALTIME/Verb=FullQuote/ric=.SPLRCT" data-type="ric" data-ric=".SPLRCT" translate="no" dir="ltr">.SPLRCT</a> .</p><p><br/></p><p><br/></p><p class="tr-signoff"> (Reportes de Ankika Biswas y Shreyashi Sanyal en Bengaluru; reporte adicional de Bansari Mayur Kamdar. Editado en español por Marion Giraldo)</p><p class="tr-contactinfo">((Mesa de edición en español +562 24374447. Twitter: <a href="https://twitter.com/ReutersLatam" data-type="url" class="tr-link" translate="no">https://twitter.com/ReutersLatam</a>; ))</p><div class="tr-additinfo tr-desktop-part"><pre>REUTERS MG/\n</pre></div><p class="line-break"><br/></p><p class="tr-copyright">(c) Copyright Thomson Reuters 2022. Click For Restrictions - https://agency.reuters.com/en/copyright.html</p><p class="line-break"><br/></p><p class="tr-slugline">Keywords: MERCADOS-WALLST/ (MEDIA)</p></div>',
            "storyInfoHtml": '<h5 style="direction:ltr"><span data-version-created-date="2022-10-10T15:25:07.000Z" class="releasedDate">10-Oct-2022 15:25:07</span></h5>',
        }
    }
)

FUNDAMENTAL_AND_REFERENCE_DEFINITION = rdc.fundamental_and_reference.Definition(
    ["IBM"], ["TR.Volume"]
)
FUNDAMENTAL_AND_REFERENCE_RESPONSE_DESKTOP = StubResponse(
    {
        "responses": [
            {
                "columnHeadersCount": 1,
                "data": [["IBM", 3143309]],
                "headerOrientation": "horizontal",
                "headers": [
                    [
                        {"displayName": "Instrument"},
                        {"displayName": "Volume", "field": "TR.VOLUME"},
                    ]
                ],
                "rowHeadersCount": 1,
                "totalColumnsCount": 2,
                "totalRowsCount": 2,
            }
        ]
    }
)
FUNDAMENTAL_AND_REFERENCE_RESPONSE_PLATFORM = StubResponse(
    {
        "links": {"count": 1},
        "variability": "",
        "universe": [
            {
                "Instrument": "IBM",
                "Company Common Name": "International Business Machines Corp",
                "Organization PermID": "4295904307",
                "Reporting Currency": "USD",
            }
        ],
        "data": [["IBM", 3538317]],
        "messages": {
            "codes": [[-1, -1]],
            "descriptions": [{"code": -1, "description": "ok"}],
        },
        "headers": [
            {
                "name": "instrument",
                "title": "Instrument",
                "type": "string",
                "description": "The requested Instrument as defined by the user.",
            },
            {
                "name": "TR.Volume",
                "title": "Volume",
                "type": "number",
                "decimalChar": ".",
                "description": "Volume for the latest trading day.",
            },
        ],
    }
)

NEWS_HEADLINES_DEFINITION = rdc.news.headlines.Definition("Refinitiv")
NEWS_HEADLINES_RESPONSE_UDF = StubResponse(
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
            },
        ],
        "newer": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJvbGRUb05ldyIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjQxOjEwLjQ5OFoiLCJwbmFjIjoiblZFTjI1NjA5NiJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
        "older": "/headlines?payload=eyJxdWVyeSI6eyJpbnB1dCI6IlJlZmluaXRpdiIsImNhdGVnb3J5IjoiU291cmNlIiwiZ3JvdXAiOiJOZXdzV2lyZVNvdXJjZSIsImlkIjoiTlM6UkZUIiwibGFiZWwiOiJSZWZpbml0aXYiLCJsYWJlbHMiOnsiamEiOiLjg6rjg5XjgqPjg4vjg4bjgqPjg5YifSwicmVhZGFibGUiOiJTb3VyY2U6UkZUIiwicmVhbHRpbWVGaWx0ZXIiOiJOUzpSRlQiLCJyZWFsdGltZUZpbHRlcnMiOlsiTlM6UkZUIl0sInJlYWx0aW1lQ2FwYWJpbGl0aWVzIjpbXSwibmV3c3dpcmUiOiJ2YWx1ZSIsIm5ld3Nyb29tIjoiYmxvY2siLCJ3ZWJuZXdzIjoiYmxvY2siLCJzb2NpYWwiOiJibG9jayIsImZpbHRlciI6InZhbHVlIiwibmV3c3dpcmVTZWxlY3RhYmxlIjp0cnVlLCJuZXdzcm9vbVNlbGVjdGFibGUiOmZhbHNlLCJ3ZWJuZXdzU2VsZWN0YWJsZSI6ZmFsc2UsInNvY2lhbFNlbGVjdGFibGUiOmZhbHNlLCJpc1JlY29tbWVuZGVkIjp0cnVlLCJwYXJlbnRzSWRzIjpbIk06MSIsIk06Q1kiLCJSRVBPU0lUT1JZOk5ld3NXaXJlIiwiTToyQ1QiLCJNOjJDUyIsIk06MkNSIiwiTToyQ1EiLCJNOjFRRCIsIk5TOjM1MTllNzk0LTU5YWYtNGYyMS1iMmZkLWMxZmFmYmY4ZWQwMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjE0ZTNhMWZiLTE5YTctNDk4Mi05OTY2LWVkOGJmN2Q4ZWE1NC1OZXdzV2lyZVNvdXJjZSIsIk5TOjM4NDUyMDM4LTJmOTQtNDVmOC1iYjZhLWNhYTk2ZTQ0ZGZhNi1OZXdzV2lyZVNvdXJjZSIsIk5TOmY3YmNhNDAxLTJlYjUtNGRhNS1iYmNjLTE0NDc0Mzk4ZTdhZC1OZXdzV2lyZVNvdXJjZSIsIk5TOjJiMzVjYTIzLWQ0ZjctNDk5ZC1iODc5LWM3YTMzMjIwYzliZS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM0NzdhMWQ4LTcwZDQtNDQ4NS05MTJmLTFiYjkxNzQ1OGM1MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmMwOWNmYjE2LWM0YmMtNGE5MS04NWYwLWNkMzZjYzQ3Y2MxMi1OZXdzV2lyZVNvdXJjZSIsIk5TOjhlYmNiZjkzLWRjM2EtNDRmYy1iMzViLWJmYzVjNGEwM2NiNC1OZXdzV2lyZVNvdXJjZSIsIk5TOjhkYWY5YTg3LTFkOTYtNDM0YS05MmZhLWZhMWNkODZkM2Y4Yy1OZXdzV2lyZVNvdXJjZSIsIk5TOjQ1MGJiYzliLTVhN2YtNGU2NC05ODU3LTVjMzEzMTc0ZmM0MS1OZXdzV2lyZVNvdXJjZSIsIk5TOmM1MmE3M2I4LWNmYTgtNDYzNi05MzhiLTllNjE1MWU4NGE0YS1OZXdzV2lyZVNvdXJjZSIsIlJFUE9TSVRPUlk6TmV3c1Jvb20iLCJSRVBPU0lUT1JZOldlYk5ld3MiLCJSRVBPU0lUT1JZOlNvY2lhbCJdLCJoYXNDaGlsZHJlbiI6ZmFsc2UsImNoaWxkcmVuQ291bnQiOnsid2VibmV3cyI6MCwibmV3c3dpcmUiOjAsInNvY2lhbCI6MCwibmV3c3Jvb20iOjAsInVuaXEiOjB9fSwicGFyYW0iOnsicmVwb3NpdG9yaWVzIjpbIk5ld3NXaXJlIl0sInNlYXJjaEluIjoiSGVhZGxpbmVPbmx5IiwibnVtYmVyIjoxMCwicmVzZWFyY2hSZXN1bHRzIjpmYWxzZSwic25pcHBldHMiOmZhbHNlLCJvbGRlclRoYW4iOiIiLCJuZXdlclRoYW4iOiIiLCJoaWdobGlnaHRzIjpmYWxzZSwic29ydE9yZGVyIjoibmV3VG9PbGQiLCJhcmNoaXZlIjpmYWxzZSwidHJhY2tpbmciOiJhdXRvIiwic2VudGltZW50IjpmYWxzZSwicmVsZXZhbmNlIjoiSGlnaCJ9LCJwaXZvdCI6eyJzb3J0T3JkZXIiOiJuZXdUb09sZCIsIm5ld3Nyb29tQ29udGV4dCI6bnVsbCwibmV3c3Jvb21PZmZzZXQiOjAsIm5ld3N3aXJlUGl2b3QiOnsiZGF0ZXRpbWUiOiIyMDIyLTA0LTA4VDE0OjIzOjIzLjY2MVoiLCJwbmFjIjoibklmcDk1NWRtMCJ9LCJmZWRlcmF0ZWRDb250ZXh0IjpudWxsLCJpbml0aWFsU29ydE9yZGVyIjoibmV3VG9PbGQifX0=",
    }
)
NEWS_HEADLINES_RESPONSE = StubResponse(
    {
        "data": [
            {
                "storyId": "urn:newsml:reuters.com:20220408:nRTV7TbbdW:5",
                "newsItem": {
                    "_version": 5,
                    "contentMeta": {
                        "audience": [{"_qcode": "NP:RITV"}],
                        "creator": [{"_qcode": "NS:RTRS", "_role": "sRole:source"}],
                        "infoSource": [
                            {"_qcode": "NS:RTRS", "_role": "sRole:source"},
                            {"_qcode": "NS:RTRS", "_role": "sRole:origProv"},
                        ],
                        "language": [{"_tag": "de"}],
                        "subject": [
                            {"_qcode": "M:2CS"},
                            {"_qcode": "M:2CU"},
                            {"_qcode": "M:1Q1"},
                            {"_qcode": "G:A"},
                            {"_qcode": "M:2CM"},
                            {"_qcode": "M:2CQ"},
                            {"_qcode": "M:1QD"},
                            {"_qcode": "M:2CR"},
                            {"_qcode": "M:2CT"},
                            {"_qcode": "G:1"},
                            {"_qcode": "M:2CV"},
                            {"_qcode": "G:71"},
                            {"_qcode": "G:B"},
                            {"_qcode": "M:2CN"},
                            {"_qcode": "M:2CP"},
                            {"_qcode": "M:2D1"},
                        ],
                        "urgency": {"$": 3},
                    },
                    "itemMeta": {
                        "firstCreated": {"$": "2022-04-08T06:00:00.972Z"},
                        "versionCreated": {"$": "2022-04-08T06:02:25.633Z"},
                        "title": [
                            {
                                "$": "Refinitiv Newscasts - Scholz lobt Schulterschluss bei Kriegsflüchtlingen"
                            }
                        ],
                    },
                },
            },
        ],
        "meta": {
            "count": 10,
            "pageLimit": 10,
            "next": "H4sIAAAAAAAAABXNwQ6CMBAE0H/Zq5iUWhDqWb1hQogX46GBRZvUlrSlYgj/bnvc2cmbFUapPFrgK/jfhMBhtIgeFw8ZBKHmFLU4Si29DDEblXg54A94oxiU1AjPLYOPWHozaw88JxlMMhifSI1fJ4co5CWrD1XN2LEuKn0/N7SoypzsKKGUMFKeyL69dJGXrknbHLyN01F2xqYzSp25qSFWLCoMQvd4tWae4k8oBdsfCNrjlMoAAAA=",
            "prev": "H4sIAAAAAAAAABXOTQ6CMBAF4LvMVkzKj6B4AHea1EYXxkWBqTYZW9IWxBDublnOm5dvZgalKaCDeobw6xFqUA4x4BQggVHSsEYclTY66DFmiuTLQ/2AN8qOtEF4Lgl85NTawQSoU5ZAr0cbVtLg1+suCmlZHPJDVRW7Ms8NF7dKNE1332Qsy1jB9ke25YJfo6/9eT0e/5DkEaLtrVvnaAl7oS52HBKO0rR4cnbo404SwfIHSJxlH8wAAAA=",
        },
    }
)

SURFACE_SWAPTION_DEFINITION = rdc.ipa.surfaces.swaption.Definition(
    surface_tag="My EUR VolCube",
    underlying_definition=rdc.ipa.surfaces.swaption.SwaptionSurfaceDefinition(
        instrument_code="EUR",
        discounting_type=rdc.ipa.surfaces.swaption.DiscountingType.OIS_DISCOUNTING,
    ),
    surface_parameters=rdc.ipa.surfaces.swaption.SwaptionCalculationParams(
        shift_percent=3,
        x_axis=rdc.ipa.surfaces.swaption.Axis.STRIKE,
        y_axis=rdc.ipa.surfaces.swaption.Axis.TENOR,
        z_axis=rdc.ipa.surfaces.swaption.Axis.EXPIRY,
    ),
    surface_layout=rdc.ipa.surfaces.swaption.SurfaceLayout(
        format=rdc.ipa.surfaces.swaption.Format.MATRIX,
    ),
)

SURFACE_SWAPTION_RESPONSE = StubResponse(
    {
        "data": [
            {
                "surfaceTag": "My EUR VolCube",
                "surface": [
                    [
                        None,
                        "-2.00",
                        "-1.50",
                        "-1.00",
                    ],
                    [
                        "1",
                        "124.63",
                        "108.79",
                        "91.51",
                    ],
                    [
                        "2",
                        "157.25",
                        "139.29",
                        "120.61",
                    ],
                ],
            }
        ]
    }
)

SURFACES_DEFINITION = rdc.ipa.surfaces.Definitions(
    [
        SURFACE_SWAPTION_DEFINITION,
    ]
)

SURFACES_RESPONSE = SURFACE_SWAPTION_RESPONSE

PRICING_DEFINITION = rdc.pricing.Definition("EUR=")
PRICING_RESPONSE = StubResponse(
    [
        {
            "ID": 754,
            "Type": "Refresh",
            "Key": {"Service": "ERT_FD3_LF1", "Name": "EUR="},
            "State": {
                "Stream": "NonStreaming",
                "Data": "Ok",
                "Text": "**All is well",
            },
            "Qos": {
                "Timeliness": "Realtime",
                "Rate": "TimeConflated",
                "RateInfo": 3000,
            },
            "PermData": "AwD9Umw=",
            "SeqNumber": 38494,
            "Fields": {
                "PROD_PERM": 526,
                "RDNDISPLAY": 153,
            },
        }
    ]
)

PRICING_DF_CREATING_RESPONSE = StubResponse(
    [
        {
            "ID": 207,
            "Type": "Refresh",
            "Key": {"Service": "ERT_FD3_LF1", "Name": "EUR="},
            "State": {"Stream": "NonStreaming", "Data": "Ok", "Text": "**All is well"},
            "Qos": {
                "Timeliness": "Realtime",
                "Rate": "TimeConflated",
                "RateInfo": 3000,
            },
            "PermData": "AwD9Umw=",
            "SeqNumber": 50430,
            "Fields": {
                "CF_NAME": "Euro",
                "DDS_DSO_ID": 12348,
                "BR_LINK1": None,
                "QUOTIM_2": "10:30:40",
                "QUOTE_DT2": "2022-06-22",
                "ASKHI1_MS": "22:55:25.876",
            },
        }
    ]
)

FORWARD_CURVE_RESPONSE = StubResponse(
    {
        "data": [
            {
                "forwardCurves": [{"curvePoints": []}],
            }
        ]
    }
)

FORWARD_CURVES_RESPONSE = FORWARD_CURVE_RESPONSE

ZC_CURVE_RESPONSE = StubResponse(
    {
        "data": [
            {
                "curves": {"key": {"curvePoints": []}},
            }
        ]
    }
)

ZC_CURVE_DEFINITION_RESPONSE = StubResponse(
    {
        "data": [
            {
                "curveDefinitions": [{}],
            }
        ]
    }
)

ZC_CURVE_DEFINITIONS_RESPONSE = ZC_CURVE_DEFINITION_RESPONSE

ZC_CURVES_RESPONSE = StubResponse(
    {
        "data": [
            {
                "curves": {"key": {"curvePoints": []}},
            }
        ]
    }
)

SURFACE_CAP_DEFINITION = rdc.ipa.surfaces.cap.Definition(
    surface_tag="USD_Strike__Tenor_",
    underlying_definition=cap.CapSurfaceDefinition(
        instrument_code="USD",
        discounting_type=cap.DiscountingType.OIS_DISCOUNTING,
    ),
    surface_layout=cap.SurfaceLayout(format=cap.Format.MATRIX),
    surface_parameters=cap.CapCalculationParams(
        valuation_date="2020-03-20",
        x_axis=cap.Axis.STRIKE,
        y_axis=cap.Axis.TENOR,
    ),
)

SURFACE_CAP_RESPONSE = StubResponse(
    {
        "data": [
            {
                "surfaceTag": "USD_Strike__Tenor_",
                "surface": [
                    [
                        None,
                        "0.250000",
                    ],
                    [
                        "3",
                        "49.20",
                    ],
                    [
                        "9",
                        "49.20",
                    ],
                ],
            }
        ]
    }
)

SURFACE_ETI_DEFINITION = rdc.ipa.surfaces.eti.Definition(
    surface_tag="1",
    underlying_definition=rdc.ipa.surfaces.eti.EtiSurfaceDefinition(
        instrument_code="BNPP.PA@RIC",
    ),
    surface_parameters=rdc.ipa.surfaces.eti.EtiCalculationParams(
        price_side=rdc.ipa.surfaces.eti.PriceSide.MID,
        volatility_model=rdc.ipa.surfaces.eti.VolatilityModel.SVI,
        x_axis=rdc.ipa.surfaces.cap.Axis.DATE,
        y_axis=rdc.ipa.surfaces.cap.Axis.STRIKE,
    ),
    surface_layout=rdc.ipa.surfaces.eti.SurfaceLayout(
        format=rdc.ipa.surfaces.cap.Format.MATRIX, y_point_count=10
    ),
)

SURFACE_ETI_RESPONSE = StubResponse(
    {
        "data": [
            {
                "surfaceTag": "1",
                "surface": [
                    [
                        None,
                        "37.656",
                        "40.0095",
                        "42.363",
                    ],
                    [
                        "2022-04-14",
                        100.646188439577,
                        85.3825756996221,
                        71.1129204322784,
                    ],
                    [
                        "2022-05-20",
                        63.6892177011107,
                        58.93280211148571,
                        54.4441693428238,
                    ],
                ],
            }
        ]
    }
)

SURFACE_FX_DEFINITION = rdc.ipa.surfaces.fx.Definition(
    underlying_definition={"fxCrossCode": "EURUSD"},
    surface_tag="FxVol-EURUSD",
    surface_layout=fx.SurfaceLayout(format=fx.Format.MATRIX),
    surface_parameters=fx.FxCalculationParams(
        x_axis=fx.Axis.DATE,
        y_axis=fx.Axis.STRIKE,
        calculation_date="2018-08-20T00:00:00Z",
    ),
)

SURFACE_FX_RESPONSE = StubResponse(
    {
        "data": [
            {
                "surfaceTag": "FxVol-EURUSD",
                "surface": [
                    [
                        None,
                        1.1038366375817679,
                        1.109416864898416,
                        1.114997092215064,
                    ],
                    [
                        "2018-08-21T00:00:00Z",
                        14.680556199566963,
                        13.940204590775027,
                        13.164852627183423,
                    ],
                    [
                        "2018-08-27T00:00:00Z",
                        9.405878307234056,
                        9.105090369857033,
                        8.797664558348064,
                    ],
                ],
            }
        ]
    }
)

NONE_REPLACED_WITH_NA_RDP_DATA = {
    "data": [
        ["GOOG.O", "2020-01-20T00:00:00Z", None],
        ["GOOG.O", "2020-12-31T00:00:00Z", None],
    ],
    "headers": [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
        {"name": "TR.RevenueMean", "title": "Currency"},
    ],
}

NONE_REPLACED_WITH_NA_UDF_DATA = {
    "data": [
        ["GOOG.O", "2020-01-20T00:00:00Z", None],
        ["GOOG.O", "2020-12-31T00:00:00Z", None],
    ],
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Date"},
            {"displayName": "Currency"},
        ]
    ],
}

NAN_REPLACED_WITH_NA_RDP_DATA = {
    "data": [
        ["GOOG.O", "2020-01-20T00:00:00Z", 1000],
        ["GOOG.O", "2020-12-31T00:00:00Z", None],
    ],
    "headers": [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
        {"name": "TR.RevenueMean", "title": "Currency"},
    ],
}

NAN_REPLACED_WITH_NA_UDF_DATA = {
    "data": [
        ["GOOG.O", "2020-01-20T00:00:00Z", 1000],
        ["GOOG.O", "2020-12-31T00:00:00Z", None],
    ],
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Date"},
            {"displayName": "Currency"},
        ]
    ],
}

EMPTY_STRING_LEAVE_AS_IT_IS_RDP_DATA = {
    "data": [
        ["GOOG.O", "2020-01-20T00:00:00Z", ""],
        ["GOOG.O", "2020-12-31T00:00:00Z", ""],
    ],
    "headers": [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
        {"name": "TR.RevenueMean", "title": "Currency"},
    ],
}
EMPTY_STRING_LEAVE_AS_IT_IS_UDF_DATA = {
    "data": [
        ["GOOG.O", "2020-01-20T00:00:00Z", ""],
        ["GOOG.O", "2020-12-31T00:00:00Z", ""],
    ],
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Date"},
            {"displayName": "Currency"},
        ]
    ],
}

TWO_UNIVERSES_ONE_FIELD_RDP_DATA = {
    "data": [
        ["EUR=", "2022-01-31", 2000],
        ["EUR=", "2022-02-28", 2000],
        ["LSEG.L", "2020-01-20T00:00:00Z", 1000],
        ["LSEG.L", "2020-12-31T00:00:00Z", 1000],
    ],
    "headers": [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
        {"name": "BID", "title": "BID"},
    ],
}
TWO_UNIVERSES_ONE_FIELD_UDF_DATA = {
    "data": [
        ["EUR=", "2022-01-31", 2000],
        ["EUR=", "2022-02-28", 2000],
        ["LSEG.L", "2020-01-20T00:00:00Z", 1000],
        ["LSEG.L", "2020-12-31T00:00:00Z", 1000],
    ],
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Date"},
            {"displayName": "BID"},
        ]
    ],
}

INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_RDP_DATA = {
    "data": [
        ["", "2020-01-20T00:00:00Z", ""],
        ["GOOG.O", "2020-12-31T00:00:00Z", 1000],
    ],
    "headers": [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
        {"name": "TR.RevenueMean", "title": "Currency"},
    ],
}
INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_UDF_DATA = {
    "data": [
        ["", "2020-01-20T00:00:00Z", ""],
        ["GOOG.O", "2020-12-31T00:00:00Z", 1000],
    ],
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Date"},
            {"displayName": "Currency"},
        ]
    ],
}

headers_rdp = [
    {"name": "instrument", "title": "Instrument"},
    {"name": "date", "title": "Date"},
    {"name": "TR.RevenueMean", "title": "Currency"},
    {"name": "TR.RevenueMean", "title": "Revenue - Mean"},
]

headers_udf = [
    [
        {"displayName": "Instrument"},
        {"displayName": "Date"},
        {"displayName": "Currency", "field": "TR.REVENUEMEAN.currency"},
        {"displayName": "Revenue - Mean", "field": "TR.REVENUEMEAN"},
    ]
]

TWO_SAME_DATES_DOES_NOT_MERGE_IN_ONE_RDP_DATA = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["IBM", "2020-12-16T00:00:00", "USD", 73950729070],
        ["IBM", "2021-01-27T00:00:00", "USD", 74195199870],
        ["IBM", "2021-02-11T00:00:00", "USD", 74195199870],
        ["IBM", "2021-03-22T00:00:00", "USD", 74221312380],
        ["IBM", "2021-04-25T00:00:00", "USD", 74397055190],
        ["IBM", "2021-05-21T00:00:00", "USD", 74329699000],
        ["IBM", "2021-05-21T00:00:00", "USD", 74329699000],
        ["IBM", "2021-07-29T00:00:00", "USD", 75129376130],
        ["IBM", "2021-08-30T00:00:00", "USD", 75127177530],
    ],
    "headers": headers_rdp,
}
TWO_SAME_DATES_DOES_NOT_MERGE_IN_ONE_UDF_DATA = {
    "data": [
        ["IBM", "2020-10-23T00:00:00Z", "USD", 73965242400],
        ["IBM", "2020-10-23T00:00:00Z", "USD", 73965242400],
        ["IBM", "2020-12-16T00:00:00Z", "USD", 73950729070],
        ["IBM", "2021-01-27T00:00:00Z", "USD", 74195199870],
        ["IBM", "2021-02-11T00:00:00Z", "USD", 74195199870],
        ["IBM", "2021-03-22T00:00:00Z", "USD", 74221312380],
        ["IBM", "2021-04-25T00:00:00Z", "USD", 74397055190],
        ["IBM", "2021-05-21T00:00:00Z", "USD", 74329699000],
        ["IBM", "2021-05-21T00:00:00Z", "USD", 74329699000],
        ["IBM", "2021-07-29T00:00:00Z", "USD", 75129376130],
        ["IBM", "2021-08-30T00:00:00Z", "USD", 75127177530],
    ],
    "headers": headers_udf,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["IBM", "2020-12-16T00:00:00", "USD", 73950729070],
        ["IBM", "2021-01-27T00:00:00", "USD", 74195199870],
        ["IBM", "2021-02-11T00:00:00", "USD", 74195199870],
        ["IBM", "2021-03-22T00:00:00", "USD", 74221312380],
        ["IBM", "2021-04-25T00:00:00", "USD", 74397055190],
        ["IBM", "2021-05-21T00:00:00", "USD", 74329699000],
        ["IBM", "2021-05-21T00:00:00", "USD", 74329699000],
        ["IBM", "2021-07-29T00:00:00", "USD", 75129376130],
        ["IBM", "2021-08-30T00:00:00", "USD", 75127177530],
        ["VOD.L", "2020-10-21T00:00:00", "EUR", 43375027760],
        ["VOD.L", "2020-11-23T00:00:00", "EUR", 43442990380],
        ["VOD.L", "2020-12-16T00:00:00", "EUR", 43372965910],
        ["VOD.L", "2021-01-20T00:00:00", "EUR", 43333798760],
        ["VOD.L", "2021-02-24T00:00:00", "EUR", 43421860050],
        ["VOD.L", "2021-03-31T00:00:00", "EUR", 43445947190],
        ["VOD.L", "2021-04-28T00:00:00", "EUR", 43503348730],
        ["VOD.L", "2021-05-27T00:00:00", "EUR", 44918585000],
        ["VOD.L", "2021-06-29T00:00:00", "EUR", 44967283500],
        ["VOD.L", "2021-07-29T00:00:00", "EUR", 45109776750],
        ["VOD.L", "2021-08-25T00:00:00", "EUR", 45088444860],
    ],
    "headers": headers_rdp,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["IBM", "2020-12-16T00:00:00", "USD", 73950729070],
        ["IBM", "2021-01-27T00:00:00", "USD", 74195199870],
        ["IBM", "2021-02-11T00:00:00", "USD", 74195199870],
        ["IBM", "2021-03-22T00:00:00", "USD", 74221312380],
        ["IBM", "2021-04-25T00:00:00", "USD", 74397055190],
        ["IBM", "2021-05-21T00:00:00", "USD", 74329699000],
        ["IBM", "2021-05-21T00:00:00", "USD", 74329699000],
        ["IBM", "2021-07-29T00:00:00", "USD", 75129376130],
        ["IBM", "2021-08-30T00:00:00", "USD", 75127177530],
        ["VOD.L", "2020-10-21T00:00:00", "EUR", 43375027760],
        ["VOD.L", "2020-11-23T00:00:00", "EUR", 43442990380],
        ["VOD.L", "2020-12-16T00:00:00", "EUR", 43372965910],
        ["VOD.L", "2021-01-20T00:00:00", "EUR", 43333798760],
        ["VOD.L", "2021-02-24T00:00:00", "EUR", 43421860050],
        ["VOD.L", "2021-03-31T00:00:00", "EUR", 43445947190],
        ["VOD.L", "2021-04-28T00:00:00", "EUR", 43503348730],
        ["VOD.L", "2021-05-27T00:00:00", "EUR", 44918585000],
        ["VOD.L", "2021-06-29T00:00:00", "EUR", 44967283500],
        ["VOD.L", "2021-07-29T00:00:00", "EUR", 45109776750],
        ["VOD.L", "2021-08-25T00:00:00", "EUR", 45088444860],
    ],
    "headers": headers_udf,
}

# Combinations:
# 1. x x -
# 2. x x x
# 3. - - -
# 4. - x x
# 5. x - x

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_1 = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-05-07T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_rdp,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_1 = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-05-07T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_udf,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_2 = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-10-23T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_rdp,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_2 = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-10-23T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_udf,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_3 = {
    "data": [
        ["IBM", "2020-09-18T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-05-07T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_rdp,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_3 = {
    "data": [
        ["IBM", "2020-09-18T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-05-07T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_udf,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_4 = {
    "data": [
        ["IBM", "2020-05-07T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-10-23T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_rdp,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_4 = {
    "data": [
        ["IBM", "2020-05-07T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-10-23T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-10-23T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_udf,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_5 = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-05-07T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-10-23T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_rdp,
}

MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_5 = {
    "data": [
        ["IBM", "2020-10-23T00:00:00", "USD", 73965242400],
        ["VOD.L", "2020-05-07T00:00:00", "EUR", 43375027760],
        ["NKE.N", "2020-10-23T00:00:00", "GBP", 43375027760],
    ],
    "headers": headers_udf,
}

DELETE_ROW_IF_DATE_IS_NONE_UDF_DATA = {
    "data": [
        ["GOOG.O", "", "", "", None],
        ["GOOG.O", "2021-12-31T00:00:00Z", 257637000000, 146698000000, ""],
        ["INVAL", "", None, None, None],
        ["FB.O", "", "", "", None],
        ["FB.O", "2020-12-31T00:00:00Z", 85965000000, 69273000000, ""],
    ],
    "headers": [
        [
            {"displayName": "Instrument"},
            {"displayName": "Date"},
            {"displayName": "Revenue", "field": "TR.REVENUE"},
            {"displayName": "Gross Profit", "field": "TR.GROSSPROFIT"},
            {"displayName": "INVALID_FIELD", "field": "INVALID_FIELD"},
        ]
    ],
}
DELETE_ROW_IF_DATE_IS_NONE_RDP_DATA = {
    "data": [
        ["GOOG.O", "2021-12-31T00:00:00", 257637000000, 146698000000],
        ["INVAL", None, None, None],
        ["FB.O", "2020-12-31T00:00:00", 85965000000, 69273000000],
    ],
    "headers": [
        {"name": "instrument", "title": "Instrument"},
        {"name": "date", "title": "Date"},
        {"name": "TR.Revenue", "title": "Revenue"},
        {"name": "TR.GrossProfit", "title": "Gross Profit"},
    ],
}
zc_curves_definitions = [
    rdc.ipa.curves.zc_curve_definitions.Definition(source="Refinitiv"),
    rdc.ipa.curves.zc_curve_definitions.Definition(source="Peugeot"),
]
calendars_definitions = [
    rdc.ipa.dates_and_calendars.add_periods.Definition(
        tag="first",
        start_date="2020-01-01",
    ),
    rdc.ipa.dates_and_calendars.add_periods.Definition(
        tag="second",
        start_date="2018-01-01",
    ),
]
universe_definitions = [
    rdc.esg.basic_overview.Definition,
    rdc.esg.full_scores.Definition,
    rdc.esg.full_measures.Definition,
    rdc.esg.standard_scores.Definition,
    rdc.esg.standard_measures.Definition,
    partial(rdc.estimates.view_actuals.annual.Definition, package="basic"),
    partial(rdc.estimates.view_actuals.interim.Definition, package="basic"),
    rdc.estimates.view_actuals_kpi.annual.Definition,
    rdc.estimates.view_actuals_kpi.interim.Definition,
    partial(rdc.estimates.view_summary.annual.Definition, package="basic"),
    partial(
        rdc.estimates.view_summary.historical_snapshots_non_periodic_measures.Definition,
        package="basic",
    ),
    partial(
        rdc.estimates.view_summary.historical_snapshots_periodic_measures_annual.Definition,
        package="basic",
    ),
    partial(
        rdc.estimates.view_summary.historical_snapshots_periodic_measures_interim.Definition,
        package="basic",
    ),
    partial(
        rdc.estimates.view_summary.historical_snapshots_recommendations.Definition,
        package="basic",
    ),
    partial(rdc.estimates.view_summary.interim.Definition, package="basic"),
    partial(
        rdc.estimates.view_summary.non_periodic_measures.Definition, package="basic"
    ),
    partial(rdc.estimates.view_summary.recommendations.Definition, package="basic"),
    rdc.estimates.view_summary_kpi.annual.Definition,
    rdc.estimates.view_summary_kpi.historical_snapshots_kpi.Definition,
    rdc.estimates.view_summary_kpi.interim.Definition,
    partial(rdc.ownership.consolidated.breakdown.Definition, stat_type=1),
    rdc.ownership.consolidated.concentration.Definition,
    rdc.ownership.consolidated.investors.Definition,
    partial(rdc.ownership.consolidated.recent_activity.Definition, sort_order="asc"),
    rdc.ownership.consolidated.shareholders_report.Definition,
    partial(rdc.ownership.consolidated.top_n_concentration.Definition, count=5),
    partial(rdc.ownership.fund.breakdown.Definition, stat_type=1),
    rdc.ownership.fund.concentration.Definition,
    rdc.ownership.fund.holdings.Definition,
    rdc.ownership.fund.investors.Definition,
    partial(rdc.ownership.fund.recent_activity.Definition, sort_order="asc"),
    rdc.ownership.fund.shareholders_report.Definition,
    partial(rdc.ownership.fund.top_n_concentration.Definition, count=5),
    rdc.ownership.insider.shareholders_report.Definition,
    rdc.ownership.insider.transaction_report.Definition,
    rdc.ownership.investor.holdings.Definition,
    rdc.ownership.org_info.Definition,
    rdc.pricing.Definition,
]
fields_in_json_definitions = [
    rdc.ipa.financial_contracts.bond.Definition,
    rdc.ipa.financial_contracts.cap_floor.Definition,
    rdc.ipa.financial_contracts.cds.Definition,
    rdc.ipa.financial_contracts.cross.Definition,
    partial(
        rdc.ipa.financial_contracts.Definitions,
        universe=[rdc.ipa.financial_contracts.option.Definition()],
    ),
    rdc.ipa.financial_contracts.option.Definition,
    rdc.ipa.financial_contracts.repo.Definition,
    rdc.ipa.financial_contracts.swap.Definition,
    rdc.ipa.financial_contracts.swaption.Definition,
    rdc.ipa.financial_contracts.term_deposit.Definition,
]
calendars_jsons = [
    {"startDate": "2020-01-01", "tag": "first", "holidayOutputs": []},
    {"startDate": "2018-01-01", "tag": "second", "holidayOutputs": []},
]
