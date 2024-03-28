from brands.models import Brand
from brands.serializers import BrandSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.settings import api_settings

from api.permissions.is_authenticated import IsAuthenticated


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = "id"
