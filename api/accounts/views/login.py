from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import LoginSerializer


class LoginViewSet(TokenObtainPairView):
    serializer_class = LoginSerializer
