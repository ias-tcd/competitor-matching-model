from django.db import models

from api.models import BaseModel


class Brand(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=256)
    logo = models.URLField(blank=False, null=False)
    enabled = models.BooleanField(null=False, default=False)

    class Meta:
        app_label = "brands"
