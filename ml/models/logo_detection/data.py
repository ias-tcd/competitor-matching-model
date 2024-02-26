class BoundingBox:
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class LogoDetectionInference:
    def __init__(self, boundingBox: BoundingBox, confidence: float):
        self.boundingBox = boundingBox
        self.confidence = confidence
