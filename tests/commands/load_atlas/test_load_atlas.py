from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas import BaseLoadAtlasRepo, LoadAtlasCommand, BaseLoadAtlasPresenter
from slicereg.models.atlas import Atlas


@pytest.fixture
def command():
    repo = Mock(BaseLoadAtlasRepo)
    repo.get_downloaded_resolutions.return_value = (25,)
    repo.get_atlas.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25, origin=(0, 0, 0))
    return LoadAtlasCommand(repo=repo, presenter=Mock(BaseLoadAtlasPresenter))


@scenario("load_atlas.feature", "Load Atlas")
def test_outlined():
    ...


@given("the 25um atlas is already on my computer")
def check_atlas_exists(command):
    assert 25 in command._repo.get_downloaded_resolutions()


@when("I ask for a 25um atlas")
def load_atlas(command):
    command.execute(resolution=25)


@then("a 3D volume of the 25um allen reference atlas appears onscreen.")
def check_3d_atlas_data_shown(command):
    view_model = command._presenter.show.call_args[1]
    assert view_model['reference_volume'].ndim == 3
    assert view_model['atlas_transform'].shape == (4, 4)
    command._repo.get_atlas.assert_called_with(resolution=25)
