from unittest.mock import Mock

import pytest
from numpy import random
import numpy.testing as npt
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas import LoadBrainglobeAtlasCommand
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def first_volume():
    return random.normal(size=(4, 4, 4))


@pytest.fixture
def second_volume():
    return random.normal(size=(4, 4, 4))


@pytest.fixture
def model(first_volume, second_volume):
    commands = Mock(CommandProvider)
    reader = Mock(BrainglobeAtlasReader)
    reader.list_available.return_value = ['allen_mouse_25um']
    reader.read.side_effect = [
        Atlas(volume=first_volume, resolution_um=25),
        Atlas(volume=second_volume, resolution_um=100),
    ]
    commands.load_atlas = LoadBrainglobeAtlasCommand(_reader=reader, _repo=AtlasRepo())
    model = AppModel(_commands=commands)
    model.load_bgatlas("first_atlas")
    return model


@scenario("load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def load_first_atlas(model, first_volume):
    assert model.atlas_resolution == 25
    npt.assert_almost_equal(model.atlas_volume, first_volume)


@when("I ask for a 100um atlas")
def load_second_atlas(model):
    model.load_bgatlas(name="allen_mouse_100um")


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(model, second_volume):
    assert model.atlas_resolution == 100
    npt.assert_almost_equal(model.atlas_volume, second_volume)
