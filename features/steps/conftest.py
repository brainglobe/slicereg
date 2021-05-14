from unittest.mock import Mock

import numpy as np
import pytest
from numpy import random

from slicereg.app.app_model import AppModel
from slicereg.commands.base import BaseRemoteAtlasReader, BaseLocalAtlasReader, BaseLocalImageReader
from slicereg.core.atlas import Atlas
from slicereg.core.image import Image
from slicereg.gui.main_window.viewmodel import MainWindowViewModel
from slicereg.gui.sidebar import SidebarView
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.gui.slice_window.viewmodel import SliceViewModel
from slicereg.gui.volume_window.viewmodel import VolumeViewModel
from slicereg.repos import InMemoryRepo
from slicereg.utils.dependency_injector import DependencyInjector


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
    image_reader = Mock(BaseLocalImageReader)
    image_reader.read.return_value = Image(channels=channels, resolution_um=10.)

    atlas_reader = Mock(BaseRemoteAtlasReader)
    atlas_reader.list.return_value = bg_atlases
    atlas_reader.read.side_effect = [
        Atlas(volume=atlas_volume, resolution_um=25, annotation_volume=annotation_volume),
        Atlas(volume=second_volume, resolution_um=100),
    ]

    atlas_file_reader = Mock(BaseLocalAtlasReader)
    atlas_file_reader.read.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=10)

    repo = InMemoryRepo()
    repo.set_atlas(Atlas(volume=np.empty((2, 3, 4)), resolution_um=10))

    injector = DependencyInjector(
        _repo=repo,
        _remote_atlas_reader=atlas_reader,
        _local_atlas_reader=atlas_file_reader,
        _image_reader=image_reader,
    )
    model = AppModel(_injector=injector)
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


@pytest.fixture
def main_window(model: AppModel):
    return MainWindowViewModel(_model=model)
