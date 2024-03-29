import json
import logging
import os
import pickle  # nosec
import re
from typing import List, Tuple

from PIL import Image

from images.services.cropping_service import CroppingService

from ..logo_detection.data import BoundingBox
from ..logo_recognition.predict import predict

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def generate_pickles():
    cropping_service = CroppingService()
    mapped_labels = _generate_mapped_labels()
    for company, labels in mapped_labels.items():
        os.makedirs(f"/src/pickles/{company}", exist_ok=True)
        _process_company(company, labels, cropping_service)


def _process_company(company: str, labels: dict[str, List[BoundingBox]], cropping_service: CroppingService):
    company_images = _get_company_images(company)
    for image_name, bounding_boxes in labels.items():
        for bounding_box in bounding_boxes:
            try:
                image_path = next(name for name in company_images if image_name in name)
                image = Image.open(image_path)
                cropped_image = cropping_service.crop(image, bounding_box)
                vector = predict(cropped_image)
                with open(f"/src/pickles/{company}/{image_name}.pkl", "wb") as f:
                    pickle.dump(vector, f)
            except Exception as e:
                logger.error(f"Err: {e}, bounding_box: {bounding_box}")


def _get_company_images(company: str) -> List[str]:
    path = f"/src/images/{company}"
    company_images = os.listdir(path)
    images_split = "training" in company_images
    company_images = [f"{path}/{p}" for p in company_images]
    if images_split:
        company_images += (
            [f"{path}/training/{p}" for p in os.listdir(f"{path}/training")]
            + [f"{path}/test/{p}" for p in os.listdir(f"{path}/test")]
            + [f"{path}/validation/{p}" for p in os.listdir(f"{path}/validation")]
        )
    return company_images


def _generate_mapped_labels() -> dict[str, dict[str, List[BoundingBox]]]:
    classes = _load_classes()
    mapped_labels: dict[str, dict[str, List[BoundingBox]]] = {}

    for label in os.listdir("/src/labels"):
        if not label.endswith(".txt"):
            continue
        image_name = _get_image_name(label)
        bounding_boxes, class_index = _get_bounding_box_and_class(label)
        company = classes[class_index]
        mapped_labels.setdefault(company, {})[image_name] = bounding_boxes

    return mapped_labels


def _load_classes() -> dict:
    """Map the list of categories provided to a map of id -> name"""
    with open("/src/images/notes.json") as f:
        classes = json.load(f)

    categories = classes["categories"]
    return {class_json["id"]: class_json["name"] for class_json in categories}


def _get_image_name(label_name: str) -> str:
    """Remove the leading hash- and trailing .txt from a label file name"""
    return re.sub(r"^[a-zA-Z0-9]+-", "", label_name).split(".txt")[0]


def _get_bounding_box_and_class(label_file_name: str) -> Tuple[List[BoundingBox], int]:
    with open(f"/src/labels/{label_file_name}") as f:
        content = f.read()
    lines = content.split("\n")
    bounding_boxes = []
    class_index = None
    for line in lines:
        if not line:
            continue
        class_index, *coordinates = line.split(" ")
        bounding_boxes.append(BoundingBox(*[float(val) for val in coordinates]))
    return bounding_boxes, int(class_index)
