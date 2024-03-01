from ml.models.logo_detection.process import process as detect_logos

# from rest_framework import serializers


class logo_detection_service:
    def detect_in_image(self, image_path):
        inference_results = []
        inferences = detect_logos(image_path)  # List LogoDetectionInference objects (ml.models.logo_detection.data)
        for inference in inferences:
            bbox = {
                "x": inference.bounding_box.x,
                "y": inference.bounding_box.y,
                "w": inference.bounding_box.w,
                "h": inference.bounding_box.h,
            }
            detection = {"bbox": bbox, "confidence": inference.confidence}
            inference_results.append(detection)
        return inference_results
