from dataclasses import dataclass, field
from typing import Tuple

import numpy as np
from vispy.app import use_app

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass(unsafe_hash=True)
class VolumeViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)
    section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    section_transform: np.ndarray = np.eye(4)
    clim: Tuple[int, int] = (0, 2)
    atlas_volume: np.ndarray = np.zeros(shape=(3, 3, 3), dtype=np.uint16)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            print('VolumeViewModel:', key, 'updated')
            self.updated.emit(**{key: value, 'model': self, 'changed': key})

    def update(self, model: AppModel, changed: str, **kwargs):
        if changed == 'section_image':
            self.section_image = model.section_image
        elif changed == 'section_transform':
            self.section_transform = model.section_transform
        elif changed == 'clim_3d_values':
            self.clim = model.clim_3d_values
        elif changed in ['registration_volume', 'annotation_volume', 'visible_volume']:
            self.atlas_volume = model.atlas_volume

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
        self._model.keyboard_shortcut(key=key)
