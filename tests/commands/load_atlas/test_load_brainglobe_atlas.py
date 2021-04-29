from unittest.mock import Mock

import numpy.testing as npt
import pytest
from numpy import random
from pytest_bdd import scenario, when, then

from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.views.sidebar import SidebarViewModel
from slicereg.gui.views.volume import VolumeViewModel
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


@pytest.fixture
def atlas_volume():
    return random.normal(size=(4, 4, 4))


@pytest.fixture
def model(atlas_volume):
    commands = CommandProvider.from_repos(atlas_repo=AtlasRepo(), section_repo=InMemorySectionRepo())
    reader = Mock(BrainglobeAtlasReader)
    reader.list_available.return_value = ['allen_mouse_25um']
    reader.read.return_value = Atlas(volume=atlas_volume, resolution_um=25)
    commands.load_atlas._reader = reader
    model = AppModel(_commands=commands)
    commands.load_atlas.atlas_updated.connect(model.on_atlas_update)
    return model


@pytest.fixture
def sidebar_view(model):
    return SidebarViewModel(_model=model)


@pytest.fixture
def volume_view(model):
    return VolumeViewModel(_model=model)


@scenario("load_atlas.feature", "Load Atlas")
def test_outlined():
    ...


@when("I load the 25um allen mouse atlas")
def load_atlas(sidebar_view):
    sidebar_view.change_bgatlas_selection_dropdown(text="allen_mouse_25um")
    sidebar_view.click_load_bgatlas_button()


@then("a 3D volume of the 25um allen reference atlas appears onscreen.")
def check_3d_atlas_data_shown(volume_view, atlas_volume):
    npt.assert_almost_equal(volume_view.atlas_volume, atlas_volume)


@then("it is set as the current atlas for the session.")
def check_atlas_set_in_repo(sidebar_view):
    assert sidebar_view.selected_bgatlas == "allen_mouse_25um"
