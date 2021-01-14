from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.gui.presenters import LoadAtlasPresenter
from slicereg.models.atlas import Atlas
from slicereg.application.load_atlas.workflow import BaseLoadAtlasRepo, LoadAtlasWorkflow


@pytest.fixture
def workflow():
    repo = Mock(BaseLoadAtlasRepo)
    repo.get_atlas.side_effect = [
        Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25, origin=(0, 0, 0)),
        Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=100, origin=(0, 0, 0)),
    ]
    return LoadAtlasWorkflow(repo=repo, presenter=Mock(LoadAtlasPresenter))


@scenario("load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def check_atlas_exists(workflow):
    assert workflow._repo.get_atlas(resolution=25).resolution_um == 25


@when("I ask for a 100um atlas")
def load_atlas(workflow):
    workflow.execute(resolution=100)


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(workflow):
    view_model = workflow._presenter.show.call_args[0][0]
    assert view_model.reference_volume.ndim == 3
    assert view_model.atlas_transform.shape == (4, 4)
    assert view_model.atlas_resolution == 100
    assert workflow._repo.get_atlas.call_args[1]['resolution'] == 100  # repo was last asked for a 100um atlas
