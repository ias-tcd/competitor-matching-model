from typing import Optional
from unittest.mock import patch
from uuid import UUID

from django.test import Client
from django.urls import reverse
from tests.mocks.exceptions import raise_exception
from tests.mocks.files import mock_request_file
from tests.setup.images.logo_detection_inference_helpers import (  # sample_brand_inference,
    sample_inference,
    sample_inferences,
)
from tests.setup.mixins.approximately_equal_mixin import ApproximatelyEqualMixin
from tests.setup.mixins.create_user_mixin import CreateUserMixin
from tests.setup.mixins.request_mixin import RequestMixin

from ml.models.logo_detection import LogoDetectionInference


class TestPredictionViewSet(RequestMixin, CreateUserMixin, ApproximatelyEqualMixin):
    def test_list_blocks_non_authenticated_user(self):
        response = self.public_client.get(path=reverse("images:predictions-list"))
        self.assertEqual(response.status_code, 403)

    def test_allows_authenticated_user_on_list(self):
        client = self.login(self.user)
        response = self.get(client, path=reverse("images:predictions-list"))
        self.assertEqual(response.status_code, 200)

    def test_gives_400_when_no_images_passed(self):
        client = self.login(self.user)
        self._predict(client, None, 400)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_inference())
    @patch("images.services.logo_recognition_service.search", return_value=None)
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", return_value="myurl.com")
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        client = self.login(self.user)
        response = self._predict(client, {"file": mock_request_file()}).json()
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_called_once()

        self._assert_response_matches_expected(response, "myurl.com", return_value)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_inference())
    @patch("images.services.logo_recognition_service.search", return_value=None)
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", return_value="myurl.com")
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", side_effect=raise_exception())
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image_and_s3_failing(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        client = self.login(self.user)
        response = self._predict(client, {"file": mock_request_file()}).json()
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_not_called()

        self._assert_response_matches_expected(response, None, return_value)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_inference())
    @patch("images.services.logo_recognition_service.search", return_value=None)
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", side_effect=raise_exception())
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image_and_s3_failing_on_url_fetch(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        client = self.login(self.user)
        response = self._predict(client, {"file": mock_request_file()}).json()
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_called_once()

        self._assert_response_matches_expected(response, None, return_value)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_inference())
    @patch("images.services.logo_recognition_service.search", return_value=None)
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", side_effect=["my-url.com", "my-url2.com"])
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_multiple_images(self, process_mock, save_mock, url_mock, *args):
        first_return_value = sample_inferences(1)
        second_return_value = sample_inferences(1)
        process_mock.side_effect = [first_return_value, second_return_value]

        client = self.login(self.user)
        response = self._predict(client, {"file": mock_request_file(), "file2": mock_request_file()}).json()
        self.assertEqual(len(response), 2)
        self.assertEqual(process_mock.call_count, 2)
        self.assertEqual(save_mock.call_count, 2)
        self.assertEqual(url_mock.call_count, 2)

        self._assert_response_matches_expected(response[0], "my-url.com", first_return_value[0])
        self._assert_response_matches_expected(response[1], "my-url2.com", second_return_value[0])

    def _predict(self, client: Client, files: Optional[dict], status_code: Optional[int] = None):
        status_code = status_code or 200
        response = self.post(client, path=reverse("images:predictions-list"), data=files)
        self.assertEqual(response.status_code, status_code)
        return response

    def _assert_response_matches_expected(self, response: dict, url: Optional[str], expected: LogoDetectionInference):
        self.assertFalse("pkid" in response)
        self._assert_image_serialises(response["image"], url)
        self._assert_analysis_serialises(response["analysis"], response["image"]["id"], url, expected)

    def _assert_analysis_serialises(
        self, analysis: dict, image_id: str | UUID, url: Optional[str], expected: LogoDetectionInference
    ):
        self.assertFalse("pkid" in analysis)
        self._assert_string_is_uuid(analysis["id"])
        self.assertEqual(analysis["image"], image_id)
        self.assertEqual(analysis["user"], str(self.user.id))
        self._assert_detections_serialise(analysis["detections"], url, expected)

    def _assert_detections_serialise(self, detections: dict, url: Optional[str], expected: LogoDetectionInference):
        url = url or "null"
        detection = detections[url][0]
        self.assert_approximately_equal(detection["confidence"], expected.confidence)
        bbox_json = detection["bbox"]
        bbox_expected = expected.bounding_box
        self.assert_approximately_equal(bbox_json["x"], bbox_expected.x)
        self.assert_approximately_equal(bbox_json["y"], bbox_expected.y)
        self.assert_approximately_equal(bbox_json["width"], bbox_expected.w)
        self.assert_approximately_equal(bbox_json["height"], bbox_expected.h)

    def _assert_image_serialises(self, image: dict, url: Optional[str]):
        self.assertFalse("pkid" in image)
        self.assertEqual(image["source"], url)
        self.assertEqual(image["user"], str(self.user.id))
        self._assert_string_is_uuid(image["id"])

    def _assert_string_is_uuid(self, input_string: str):
        uuid_regex = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
        self.assertRegex(input_string, uuid_regex)
