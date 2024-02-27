from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.models import BaseModel


class User(AbstractUser, BaseModel):
    first_name = models.CharField(blank=False, null=False, max_length=256)
    last_name = models.CharField(blank=False, null=False, max_length=256)
    email = models.EmailField(_("email address"), unique=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        app_label = "accounts"
