from django.contrib.auth.models import AbstractUser
from django.test import TestCase

from ..accounts.creation_helpers import create_user


class CreateUserMixin(TestCase):
    user: AbstractUser

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = create_user()
