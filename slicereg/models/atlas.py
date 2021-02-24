from dataclasses import dataclass
from typing import Tuple

import numpy as np
from numpy import ndarray
from vispy.util.transforms import scale, translate

from slicereg.models.image import ImageData
from slicereg.models.section import Section
from slicereg.models.transforms import Plane3D


@dataclass
class Atlas:
    volume: ndarray
    resolution_um: float

    @property
    def affine_transform(self) -> ndarray:
        w, h, d = self.volume.shape
        return (translate((-w / 2, -h / 2, -d / 2)) @ scale((self.resolution_um,) * 3)).T

    def slice(self, plane: Plane3D, thickness_um: float) -> Section:
        return Section(
            image=ImageData(channels=np.zeros((1, 3, 3)), pixel_resolution_um=self.resolution_um),
            plane_3d=plane,
            thickness_um=thickness_um
        )
