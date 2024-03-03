from django.contrib.auth import get_user_model
from django.http.response import HttpResponse as DjangoResponse
from django.utils.timezone import now
from rest_framework.response import Response as DRFResponse

from ...setup.integration_test_case import IntegrationTestCase
from ...setup.mixins.create_user_mixin import CreateUserMixin

User = get_user_model()


class LoginViewSetIT(IntegrationTestCase, CreateUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.login_password = "Password123!"

    def test_valid_login(self):
        response = self._login()
        self.assertEqual(response.status_code, 200)

    def test_login_returns_tokens(self):
        response = self._login()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_login_updates_last_login(self):
        self.assertIsNone(self.user.last_login)
        response = self._login()
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.last_login)
        self.assertLessEqual(self.user.last_login, now())

    def test_login_with_bad_password(self):
        response = self._login(password="NotPassword123!")
        self.assertEqual(response.status_code, 400)

    def test_login_with_bad_email(self):
        response = self._login(email="another.email@example.com")
        self.assertEqual(response.status_code, 401)

    def test_empty_payload(self):
        response = self._login(password=None, email=None)
        self.assertEqual(response.status_code, 401)

    def _login(self, **kwargs) -> DjangoResponse | DRFResponse:
        payload = {
            "email": self.user.email,
            "password": self.login_password,
            **kwargs,
        }
        response = self.public_client.post("/accounts/login/", data=payload, content_type="application/json")
        return response
