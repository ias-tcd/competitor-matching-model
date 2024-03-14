import unittest

from images.services.image_processing_service import ImageProcessingService


class TestImageProcessingService(unittest.TestCase):
    def test_process_images(self):
        # Create instance of ImageProcessingService
        image_processing_service = ImageProcessingService()

        # Mock input images
        class MockImage:
            def __init__(self, name, file_content):
                self.name = name
                self.file_content = file_content

            @property
            def file(self):
                return self

            def read(self):
                return self.file_content

        images = [
            MockImage("image1.jpg", b"mock_image_data_1"),
            MockImage("image2.jpg", b"mock_image_data_2"),
        ]

        # Call process_images method
        detections = image_processing_service.process_images(images)

        # Assertions
        self.assertEqual(len(detections), 2)
        self.assertIn("image1.jpg", detections)
        self.assertIn("image2.jpg", detections)


if __name__ == "__main__":
    unittest.main()
