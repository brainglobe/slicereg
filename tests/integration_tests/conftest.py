from unittest.mock import Mock

import numpy as np
import pytest
from numpy import random

from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.gui.view_models.sidebar import SidebarViewModel
from slicereg.gui.view_models.slice import SliceViewModel
from slicereg.gui.view_models.volume import VolumeViewModel
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.io.imio import ImioAtlasReader
from slicereg.io.tifffile import OmeTiffImageReader
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def atlas_volume():
    return random.normal(size=(4, 4, 4))


@pytest.fixture
def second_volume():
    return random.normal(size=(4, 4, 4))


@pytest.fixture
def annotation_volume():
    return random.normal(size=(4, 4, 4))


@pytest.fixture
def bg_atlases():
    return ['allen_mouse_25um']


@pytest.fixture
def channels():
    return random.randint(0, 1000, size=(2, 3, 4))


@pytest.fixture
def model(atlas_volume, second_volume, annotation_volume, channels, bg_atlases):
    ome_reader = Mock(OmeTiffImageReader)
    ome_reader.read.return_value = Image(channels=channels, resolution_um=10.)

    atlas_reader = Mock(BrainglobeAtlasReader)
    atlas_reader.list_available.return_value = bg_atlases
    atlas_reader.read.side_effect = [
        Atlas(volume=atlas_volume, resolution_um=25, annotation_volume=annotation_volume),
        Atlas(volume=second_volume, resolution_um=100),
    ]

    atlas_file_reader = Mock(ImioAtlasReader)
    atlas_file_reader.read.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=10)

    atlas_repo = AtlasRepo()
    atlas_repo.set_atlas(Atlas(volume=np.empty((2, 3, 4)), resolution_um=10))
    commands = CommandProvider(
        _bgatlas_reader=atlas_reader,
        _atlas_file_reader=atlas_file_reader,
        _atlas_repo=atlas_repo,
        _section_ome_reader=ome_reader
    )
    model = AppModel(_commands=commands)
    return model


@pytest.fixture
def sidebar(model: AppModel):
    return SidebarViewModel(_model=model)


@pytest.fixture
def volume_view(model: AppModel):
    return VolumeViewModel(_model=model)


@pytest.fixture
def slice_view(model: AppModel):
    return SliceViewModel(_model=model)
