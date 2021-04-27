from dataclasses import dataclass, field
from typing import Tuple

from slicereg.commands.utils import Signal


@dataclass
class AppModel:
    clim_2d: Tuple[float, float] = (0., 1.)
    clim_3d: Tuple[float, float] = (0., 1.)
    updated: Signal = field(default_factory=Signal)

    def update(self, **attrs):
        print(attrs)
        for attr, value in attrs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                raise TypeError(f"Cannot set {attr}, {self.__class__.__name__} has no {attr} attribute.")
        self.updated.emit()



