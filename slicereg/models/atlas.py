from dataclasses import dataclass
from typing import Tuple

from numpy import ndarray
from vispy.util.transforms import scale, translate


@dataclass
class Atlas:
    volume: ndarray
    resolution_um: float

    @property
    def affine_transform(self) -> ndarray:
        w, h, d = self.volume.shape
        return (translate((-w / 2, -h / 2, -d / 2)) @ scale((self.resolution_um,) * 3)).T