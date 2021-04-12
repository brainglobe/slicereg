from contextlib import redirect_stdout
from io import StringIO
from typing import List

from bg_atlasapi import BrainGlobeAtlas
from bg_atlasapi import utils as bg_utils

from slicereg.models.atlas import Atlas


def load_atlas(name: str) -> Atlas:
    with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
        bgatlas = BrainGlobeAtlas(atlas_name=name)

    new_reference = bgatlas.space.map_stack_to("lip", bgatlas.reference)

    return Atlas(
        volume=new_reference,
        resolution_um=bgatlas.resolution[0],
    )


def list_available_atlases() -> List[str]:
    """Returns a list of keys"""
    download_url = BrainGlobeAtlas._remote_url_base.format("last_versions.conf")
    atlas_versions = dict(dict(bg_utils.conf_from_url(download_url))['atlases'])
    return list(atlas_versions.keys())
