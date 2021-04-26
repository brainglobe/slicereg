from dataclasses import dataclass, field
from typing import Tuple

from slicereg.commands.utils import Signal


@dataclass
class ViewSection:
    clim: Tuple[float, float] = (0., 1.)
    clim_updated: Signal = field(default_factory=Signal)

    def update_clim(self, min: float, max: float):
        self.clim = (min, max)
        self.clim_updated.emit()
