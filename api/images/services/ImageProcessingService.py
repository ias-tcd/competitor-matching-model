from api.utils.make_temp_directory import make_temp_directory

from .LogoDetectionService import LogoDetectionService


class ImageProcessingService:
    def process_images(self, images: dict):
        detections = {}
        with make_temp_directory() as tempDirectory:
            for image in images.keys():
                file_path = tempDirectory + "/" + image
                with open(file_path, "rb") as file:
                    file.write(image.file.read())
                detections.update({image: LogoDetectionService().detect_in_image(file_path)})
        return detections
