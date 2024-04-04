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
        x=0.5,
        y=0.5,
        w=0.3,
        h=0.4,
    )


def sample_brand_inference():
    return ["under_armour"]
