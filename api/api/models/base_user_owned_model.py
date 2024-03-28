from django.db import models

from .. import settings
from .base_model import BaseModel


class BaseUserOwnedModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field="id")

    class Meta:
        abstract = True
