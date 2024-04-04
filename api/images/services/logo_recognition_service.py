from brands.models import Brand

from ml.models.logo_recognition.predict import predict
from ml.models.search.search import search

from .cropping_service import CroppingService


class LogoRecognitionService:
    def __init__(self) -> None:
        self.cropper = CroppingService()

    def predict_and_search(self, inferences, image_file):
        results = []
        for inference in inferences:
            cropped_image = self.cropper.crop(image_file, inference.bounding_box)
            vector = predict(cropped_image)
            brands = search(vector)
            if brands is not None and brands[0]:
                name = brands[0]
                first_brand = Brand.objects.filter(name__icontains=name.replace("_", " ")).first()

            else:
                first_brand = None

            bbox = {
                "x": inference.bounding_box.x,
                "y": inference.bounding_box.y,
                "w": inference.bounding_box.w,
                "h": inference.bounding_box.h,
                "brand": first_brand,
            }
            detection = {"bbox": bbox, "confidence": inference.confidence}
            results.append(detection)
        return results
