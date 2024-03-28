import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.permissions import BasePermission

from api import settings


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        try:
            auth_token = request.headers["Authorization"].split("Bearer ")[1]
            auth_token = jwt.decode(auth_token, key=settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
            expiry = auth_token["exp"]
            token_type = auth_token["token_type"]
            expired = timezone.now().timestamp() >= expiry
            if expired or token_type != "access":  # nosec: B105
                return False
            user = get_user_model().objects.filter(id=auth_token["id"])
            if user := user.first():
                request.user = user
                return True
        except (Exception,):
            # Intentionally passing due to being handled below
            pass
        return False
