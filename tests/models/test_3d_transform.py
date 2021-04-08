import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

from slicereg.models.transforms import Transform3D

sensible_floats = floats(allow_infinity=False, allow_nan=False)


@given(x=sensible_floats, y=sensible_floats, z=sensible_floats)
def test_3d_translation_gives_correct_affine_transform(x, y, z):
    expected = [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ]
    observed = Transform3D(x=x, y=y, z=z).affine_transform
    assert np.all(np.isclose(observed, expected))


@given(rot_lateral=sensible_floats)
def test_3d_x_rotation_gives_correct_affine_transform(rot_lateral):
    expected = [
        [1, 0, 0, 0],
        [0, np.cos(np.radians(rot_lateral)), -np.sin(np.radians(rot_lateral)), 0],
        [0, np.sin(np.radians(rot_lateral)), np.cos(np.radians(rot_lateral)), 0],
        [0, 0, 0, 1],
    ]
    observed = Transform3D(rot_lateral=rot_lateral).affine_transform
    assert np.all(np.isclose(observed, expected))
