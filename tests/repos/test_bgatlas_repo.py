from unittest.mock import patch

import numpy as np

from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


def test_atlas_is_settable_gettable_for_repo_state():
    repo = AtlasRepo()
    atlas = Atlas(volume=np.random.random((3, 3, 3)), resolution_um=1)
    assert repo.get_atlas() is None

    repo.set_atlas(atlas=atlas)
    assert repo.get_atlas() == atlas


@patch("slicereg.repos.atlas_repo.bg_utils.conf_from_url")
def test_can_get_available_bgatlases_for_download(mock_conf_from_url):
    atlas_versions = {'allen2': '1.0', 'mousey3': '1.2'}
    mock_conf_from_url.return_value = {'atlases': atlas_versions}
    atlases = AtlasRepo().list_available_atlases()
    assert len(atlases) == len(atlas_versions)
    for atlas in atlas_versions:
        assert atlas in atlases
