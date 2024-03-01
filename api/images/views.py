from rest_framework import generics, status
from rest_framework.response import Response

from .services.ImageProcessingService import ImageProcessingService


# Create your views here.
class PredictionsViewSet(generics.GenericAPIView):
    def post(self, request):
        images = request.FILES
        if not images:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        images = images.values()
        return Response(data=ImageProcessingService().process_images(images))


"""
EVA PREVIOUS CODE - does not work lol
import os
import tempfile

from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.response import Response

from .services.ImageProcessingService import ImageProcessingService


# Create your views here.
class PredictionsViewSet(generics.GenericAPIView):
    def post(self, request):
        print(request.data)
        images = request.FILES.values()
        if not images:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        temp_dir = tempfile.mkdtemp()
        responses = []
        output = []
        for image in images:
            filename = image.name
            filepath = os.path.join(temp_dir, filename)

            with open(filepath, "wb") as f:
                for c in image.chunks():
                    f.write(c)

            output_path = ImageProcessingService(filepath)
            with open(output_path, "rb") as f:
                output_image = f.read()
            responses.append(output_path)
            output.append(output_image)
        print(responses)
        return Response(
            data={
                "images": responses,
            }
        )

"""
