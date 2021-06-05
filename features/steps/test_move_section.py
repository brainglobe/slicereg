from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@scenario("../section_affine_registration.feature", "Move Section in 3D")
def test_impl():
    ...


@given("I have loaded a section")
def step_impl(sidebar, model: AppModel):
    sidebar.submit_load_section_from_file("test.ome.tiff")
    assert model.section_image is not None
    assert model.section_transform is not None


@when("I <operation_type> the section along the <axis> axis by <amount>")
def step_impl(sidebar, operation_type, axis, amount):
    controls = {
        'translate': {
            'longitudinal': sidebar.change_superior_slider,
            'anteroposterior': sidebar.change_anterior_slider,
            'horizontal': sidebar.change_right_slider,
        },
        'rotate': {
            'longitudinal': sidebar.change_rot_longitudinal_slider,
            'anteroposterior': sidebar.change_rot_anteroposterior_slider,
            'horizontal': sidebar.change_rot_horizontal_slider,
        }
    }
    controls[operation_type][axis](value=float(amount))


@then("the image is updated with a new 3D transform")
def step_impl(model: AppModel):
    assert model.section_transform is not None  # todo: figure out how to detect a change


@then("an atlas section image at that transform is shown.")
def step_impl(model: AppModel):
    assert model.section_image is not None  # todo: figure out how to detect a change

