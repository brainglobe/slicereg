from contextlib import redirect_stdout
from io import StringIO

from bg_atlasapi import BrainGlobeAtlas
from numpy import ndarray

from src.core.load_atlas.repos import BaseAtlasSerializer
from src.core.models.atlas import Atlas


class BGAtlasSerializer(BaseAtlasSerializer):

    def read(self, resolution_um: int) -> Atlas:
        if resolution_um not in [10, 25, 100]:
            raise ValueError("Only 10um, 25um and 100um atlas resolutions available.")

        with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
            bgatlas = BrainGlobeAtlas(f"allen_mouse_{resolution_um}um")

        assert bgatlas.resolution[0] == resolution_um
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
