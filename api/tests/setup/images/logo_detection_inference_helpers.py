import random
from typing import Optional

from ml.models.logo_detection import BoundingBox, LogoDetectionInference


def sample_inferences(count: int = 1):
    return [sample_inference() for _ in range(count)]


def sample_inference(bounding_box: Optional[BoundingBox] = None):
    bounding_box = bounding_box or sample_bbox()
    return LogoDetectionInference(
        bounding_box=bounding_box,
        confidence=random.random(),
    )


def sample_bbox():
    return BoundingBox(
        x=random.random(),
        y=random.random(),
        w=random.random(),
        h=random.random(),
    )


def sample_brand_inference():
    return ["under_armour"]
