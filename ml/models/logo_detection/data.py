class BoundingBox:
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class LogoDetectionInference:
    def __init__(self, bounding_box: BoundingBox, confidence: float, overlap: bool = False):
        self.bounding_box = bounding_box
        self.confidence = confidence
        self.overlap = overlap
