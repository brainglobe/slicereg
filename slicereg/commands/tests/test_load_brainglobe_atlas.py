from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.commands.base import AtlasReaderData, BaseRemoteAtlasReader, BaseRepo
from slicereg.commands.load_atlas import LoadRemoteAtlasCommand


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
    load_atlas = LoadRemoteAtlasCommand(_repo=Mock(BaseRepo), _remote_atlas_reader=mock_reader)
    result = load_atlas(name='allen_mouse_10um')
    data = result.unwrap()
    assert data.resolution == 10
    assert data.volume.shape == (2, 3, 4)
    assert data.annotation_volume.shape == (2, 3, 4)


def test_load_bgatlas_command_saves_atlas_in_repo(mock_reader):
    repo = Mock(BaseRepo)
    load_atlas = LoadRemoteAtlasCommand(_repo=repo, _remote_atlas_reader=mock_reader)

    assert repo.set_atlas.call_count == 0
    load_atlas(name='allen_mouse_10um')
    assert repo.set_atlas.call_count == 1


def test_load_bgatlas_command_returns_atlas_center(mock_reader):
    repo = Mock(BaseRepo)
    load_atlas = LoadRemoteAtlasCommand(_repo=repo, _remote_atlas_reader=mock_reader)
    result = load_atlas(name='allen_mouse_10um')
    data = result.unwrap()
    assert data.atlas_center.superior == 10
    assert data.atlas_center.anterior == 15
    assert data.atlas_center.right == 20
