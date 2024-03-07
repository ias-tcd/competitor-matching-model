from .file_storage import FileStorage


class ImageStorage(FileStorage):
    """This class should be used for saving images to S3 storage

    Usage:
    from django.core.files import File
    storage = ImageStorage()
    storage.save(<file name>, File(<file>.file))
    unsigned_url = storage.unsigned_url(<file name>)
    signed_url = storage.url(<file name>)
    """

    location = "images"
