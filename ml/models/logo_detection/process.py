import torch

from .detect import Detector


def process(input_image_path: str):
    model_path = "/src/ml/models/logo_detection"
    source = input_image_path
    detector = Detector(weights=f"{model_path}/logo_detection.pt", source=source)

    with torch.no_grad():
        inferences = detector.detect()

    return inferences
