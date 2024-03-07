from django.db.models import QuerySet
from rest_framework import filters
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class IsObjectOwnerFilter(filters.BaseFilterBackend):
    """Limit querysets to only objects owned by the logged-in user for all requests"""

    def filter_queryset(self, request: Request, queryset: QuerySet, view: ViewSet) -> QuerySet:
        return queryset.filter(user=request.user)
