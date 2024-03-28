from rest_framework import serializers

from api.images.models import BoundingBox


class BoundingBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundingBox
        fields = ["id", "image_analysis", "x", "y", "width", "height", "confidence", "brand", "user"]
