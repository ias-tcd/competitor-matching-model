# from typing import Optional

from django.db import transaction

from api.images.models import Analysis, BoundingBox, Image

# from api.users.models import User
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
                self.__save_to_s3(image_name=image_name, image=image_file, detections=detection, user=user)
        return detections

    # This decorator ensures that the entire block of code is executed as a single transaction.
    @transaction.atomic
    def __save_to_s3(self, image_name, image, detections, user):
        image_url = self.storage.save(image_name, image)

        image_object = Image.objects.create(source=image_url, user=user)

        analysis_object = Analysis.objects.create(image=image_object, user=user)

        bounding_boxes = []
        for detection in detections:
            bbox = detection["bbox"]
            bounding_box = BoundingBox(
                image_analysis=analysis_object,
                x=bbox["x"],
                y=bbox["y"],
                width=bbox["w"],
                height=bbox["h"],
                confidence=detection["confidence"],
                user=user,
            )
            bounding_boxes.append(bounding_box)

        BoundingBox.objects.bulk_create(bounding_boxes)
