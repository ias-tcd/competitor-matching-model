from django.db import models

from api.models import BaseUserOwnedModel


class BoundingBox(BaseUserOwnedModel):
    image_analysis = models.ForeignKey("Analysis", on_delete=models.CASCADE, blank=False, null=False, to_field="id")
    x = models.DecimalField(blank=False, null=False, max_digits=15, decimal_places=7)
    y = models.DecimalField(blank=False, null=False, max_digits=15, decimal_places=7)
    width = models.DecimalField(blank=False, null=False, max_digits=15, decimal_places=7)
    height = models.DecimalField(blank=False, null=False, max_digits=15, decimal_places=7)
    confidence = models.DecimalField(blank=False, null=False, max_digits=15, decimal_places=7)
    brand = models.ForeignKey("brands.Brand", on_delete=models.CASCADE, blank=False, null=True, to_field="id")

    class Meta:
        app_label = "images"
