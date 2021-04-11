from unittest.mock import patch, PropertyMock

import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import BrainglobeAtlasRepo

cases = [
    [['allen_mouse_100um'], (100,)],
    [['allen_mouse_25um'], (25,)],
    [['allen_mouse_25um', 'allen_mouse_100um'], (25, 100)],
    [['example_mouse_100um', 'allen_mouse_25um', 'allen_mouse_10um'], (25, 10)],
]


@pytest.mark.parametrize("atlases,resolutions", cases)
def test_get_resolutions_from_bgatlas_list(atlases, resolutions):
    repo = BrainglobeAtlasRepo()
    with patch("slicereg.repos.atlas_repo.get_downloaded_atlases", side_effect=lambda: atlases):
        available_resolutions = repo.get_downloaded_resolutions()
        assert resolutions == available_resolutions


@given(resolution=integers())
def test_get_atlas_raises_error_on_nonallen_resolutions(resolution):
    if resolution in [10, 25, 100]:  # these values shouldn't result in an error, so don't test them.
        return
    repo = BrainglobeAtlasRepo()
    with pytest.raises(ValueError):
        repo.load_atlas(resolution=resolution)


@patch("slicereg.repos.atlas_repo.BrainGlobeAtlas")
@pytest.mark.parametrize("resolution", [100, 25, 10])
def test_get_atlas_returns_atlas_with_correct_resolution(mock_bgatlas, resolution):
    bgatlas = mock_bgatlas.return_value  # Get instance of mock class that will be provided upon instantiation.
    type(bgatlas).shape_um = PropertyMock(return_value=(20, 10, 10))
    type(bgatlas).resolution = PropertyMock(return_value=[resolution, resolution, resolution])

    repo = BrainglobeAtlasRepo()
    atlas = repo.load_atlas(resolution=resolution)
    assert atlas.resolution_um == resolution



def test_atlas_is_settable_gettable_for_repo_state():
    repo = BrainglobeAtlasRepo()
    atlas = Atlas(volume=np.random.random((3, 3, 3)), resolution_um=1)
    assert repo.get_atlas() is None

    repo.set_atlas(atlas=atlas)
    assert repo.get_atlas() == atlas



@patch("slicereg.repos.atlas_repo.bg_utils.conf_from_url")
def test_can_get_available_bgatlases_for_download(mock_conf_from_url):
    atlas_versions = {'allen2': '1.0', 'mousey3': '1.2'}
    mock_conf_from_url.return_value = {'atlases': atlas_versions}
    atlases = BrainglobeAtlasRepo().list_available_atlases()
    assert len(atlases) == len(atlas_versions)
    for atlas in atlas_versions:
        assert atlas in atlases

