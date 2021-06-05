from unittest.mock import patch

import numpy as np

from slicereg.io import ImioLocalAtlasReader


def test_imio_reader_creates_atlas():
    reader = ImioLocalAtlasReader()
    with patch("slicereg.io.imio.atlas.imio.load_any") as load_any:
        load_any.return_value = np.empty((5, 5, 5), dtype=np.uint16)
        atlas = reader.read("super_atlas")

    assert atlas.registration_volume.ndim == 3
