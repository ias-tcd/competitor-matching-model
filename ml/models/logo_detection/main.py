import logging

from .process import process

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    input_image_path = ""
    inferences = process(input_image_path)

    for inference in inferences:
        logger.info(f"x: {inference.bounding_box.x}")
        logger.info(f"y: {inference.bounding_box.y}")
        logger.info(f"Width: {inference.bounding_box.w}")
        logger.info(f"Height: {inference.bounding_box.h}")
        logger.info(f"Confidence score: {inference.confidence}\n")


if __name__ == "__main__":
    main()
