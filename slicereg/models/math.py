from numpy import ndarray  # type: ignore
from vispy.util.transforms import scale, rotate, translate  # type: ignore


def affine_transform(x: float, y: float, z: float, rx: float, ry: float, rz: float, s: float) -> ndarray:
    return \
        scale((s, s, s)) @ \
        rotate(rx, (1, 0, 0)) @ \
        rotate(ry, (0, 1, 0)) @ \
        rotate(rz, (0, 0, 1)) @ \
        translate((x, y, z))

