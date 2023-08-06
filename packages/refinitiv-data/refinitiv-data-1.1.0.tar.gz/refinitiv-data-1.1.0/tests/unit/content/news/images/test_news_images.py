import json
import os.path
import shutil

from refinitiv.data.content import news
from tests.unit.conftest import StubResponse, StubSession

path_to_save = "tests/unit/content/news/images/files"

with open("tests/unit/content/news/images/images.json") as f:
    images_response = json.loads(f.read())


def make_check_url_in_request(expected_url: str):
    def check_url_in_http_request(response):
        url = response.url
        assert url == expected_url
        response = StubResponse(images_response)
        response.content = b""
        return response

    return check_url_in_http_request


def test_news_images():
    session = StubSession(is_open=True, response=StubResponse(images_response))

    response = news.images.Definition("id").get_data(session)
    image = response.data.image

    assert response.data.raw == images_response
    assert image.provider == ["NOT AVAILABLE"]
    assert image.body_type == ["image/jpeg"]
    assert image.source == ["RTRS"]
    assert image.version_created == ["20220927T132732.524+0000"]
    assert image.first_created == ["20220927T132732.524+0000"]
    assert image.filename == "2022-09-27T132732Z_1_CN0_RTRLXPP_2_LYNXPACKAGER.JPG"
    assert image.available_rsf == ["No"]
    assert image.size == 33603
    assert image.show()


def test_save_with_size():
    image_id = "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG"
    with open(f"tests/unit/content/news/images/{image_id}", "rb") as f:
        image_data = f.read()
    stub_response = StubResponse()
    stub_response.content = image_data
    stub_response.http_headers["content-type"] = "image/jpeg"
    session = StubSession(is_open=True, response=stub_response)
    response = news.images.Definition("id", width=200).get_data(session)
    image = response.data.image
    image.save(path_to_save)

    assert os.path.exists(f"{path_to_save}/{image.filename}")

    shutil.rmtree(path_to_save)


def test_save():
    session = StubSession(is_open=True, response=StubResponse(images_response))

    response = news.images.Definition("id").get_data(session)
    image = response.data.image
    image.save(path_to_save)

    assert os.path.exists(f"{path_to_save}/{image.filename}")

    shutil.rmtree(path_to_save)


def test_url():
    session = StubSession(is_open=True)
    session.http_request = make_check_url_in_request(
        "test_get_rdp_url_root/data/news/v1/images/id?width=100&height=200"
    )

    news.images.Definition("id", width=100, height=200).get_data(session)


def test_extended_params():
    session = StubSession(is_open=True)
    session.http_request = make_check_url_in_request(
        "test_get_rdp_url_root/data/news/v1/images/id?test_param=test_value"
    )

    news.images.Definition("id", extended_params={"test_param": "test_value"}).get_data(
        session
    )
