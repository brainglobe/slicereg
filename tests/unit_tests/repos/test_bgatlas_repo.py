import numpy as np

from slicereg.core.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


def test_atlas_is_settable_gettable_for_repo_state():
    repo = AtlasRepo()
    assert repo.get_atlas() is None

    atlas = Atlas(volume=np.random.random((3, 3, 3)), resolution_um=1)
    repo.set_atlas(atlas=atlas)
    assert repo.get_atlas() == atlas
