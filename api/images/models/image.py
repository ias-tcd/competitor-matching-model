from django.db import models

from api.models import BaseUserOwnedModel


class Image(BaseUserOwnedModel):
    source = models.URLField(blank=False, null=True)

    class Meta:
        app_label = "images"
