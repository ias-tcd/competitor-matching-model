from typing import Tuple

from PIL import Image
from tensorflow import Tensor

from ml.models.logo_detection import BoundingBox


class CroppingService:
    def crop(self, image: Image, bounding_box: BoundingBox) -> Image:
        """Takes an input image and coordinates and creates and returns a new image cropped by the coordinates"""
        width, height = image.size
        cropped_x, cropped_y, cropped_width, cropped_height = self._get_coordinates_from_bounding_box(
            bounding_box, width, height
        )
        cropped_image = image.crop((cropped_x, cropped_y, cropped_x + cropped_width, cropped_y + cropped_height))
        return cropped_image

    def _get_coordinates_from_bounding_box(
        self, bounding_box: BoundingBox, pixel_width: float, pixel_height: float
    ) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
        x, y, width, height = bounding_box.x, bounding_box.y, bounding_box.w, bounding_box.h
        x -= width / 2
        y -= height / 2
        width *= pixel_width
        height *= pixel_height
        x *= pixel_width
        y *= pixel_height
        self._validate_coordinates(x, y, width, height, pixel_width, pixel_height)
        return x, y, width, height

    @staticmethod
    def _validate_coordinates(
        x: Tensor, y: Tensor, width: Tensor, height: Tensor, pixel_width: float, pixel_height: float
    ):
        if any(n < 0 for n in [x, y, width, height]):
            raise Exception("Coordinates cannot be less than 0!")
        if any(n > pixel_width for n in [x, width]) or any(n > pixel_height for n in [y, height]):
            raise Exception("Coordinates must not exceed bounds of original image!")
        if x + width > pixel_width or y + height > pixel_height:
            raise Exception("Cropped coordinates must not exceed original image bounds!")
