from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/section_affine_registration.feature", "Check Pixel Coordinate in Atlas Space")
def test_impl():
    ...


@given("I have loaded a section")
def step_impl(model: AppModel):
    model.load_section("myfile.ome.tiff")


@when("I indicate a section image coordinate")
def step_impl(model: AppModel):
    model.select_coord(i=1, j=2)


@then("the coordinate's 2D position and 3D position should appear")
def step_impl(model: AppModel):
    assert model.selected_ij == (1, 2)
    assert isinstance(model.selected_xyz, tuple) and all(isinstance(el, float) for el in model.selected_xyz)
