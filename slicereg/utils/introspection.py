import inspect
from typing import Callable, List


def get_public_attrs(fun: Callable) -> List[str]:
    return [attr for attr in inspect.signature(fun).parameters if not attr.startswith('_')]