from django.db.models import Model
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class HasObjectOwnerPermission(BasePermission):
    def has_object_permission(self, request: Request, view: ViewSet, obj: Model) -> bool:
        return obj.user_id and obj.user_id == request.user.id
