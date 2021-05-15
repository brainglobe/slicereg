from unittest.mock import patch

import numpy as np

from slicereg.core.atlas import Atlas
from slicereg.io.tifffile.tiff_atlas import TifffileAtlasReader


def test_tiff_atlas_reader_creates_atlas():
    reader = TifffileAtlasReader()
    with patch("slicereg.io.tifffile.tiff_atlas.tif.imread") as imread:
        imread.return_value = np.empty((5, 5, 5), dtype=np.uint16)
        atlas = reader.read("super_atlas", resolution_um=10)

    assert isinstance(atlas, Atlas)
    assert atlas.resolution_um == 10
