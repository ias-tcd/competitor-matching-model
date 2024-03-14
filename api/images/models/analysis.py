from django.db import models

from api.models import BaseModel


class Analysis(BaseModel):
    image = models.ForeignKey("Image", on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, blank=False, null=False)

    class meta:
        app_label = "images"
