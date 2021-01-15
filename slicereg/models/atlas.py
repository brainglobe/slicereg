from dataclasses import dataclass
from typing import Tuple

from numpy import ndarray  # type: ignore
from vispy.util.transforms import scale, translate  # type: ignore


@dataclass
class Atlas:
    volume: ndarray
    resolution_um: float
    origin: Tuple[float, float, float]

    @property
    def model_matrix(self) -> ndarray:
        x, y, z = self.origin
        return scale((self.resolution_um,) * 3) @ translate((-x, -y, -z))