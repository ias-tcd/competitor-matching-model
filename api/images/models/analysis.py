from django.db import models

from api.models import BaseUserOwnedModel


class Analysis(BaseUserOwnedModel):
    image = models.ForeignKey("Image", on_delete=models.CASCADE, blank=False, null=False, to_field="id")

    class Meta:
        app_label = "images"
