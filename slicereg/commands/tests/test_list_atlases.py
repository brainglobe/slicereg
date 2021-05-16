from __future__ import annotations

from unittest.mock import patch

from slicereg.commands.list_atlases import ListRemoteAtlasesCommand
from slicereg.io import BrainglobeRemoteAtlasReader


def test_list_atlases_gets_brainglobe_atlas_names():

    load_atlases = ListRemoteAtlasesCommand(_remote_atlas_reader=BrainglobeRemoteAtlasReader())

    fake_atlases = [('allen_rhinoceros_1000um', '1.0'), ('mpi_zebrafinch_1um', '1.2')]
    with patch("slicereg.io.brainglobe.atlas.bg_utils.conf_from_url", return_value={'atlases': fake_atlases}):
        result = load_atlases()

    assert result.atlas_names == ['allen_rhinoceros_1000um', 'mpi_zebrafinch_1um']