import torch
from detect import Detector  # Importing the Detector class from detect.py

def process(input_image_path):

    source = input_image_path
    detector = Detector(weights='logo_detection.pt', source=source)

    with torch.no_grad():
        inferences = detector.detect()

    return inferences
