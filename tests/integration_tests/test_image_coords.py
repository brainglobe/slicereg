from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/section_affine_registration.feature", "Check Pixel Coordinate in Atlas Space")
def test_impl():
    ...


@given("I have loaded a section")
def step_impl(sidebar):
    sidebar.submit_load_section_from_file("myfile.ome.tiff")


@when("I indicate a section image coordinate")
def step_impl(slice_view):
    slice_view.on_mouse_move(x=1, y=2)


@then("the coordinate's 2D position and 3D position should appear")
def step_impl(model: AppModel):
    assert model.selected_ij == (1, 2)
    assert isinstance(model.selected_xyz, tuple) and all(isinstance(el, float) for el in model.selected_xyz)
