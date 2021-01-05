from dataclasses import dataclass
from typing import Tuple
from warnings import warn

from numpy.core._multiarray_umath import ndarray
from vispy.util.transforms import scale, translate


@dataclass
class Atlas:
    volume: ndarray
    resolution_um: float
    origin: Tuple[float, float, float]

    @property
    def model_matrix(self) -> ndarray:
        x, y, z = self.origin
        return scale((self.resolution_um,) * 3) @ translate((-x, -y, -z))

    def slice(self, width: float, transform: ndarray) -> ndarray:
        warn("Atlas Slicing not correctly implemented, don't rely on this result!")
        return self.volume[20]