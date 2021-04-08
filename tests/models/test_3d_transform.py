from functools import partial

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

from slicereg.models.transforms import Transform3D

real_floats = partial(floats, allow_infinity=False, allow_nan=False)


@given(x=real_floats(), y=real_floats(), z=real_floats())
def test_3d_translation_gives_correct_affine_transform(x, y, z):
    expected = [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ]
    observed = Transform3D(x=x, y=y, z=z).affine_transform
    assert np.all(np.isclose(observed, expected))


@given(rx=real_floats())
def test_3d_x_rotation_gives_correct_affine_transform(rx):
    expected = [
        [1, 0, 0, 0],
        [0, np.cos(np.radians(rx)), -np.sin(np.radians(rx)), 0],
        [0, np.sin(np.radians(rx)), np.cos(np.radians(rx)), 0],
        [0, 0, 0, 1],
    ]
    observed = Transform3D(rx=rx).affine_transform
    assert np.all(np.isclose(observed, expected))


@given(x=real_floats(), y=real_floats(), z=real_floats(), dx=real_floats(), dy=real_floats(), dz=real_floats())
def test_translation_updates_xyz(x, y, z, dx, dy, dz):
    plane = Transform3D(x=x, y=y, z=z)
    plane2 = plane.translate(dx, dy, dz)
    assert (plane2.x, plane2.y, plane2.z) == (x + dx, y + dy, z + dz)


@given(x=real_floats(), y=real_floats(), z=real_floats(), dx=real_floats(), dy=real_floats(), dz=real_floats())
def test_rotation_updates_xyz(x, y, z, dx, dy, dz):
    plane = Transform3D(rx=x, ry=y, rz=z)
    plane2 = plane.rotate(dx, dy, dz)
    assert (plane2.rx, plane2.ry, plane2.rz) == (x + dx, y + dy, z + dz)