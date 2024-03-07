from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "accounts"

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("register/", views.RegisterViewSet.as_view(), name="register"),
        path(
            "login/",
            include(
                [
                    path("", views.LoginViewSet.as_view(), name="login"),
                    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
                ]
            ),
        ),
    ]
)
