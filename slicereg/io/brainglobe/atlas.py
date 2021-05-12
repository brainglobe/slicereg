from contextlib import redirect_stdout
from io import StringIO
from typing import List, Optional

from bg_atlasapi import BrainGlobeAtlas
from bg_atlasapi import utils as bg_utils

from slicereg.commands.base import BaseRemoteAtlasReader
from slicereg.core.atlas import Atlas


class BrainglobeRemoteAtlasReader(BaseRemoteAtlasReader):

    @property
    def name(self) -> str:
        return "Brainglobe"

    def read(self, name: str) -> Atlas:
        with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
            bgatlas = BrainGlobeAtlas(atlas_name=name)

        # Brainglobe atlases have a "reference volume" and an "annotation volume"
        assert bgatlas.annotation.shape == bgatlas.reference.shape
        new_reference = bgatlas.space.map_stack_to("asl", bgatlas.reference)
        new_annotation = bgatlas.space.map_stack_to("asl", bgatlas.annotation)

        return Atlas(
            volume=new_reference,
            resolution_um=bgatlas.resolution[0],
            annotation_volume=new_annotation,
        )

    def list(self) -> List[str]:
        """Returns a list of keys"""
        download_url = BrainGlobeAtlas._remote_url_base.format("last_versions.conf")
        atlas_versions = dict(dict(bg_utils.conf_from_url(download_url))['atlases'])
        return list(atlas_versions.keys())
