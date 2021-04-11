import re
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from io import StringIO
from typing import Tuple, Optional, List

from bg_atlasapi import BrainGlobeAtlas
from bg_atlasapi import utils as bg_utils
from bg_atlasapi.list_atlases import get_downloaded_atlases

from slicereg.models.atlas import Atlas


class BaseAtlasRepo(ABC):

    @abstractmethod
    def load_atlas(self, resolution: int) -> Atlas: ...

    @abstractmethod
    def get_downloaded_resolutions(self) -> Tuple[int, ...]: ...

    @abstractmethod
    def get_atlas(self) -> Optional[Atlas]: ...

    @abstractmethod
    def set_atlas(self, atlas: Atlas) -> None: ...


class BrainglobeAtlasRepo(BaseAtlasRepo):

    def __init__(self):
        self._atlas: Optional[Atlas] = None

    def load_atlas(self, resolution: int) -> Atlas:
        if resolution not in [10, 25, 100]:
            raise ValueError("Only 10um, 25um and 100um atlas resolutions available.")

        with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
            bgatlas = BrainGlobeAtlas(f"allen_mouse_{resolution}um")

        new_reference = bgatlas.space.map_stack_to("lip", bgatlas.reference)

        return Atlas(
            volume=new_reference,
            resolution_um=bgatlas.resolution[0],
        )

    def list_available_atlases(self) -> List[str]:
        """Returns a list of keys"""
        download_url = BrainGlobeAtlas._remote_url_base.format("last_versions.conf")
        atlas_versions = dict(dict(bg_utils.conf_from_url(download_url))['atlases'])
        return list(atlas_versions.keys())

    def get_downloaded_resolutions(self) -> Tuple[int, ...]:
        pattern = re.compile("allen_mouse_(\d{2,})um")  # look for the name "allen_mouse_XXXum"
        downloaded = get_downloaded_atlases()
        maybe_matches = [re.match(pattern, name) for name in downloaded]
        resolutions = [int(match.group(1)) for match in maybe_matches if match]
        return tuple(resolutions)

    def get_atlas(self) -> Optional[Atlas]:
        return self._atlas

    def set_atlas(self, atlas: Atlas) -> None:
        self._atlas = atlas