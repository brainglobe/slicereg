import numpy as np
import numpy.testing as npt
from hypothesis import given
from hypothesis.strategies import integers, floats
from pytest import approx

from slicereg.core.atlas import Atlas


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_scale_matrix_is_scaled_to_um_according_to_resolution_and_not_shape(res, w, h, d):
    atlas = Atlas(volume=np.empty((w, h, d)), resolution_um=res)
    expected = np.array([
        [res, 0, 0, 0],
        [0, res, 0, 0],
        [0, 0, res, 0],
        [0, 0, 0, 1],
    ])
    assert np.all(np.isclose(atlas.scale_matrix, expected))


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_can_get_atlas_center_in_shared_space(res, w, h, d):
    atlas = Atlas(volume=np.empty((w, h, d)), resolution_um=res)
    assert atlas.center == approx((h * res / 2, -w * res / 2, d * res / 2))


def test_atlas_contains_an_annotation_volume():
    atlas = Atlas(volume=np.empty((5, 4, 6)), annotation_volume=np.empty((5, 4, 6)), resolution_um=10)
    assert atlas.annotation_volume.shape == atlas.volume.shape


@given(x=floats(0, 30), y=floats(0, 30), z=floats(0, 30), res=floats(0.5, 10))
def test_atlas_converts_xyz_to_ijk(x, y, z, res):
    atlas = Atlas(volume=np.empty((20, 20, 20)), annotation_volume=np.empty((20, 20, 20)), resolution_um=res)
    i, j, k = atlas.map_xyz_to_ijk(x=x, y=y, z=z)
    assert i == x // res
    assert j == y // res
    assert k == z // res


@given(x=floats(-30, -0.1), y=floats(-30, -0.1), z=floats(-30, -0.1), res=floats(0.5, 10))
def test_atlas_converts_negative_xyz_to_no_ijk(x, y, z, res):
    atlas = Atlas(volume=np.empty((20, 20, 20)), annotation_volume=np.empty((20, 20, 20)), resolution_um=res)
    ijk = atlas.map_xyz_to_ijk(x=x, y=y, z=z)
    assert ijk is None


def test_can_get_atlas_image_coords_from_xyz():
    atlas = Atlas(volume=np.empty((5, 4, 6)), annotation_volume=np.empty((5, 5, 5)), resolution_um=10)
    assert atlas.map_xyz_to_ijk(x=0, y=0, z=0) == (0, 0, 0)


def test_can_get_atlas_coronal_section_from_xyz():
    atlas = Atlas(volume=np.empty((10, 10, 10)), annotation_volume=np.empty((10, 10, 10)), resolution_um=2)
    sections = atlas.orthogonal_sections_at(x=0, y=0, z=0)
    npt.assert_almost_equal(sections.coronal, atlas.volume[0])
