from typing import Optional

from api.utils.file_storage.image_storage import ImageStorage
from api.utils.make_temp_directory import make_temp_directory

from .logo_detection_service import LogoDetectionService


class ImageProcessingService:
    def __init__(self) -> None:
        self.storage = ImageStorage()

    def process_images(self, images, user):
        detections = {}

        with make_temp_directory() as temp_directory:
            for image in images:
                image_file = image.file.read()
                image_name = image.name
                file_path = temp_directory + "/" + image_name
                with open(file_path, "wb") as file:
                    file.write(image_file)
                detection = LogoDetectionService().detect_in_image(file_path)
                detections.update({image.name: detection})
                self.__save_to_s3(image_name=image_name, image=image_file, detections=detection)
        return detections

    def __save_to_s3(self, image_name, image, detetctions):
        pass
