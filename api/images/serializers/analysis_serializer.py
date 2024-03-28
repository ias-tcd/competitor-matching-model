from rest_framework import serializers

from images.models.analysis import Analysis

from .bounding_box_serializer import BoundingBoxSerializer


class AnalysisSerializer(serializers.ModelSerializer):
    bounding_boxes = BoundingBoxSerializer(many=True, read_only=True)

    class Meta:
        model = Analysis
        fields = ["id", "image", "user", "bounding_boxes"]
