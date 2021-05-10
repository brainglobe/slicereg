from unittest import mock

import pytest
from pytest_bdd import scenario, when, then

from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider


@pytest.fixture
def model():
    return AppModel(_commands=CommandProvider())


@scenario("features/load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@when("I refresh the brainglobe atlas list")
def step_impl(model: AppModel):
    fake_atlases = [('allen_rhinoceros_1000um', '1.0'), ('mpi_zebrafinch_1um', '1.2')]
    with mock.patch("slicereg.io.bg_atlasapi.bg_utils.conf_from_url", return_value={'atlases': fake_atlases}):
        model.list_bgatlases()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(model: AppModel):
    expected_atlases = ['allen_rhinoceros_1000um', 'mpi_zebrafinch_1um']
    assert model.bgatlas_names == expected_atlases
