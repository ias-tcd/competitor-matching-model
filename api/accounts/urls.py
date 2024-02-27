from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "accounts"

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("register/", views.RegisterViewSet.as_view(), name="register"),
        path("login/", views.LoginViewSet.as_view(), name="login"),
    ]
)
