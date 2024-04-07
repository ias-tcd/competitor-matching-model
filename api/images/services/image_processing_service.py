import logging
from io import BytesIO
from uuid import uuid4

from django.db import transaction
from PIL import Image as PILImage

from api.utils.file_storage.image_storage import ImageStorage
from api.utils.make_temp_directory import make_temp_directory
from images.models import Analysis, BoundingBox, Image

from .logo_detection_service import LogoDetectionService
from .logo_recognition_service import LogoRecognitionService

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ImageProcessingService:
    def __init__(self) -> None:
        self.storage = ImageStorage()
        self.logo_detection = LogoDetectionService()
        self.logo_recognition = LogoRecognitionService()

    def process_images(self, images, user, selectedBrands):
        results = []

        with make_temp_directory() as temp_directory:
            for image in images:
                image_file = image.file.read()
                image_name = image.name
                file_path = temp_directory + "/" + image_name
                with open(file_path, "wb") as file:
                    file.write(image_file)
                # detections = self.logo_detection.detect_in_image(file_path)  # Juts bboxes and confidence
                detection_inferences = self.logo_detection.detect_for_recognition(file_path)
                recognitions = self.logo_recognition.predict_and_search(
                    detection_inferences, PILImage.open(file_path)
                )  # Brands
                result = self.__save_to_s3(
                    image_name=image_name,
                    image=image_file,
                    recognitions=recognitions,
                    user=user,
                    selectedBrands=selectedBrands,
                )
                results.append(result)
        return results

    # This decorator ensures that the all the create and bulk_create operations are done in one transaction.
    @transaction.atomic
    def __save_to_s3(self, image_name, image, recognitions, user, selectedBrands):
        image_file = BytesIO(image)
        image_obj = Image(user=user)

        try:
            file_name = f"{user.id}/{uuid4()}_{image_name}"
            self.storage.save(file_name, image_file)
            image_url = self.storage.unsigned_url(file_name)
            image_obj.source = image_url
        except Exception as e:
            logger.error(f"[IMAGES] Error in saving to S3: {e} for user {user.id}")
        image_obj.save()

        analysis_obj = Analysis.objects.create(image=image_obj, user=user)

        bounding_boxes = []
        for recognition in recognitions:
            bbox = recognition["bbox"]

            if bbox["brand"] not in selectedBrands:
                bounding_box = BoundingBox(
                    image_analysis=analysis_obj,
                    x=bbox["x"],
                    y=bbox["y"],
                    width=bbox["w"],
                    height=bbox["h"],
                    confidence=recognition["confidence"],
                    brand=bbox["brand"],
                    user=user,
                    excluded=True,
                )
            else:
                bounding_box = BoundingBox(
                    image_analysis=analysis_obj,
                    x=bbox["x"],
                    y=bbox["y"],
                    width=bbox["w"],
                    height=bbox["h"],
                    confidence=recognition["confidence"],
                    brand=bbox["brand"],
                    user=user,
                    excluded=False,
                )

            bounding_boxes.append(bounding_box)

        BoundingBox.objects.bulk_create(bounding_boxes)

        return {"image": image_obj, "analysis": analysis_obj}
