import logging

from PIL import Image

from .predict import predict

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    image = "competitor-matching-model/images/adidas"
    image = Image.open(image)
    predictions = predict(image)
    logger.info(predictions)
