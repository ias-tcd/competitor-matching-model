import logging
import os
import re

from django.core.management.base import BaseCommand
from PIL import Image

from images.services.cropping_service import CroppingService
from ml.models.logo_detection import process
from ml.models.logo_recognition.predict import predict
from ml.models.search.search import search_and_distances

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Runs the full model flow in one go, outputting the results to the user"

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        files = [file for file in os.listdir(".") if re.search(r"(jpg|png|jpeg)$", file)]
        outputs = []
        service = CroppingService()
        for file in files:
            image = Image.open(file)
            inferences = process(file)
            nested_output = []
            for i, inference in enumerate(inferences):
                try:
                    cropped_image = service.crop(image, inference.bounding_box)
                    logger.info(f"Bounding box is {inference.bounding_box}, confidence is {inference.confidence}")
                    vector = predict(cropped_image)
                    brands, distances = search_and_distances(vector)
                    logger.info(f"Brands detected in order: {brands} with bbox: {inference}")
                    nested_output.append(f"{file} {i}: brands: {brands}, distances: {distances}")
                except Exception as e:
                    logger.error(f"Error in infering brand: {e}, bbox: {inference.bounding_box}")
            outputs.append("\n".join(nested_output))

        os.makedirs("runs", exist_ok=True)
        count = len(os.listdir("runs"))
        with open(f"runs/run{count}.txt", "w") as file:
            file.write("\n".join(outputs))
