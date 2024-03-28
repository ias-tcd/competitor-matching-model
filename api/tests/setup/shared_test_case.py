from django.test import TestCase


class SharedTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Initialise any test data here, such as users"""
        super().setUpTestData()
