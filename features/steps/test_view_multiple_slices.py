


import pytest
from pytest import approx
from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@pytest.mark.skip()
@scenario("../load_slice.feature", "Multiple Slice Import")
def test_outlined():
    ...


@given("No sections have been loaded yet")
def no_sections_loaded(model: AppModel):
    assert model.section_image is None
    assert model.atlas_image is None
    assert model.section_transform is None


@given("an atlas has been loaded")
def atlas_is_loaded(sidebar, model):
    sidebar.change_bgatlas_selection_dropdown("allen_mouse_25um")
    sidebar.click_load_bgatlas_button()
    assert model.registration_volume is not None


@when("I load a section file")
def load_file(sidebar):
    sidebar.submit_load_section_from_file(filename="data1.ome.tiff")


@when("I load another section file")
def load_file2(sidebar):
    sidebar.submit_load_section_from_file(filename="data2.ome.tiff")


@then("both slices are visible in 3D")
def view_all_sections(volume_view):
    assert len(volume_view.sections) == 2
    assert volume_view.sections[0].transform.shape == (4, 4)
    assert volume_view.sections[1].transform.shape == (4, 4)
    
@then("the second slice is highlighted.")
def slice_highlighted(volume_view):
    assert volume_view.highlighted_section == 1


