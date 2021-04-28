import pytest
from pytest_bdd import scenario, when, then

from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.views.sidebar import SidebarViewModel
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


@pytest.fixture
def view():
    view = SidebarViewModel(
        _model=AppModel(),
        _commands=CommandProvider.from_repos(atlas_repo=AtlasRepo(), section_repo=InMemorySectionRepo())
    )
    view._commands.list_bgatlases.atlas_list_updated.connect(view._model.on_bgatlas_list_update)
    return view


@scenario("load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@when("I refresh the brainglobe atlas list")
def step_impl(view: SidebarViewModel):
    view.click_update_bgatlas_list_button()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(view: SidebarViewModel):
    assert 'allen_mouse_25um' in view.bgatlas_names
    assert 'mpin_zfish_1um' in view.bgatlas_names
