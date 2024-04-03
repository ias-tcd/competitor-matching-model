from unittest.mock import patch

from tests.mocks.exceptions import raise_exception
from tests.setup.images.logo_detection_inference_helpers import sample_inference, sample_inferences
from tests.setup.unit_test_case import UnitTestCase

from images.services.logo_detection_service import LogoDetectionService
from ml.models.logo_detection import LogoDetectionInference


class TestLogoDetectionService(UnitTestCase):
    service: LogoDetectionService

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = LogoDetectionService()

    @patch("images.services.logo_detection_service.detect_logos")
    def test_detect_in_image_with_one_response(self, process_mock):
        return_value = sample_inference()
        process_mock.return_value = [return_value]

        response = self.service.detect_in_image("my-image.png")
        process_mock.assert_called_once()
        self.assertEqual(len(response), 1)
        inference = response[0]
        self._assert_dictionary_matches_inference(inference, return_value)

    @patch("images.services.logo_detection_service.detect_logos")
    def test_detect_in_image_with_multiple_responses(self, process_mock):
        return_value = sample_inferences(4)
        process_mock.return_value = return_value

        response = self.service.detect_in_image("my-image.png")
        process_mock.assert_called_once()
        self.assertEqual(len(response), 4)
        for output, expected in zip(response, return_value):
            self._assert_dictionary_matches_inference(output, expected)

    @patch("images.services.logo_detection_service.detect_logos")
    def test_detect_in_image_raises_exception_if_model_does(self, process_mock):
        process_mock.side_effect = raise_exception()
        with self.assertRaises(Exception):
            self.service.detect_in_image("my-image.png")

    def _assert_dictionary_matches_inference(self, response: dict, expected: LogoDetectionInference):
        self.assertEqual(response["confidence"], expected.confidence)
        bbox_response = response["bbox"]
        bbox_expected = expected.bounding_box
        self.assertEqual(bbox_response["x"], bbox_expected.x)
        self.assertEqual(bbox_response["y"], bbox_expected.y)
        self.assertEqual(bbox_response["w"], bbox_expected.w)
        self.assertEqual(bbox_response["h"], bbox_expected.h)
