from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas import LoadBrainglobeAtlasCommand
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas


@pytest.fixture
def command():
    reader = Mock(BrainglobeAtlasReader)
    reader.read.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=100)
    return LoadBrainglobeAtlasCommand(_repo=AtlasRepo(), _reader=reader, atlas_updated=Mock(Signal))


@scenario("load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def load_first_atlas(command):
    command._repo.set_atlas(Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25))


@when("I ask for a 100um atlas")
def load_atlas(command):
    command(bgatlas_name="allen_mouse_100um")


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(command):
    view_model = command.atlas_updated.emit.call_args[1]
    assert view_model['volume'].ndim == 3
    assert view_model['transform'].shape == (4, 4)
    command._reader.read.assert_called_with(path="allen_mouse_100um")
