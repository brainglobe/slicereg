from dataclasses import dataclass, field
from typing import Tuple, Optional

from numpy import ndarray

from slicereg.commands.utils import Signal


@dataclass
class AppModel:
    clim_2d: Tuple[float, float] = (0., 1.)
    clim_3d: Tuple[float, float] = (0., 1.)
    section_image: Optional[ndarray] = None
    atlas_image: Optional[ndarray] = None
    updated: Signal = field(default_factory=Signal)

    def update(self, **attrs):
        print(attrs)
        for attr, value in attrs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                raise TypeError(f"Cannot set {attr}, {self.__class__.__name__} has no {attr} attribute.")
        self.updated.emit()

    def on_section_loaded(self, image: ndarray, atlas_image: ndarray, transform: ndarray, resolution_um: int) -> None:
        self.update(section_image=image, atlas_image=atlas_image)

    def on_channel_select(self, image: ndarray, channel: int) -> None:
        self.update(section_image=image)

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray, atlas_image: ndarray) -> None:
        self.update(section_image=section_image, atlas_image=atlas_image)

    def on_section_moved(self, transform: ndarray, atlas_slice_image: ndarray) -> None:
        self.update(atlas_image=atlas_slice_image)
