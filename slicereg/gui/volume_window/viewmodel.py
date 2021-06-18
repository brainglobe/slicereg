from dataclasses import dataclass, field
from typing import Tuple, List

import numpy as np
from numpy import ndarray

from slicereg.gui.app_model import AppModel
from slicereg.gui.constants import VolumeType
from slicereg.utils.observable import HasObservableAttributes

@dataclass
class SectionViewData:
    image: ndarray
    transform: ndarray
    clim: Tuple[int, int]




@dataclass(unsafe_hash=True)
class VolumeViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    section_image: np.ndarray = np.zeros(shape=(3, 3), dtype=np.uint16)
    section_transform: np.ndarray = np.eye(4)
    clim: Tuple[int, int] = (0, 2)
    atlas_volume: np.ndarray = np.zeros(shape=(3, 3, 3), dtype=np.uint16)
    sections: List[SectionViewData] = field(default_factory=list)

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        update_funs = {
            'section_image': self._update_section_image,
            'section_transform': self._update_section_transform,
            'clim_3d': self._update_clim,
            'visible_volume': self._switch_visible_volume,
            'registration_volume': self._update_visible_volume_to_registration,
            'annotation_volume': self._update_visible_volume_to_annotation,
            'loaded_sections': self._update_visible_sections,
        }
        if (fun := update_funs.get(changed)) is not None:
            fun()

    def _update_visible_sections(self):
        self.sections = self._model.loaded_sections
    
    def _update_section_image(self):
        if (image := self._model.section_image) is not None:
            self.section_image = image
            self._update_clim()

    def _update_section_transform(self):
        if (transform := self._model.section_transform) is not None:
            self.section_transform = transform

    def _update_clim(self):
        self.clim = self._model.clim_3d_values

    def _switch_visible_volume(self):
        m = self._model
        if m.visible_volume == VolumeType.REGISTRATION and (volume := m.registration_volume) is not None:
            self.atlas_volume = volume
        elif m.visible_volume == VolumeType.ANNOTATION and m.annotation_volume is not None:
            self.atlas_volume = m.annotation_volume

    def _update_visible_volume_to_registration(self):
        m = self._model
        if m.visible_volume == VolumeType.REGISTRATION and m.registration_volume is not None:
            self.atlas_volume = m.registration_volume

    def _update_visible_volume_to_annotation(self):
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
        return int(np.min(self.atlas_volume)), int(np.max(self.atlas_volume))

    def press_key(self, key: str) -> None:
        self._model.press_key(key=key)
