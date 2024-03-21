import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def mock_file(**kwargs) -> SimpleUploadedFile:
    """
    Creates a file suitable for using in unit tests where the file is being passed as arguments to functions
    It is not suitable for use in integration tests where it is being passed as part of a request body
    """
    kwargs.setdefault("name", "my document")
    kwargs.setdefault("content", b"this is my document")
    return SimpleUploadedFile(**kwargs)


def mock_request_file():
    """
    Creates a file object suitable for using in integration tests where it is being passed as part of a request body
    """
    image = Image.new(mode="RGB", size=(100, 100))
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(temp_file)
    temp_file.seek(0)
    return temp_file
