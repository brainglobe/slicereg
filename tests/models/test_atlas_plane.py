import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

from slicereg.models.transforms import AtlasTransform

sensible_floats = floats(allow_infinity=False, allow_nan=False)


@given(right=sensible_floats, superior=sensible_floats, anterior=sensible_floats)
def test_3d_translation_gives_correct_affine_transform(right, superior, anterior):
    expected = [
        [1, 0, 0, right],
        [0, 1, 0, superior],
        [0, 0, 1, anterior],
        [0, 0, 0, 1],
    ]
    observed = AtlasTransform(right=right, superior=superior, anterior=anterior).affine_transform
    assert np.all(np.isclose(observed, expected))


@given(rot_lateral=sensible_floats)
def test_3d_x_rotation_gives_correct_affine_transform(rot_lateral):
    expected = [
        [1, 0, 0, 0],
        [0, np.cos(np.radians(rot_lateral)), -np.sin(np.radians(rot_lateral)), 0],
        [0, np.sin(np.radians(rot_lateral)), np.cos(np.radians(rot_lateral)), 0],
        [0, 0, 0, 1],
    ]
    observed = AtlasTransform(rot_lateral=rot_lateral).affine_transform
    assert np.all(np.isclose(observed, expected))
