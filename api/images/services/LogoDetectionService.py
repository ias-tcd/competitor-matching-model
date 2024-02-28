from ml.models.logo_detection.process import process as detectLogos

# from rest_framework import serializers


class LogoDetectionService:
    def detect_in_image(self, imagePath):
        inference_results = []
        inferences = detectLogos(imagePath)  # List LogoDetectionInference objects (ml.models.logo_detection.data)
        for inference in inferences:
            bbox = {
                "x": inference.bounding_box.x,
                "y": inference.bounding_box.y,
                "w": inference.bounding_box.w,
                "h": inference.bounding_box.h,
            }
            detection = {"bbox": bbox, "confifence": inference.confidence}
            inference_results.append(detection)
        return inference_results
