from dataclasses import dataclass, field
from typing import Tuple, Callable

import numpy as np

from slicereg.utils.signal import Signal
from slicereg.app.app_model import AppModel


@dataclass(unsafe_hash=True)
class VolumeViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)
    section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    section_transform: np.ndarray = np.eye(4)
    clim: Tuple[int, int] = (0, 2)
    atlas_volume: np.ndarray = np.zeros(shape=(3, 3, 3), dtype=np.uint16)

    def __post_init__(self):
        self._model.register(self.update)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(changed=key)

    def register(self, fun: Callable[[str], None]):
        """Takes a callback function that gets called with the name of the changed argument."""
        self.updated.connect(fun)

    def update(self, changed: str):
        if changed == 'section_image':
            self.section_image = self._model.section_image
        elif changed == 'section_transform':
            self.section_transform = self._model.section_transform
        elif changed == 'clim_3d_values':
            self.clim = self._model.clim_3d_values
        elif changed in ['registration_volume', 'annotation_volume', 'visible_volume']:
            self.atlas_volume = self._model.atlas_volume

    @property
    def camera_center(self) -> Tuple[float, float, float]:
        x, y, z = self.atlas_volume.shape
        return x / 2, y / 2, z / 2

    @property
    def camera_distance(self) -> float:
        return np.mean(self.atlas_volume.shape)

    @property
    def volume_clim(self) -> Tuple[int, int]:
        return np.min(self.atlas_volume), np.max(self.atlas_volume)

    def press_key(self, key: str):
        self._model.press_key(key=key)
