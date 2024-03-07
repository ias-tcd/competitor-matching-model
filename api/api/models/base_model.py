import uuid

from django.db import models
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class BaseModel(models.Model):
    pkid = models.BigAutoField(primary_key=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = AutoCreatedField()
    updated_at = AutoLastModifiedField()

    class Meta:
        abstract = True
        ordering = ("-pkid",)
