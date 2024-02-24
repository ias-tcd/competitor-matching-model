from rest_framework import generics
from rest_framework.response import Response


# Create your views here.
class PredictionsViewSet(generics.GenericAPIView):
    def post(self, request):
        return Response(
            data={
                "x1": 30,
                "x2": 78,
                "y1": 79,
                "y2": 89,
                "Confidence": 97.96,
            }
        )
