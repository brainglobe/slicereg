from pytest_bdd import scenario, given, when, then
import numpy.testing as npt

@scenario("../annotated_atlas.feature", "Get Brain Region Name from Slice Image position")
def test_impl():
    ...



@given("a slice image has been loaded")
def step_impl(sidebar):
    sidebar.submit_load_section_from_file("myfile.ome.tiff")


@given("a brain atlas has been loaded")
def load_slice_image(sidebar, model, atlas_volume):
    sidebar.change_bgatlas_selection_dropdown("first_atlas")
    sidebar.click_load_bgatlas_button()
    assert model.atlas_resolution == 25
    npt.assert_almost_equal(model.registration_volume, atlas_volume)


@when("I highlight a position on my registered slice")
def highlight_position():
    ...

@then("the name of the brain region associaed with the atlas brain region appears")
def check_associated_brain_region_appears():
    ...
