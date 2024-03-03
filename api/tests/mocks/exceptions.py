from typing import Optional


def raise_exception(e: Optional[BaseException] = None):
    """Helper function to be used as a mock for a function to simulate that function raising an exception

    Usage:
    @patch("path.to.function", side_effect=raise_exception(<exception to raise, or blank of `Exception` is suitable>))
    def test_func(self, *args):
        ...
    """
    if not e:
        e = Exception()

    def func(*args, **kwargs):
        raise e

    return func
