from api.utils.make_temp_directory import make_temp_directory

from .LogoDetectionService import LogoDetectionService


class ImageProcessingService:
    def process_images(self, images):
        detections = {}

        with make_temp_directory() as temp_directory:
            for image in images:
                file_path = temp_directory + "/" + image.name
                with open(file_path, "wb") as file:
                    file.write(image.file.read())
                detections.update({image.name: LogoDetectionService().detect_in_image(file_path)})
        return detections
