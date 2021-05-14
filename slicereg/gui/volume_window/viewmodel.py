from dataclasses import dataclass, field
from typing import Tuple, Callable

import numpy as np

from slicereg.app.app_model import AppModel, VolumeType
from slicereg.utils.observable import HasObservableAttributes


@dataclass(unsafe_hash=True)
class VolumeViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    section_transform: np.ndarray = np.eye(4)
    clim: Tuple[int, int] = (0, 2)
    atlas_volume: np.ndarray = np.zeros(shape=(3, 3, 3), dtype=np.uint16)

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        if changed == 'section_image' and (image := self._model.section_image) is not None:
            self.section_image = image
        elif changed == 'section_transform' and (transform := self._model.section_transform) is not None:
            self.section_transform = transform
        elif changed == 'clim_3d_values':
            self.clim = self._model.clim_3d_values
        elif changed == 'visible_volume':
            m = self._model
            if m.visible_volume == VolumeType.REGISTRATION and (volume := m.registration_volume) is not None:
                self.atlas_volume = volume
            elif m.visible_volume == VolumeType.ANNOTATION and m.annotation_volume is not None:
                self.atlas_volume = m.annotation_volume
        elif changed == 'registration_volume':
            m = self._model
            if m.visible_volume == VolumeType.REGISTRATION and m.registration_volume is not None:
                self.atlas_volume = m.registration_volume
        elif changed == 'annotation_volume':
            m = self._model
            if m.visible_volume == VolumeType.ANNOTATION and m.annotation_volume is not None:
                self.atlas_volume = m.annotation_volume

    @property
    def camera_center(self) -> Tuple[float, float, float]:
        x, y, z = self.atlas_volume.shape
        return x / 2, y / 2, z / 2

    @property
    def camera_distance(self) -> float:
        return float(np.mean(self.atlas_volume.shape))

    @property
    def volume_clim(self) -> Tuple[int, int]:
        return np.min(self.atlas_volume), np.max(self.atlas_volume)

    def press_key(self, key: str):
        self._model.press_key(key=key)
