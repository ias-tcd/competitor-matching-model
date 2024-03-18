from tests.mocks.files import mock_image
from tests.setup.unit_test_case import UnitTestCase

from images.services.cropping_service import CroppingService
from ml.models.logo_detection import BoundingBox


class CroppingServiceUT(UnitTestCase):
    service: CroppingService

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = CroppingService()

    def test_crop(self):
        image = mock_image(100, 100)
        cropped_image = self.service.crop(image, BoundingBox(0.5, 0.5, 0.4, 0.4))
        size = cropped_image.size
        self.assertEqual(size[0], 40)
        self.assertEqual(size[1], 40)

    def test_crop_with_extended_x_coordinates(self):
        image = mock_image()
        with self.assertRaises(Exception):
            self.service.crop(image, BoundingBox(1.5, 0.5, 0.1, 0.4))

    def test_crop_with_extended_y_coordinates(self):
        image = mock_image()
        with self.assertRaises(Exception):
            self.service.crop(image, BoundingBox(0.5, 1.5, 0.1, 0.4))

    def test_crop_with_extended_width_coordinates(self):
        image = mock_image()
        with self.assertRaises(Exception):
            self.service.crop(image, BoundingBox(0.5, 0.5, 1.1, 0.4))

    def test_crop_with_extended_height_coordinates(self):
        image = mock_image()
        with self.assertRaises(Exception):
            self.service.crop(image, BoundingBox(0.5, 0.5, 0.1, 1.4))

    def test_crop_with_extended_x_plus_width_coordinates(self):
        image = mock_image()
        with self.assertRaises(Exception):
            self.service.crop(image, BoundingBox(0.7, 0.5, 0.65, 0.4))

    def test_crop_with_extended_y_plus_height_coordinates(self):
        image = mock_image()
        with self.assertRaises(Exception):
            self.service.crop(image, BoundingBox(0.5, 0.8, 0.1, 1.3))
