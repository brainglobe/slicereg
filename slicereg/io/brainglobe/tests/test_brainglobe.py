from unittest.mock import patch, Mock

import numpy as np

from slicereg.core.atlas import Atlas
from slicereg.io import BrainglobeRemoteAtlasReader
import numpy.testing as npt

def test_brainglobe_reader_gets_reference_resolution_and_annotation():
    reader = BrainglobeRemoteAtlasReader()
    with patch("slicereg.io.brainglobe.atlas.BrainGlobeAtlas") as bgatlas:
        mock_atlas = Mock()
        bgatlas.return_value = mock_atlas
        mock_atlas.annotation = np.empty((5, 5, 5), dtype=np.uint16)
        mock_atlas.reference = np.empty((5, 5, 5), dtype=np.uint16)
        mock_atlas.resolution = [10, 10, 10]
        mock_atlas.space.map_stack_to.side_effect = [
            np.empty((5, 5, 5), dtype=np.uint16),
            np.empty((5, 5, 5), dtype=np.uint16),
        ]
        mock_atlas.local_full_name = "I exist, I promise"

        atlas = reader.read("super_atlas")

    assert mock_atlas.reference.shape == atlas.registration_volume.shape
    assert mock_atlas.annotation.shape == atlas.annotation_volume.shape


def test_brainglobe_reader_gets_list_of_atlases():
    reader = BrainglobeRemoteAtlasReader()

    fake_atlases = [('allen_rhinoceros_1000um', '1.0'), ('mpi_zebrafinch_1um', '1.2')]
    with patch("slicereg.io.brainglobe.atlas.bg_utils.conf_from_url", return_value={'atlases': fake_atlases}):
        assert reader.list() == ['allen_rhinoceros_1000um', 'mpi_zebrafinch_1um']