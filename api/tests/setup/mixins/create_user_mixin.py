from django.test import TestCase

from ..accounts.creation_helpers import create_user


class CreateUserMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = create_user()
