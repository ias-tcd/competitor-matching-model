from typing import Optional


class BaseMockStorage:
    """Class that should be used in any tests that interact with S3 buckets to prevent test data from being written
    to the buckets. See .generators for functions to generate different options to"""

    mock_url: Optional[str] = None
    mock_unsigned_url: Optional[str] = None
    mock_save: bool = True
    mock_exists: bool = False

    def unsigned_url(self, name: str, *args, **kwargs) -> str:
        return self.mock_unsigned_url or self.url(name, *args, **kwargs).split("?")[0]

    def url(self, name: str, *args, **kwargs) -> str:
        return self.mock_url or f"https://ias-tcd.s3.amazonaws.com/{name}?signedPortion=True"

    def save(self, name: str, *args, **kwargs) -> str:
        if self.mock_save:
            return name
        raise Exception()

    def exists(self, name: str, *args, **kwargs) -> bool:
        return self.mock_exists
