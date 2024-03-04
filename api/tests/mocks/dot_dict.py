from __future__ import annotations

from typing import Any


def convert_to_dot_dict(d: dict) -> DotDict:
    """
    Converts a dictionary to a `DotDict`.
    Useful for mocking complex responses from a function that returns an object instance. Instead of needing to
    instantiate and assign values to the object instance, you can create a dictionary mocking the response and feed it
    through this function to allow the properties of the dictionary to be accessed using dot notation
    """
    result = DotDict()
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = convert_to_dot_dict(v)
        else:
            result[k] = v
    return result


class DotDict(dict):
    """Class to allow accessing of dictionary values using dot notation instead of subscript key notation"""

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        del self[name]
