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
    repo.get_downloaded_resolutions.return_value = (25,)
    repo.get_atlas.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25, origin=(0, 0, 0))
    return LoadAtlasWorkflow(repo=repo, presenter=Mock(LoadAtlasPresenter))


@scenario("load_atlas.feature", "Load Atlas")
def test_outlined():
    ...


@given("the 25um atlas is already on my computer")
def check_atlas_exists(workflow):
    assert 25 in workflow._repo.get_downloaded_resolutions()


@when("I ask for a 25um atlas")
def load_atlas(workflow):
    workflow.execute(resolution=25)


@then("a 3D volume of the 25um allen reference atlas appears onscreen.")
def check_3d_atlas_data_shown(workflow):
    view_model = workflow._presenter.show.call_args[0][0]
    assert view_model.reference_volume.ndim == 3
    assert view_model.atlas_transform.shape == (4, 4)
