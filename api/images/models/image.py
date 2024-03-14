from django.db import models

from api.models import BaseModel


class Image(BaseModel):
    source = models.URLField(blank=False, null=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, blank=False, null=False)

    class meta:
        app_label = "images"
