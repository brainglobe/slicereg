from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.commands.base import AtlasReaderData, BaseRemoteAtlasReader, BaseRepo, BaseLocalAtlasReader
from slicereg.commands.load_atlas import LoadAtlasCommand, LoadBrainglobeAtlasRequest


@pytest.fixture
def mock_reader():
    reader = Mock(BaseRemoteAtlasReader)
    reader.read.return_value = AtlasReaderData(
        source="Brainglobe",
        name="allen_mouse_10um",
        registration_volume=np.empty((2, 3, 4), dtype=np.uint16),
        annotation_volume=np.empty((2, 3, 4), dtype=np.uint16),
        resolution_um=10,
    )
    return reader


def test_load_bgatlas_command_gets_atlas(mock_reader):
    load_atlas = LoadAtlasCommand(_repo=Mock(BaseRepo), _remote_atlas_reader=mock_reader, _local_atlas_reader=Mock(BaseLocalAtlasReader))
    request = LoadBrainglobeAtlasRequest(name='allen_mouse_10um')
    result = load_atlas(request)
    data = result.unwrap()
    assert data.resolution == 10
    assert data.volume.shape == (2, 3, 4)
    assert data.annotation_volume.shape == (2, 3, 4)


def test_load_bgatlas_command_saves_atlas_in_repo(mock_reader):
    repo = Mock(BaseRepo)
    load_atlas = LoadAtlasCommand(_repo=repo, _remote_atlas_reader=mock_reader, _local_atlas_reader=Mock(BaseLocalAtlasReader))

    assert repo.set_atlas.call_count == 0
    request = LoadBrainglobeAtlasRequest(name='allen_mouse_10um')
    load_atlas(request)
    assert repo.set_atlas.call_count == 1
