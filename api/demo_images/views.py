from rest_framework import generics
from rest_framework.response import Response


class PredictionsViewSet(generics.GenericAPIView):
    def post(self, request):
        return Response()
