import numpy.testing as npt
from pytest_bdd import scenario, given, when, then

from slicereg.app.app_model import VolumeType


@scenario("../load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def load_first_atlas(sidebar, model, atlas_volume):
    sidebar.change_bgatlas_selection_dropdown("first_atlas")
    sidebar.click_load_bgatlas_button()
    assert model.atlas_resolution == 25
    npt.assert_almost_equal(model.registration_volume, atlas_volume)


@when("I ask for a 100um atlas")
def load_second_atlas(sidebar):
    sidebar.change_bgatlas_selection_dropdown("allen_mouse_100um")
    sidebar.click_load_bgatlas_button()


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(model, second_volume):
    assert model.atlas_resolution == 100
    assert model.visible_volume == VolumeType.REGISTRATION
    npt.assert_almost_equal(model.registration_volume, second_volume)
