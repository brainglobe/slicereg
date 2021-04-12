from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def command():
    repo = Mock(AtlasRepo)
    repo.list_available_atlases.return_value = ['allen_mouse_25um']
    repo.load_atlas.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25)
    return LoadAtlasCommand(_repo=repo, atlas_updated=Mock(Signal))


@scenario("load_atlas.feature", "Load Atlas")
def test_outlined():
    ...


@given("the 25um atlas is already on my computer")
def check_atlas_exists(command):
    assert 'allen_mouse_25um' in command._repo.list_available_atlases()


@when("I ask for a 25um atlas")
def load_atlas(command):
    command(bgatlas_name="allen_mouse_25um")


@then("a 3D volume of the 25um allen reference atlas appears onscreen.")
def check_3d_atlas_data_shown(command):
    output = command.atlas_updated.emit.call_args[1]
    assert output['volume'].ndim == 3
    assert output['transform'].shape == (4, 4)
    command._repo.load_atlas.assert_called_with(name="allen_mouse_25um")


@then("it is set as the current atlas for the session.")
def check_atlas_set_in_repo(command):
    assert command._repo.set_atlas.call_count == 1
