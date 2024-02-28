from LogoDetectionService import LogoDetectionService
from api.api.utils.make_temp_directory import make_temp_directory
class ImageProcessingService:
    def process_images(images: dict):
        detections = {}
        for image in images.keys():
            with make_temp_directory() as tempDirectory:
                filePath = tempDirectory + "/" + image
                # do I also have to write the image to the temporary directory?
                detections.update({image: LogoDetectionService.detectInImage(filePath)})
        
        return detections