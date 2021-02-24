from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.repos.atlas_repo import BaseAtlasRepo
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas


@pytest.fixture
def command():
    repo = Mock(BaseAtlasRepo)
    repo.load_atlas.side_effect = [
        Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25),
        Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=100),
    ]
    return LoadAtlasCommand(_repo=repo, atlas_updated=Mock(Signal))


@scenario("load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def check_atlas_exists(command):
    assert command._repo.load_atlas(resolution=25).resolution_um == 25


@when("I ask for a 100um atlas")
def load_atlas(command):
    command(resolution=100)


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(command):
    view_model = command.atlas_updated.emit.call_args[1]
    assert view_model['volume'].ndim == 3
    assert view_model['transform'].shape == (4, 4)
    command._repo.load_atlas.assert_called_with(resolution=100)
