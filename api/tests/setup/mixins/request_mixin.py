from unittest.mock import MagicMock

import jwt
from django.test import Client
from django.utils import timezone
from tests.setup.integration_test_case import IntegrationTestCase


class RequestMixin(IntegrationTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._mock_jwt_decode()

    @classmethod
    def _mock_jwt_decode(cls):
        now = timezone.now().timestamp()
        jwt_decode = MagicMock(return_value={"token_type": "access", "exp": now + 1000, "id": cls.user.id})
        jwt.decode = jwt_decode
        cls.jwt_decode = jwt_decode

    @staticmethod
    def get(client: Client, path: str, *args, **kwargs):
        kwargs.setdefault("headers", {"Authorization": "Bearer 123"})
        return client.get(path, *args, **kwargs)

    @staticmethod
    def post(client: Client, path: str, *args, **kwargs):
        kwargs.setdefault("headers", {"Authorization": "Bearer 123"})
        return client.post(path, *args, **kwargs)

    @staticmethod
    def put(client: Client, path: str, *args, **kwargs):
        kwargs.setdefault("headers", {"Authorization": "Bearer 123"})
        return client.put(path, *args, **kwargs)

    @staticmethod
    def delete(client: Client, path: str, *args, **kwargs):
        kwargs.setdefault("headers", {"Authorization": "Bearer 123"})
        return client.delete(path, *args, **kwargs)
