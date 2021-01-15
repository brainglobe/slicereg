import re
from contextlib import redirect_stdout
from io import StringIO
from typing import Tuple

from bg_atlasapi import BrainGlobeAtlas  # type: ignore
from bg_atlasapi.list_atlases import get_downloaded_atlases  # type: ignore
from numpy import ndarray  # type: ignore

from slicereg.commands.load_atlas import BaseLoadAtlasRepo
from slicereg.models.atlas import Atlas


class BrainglobeAtlasRepo(BaseLoadAtlasRepo):

    def get_atlas(self, resolution: int) -> Atlas:
        if resolution not in [10, 25, 100]:
            raise ValueError("Only 10um, 25um and 100um atlas resolutions available.")

        with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
            bgatlas = BrainGlobeAtlas(f"allen_mouse_{resolution}um")

        assert bgatlas.resolution[0] == resolution
        assert isinstance(bgatlas.reference, ndarray)
        assert bgatlas.reference.ndim == 3
        assert len(set(bgatlas.resolution)) == 1, \
            f"BGAtlas has different resolution for given dimensions ({bgatlas.resolution})"

        w, h, d = bgatlas.shape_um

        return Atlas(
            volume=bgatlas.reference,
            resolution_um=bgatlas.resolution[0],
            origin=(w / 2., h / 2., d / 2.)
        )

    @property
    def get_downloaded_resolutions(self) -> Tuple[int, ...]:
        pattern = re.compile("allen_mouse_(\d{2,})um")  # look for the name "allen_mouse_XXXum"
        downloaded = get_downloaded_atlases()
        maybe_matches = [re.match(pattern, name) for name in downloaded]
        resolutions = [int(match.group(1)) for match in maybe_matches if match]
        return tuple(resolutions)
