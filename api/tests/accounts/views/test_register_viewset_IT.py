from django.contrib.auth import get_user_model
from django.http.response import HttpResponse as DjangoResponse
from rest_framework.response import Response as DRFResponse

from ...setup.integration_test_case import IntegrationTestCase

User = get_user_model()


class TestRegisterViewSetIT(IntegrationTestCase):
    def test_register(self):
        response = self._register()
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email="test@example.com")
        self.assertEqual(created_user.first_name, "Test")
        self.assertEqual(created_user.last_name, "Name")
        self.assertEqual(created_user.username, "test@example.com")

    def test_hashes_password(self):
        response = self._register()
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email="test@example.com")
        self.assertNotEqual(created_user.password, "Password123!")

    def test_password_matching_confirm_validation(self):
        response = self._register(confirm_password="NotPassword123!")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_email_validation(self):
        response = self._register(email="email")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="email").exists())

    def test_minimum_length_password_validation(self):
        response = self._register(
            password="Pass12!",
            confirm_password="Pass12!",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_common_password_validation(self):
        response = self._register(
            password="Password123",
            confirm_password="Password123",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_numeric_password_validation(self):
        response = self._register(
            password="68495023",
            confirm_password="68495023",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_removal_of_required_fields(self):
        response = self._register(
            first_name=None,
            last_name=None,
            email=None,
            password=None,
            confirm_password=None,
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(first_name="Test").exists())

    def _register(self, **kwargs) -> DjangoResponse | DRFResponse:
        payload = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            **kwargs,
        }
        response = self.public_client.post("/accounts/register/", data=payload, content_type="application/json")
        return response
