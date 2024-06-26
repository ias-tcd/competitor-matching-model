from rest_framework.routers import DefaultRouter

from . import views

app_name = "images"

router = DefaultRouter()

router.register(r"predictions", views.PredictionsViewSet, basename="predictions")

urlpatterns = router.urls

# urlpatterns.extend([path("predictions/", views.PredictionsViewSet.as_view(), name="Predictions")])
