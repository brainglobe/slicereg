from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/section_affine_registration.feature", "Set Section's 3D Coordinates")
def test_impl():
    ...


@given("I have loaded a section")
def step_impl(model, sidebar):
    sidebar.submit_load_section_from_file("test.ome.tiff")
    assert model.section_image is not None
    assert model.section_transform is not None


@when("I <operation_type> the section along the <axis> axis by <amount>")
def step_impl(slice_view, operation_type, axis, amount):
    controls = {
        'translate': {
            'x': lambda: slice_view.on_left_mouse_drag(x1=0, y1=0, x2=10, y2=0),
            'y': lambda: slice_view.on_left_mouse_drag(x1=0, y1=0, x2=0, y2=10),
            'z': lambda: slice_view.on_mousewheel_move(increment=10),
        },
        'rotate': {
            'x': lambda: slice_view.on_right_mouse_drag(x1=0, y1=0, x2=10, y2=0),
            'y': lambda: slice_view.on_right_mouse_drag(x1=0, y1=0, x2=0, y2=10),
            'z': lambda: (),
        }
    }
    controls[operation_type][axis]()


@then("the image is updated with a new 3D transform with indicated paramters set to the requested value")
def step_impl(model: AppModel):
    assert model.section_transform is not None  # todo: figure out how to detect a change


@then("an atlas section image at that transform is shown.")
def step_impl(model: AppModel):
    assert model.section_image is not None  # todo: figure out how to detect a change

