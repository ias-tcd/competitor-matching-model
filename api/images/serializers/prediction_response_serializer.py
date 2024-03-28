from rest_framework import serializers

from .analysis_serializer import AnalysisSerializer
from .image_serializer import ImageSerializer


class PredictionResponseSerializer(serializers.Serializer):
    image = ImageSerializer()
    analysis = AnalysisSerializer()
