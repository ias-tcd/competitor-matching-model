from dataclasses import dataclass

from tensorflow import Tensor


@dataclass
class BoundingBox:
    x: Tensor | float
    y: Tensor | float
    w: Tensor | float
    h: Tensor | float


@dataclass
class LogoDetectionInference:
    bounding_box: BoundingBox
    confidence: float
