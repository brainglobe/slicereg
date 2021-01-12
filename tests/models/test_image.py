import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

from slicereg.models.section import Plane


def test_planar_translation_assigns_correct_positions():
    plane = Plane(x=3, y=4)
    plane2 = plane.translate(10, 5)
    assert plane2.x == 13 and plane2.y == 9


def test_planar_rotation_assigns_correct_translations():
    plane = Plane(x=0, y=0, theta=45)
    plane2 = plane.rotate(45)
    assert plane2.theta == 90


@given(x=floats(allow_nan=False), y=floats(allow_nan=False))
def test_planes_affine_transform_is_correct(x, y):
    plane = Plane(x=x, y=y, theta=0)
    expected_transform = np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    assert np.all(np.isclose(plane.affine_transform, expected_transform))
