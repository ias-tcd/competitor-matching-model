from typing import Optional

from django.test.client import Client

from .shared_test_case import SharedTestCase


class IntegrationTestCase(SharedTestCase):
    public_client: Client

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.public_client = Client()

    @classmethod
    def login(cls, user, password: Optional[str] = None) -> Client:
        if not password:
            password = "Password123!"
        client = Client()
        client.login(username=user.username, password=password)
        return client
