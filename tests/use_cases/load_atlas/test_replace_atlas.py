from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.models.atlas import Atlas
from slicereg.commands import BaseLoadAtlasRepo, LoadAtlasCommand, BaseLoadAtlasPresenter


@pytest.fixture
def command():
    repo = Mock(BaseLoadAtlasRepo)
    repo.get_atlas.side_effect = [
        Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25, origin=(0, 0, 0)),
        Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=100, origin=(0, 0, 0)),
    ]
    return LoadAtlasCommand(repo=repo, presenter=Mock(BaseLoadAtlasPresenter))


@scenario("load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def check_atlas_exists(command):
    assert command._repo.get_atlas(resolution=25).resolution_um == 25


@when("I ask for a 100um atlas")
def load_atlas(command):
    command.execute(resolution=100)


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(command):
    view_model = command._presenter.show.call_args[1]
    assert view_model['reference_volume'].ndim == 3
    assert view_model['atlas_transform'].shape == (4, 4)
    assert view_model['atlas_resolution'] == 100
    command._repo.get_atlas.assert_called_with(resolution=100)
