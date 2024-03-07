from typing import Any, Callable, Dict, Literal, Optional

from .base_mock_storage import BaseMockStorage

ALLOWED_OPTIONS = Literal["save", "exists", "url", "unsigned_url"]


def mock_save(save: bool = False, storage: Optional[BaseMockStorage] = None) -> BaseMockStorage:
    storage = storage or BaseMockStorage()
    storage.mock_save = save
    return storage


def mock_exists(exists: bool = True, storage: Optional[BaseMockStorage] = None) -> BaseMockStorage:
    storage = storage or BaseMockStorage()
    storage.mock_exists = exists
    return storage


def mock_signed_url(url: str, storage: Optional[BaseMockStorage] = None) -> BaseMockStorage:
    storage = storage or BaseMockStorage()
    storage.mock_url = url
    return storage


def mock_unsigned_url(url: str, storage: Optional[BaseMockStorage] = None) -> BaseMockStorage:
    storage = storage or BaseMockStorage()
    storage.mock_unsigned_url = url
    return storage


def combine(options: Dict[ALLOWED_OPTIONS, Dict[str, Any]]) -> BaseMockStorage:
    """Combine multiple options for the returns of the base functions for an S3Storage instance"""
    storage = BaseMockStorage()
    function_map: Dict[ALLOWED_OPTIONS, Callable[..., BaseMockStorage]] = {
        "save": mock_save,
        "exists": mock_exists,
        "url": mock_signed_url,
        "unsigned_url": mock_unsigned_url,
    }
    for key, value in options.items():
        function = function_map[key]
        storage = function(storage=storage, **value)
    return storage
