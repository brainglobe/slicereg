from typing import Callable

from slicereg.utils import Signal


class HasObservableAttributes:

    def __init__(self):
        self.updated = Signal()

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated') and not key.startswith('_'):
            self.updated.emit(changed=key)

    def register(self, fun: Callable[[str], None]):
        """
        Takes a callback function that gets called with the name of the changed argument.

        Example:
        >> observable = HasObservableAttributes()
        >> observable.register(lambda changed: print(f"You updated {changed}!"))
        >> observable.a = 5
        You updated a!
        """
        self.updated.connect(fun)
