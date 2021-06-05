from unittest.mock import Mock

import numpy as np
import pytest
from numpy import random

from slicereg.gui.app_model import AppModel
from slicereg.commands.base import BaseRemoteAtlasReader, BaseLocalAtlasReader, BaseLocalImageReader, RemoteAtlasReaderData, \
    ImageReaderData
from slicereg.core.atlas import Atlas
from slicereg.gui.main_window.viewmodel import MainWindowViewModel
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.gui.slice_window.viewmodel import SliceViewModel
from slicereg.gui.volume_window.viewmodel import VolumeViewModel
from slicereg.gui.atlas_section_window import AtlasSectionViewModel
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
    image_reader.read.return_value = ImageReaderData(channels=channels, resolution_um=10.)

    atlas_reader = Mock(BaseRemoteAtlasReader)
    atlas_reader.list.return_value = bg_atlases
    atlas_reader.read.side_effect = [
        RemoteAtlasReaderData(source="MockBrainglobe", name="fake_atlas", registration_volume=atlas_volume, resolution_um=25, annotation_volume=annotation_volume),
        RemoteAtlasReaderData(source="MockBrainglobe", name="fake_atlas2", registration_volume=second_volume, resolution_um=100, annotation_volume=annotation_volume),
    ]

    atlas_file_reader = Mock(BaseLocalAtlasReader)
    atlas_file_reader.read.return_value = RemoteAtlasReaderData(source='Mock',
                                                                name='filename.tiff',
                                                                registration_volume=random.normal(size=(4, 4, 4)),
                                                                annotation_volume=None,
                                                                resolution_um=None)

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
def coronal_view(model: AppModel):
    return AtlasSectionViewModel(_model=model, plane='coronal')


@pytest.fixture
def axial_view(model: AppModel):
    return AtlasSectionViewModel(_model=model, plane='axial')


@pytest.fixture
def sagittal_view(model: AppModel):
    return AtlasSectionViewModel(_model=model, plane='sagittal')


@pytest.fixture
def main_window(model: AppModel):
    return MainWindowViewModel(_model=model)
