from storages.backends.s3 import S3Storage

from ... import settings


class FileStorage(S3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def unsigned_url(self, name, parameters=None, expire=None, http_method=None) -> str:
        """
        Returns the unsigned URL for a resource saved to the bucket.
        Unsigned URLs don't have a signature, so don't expire and can be viewed by anybody when they get the URL.
        For our purposes this is easier to deal with though less secure.
        """
        url = self.url(name, parameters, expire, http_method)
        return url.split("?")[0]
