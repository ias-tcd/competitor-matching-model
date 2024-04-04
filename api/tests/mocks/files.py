import tempfile
from decimal import Decimal
from typing import Optional, Union

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

Number = Union[Decimal, float, int]


def mock_file() -> SimpleUploadedFile:
    """
    Creates a file suitable for using in unit tests where the file is being passed as arguments to functions
    It is not suitable for use in integration tests where it is being passed as part of a request body
    """
    image = mock_image(600, 600)
    image_file = ContentFile(b"")
    image.save(image_file, "PNG")
    image_file.seek(0)
    return SimpleUploadedFile("image.png", image_file.read(), content_type="image/png")


def mock_request_file():
    """
    Creates a file object suitable for using in integration tests where it is being passed as part of a request body
    """
    image = mock_image(100, 100)
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(temp_file)
    temp_file.seek(0)
    return temp_file


def mock_image(x: Optional[Number] = None, y: Optional[Number] = None) -> Image:
    x = x or 255
    y = y or 255
    return Image.new(mode="RGB", size=(x, y))
