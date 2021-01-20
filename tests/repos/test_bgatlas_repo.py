from unittest.mock import patch, PropertyMock

import pytest
from bg_atlasapi import BrainGlobeAtlas
from hypothesis import given
from hypothesis.strategies import integers

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
        resolutions = repo.get_downloaded_resolutions()
        assert resolutions == resolutions


@given(resolution=integers())
def test_get_atlas_raises_error_on_nonallen_resolutions(resolution):
    if resolution in [10, 25, 100]:  # these values shouldn't result in an error, so don't test them.
        return
    repo = BrainglobeAtlasRepo()
    with pytest.raises(ValueError):
        repo.get_atlas(resolution=resolution)


@patch("slicereg.repos.atlas_repo.BrainGlobeAtlas")
@pytest.mark.parametrize("resolution", [100, 25, 10])
def test_get_atlas_returns_atlas_with_correct_resolution(MockBGAtlas, resolution):
    bgatlas = MockBGAtlas.return_value  # Get instance of mock class that will be provided upon instantiation.
    type(bgatlas).shape_um = PropertyMock(return_value=(20, 10, 10))
    type(bgatlas).resolution = PropertyMock(return_value=[resolution, resolution, resolution])

    repo = BrainglobeAtlasRepo()
    atlas = repo.get_atlas(resolution=resolution)
    assert atlas.resolution_um == resolution
