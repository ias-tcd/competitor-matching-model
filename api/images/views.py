from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.permissions import HasObjectOwnerPermission, IsAuthenticated

from .models import Image
from .serializers.prediction_response_serializer import PredictionResponseSerializer
from .services.image_processing_service import ImageProcessingService


# Create your views here.
class PredictionsViewSet(generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = PredictionResponseSerializer
    permission_classes = [IsAuthenticated, HasObjectOwnerPermission]
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    lookup_field = "id"

    def create(self, request):
        images = request.FILES
        if not images:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        images = images.values()
        results = ImageProcessingService().process_images(images=images, user=request.user)
        serializer = PredictionResponseSerializer(results, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
