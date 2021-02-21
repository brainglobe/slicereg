from functools import partial

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

from slicereg.models.transforms import Plane2D

np.set_printoptions(suppress=True, precision=1)

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)


def test_planar_translation_assigns_correct_positions():
    plane = Plane2D(x=3, y=4)
    plane2 = plane.translate(10, 5)
    assert plane2.x == 13 and plane2.y == 9


def test_planar_rotation_assigns_correct_translations():
    plane = Plane2D(x=0, y=0, theta=45)
    plane2 = plane.rotate(45)
    assert plane2.theta == 90


@given(x=sensible_floats(), y=sensible_floats())
def test_planes_affine_transform_with_no_rotation_is_correct(x, y):
    plane = Plane2D(x=x, y=y, theta=0)
    expected_transform = np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    assert np.all(np.isclose(plane.affine_transform, expected_transform))


@given(x=sensible_floats(), y=sensible_floats(), theta=sensible_floats())
def test_planes_affine_transform_with_rotation_is_correct(x, y, theta):
    plane = Plane2D(x=x, y=y, theta=theta)
    t = np.radians(theta)
    expected = np.array([
        [np.cos(t), -np.sin(t), 0, x],
        [np.sin(t),  np.cos(t), 0, y],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1],
    ], dtype=float)
    observed = plane.affine_transform
    assert np.all(np.isclose(observed, expected))


