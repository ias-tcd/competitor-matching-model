from rest_framework import serializers

from images.models import Analysis

from .bounding_box_serializer import BoundingBoxSerializer


class AnalysisSerializer(serializers.ModelSerializer):
    bounding_boxes = BoundingBoxSerializer(many=True, read_only=True)
    detections = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = ["id", "image", "user", "bounding_boxes", "detections"]

    def get_detections(self, obj):
        detections = {}
        for bounding_box in obj.boundingbox_set.filter(excluded=False):
            image_name = bounding_box.image_analysis.image.source
            if image_name not in detections:
                detections[image_name] = []
            detections[image_name].append(
                {
                    "bbox": {
                        "x": bounding_box.x,
                        "y": bounding_box.y,
                        "width": bounding_box.width,
                        "height": bounding_box.height,
                        "brand": bounding_box.brand.name if bounding_box.brand else None,
                    },
                    "confidence": float(bounding_box.confidence),
                }
            )
        return detections
