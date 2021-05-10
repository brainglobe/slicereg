from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/load_slice.feature", "Single Slice Import")
def test_outlined():
    ...


@given("I have a multichannel OME-TIFF file on my computer.", target_fixture="filename")
def filename():
    return 'a_real_file.ome.tiff'


@given("No sections have been loaded yet")
def no_sections_loaded(model: AppModel):
    assert model.section_image is None
    assert model.atlas_image is None
    assert model.section_transform is None


@given("An atlas has been loaded")
def atlas_is_loaded(sidebar, model):
    sidebar.change_bgatlas_selection_dropdown("allen_mouse_25um")
    sidebar.click_load_bgatlas_button()
    assert model.atlas_volume is not None


@when("I load the file")
def load_file(sidebar, filename: str):
    sidebar.submit_load_section_from_file(filename=filename)


@then("I should see the slice image onscreen in 3D")
def check_for_loaded_3d_section(model: AppModel):
    assert model.section_image.ndim == 2
    assert model.section_transform.shape == (4, 4)


@then("I should see the atlas image onscreen in slice view")
def check_atlas_image_displayed(model: AppModel):
    assert model.atlas_image.ndim == 2


@then("The slice is centered on the image")
def check_the_transform_isnt_zero(model: AppModel):
    assert model.section_transform[0, -1] != 0
    assert model.section_transform[1, -1] != 0


@then("The displayed resolution is set to the image's resolution")
def check_resolution_is_sent(model: AppModel):
    assert model.section_image_resolution == 10
