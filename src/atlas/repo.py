from contextlib import redirect_stdout
from io import StringIO
from typing import Optional

from bg_atlasapi import BrainGlobeAtlas
from numpy import ndarray

from src.atlas.models import Atlas
from src.atlas.load_atlas import BaseAtlasRepo


class BGAtlasAllenRepo(BaseAtlasRepo):

    def __init__(self):
        self._bgatlas: Optional[BrainGlobeAtlas] = None
        self._current_atlas: Optional[Atlas] = None

    def get_atlas(self, resolution_um: int) -> Atlas:
        if resolution_um not in [10, 25, 100]:
            raise ValueError("Only 10um, 25um and 100um atlas resolutions available.")

        if self._bgatlas is None or self._bgatlas.resolution[0] != resolution_um:
            with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
                bgatlas = BrainGlobeAtlas(f"allen_mouse_{resolution_um}um")

            assert bgatlas.resolution[0] == resolution_um, \
                f"{bgatlas.resolution[0]} not {resolution_um}"

            assert isinstance(bgatlas.reference, ndarray)
            assert bgatlas.reference.ndim == 3
            assert len(set(bgatlas.resolution)) == 1, \
                f"BGAtlas has different resolution for given dimensions ({bgatlas.resolution})"

            self._bgatlas = bgatlas

        bgatlas = self._bgatlas
        w, h, d = bgatlas.shape_um

        atlas = Atlas(
            volume=bgatlas.reference,
            resolution_um=bgatlas.resolution[0],
            origin=(w / 2., h / 2., d / 2.)
        )
        self._current_atlas = atlas
        return atlas

    def get_current_atlas(self) -> Atlas:
        return self._current_atlas

