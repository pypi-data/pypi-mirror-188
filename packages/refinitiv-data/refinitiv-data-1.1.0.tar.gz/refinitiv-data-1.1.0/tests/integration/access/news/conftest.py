def check_story_response_format(response, format):
    html_tags = [
        "html lang",
        "xml:lang",
        "<head>",
        "<body>",
        "<div class=",
        "<style type=",
    ]
    if format.value == "Html":
        assert any(tag in response for tag in html_tags)
    elif format.value == "Text":
        assert not all(tag in response for tag in html_tags)
