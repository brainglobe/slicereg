from pytest_bdd import scenario, given, when, then


@scenario("../section_affine_registration.feature", "Check Pixel Coordinate in Atlas Space")
def test_impl():
    ...


@given("I have loaded a section")
def step_impl(sidebar):
    sidebar.submit_load_section_from_file("myfile.ome.tiff")


@when("I indicate a section image coordinate")
def step_impl(slice_view):
    slice_view.on_mouse_move(x=1, y=2)


@then("the coordinate's 2D position and 3D position should appear")
def step_impl(main_window):
    assert main_window.highlighted_image_coords == (1, 2)
    assert isinstance(main_window.highlighted_physical_coords, tuple)
    assert all(isinstance(el, float) for el in main_window.highlighted_physical_coords)
