from rest_framework import generics, status
from rest_framework.response import Response

from .services.ImageProcessingService import ImageProcessingService


# Create your views here.
class PredictionsViewSet(generics.GenericAPIView):
    def post(self, request):
        print(request.data)
        images = request.FILES
        if not images:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response (
            data = ImageProcessingService().process_images(images)
        )
        
        
        
        # return Response(
        #     data={
        #         "x1": 30,
        #         "x2": 78,
        #         "y1": 79,
        #         "y2": 89,
        #         "Confidence": 97.96,
        #     }
        # )
