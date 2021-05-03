from unittest import mock

import pytest
from pytest_bdd import scenario, when, then

from slicereg.gui.commands import CommandProvider
from slicereg.gui.app_model import AppModel
from slicereg.gui.views.sidebar import SidebarViewModel
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


@pytest.fixture
def view():
    commands = CommandProvider.from_repos(atlas_repo=AtlasRepo(), section_repo=InMemorySectionRepo())
    model = AppModel(_commands=commands)
    commands.list_bgatlases.atlas_list_updated.connect(model.on_bgatlas_list_update)
    view = SidebarViewModel(_model=model)
    return view


@scenario("load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@when("I refresh the brainglobe atlas list")
def step_impl(view: SidebarViewModel):
    fake_atlases = [('allen_rhinoceros_1000um', '1.0'), ('mpi_zebrafinch_1um', '1.2')]
    with mock.patch("slicereg.io.bg_atlasapi.bg_utils.conf_from_url", return_value={'atlases': fake_atlases}):
        view.click_update_bgatlas_list_button()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(view: SidebarViewModel):
    expected_atlases = ['allen_rhinoceros_1000um', 'mpi_zebrafinch_1um']
    assert view.bgatlas_names == expected_atlases
