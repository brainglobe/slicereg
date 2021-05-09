from unittest.mock import Mock

import numpy.testing as npt
import pytest
from numpy import random
from pytest_bdd import scenario, when, then

from slicereg.commands.load_atlas import LoadBrainglobeAtlasCommand
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


@pytest.fixture
def atlas_volume():
    return random.normal(size=(4, 4, 4))

@pytest.fixture
def annotation_volume():
    return random.normal(size=(4, 4, 4))

@pytest.fixture
def model(atlas_volume, annotation_volume):
    commands = Mock(CommandProvider)
    reader = Mock(BrainglobeAtlasReader)
    reader.list_available.return_value = ['allen_mouse_25um']
    reader.read.return_value = Atlas(volume=atlas_volume, resolution_um=25, annotation_volume=annotation_volume)
    commands.load_atlas = LoadBrainglobeAtlasCommand(_reader = reader, _repo=AtlasRepo())
    model = AppModel(_commands=commands)
    return model


@scenario("load_atlas.feature", "Load Atlas")
def test_outlined():
    ...


@when("I load the 25um allen mouse atlas")
def load_atlas(model):
    model.load_bgatlas('allen_mouse_25um')


@then("a 3D volume of the 25um allen reference atlas is loaded.")
def check_3d_atlas_data_shown(model, atlas_volume):
    npt.assert_almost_equal(model.atlas_volume, atlas_volume)

@then("a 3D annotation volume of the 25um allen reference atlas is loaded.")
def check_3d_atlas_data_shown(model, annotation_volume):
    npt.assert_almost_equal(model.annotation_volume, annotation_volume)
