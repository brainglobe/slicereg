from dataclasses import dataclass, field
from typing import Tuple, Optional

from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass
class AtlasSectionDTO:
    section_image: Optional[ndarray] = None
    coords: Tuple[int, int] = None


@dataclass(unsafe_hash=True)
class AtlasSectionViewModel:
    axis: int
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs.keys()}")
        updates = AtlasSectionDTO()
        if 'atlas_volume' in kwargs:
            updates.section_image = self.section_image
        if 'atlas_section_coords' in kwargs:
            updates.coords = kwargs['atlas_section_coords']
        self.updated.emit(dto=updates)

    @property
    def section_image(self):
        if (volume := self._model.atlas_volume) is not None:
            section_slice_idx = self._model.atlas_section_coords[self.axis]
            return volume.swapaxes(self.axis, 0)[section_slice_idx]
        else:
            return None

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        print(x1, y1, x2, y2)
