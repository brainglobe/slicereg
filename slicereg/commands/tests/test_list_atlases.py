from __future__ import annotations

from unittest.mock import Mock

from slicereg.commands.base import BaseRemoteAtlasReader
from slicereg.commands.list_atlases import ListRemoteAtlasesCommand


def test_list_atlases_gets_brainglobe_atlas_names():

    atlases = ['allen_rhinoceros_1000um', 'mpi_zebrafinch_1um']

    reader = Mock(BaseRemoteAtlasReader)
    reader.list.return_value = atlases

    list_atlases = ListRemoteAtlasesCommand(_remote_atlas_reader=reader)

    result = list_atlases()
    assert result.atlas_names == atlases