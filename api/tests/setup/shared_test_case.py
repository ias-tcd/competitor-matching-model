from accounts.models import User
from django.test import TestCase


class SharedTestCase(TestCase):
    user: User

    @classmethod
    def setUpTestData(cls):
        """Initialise any test data here, such as users"""
        super().setUpTestData()
