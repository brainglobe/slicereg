import numpy.testing as npt
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.gui.atlas_section_window import AtlasSectionViewModel


@pytest.mark.skip(reason='Not done yet.')
@scenario("../browse_atlas.feature", "View Brain Position from Three Planes")
def test_impl():
    ...


@given("the 25um atlas is currently loaded")
def load_first_atlas(sidebar, model, atlas_volume):
    sidebar.change_bgatlas_selection_dropdown("first_atlas")
    sidebar.click_load_bgatlas_button()
    assert model.atlas_resolution == 25
    npt.assert_almost_equal(model.registration_volume, atlas_volume)


@given("that the current position is at the origin")
def step_impl(model, coronal_view, sagittal_view, axial_view):
    model.x = 0
    model.y = 0
    model.z = 0
    assert coronal_view.image_coords == (0, 0)
    assert coronal_view.depth == 0
    assert sagittal_view.image_coords == (0, 0)
    assert sagittal_view.depth == 0
    assert axial_view.image_coords == (0, 0)
    assert axial_view.depth == 0


@when("I click on a location in the coronal section")
def step_impl(coronal_view: AtlasSectionViewModel):
    coronal_view.click_left_mouse_button(x=50, y=60)


@then("I see a view of that location along the sagittal plane.")
def step_impl(sagittal_view):
    assert sagittal_view.atlas_section_image.ndim == 2
    assert sagittal_view.image_coords[0] == 0
    assert sagittal_view.image_coords[1] != 0
    assert sagittal_view.depth != 0


@then("I see a view of that location along the axial plane.")
def step_impl(axial_view):
    assert axial_view.atlas_section_image.ndim == 2
    assert axial_view.image_coords[0] != 0
    assert axial_view.image_coords[1] == 0
    assert axial_view.depth != 0
