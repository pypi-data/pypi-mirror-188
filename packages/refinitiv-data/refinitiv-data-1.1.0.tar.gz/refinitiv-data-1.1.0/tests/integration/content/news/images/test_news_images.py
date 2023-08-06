import allure
import pytest
from IPython.core.display import Image

from refinitiv.data.errors import RDError
from refinitiv.data.content import news
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.news.conftest import (
    check_file_is_saved,
)
from tests.integration.helpers import (
    check_response_status,
    get_async_response_from_definition, check_extended_params_were_sent_in_request,
)


@allure.suite("Content object - News Images")
@allure.feature("Content object - News Images")
@allure.severity(allure.severity_level.CRITICAL)
class TestNewsImages:
    @allure.title("Get News Images object and check data")
    @pytest.mark.caseid("51083859")
    @pytest.mark.parametrize(
        "image_id,width,height,expected_filename,expected_size",
        [
            (
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG",
                None,
                None,
                "2022-11-22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER.JPG",
                38174,
            ),
            (
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG",
                100,
                70,
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG.jpeg",
                2241,
            ),
            (
                "tag:reuters__com,2023:newsml_LYNXMPEJ0F0CH:1___tag:reuters__com,2023:binary_LYNXMPEJ0F0CH-VIEWIMAGE",
                None,
                1100,
                "tag_reuters__com,2023_newsml_LYNXMPEJ0F0CH_1___tag_reuters__com,2023_binary_LYNXMPEJ0F0CH-VIEWIMAGE.jpeg",
                90226,
            ),
        ],
    )
    @pytest.mark.smoke
    def test_get_news_images_object_and_check_data(
        self,
        open_platform_session,
        image_id,
        width,
        height,
        expected_filename,
        expected_size,
    ):
        response = news.images.Definition(image_id, width, height).get_data()
        image = response.data.image

        assert isinstance(response.data.raw, dict)
        assert image.size == expected_size, f"Actual size: {image.size}"
        assert image.filename == expected_filename
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)

    @allure.title("Get News Images object and save image")
    @pytest.mark.caseid("C51083860")
    @pytest.mark.parametrize(
        "image_id,width,height,expected_filename",
        [
            (
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG",
                None,
                None,
                "2022-11-22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER.JPG",
            ),
            (
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG",
                100,
                70,
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG.jpeg",
            ),
        ],
    )
    @pytest.mark.smoke
    def test_get_news_images_object_and_save_image(
        self, open_platform_session, image_id, width, height, expected_filename
    ):
        response = news.images.Definition(image_id, width, height).get_data()
        image = response.data.image
        image.save()

        check_file_is_saved(expected_filename)
        assert isinstance(image.show(), Image)

    @allure.title("Get News Images object async and save image")
    @pytest.mark.caseid("C51083861")
    @pytest.mark.parametrize(
        "image_id,path,expected_filename",
        [
            (
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG",
                "./images",
                "2022-11-22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER.JPG",
            )
        ],
    )
    @pytest.mark.smoke
    async def test_get_news_images_object_async_and_save_image(
        self, open_platform_session, image_id, path, expected_filename
    ):
        response = await get_async_response_from_definition(
            news.images.Definition(image_id)
        )
        image = response.data.image
        image.save(path=path)

        check_file_is_saved(expected_filename, path)
        assert isinstance(image.show(), Image)

    @allure.title("Get News Images object with invalid image_id")
    @pytest.mark.caseid("C51083862")
    @pytest.mark.smoke
    def test_get_news_images_object_with_invalid_image_id(self, open_platform_session):
        with pytest.raises(RDError) as error:
            news.images.Definition("INVALID_IMAGE_ID").get_data()

        assert str(error.value) == "Error code 404 | Story not found"

    @allure.title("Get News Images object with extended params and check data")
    @pytest.mark.caseid("C53961917")
    @pytest.mark.parametrize(
        "image_id,width,height,extended_params,expected_filename,expected_size",
        [
            (
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG",
                400,
                200,
                {"width": 100, "height": 70},
                "22T112537Z_1_MQ4_RTRLXPP_2_LYNXPACKAGER__JPG.jpeg",
                2241,
            ),
        ],
    )
    @pytest.mark.smoke
    def test_get_news_images_object_with_extended_params(
        self,
        open_platform_session,
        image_id,
        width,
        height,
        extended_params,
        expected_filename,
        expected_size,
    ):
        response = news.images.Definition(image_id, width, height, extended_params).get_data()
        image = response.data.image

        assert isinstance(response.data.raw, dict)
        assert image.size == expected_size, f"Actual size: {image.size}"
        assert image.filename == expected_filename
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_extended_params_were_sent_in_request(response, extended_params)
