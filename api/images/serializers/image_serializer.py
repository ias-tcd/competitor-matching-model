from rest_framework import serializers

from api.images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "source", "user"]
