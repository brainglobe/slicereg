import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from slicereg.models.atlas import Atlas
from slicereg.models.section import Section
from slicereg.models.transforms import Plane3D, Plane2D


@given(res=integers(1, 1000), w=integers(1, 100), h=integers(1, 100), d=integers(1, 100))
def test_atlas_matrix_is_scaled_to_um_according_to_resolution_and_shape(res, w, h, d):
    atlas = Atlas(volume=np.random.random((w, h, d)), resolution_um=res)
    expected = [
        [res, 0, 0, -w / 2 * res],
        [0, res, 0, -h / 2 * res],
        [0, 0, res, -d / 2 * res],
        [0, 0, 0, 1],
    ]
    observed = atlas.affine_transform
    assert np.all(np.isclose(observed, np.array(expected)))


def test_slicing_an_atlas_gets_a_new_section_with_correct_parameters():
    atlas = Atlas(
        volume=np.broadcast_to(np.array([10, 20, 30]), (3, 3, 3)).swapaxes(0, 2),
        resolution_um=1
    )
    plane = Plane3D()
    section = atlas.slice(plane)
    assert isinstance(section, Section)
    assert section.plane_3d == plane
    assert section.plane_2d == Plane2D()
    assert section.image.pixel_resolution_um == atlas.resolution_um
    assert section.image.channels.shape == (1, 3, 3)
    assert section.thickness_um == atlas.resolution_um


@pytest.mark.parametrize('anterior,out', [(0, 10), (1, 16), (2, 21), (3, 0), (-1, 0)])
def test_slicing_atlas_along_postant_axis_gets_correct_section_image(anterior, out):
    atlas = Atlas(
        volume=np.broadcast_to(np.array([10, 16, 21]), (3, 3, 3)),
        resolution_um=1,
    )
    section = atlas.slice(Plane3D(anterior=anterior))
    assert np.all(section.image.channels == out)


@pytest.mark.parametrize('right,out', [(0, 10), (1, 16), (2, 21), (3, 0), (-1, 0)])
def test_slicing_atlas_along_leftright_axis_gets_correct_section_image(right, out):
    atlas = Atlas(
        volume=np.broadcast_to(np.array([10, 16, 21]), (3, 3, 3)).swapaxes(0, 2),
        resolution_um=1,
    )
    section = atlas.slice(Plane3D(right=right, ry=-90))
    assert np.all(section.image.channels == out)


@pytest.mark.parametrize('superior,out', [(0, 10), (1, 16), (2, 21), (3, 0), (-1, 0)])
def test_slicing_atlas_along_infsup_axis_gets_correct_section_image(superior, out):
    atlas = Atlas(
        volume=np.broadcast_to(np.array([10, 16, 21]), (3, 3, 3)).swapaxes(1, 2),
        resolution_um=1,
    )
    section = atlas.slice(Plane3D(superior=superior, rx=90))
    assert np.all(section.image.channels == out)
