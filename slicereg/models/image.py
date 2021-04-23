from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property

import numpy as np

@dataclass(frozen=True)
class Image:
    channels: np.ndarray = field(repr=False)

    @property
    def num_channels(self) -> int:
        return self.channels.shape[0]

    @property
    def height(self) -> int:
        return self.channels.shape[1]

    @property
    def width(self) -> int:
        return self.channels.shape[2]

    @property
    def full_shift_matrix(self) -> np.ndarray:
        return np.array([
            [1, 0, 0, self.height],
            [0, 1, 0, self.width],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    @cached_property
    def inds_homog(self) -> np.ndarray:
        """All the i,j indices in the image as a 4 x (width x height) homogonous vertex array"""
        return np.mgrid[:self.height, :self.width, :1, 1:2].reshape(-1, self.width * self.height)


