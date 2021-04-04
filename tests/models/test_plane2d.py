from functools import partial

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, booleans

from slicereg.models.transforms import Image2DTransform

np.set_printoptions(suppress=True, precision=1)

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)


@given(i=sensible_floats(), j=sensible_floats(), i2=sensible_floats(), j2=sensible_floats(), theta=sensible_floats(), rot=sensible_floats(), rot_first=booleans())
def test_planar_rotation_and_translate_updates_correct_parameters_with_order_independent(i, j, i2, j2, theta, rot, rot_first):
    plane = Image2DTransform(i=i, j=j, theta=theta)
    if rot_first:
        plane2 = plane.rotate(theta=rot).translate(i=i2, j=j2)
    else:
        plane2 = plane.translate(i=i2, j=j2).rotate(theta=rot)
    assert plane2.theta == theta + rot
    assert plane2.i == i + i2 and plane2.j == j + j2


@given(i=sensible_floats(), j=sensible_floats(), theta=sensible_floats())
def test_planes_affine_transform_with_rotation_is_correct(i, j, theta):
    plane = Image2DTransform(i=i, j=j, theta=theta)
    t = np.radians(theta)
    expected = np.array([
        [np.cos(t), -np.sin(t), 0, i],
        [np.sin(t),  np.cos(t), 0, j],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1],
    ], dtype=float)
    observed = plane.affine_transform
    assert np.all(np.isclose(observed, expected))


