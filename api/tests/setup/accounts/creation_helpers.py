from typing import Optional

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(email: Optional[str] = None, password: Optional[str] = None):
    email = email or "test@example.com"
    password = password or "Password123!"
    user = User.objects.create(
        first_name="Test",
        last_name="User",
        email=email,
        username=email,
    )
    user.set_password(password)
    user.save()
    return user
