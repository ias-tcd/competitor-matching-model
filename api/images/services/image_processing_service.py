from api.utils.make_temp_directory import make_temp_directory

from .logo_detection_service import logo_detection_service


class image_processing_service:
    def process_images(self, images):
        detections = {}

        with make_temp_directory() as temp_directory:
            for image in images:
                file_path = temp_directory + "/" + image.name
                with open(file_path, "wb") as file:
                    file.write(image.file.read())
                detections.update({image.name: logo_detection_service().detect_in_image(file_path)})
        return detections
