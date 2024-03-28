from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        users = get_user_model()
        username = username or kwargs.get(users.USERNAME_FIELD)
        try:
            user = users.objects.get(email=username)
        except users.DoesNotExist:
            return None
        return user if user.check_password(password) else None
