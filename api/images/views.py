from typing import Optional

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.permissions import HasObjectOwnerPermission, IsAuthenticated

from .models import Image
from .serializers.prediction_response_serializer import PredictionResponseSerializer
from .services.image_processing_service import ImageProcessingService


class PredictionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = PredictionResponseSerializer
    permission_classes = [IsAuthenticated, HasObjectOwnerPermission]
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    lookup_field = "id"
    service: Optional[ImageProcessingService]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.service = ImageProcessingService()

    def create(self, request):
        images = request.FILES
        if not images:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        images = images.values()
        selected_brands = request.data.get("brands", "").split(",")
        results = self.service.process_images(images=images, user=request.user, selected_brands=selected_brands)
        serializer = PredictionResponseSerializer(results, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
