from brands.serializers.brand import BrandSerializer
from rest_framework import serializers

from images.models.bounding_box import BoundingBox


class BoundingBoxSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = BoundingBox
        fields = ["id", "image_analysis", "x", "y", "width", "height", "confidence", "brand", "user"]
