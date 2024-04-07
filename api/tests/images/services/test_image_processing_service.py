from decimal import Decimal
from typing import List, Optional
from unittest.mock import patch
from uuid import UUID

from brands.models import Brand
from tests.mocks.exceptions import raise_exception
from tests.mocks.files import mock_file
from tests.setup.images.logo_detection_inference_helpers import (
    sample_brand_inference,
    sample_inference,
    sample_inferences,
)
from tests.setup.mixins.approximately_equal_mixin import ApproximatelyEqualMixin
from tests.setup.mixins.create_user_mixin import CreateUserMixin
from tests.setup.unit_test_case import UnitTestCase

from images.models import Analysis, BoundingBox, Image
from images.services.image_processing_service import ImageProcessingService
from ml.models.logo_detection import LogoDetectionInference


class TestImageProcessingService(UnitTestCase, CreateUserMixin, ApproximatelyEqualMixin):
    service: ImageProcessingService
    all_brand_ids: List[str | UUID]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = ImageProcessingService()
        cls.all_brand_ids = Brand.objects.values_list("id", flat=True)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_brand_inference())
    @patch("images.services.logo_recognition_service.search", return_value=sample_brand_inference())
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", return_value="myurl.com")
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        response = self.service.process_images([mock_file()], self.user, self.all_brand_ids)
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_called_once()

        self._assert_image_analysis_and_bboxes_exist("myurl.com", response, return_value)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_brand_inference())
    @patch("images.services.logo_recognition_service.search", return_value=sample_brand_inference())
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", return_value="myurl.com")
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", side_effect=raise_exception())
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image_and_s3_failing(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        response = self.service.process_images([mock_file()], self.user, self.all_brand_ids)
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_not_called()

        self._assert_image_analysis_and_bboxes_exist(None, response, return_value)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_brand_inference())
    @patch("images.services.logo_recognition_service.search", return_value=sample_brand_inference())
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", side_effect=raise_exception())
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image_and_s3_failing_on_url_fetch(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        response = self.service.process_images([mock_file()], self.user, self.all_brand_ids)
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_called_once()

        self._assert_image_analysis_and_bboxes_exist(None, response, return_value)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_brand_inference())
    @patch("images.services.logo_recognition_service.search", return_value=sample_brand_inference())
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", side_effect=["my-url.com", "my-url2.com"])
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_multiple_images(self, process_mock, save_mock, url_mock, *args):
        first_return_value = sample_inferences(1)
        second_return_value = sample_inferences(1)
        process_mock.side_effect = [first_return_value, second_return_value]

        response = self.service.process_images([mock_file(), mock_file()], self.user, self.all_brand_ids)
        self.assertEqual(len(response), 2)
        self.assertEqual(process_mock.call_count, 2)
        self.assertEqual(save_mock.call_count, 2)
        self.assertEqual(url_mock.call_count, 2)

        self._assert_image_analysis_and_bboxes_exist("my-url.com", response[0], first_return_value[0])
        self._assert_image_analysis_and_bboxes_exist("my-url2.com", response[1], second_return_value[0])

    @patch("images.services.logo_recognition_service.predict", return_value=sample_brand_inference())
    @patch("images.services.logo_recognition_service.search", return_value=sample_brand_inference())
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", return_value="myurl.com")
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image_and_brand_filtering(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        under_armour_id = str(Brand.objects.get(name="Under Armour").id)
        response = self.service.process_images([mock_file()], self.user, [under_armour_id])
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_called_once()

        bounding_box = self._assert_image_analysis_and_bboxes_exist("myurl.com", response, return_value)
        self.assertFalse(bounding_box.excluded)

    @patch("images.services.logo_recognition_service.predict", return_value=sample_brand_inference())
    @patch("images.services.logo_recognition_service.search", return_value=sample_brand_inference())
    @patch("api.utils.file_storage.image_storage.ImageStorage.unsigned_url", return_value="myurl.com")
    @patch("api.utils.file_storage.image_storage.ImageStorage.save", return_value="")
    @patch("images.services.logo_detection_service.detect_logos")
    def test_process_images_with_one_image_and_brand_filtering_excludes(self, process_mock, save_mock, url_mock, *args):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        new_balance_id = Brand.objects.get(name="New Balance").id
        response = self.service.process_images([mock_file()], self.user, [new_balance_id])
        self.assertEqual(len(response), 1)
        response = response[0]
        process_mock.assert_called_once()
        save_mock.assert_called_once()
        url_mock.assert_called_once()

        bounding_box = self._assert_image_analysis_and_bboxes_exist("myurl.com", response, return_value)
        self.assertTrue(bounding_box.excluded)

    def _assert_image_analysis_and_bboxes_exist(
        self, image_source: Optional[str], response: dict, return_value: LogoDetectionInference
    ) -> BoundingBox:
        image = Image.objects.get(user=self.user, source=image_source)
        self.assertEqual(image.analysis_set.count(), 1)
        analysis = Analysis.objects.get(user=self.user, image=image)
        self.assertEqual(analysis.boundingbox_set.count(), 1)
        bounding_box = analysis.boundingbox_set.first()
        self._assert_response_matches_inference(bounding_box, return_value)
        self.assertEqual(bounding_box.user, self.user)
        self.assertEqual(response["image"], image)
        self.assertEqual(response["analysis"], analysis)
        return bounding_box

    def _assert_response_matches_inference(self, response: BoundingBox, expected: LogoDetectionInference):
        self.assert_approximately_equal(response.confidence, expected.confidence)
        self.assertAlmostEqual(response.confidence, Decimal(expected.confidence), places=5)
        bbox_expected = expected.bounding_box
        self.assert_approximately_equal(response.x, bbox_expected.x)
        self.assert_approximately_equal(response.y, bbox_expected.y)
        self.assert_approximately_equal(response.width, bbox_expected.w)
        self.assert_approximately_equal(response.height, bbox_expected.h)
