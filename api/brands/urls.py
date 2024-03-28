from rest_framework.routers import DefaultRouter

from . import views

app_name = "brands"

router = DefaultRouter()

router.register(r"brands", views.BrandViewSet, basename="brands")

urlpatterns = router.urls
