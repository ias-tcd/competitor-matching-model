import os
import tempfile

from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.response import Response

from ml_models.models.logo_detection import get_result

# from logo_detection import get_result as get_result_top_level


class PredictionsViewSet(generics.GenericAPIView):
    def post(self, request):
        print(request.data)
        print(request.FILES)
        files = request.FILES.values()
        if not files:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        temp_dir = tempfile.mkdtemp()
        responses = []
        output = []
        for image in files:
            filename = image.name
            filepath = os.path.join(temp_dir, filename)

            with open(filepath, "wb") as f:
                for c in image.chunks():
                    f.write(c)

            output_path = get_result(filepath)
            with open(output_path, "rb") as f:
                output_image = f.read()
            # print(f'Have bbox: {bbox} and have "confidence": {confidence}')
            responses.append(output_path)
            output.append(output_image)
        print(responses)
        return Response(
            data={
                "images": responses,
            }
        )


class PredictionsListViewSet(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        image_path = request.GET.get("image_path")
        return FileResponse(open(image_path, "rb"))
        # with open(image_path, 'rb') as f:
        #     return FileResponse(f)
        # return Response()
