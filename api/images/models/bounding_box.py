from django.db import models

from api.models import BaseModel


class BoundingBox(BaseModel):
    image_analysis = models.ForeignKey("Analysis", blank=False, null=False)
    x = models.DecimalField(blank=False, null=False)
    y = models.DecimalField(blank=False, null=False)
    width = models.DecimalField(blank=False, null=False)
    height = models.DecimalField(blank=False, null=False)
    confidence = models.DecimalField(blank=False, null=False)
    brand = models.ForeignKey("brands.Brand", on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, blank=False, null=False)

    class meta:
        app_label = "images"
