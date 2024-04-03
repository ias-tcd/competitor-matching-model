from typing import Optional

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(email: Optional[str] = None, password: Optional[str] = None, **kwargs):
    email = email or "test@example.com"
    password = password or "Password123!"
    kwargs.setdefault("first_name", "Test")
    kwargs.setdefault("last_name", "User")
    user = User.objects.create(
        email=email,
        username=email,
        **kwargs,
    )
    user.set_password(password)
    user.save()
    return user
