import numpy.testing as npt
from pytest_bdd import scenario, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/load_atlas.feature", "Load Atlas")
def test_outlined():
    ...


@when("I load the 25um allen mouse atlas")
def load_atlas(sidebar):
    sidebar.change_bgatlas_selection_dropdown('allen_mouse_25um')
    sidebar.click_load_bgatlas_button()


@then("a 3D volume of the 25um allen reference atlas is loaded.")
def check_3d_atlas_data_shown(model: AppModel, atlas_volume):
    npt.assert_almost_equal(model.atlas_volume, atlas_volume)

@then("a 3D annotation volume of the 25um allen reference atlas is loaded.")
def check_3d_atlas_data_shown(model: AppModel, annotation_volume):
    npt.assert_almost_equal(model.annotation_volume, annotation_volume)
