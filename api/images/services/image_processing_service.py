# from typing import Optional

from io import BytesIO

from django.db import transaction

# from api.users.models import User
from api.utils.file_storage.image_storage import ImageStorage
from api.utils.make_temp_directory import make_temp_directory
from images.models import Analysis, BoundingBox, Image

from .logo_detection_service import LogoDetectionService


class ImageProcessingService:
    def __init__(self) -> None:
        self.storage = ImageStorage()

    def process_images(self, images, user):
        results = []

        with make_temp_directory() as temp_directory:
            for image in images:
                image_file = image.file.read()
                image_name = image.name
                file_path = temp_directory + "/" + image_name
                with open(file_path, "wb") as file:
                    file.write(image_file)
                detections = LogoDetectionService().detect_in_image(file_path)
                result = self.__save_to_s3(image_name=image_name, image=image_file, detections=detections, user=user)
                results.append(result)
        return results

    # This decorator ensures that the all the create and bulk_create operations are done in one transaction.
    @transaction.atomic
    def __save_to_s3(self, image_name, image, detections, user):
        image_file = BytesIO(image)

        image_url = self.storage.save(image_name, image_file)

        image_obj = Image.objects.create(source=image_url, user=user)

        analysis_obj = Analysis.objects.create(image=image_obj, user=user)

        bounding_boxes = []
        for detection in detections:
            bbox = detection["bbox"]
            bounding_box = BoundingBox(
                image_analysis=analysis_obj,
                x=bbox["x"],
                y=bbox["y"],
                width=bbox["w"],
                height=bbox["h"],
                confidence=detection["confidence"],
                user=user,
            )
            bounding_boxes.append(bounding_box)

        BoundingBox.objects.bulk_create(bounding_boxes)

        return {"image": image_obj, "analysis": analysis_obj}
