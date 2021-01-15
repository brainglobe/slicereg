from dataclasses import dataclass
from typing import Tuple

from numpy import ndarray
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