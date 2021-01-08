from numpy import ndarray

from src.workflows.load_atlas.load_atlas import BaseRepo
from src.models.atlas import Atlas
from contextlib import redirect_stdout
from io import StringIO

from bg_atlasapi import BrainGlobeAtlas


def load_bgatlas(resolution_um: int) -> BrainGlobeAtlas:
    if resolution_um not in [10, 25, 100]:
        raise ValueError("Only 10um, 25um and 100um atlas resolutions available.")

    with redirect_stdout(StringIO()):  # blocks the BrainGlobeAtlas print to console
        atlas = BrainGlobeAtlas(f"allen_mouse_{resolution_um}um")

    assert atlas.resolution[0] == resolution_um
    assert isinstance(atlas.reference, ndarray)
    assert atlas.reference.ndim == 3
    assert len(set(atlas.resolution)) == 1, \
        f"BGAtlas has different resolution for given dimensions ({atlas.resolution})"

    return atlas


class BrainglobeAtlasRepo(BaseRepo):

    def load_atlas(self, resolution: int) -> Atlas:
        bgatlas = load_bgatlas(resolution_um=resolution)

        w, h, d = bgatlas.shape_um

        return Atlas(
            volume=bgatlas.reference,
            resolution_um=bgatlas.resolution[0],
            origin=(w / 2., h / 2., d / 2.)
        )
