from typing import Optional

from ...setup.integration_test_case import IntegrationTestCase
from ...setup.mixins.create_user_mixin import CreateUserMixin


class RefreshTokenViewSetIT(IntegrationTestCase, CreateUserMixin):
    access_token: Optional[str]
    refresh_token: Optional[str]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._set_tokens()

    def test_refresh_token(self):
        response = self._refresh_token()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["refresh"], self.refresh_token)
        self.assertNotEqual(response.data["access"], self.access_token)

    def test_refresh_token_with_access_token(self):
        response = self._refresh_token(self.access_token)
        self.assertEqual(response.status_code, 400)

    def test_refresh_token_with_shortened_refresh_token(self):
        response = self._refresh_token(self.refresh_token[:-1])
        self.assertEqual(response.status_code, 400)

    def test_refresh_token_with_extended_token(self):
        response = self._refresh_token(self.refresh_token + "c")
        self.assertEqual(response.status_code, 400)

    def test_refreshed_token_allows_future_refreshes(self):
        response = self._refresh_token()
        self.assertEqual(response.status_code, 200)
        self.refresh_token = response.data["refresh"]
        response = self._refresh_token()
        self.assertEqual(response.status_code, 200)

    def test_refreshed_token_allows_authenticated_access(self):
        response = self._refresh_token()
        self.assertEqual(response.status_code, 200)
        self.access_token = response.data["access"]
        # TODO once an endpoint has an auth guard, send a request with auth header to check it works

    def _refresh_token(self, refresh_token: Optional[str] = None):
        refresh_token = refresh_token or self.refresh_token
        return self.public_client.post(
            "/accounts/login/refresh/", data={"refresh": refresh_token}, content_type="application/json"
        )

    @classmethod
    def _set_tokens(cls):
        response = cls.public_client.post(
            "/accounts/login/",
            data={
                "email": cls.user.email,
                "password": "Password123!",
            },
            content_type="application/json",
        )
        cls.access_token = response.data["access"]
        cls.refresh_token = response.data["refresh"]
