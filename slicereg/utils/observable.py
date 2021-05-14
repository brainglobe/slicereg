from collections import Callable

from slicereg.utils import Signal


class ObservableAttributes:

    def __init__(self):
        self.updated = Signal()

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(changed=key)

    def register(self, fun: Callable[[str], None]):
        """
        Takes a callback function that gets called with the name of the changed argument.

        Example:
        def update(changed: str):
            if changed == 'a':
                print("You updated a!")
            elif changed == 'b':
                print("You updated b!")

        >> observable.register(update)
        >> observable.a = 5
        You updated a!
        """
        self.updated.connect(fun)
