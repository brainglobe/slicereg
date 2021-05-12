from typing import Callable


class Signal:
    """
    Creates callback functions.

    Example:
        >> name_created = Signal()
        >> name_created.connect(lambda name: print("Hello,", name))
        >> name_created.connect(lambda name: print("Hi,", name))
        >> name_created.emit(name="Nick")
        Hello, Nick
        Hi, Nick
    """

    def __init__(self):
        self._callbacks = set()

    def emit(self, *args, **kwargs) -> None:
        for callback in self._callbacks:
            callback(*args, **kwargs)

    def connect(self, callback: Callable) -> None:
        self._callbacks.add(callback)

    def disconnect(self, callback: Callable) -> None:
        self._callbacks.remove(callback)
