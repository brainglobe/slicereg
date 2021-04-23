from __future__ import annotations

from dataclasses import dataclass, field, replace
from functools import cached_property

import numpy as np
from scipy import ndimage

@dataclass(frozen=True)
class Image:
    channels: np.ndarray = field(repr=False)
    resolution_um: float = 1.

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
        """The i,j shift that would move the origin fully from the upper-left corner to the lower-right corner."""
        return np.array([
            [1, 0, 0, self.height],
            [0, 1, 0, self.width],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    @property
    def resolution_matrix(self) -> np.ndarray:
        return np.diag([self.resolution_um, self.resolution_um, 1., 1.])

    @cached_property
    def inds_homog(self) -> np.ndarray:
        """All the i,j indices in the image as a 4 x (width x height) homogonous vertex array"""
        return np.mgrid[:self.height, :self.width, :1, 1:2].reshape(-1, self.width * self.height)

    def resample(self, resolution_um: float) -> Image:
        if resolution_um <= 0:
            raise ValueError("Resolution must be positive.")

        zoom_level = self.resolution_um / resolution_um
        zoomed_channels = ndimage.zoom(self.channels, zoom=(1, zoom_level, zoom_level))
        return replace(self, channels=zoomed_channels, resolution_um=resolution_um)
