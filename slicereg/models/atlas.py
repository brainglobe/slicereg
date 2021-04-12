from dataclasses import dataclass, field

import numpy as np


@dataclass
class Atlas:
    volume: np.ndarray = field(repr=False)
    resolution_um: float

    @property
    def affine_transform(self) -> np.ndarray:
        # need -90 degree rotation (ignore left-handed nature of Z coords, since don't exist)
        ijk_to_xyz_matrix = np.array([
            [ 0, 1, 0, 0],
            [-1, 0, 0, 0],
            [ 0, 0, 1, 0],
            [ 0, 0, 0, 1],
        ])
        return self.scale_matrix @ ijk_to_xyz_matrix

    @property
    def scale_matrix(self) -> np.ndarray:
        res = self.resolution_um
        matrix = np.diag((res, res, res, 1))
        return matrix