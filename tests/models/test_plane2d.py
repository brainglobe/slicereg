from functools import partial

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

from slicereg.models.transforms import Image2DTransform

np.set_printoptions(suppress=True, precision=1)

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)


def test_planar_translation_assigns_correct_positions():
    plane = Image2DTransform(i=3, j=4)
    plane2 = plane.translate(i=10, j=5)
    assert plane2.i == 13 and plane2.j == 9


def test_planar_rotation_assigns_correct_translations():
    plane = Image2DTransform(i=0, j=0, theta=45)
    plane2 = plane.rotate(45)
    assert plane2.theta == 90


@given(i=sensible_floats(), j=sensible_floats())
def test_planes_affine_transform_with_no_rotation_is_correct(i, j):
    plane = Image2DTransform(i=i, j=j, theta=0)
    expected_transform = np.array([
        [1, 0, 0, i],
        [0, 1, 0, j],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    assert np.all(np.isclose(plane.affine_transform, expected_transform))


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


