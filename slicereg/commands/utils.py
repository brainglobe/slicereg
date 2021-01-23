from typing import Callable


class Signal:

    def __init__(self):
        self._callbacks = set()

    def emit(self, *args, **kwargs) -> None:
        for callback in self._callbacks:
            callback(*args, **kwargs)

    def connect(self, callback: Callable) -> None:
        self._callbacks.add(callback)

    def disconnect(self, callback: Callable) -> None:
        self._callbacks.remove(callback)