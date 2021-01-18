from unittest.mock import patch

import pytest

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
