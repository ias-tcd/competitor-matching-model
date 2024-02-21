from django.urls import path

from . import views

urlpatterns = [
    path("predictions/", views.PredictionsViewSet.as_view(), name="predictions"),
]
