from django.contrib.auth import get_user_model

from ...setup.integration_test_case import IntegrationTestCase

User = get_user_model()


class TestRegisterViewSetIT(IntegrationTestCase):
    def test_register(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "test@example.com",
                "password": "Password123!",
                "confirm_password": "Password123!",
            }
        )
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email="test@example.com")
        self.assertEqual(created_user.first_name, "Test")
        self.assertEqual(created_user.last_name, "Name")
        self.assertEqual(created_user.username, "test@example.com")

    def test_hashes_password(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "test@example.com",
                "password": "Password123!",
                "confirm_password": "Password123!",
            }
        )
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.get(email="test@example.com")
        self.assertNotEqual(created_user.password, "Password123!")

    def test_password_matching_confirm_validation(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "test@example.com",
                "password": "Password123!",
                "confirm_password": "NotPassword123!",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_email_validation(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "email",
                "password": "Password123!",
                "confirm_password": "Password123!",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="email").exists())

    def test_minimum_length_password_validation(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "test@example.com",
                "password": "Pass12!",
                "confirm_password": "Pass12!",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_common_password_validation(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "test@example.com",
                "password": "Password123",
                "confirm_password": "Password123",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def test_numeric_password_validation(self):
        response = self._register(
            {
                "first_name": "Test",
                "last_name": "Name",
                "email": "test@example.com",
                "password": "68495023",
                "confirm_password": "68495023",
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    def _register(self, payload: dict):
        response = self.public_client.post("/accounts/register/", data=payload, content_type="application/json")
        return response
