import os
import tempfile

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
        for image in files:
            filename = image.name
            filepath = os.path.join(temp_dir, filename)

            with open(filepath, "wb") as f:
                for c in image.chunks():
                    f.write(c)

            bbox, confidence = get_result(filepath)
            responses.append(filename)
        print(responses)
        return Response()
