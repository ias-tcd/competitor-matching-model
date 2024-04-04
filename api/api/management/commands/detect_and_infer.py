import logging

from django.core.management.base import BaseCommand
from PIL import Image

from images.services.cropping_service import CroppingService
from ml.models.logo_detection import process
from ml.models.logo_recognition.predict import predict
from ml.models.search.search import search

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Runs the full model flow in one go, outputting the results to the user"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("file")

    def handle(self, *args, **options):
        file = options.get("file")
        logger.info(f"Running full flow for image {file}")
        service = CroppingService()
        image = Image.open(file)
        inferences = process(file)
        for inference in inferences:
            try:
                cropped_image = service.crop(image, inference.bounding_box)
                logger.info(f"Bounding box is {inference.bounding_box}, confidence is {inference.confidence}")
                vector = predict(cropped_image)
                brands = search(vector)
                logger.info(f"Brands detected in order: {brands} with bbox: {inference}")
            except Exception as e:
                logger.error(f"Error in infering brand: {e}, bbox: {inference.bounding_box}")
