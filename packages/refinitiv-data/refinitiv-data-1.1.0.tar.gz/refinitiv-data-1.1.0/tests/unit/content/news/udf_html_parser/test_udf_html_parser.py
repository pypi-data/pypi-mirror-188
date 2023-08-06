import pytest

from refinitiv.data.content.news._udf_html_parser import HeadlineHTMLParser


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        (
            '<h1 class="storyHeadline">'
            '\n<span class="headline">Test headline</span> -'
            '\n<span class="source" title="test_title">Test title</span>'
            "\n</h1>",
            {
                "headline": "Test headline",
                "creator": "test_title",
            },
        ),
        (
            '<div class="storyContent" lang="en">'
            '<style type="text/css">'
            ".storyContent * {border-color: inherit !important;outline-color: inherit !important;}</style>"
            '<div class="tr-npp-lead"><p>Text</p><p>for</p></div><div class="tr-npp-body"><p>test</p><p>parser.</p>'
            '<p>Read More</p><p><a href=""data-type="url" class="tr-link" translate="no">AP News Digest 6:30 a.m.'
            '</a></p><p><a href=""data-type="url" class="tr-link" translate="no">...</a></p><p>'
            '<a href=""data-type="url" class="tr-link" translate="no">...</a></p>'
            '</div><p class="line-break"><br/></p><p class="tr-copyright">Copyright</p></div>',
            {
                "text": [
                    "Text",
                    "for",
                    "test",
                    "parser.",
                    "Read More",
                    "AP News Digest 6:30 a.m.",
                    "...",
                    "...",
                    "Copyright",
                ]
            },
        ),
        (
            '<h5 style="direction:ltr"><span data-version-created-date="2021-10-03T11:08:19.096Z" class="releasedDate">03-Oct-2021 11:08:19</span></h5>',
            {"creation_date": "2021-10-03T11:08:19.096Z"},
        ),
    ],
)
def test_udf_html_parser(input_data, expected_result):
    # given
    parser = HeadlineHTMLParser()

    # when
    parser.feed(input_data)
    result = parser.data

    # then
    assert result == expected_result
