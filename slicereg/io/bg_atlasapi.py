from contextlib import redirect_stdout
from io import StringIO
from typing import List

from bg_atlasapi import BrainGlobeAtlas
from bg_atlasapi import utils as bg_utils

from slicereg.models.atlas import Atlas


class BrainglobeAtlasReader:

    @staticmethod
    def read(path: str) -> Atlas:
        with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
            bgatlas = BrainGlobeAtlas(atlas_name=path)

        # Brainglobe atlases have a "reference volume" and an "annotation volume"
        assert bgatlas.annotation.shape == bgatlas.reference.shape
        new_reference = bgatlas.space.map_stack_to("lip", bgatlas.reference)
        new_annotation = bgatlas.space.map_stack_to("lip", bgatlas.annotation)

        return Atlas(
            volume=new_reference,
            resolution_um=bgatlas.resolution[0],
            annotation_volume=new_annotation,
        )

    @staticmethod
    def list_available() -> List[str]:
        """Returns a list of keys"""
        download_url = BrainGlobeAtlas._remote_url_base.format("last_versions.conf")
        atlas_versions = dict(dict(bg_utils.conf_from_url(download_url))['atlases'])
        return list(atlas_versions.keys())
